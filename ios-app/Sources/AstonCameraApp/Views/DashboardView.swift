import SwiftUI

struct DashboardView: View {
    @ObservedObject var appState: AppState

    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            Text("ASTON Ultimate X")
                .font(.largeTitle)
                .bold()

            HStack {
                Circle()
                    .fill(statusColor)
                    .frame(width: 12, height: 12)
                Text(statusLabel)
                    .font(.headline)
            }

            VStack(alignment: .leading, spacing: 8) {
                Text("Camera IP")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Text(appState.cameraIP)
                    .font(.body)
                    .monospaced()
            }

            VStack(alignment: .leading, spacing: 6) {
                Text("Connection")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Text(appState.connectedState.rawValue.capitalized)
                    .font(.body)
                    .fontWeight(.semibold)
            }

            Text(appState.status.message)
                .font(.callout)
                .foregroundStyle(.secondary)
                .padding(.top, 4)

            if let error = appState.lastError {
                Text("Error: \(error)")
                    .font(.footnote)
                    .foregroundStyle(.red)
            }

            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        .task {
            await appState.refresh()
        }
    }

    private var statusColor: Color {
        switch appState.connectedState {
        case .connected:
            return appState.status.isRecording ? .green : .orange
        case .loading:
            return .yellow
        case .error:
            return .red
        case .disconnected:
            return .gray
        }
    }

    private var statusLabel: String {
        switch appState.connectedState {
        case .connected:
            return appState.status.isRecording ? "Recording" : "Standby"
        case .loading:
            return "Loading"
        case .error:
            return "Error"
        case .disconnected:
            return "Disconnected"
        }
    }
}
