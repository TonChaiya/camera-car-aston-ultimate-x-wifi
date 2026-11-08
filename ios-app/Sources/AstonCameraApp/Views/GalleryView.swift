import SwiftUI

struct GalleryView: View {
    @ObservedObject var appState: AppState

    var body: some View {
        NavigationStack {
            List {
                Section("Front") {
                    ForEach(appState.videoList.filter { $0.camera == .front }) { video in
                        NavigationLink(destination: VideoDetailView(video: video)) {
                            VideoRow(video: video)
                        }
                    }
                }

                Section("Rear") {
                    ForEach(appState.videoList.filter { $0.camera == .rear }) { video in
                        NavigationLink(destination: VideoDetailView(video: video)) {
                            VideoRow(video: video)
                        }
                    }
                }
            }
            .navigationTitle("Gallery")
            .overlay(alignment: .top) {
                if appState.connectedState == .loading {
                    ProgressView("Loading camera files")
                        .padding()
                }
            }
        }
        .task {
            await appState.refresh()
        }
    }
}

struct VideoRow: View {
    let video: RecordedVideo

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(video.displayName)
                .font(.subheadline)
                .fontWeight(.semibold)
            Text(video.timeText)
                .font(.caption)
                .foregroundStyle(.secondary)
            Text(video.fileSizeDescription)
                .font(.caption2)
                .foregroundStyle(.secondary)
        }
        .padding(.vertical, 2)
    }
}
