import SwiftUI

@main
struct AstonCameraApp: App {
    @StateObject private var appState = AppState(mode: .mockPreview)

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
    }
}

@MainActor
final class AppState: ObservableObject {
    @Published var cameraIP: String = CameraNetworkConstants.cameraHost
    @Published var isConnected: Bool = true
    @Published var connectedState: CameraConnectionState = .loading
    @Published var status: CameraStatus = .mock
    @Published var videoList: [RecordedVideo] = MockData.recordedVideos
    @Published var lastError: String?
    @Published var runtimeMode: CameraRuntimeMode

    private let cameraClient: CameraAPIClient

    init(mode: CameraRuntimeMode = .mockPreview) {
        self.runtimeMode = mode
        self.cameraClient = CameraAPIClient(runtimeMode: mode)
        self.connectedState = mode == .mockPreview ? .connected : .loading
        self.isConnected = mode == .mockPreview
    }

    func setLiveMode() {
        runtimeMode = .liveCamera
        cameraClient.connectionState = .disconnected
        connectedState = .disconnected
        lastError = nil
    }

    func refresh() async {
        do {
            connectedState = .loading
            lastError = nil

            if runtimeMode == .liveCamera {
                connectedState = .disconnected
                lastError = CameraAPIError.liveModeDisabled.errorDescription
                isConnected = false
                return
            }

            status = try await cameraClient.fetchStatus()
            let frontVideos = try await cameraClient.fetchRecordedVideos(camera: .front)
            let rearVideos = try await cameraClient.fetchRecordedVideos(camera: .rear)
            videoList = frontVideos + rearVideos
            isConnected = cameraClient.connectionState == .connected
            connectedState = cameraClient.connectionState
        } catch let error as LocalizedError {
            lastError = error.errorDescription ?? error.localizedDescription
            connectedState = .error
            isConnected = false
        } catch {
            lastError = error.localizedDescription
            connectedState = .error
            isConnected = false
        }
    }
}

struct ContentView: View {
    @EnvironmentObject private var appState: AppState

    var body: some View {
        TabView {
            DashboardView(appState: appState)
                .tabItem {
                    Label("Dashboard", systemImage: "speedometer")
                }

            LiveView()
                .tabItem {
                    Label("Live", systemImage: "video.fill")
                }

            GalleryView(appState: appState)
                .tabItem {
                    Label("Gallery", systemImage: "photo.on.rectangle")
                }
        }
        .tint(.blue)
        .task {
            await appState.refresh()
        }
    }
}
