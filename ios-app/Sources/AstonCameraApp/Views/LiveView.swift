import SwiftUI

struct LiveView: View {
    private let rtspEndpoint = "rtsp://192.72.1.1/liveRTSP/v1"

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Front Camera Live")
                .font(.headline)

            RTSPPlayerPlaceholder(endpoint: rtspEndpoint)

            VStack(alignment: .leading, spacing: 6) {
                Text("RTSP Endpoint")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Text(rtspEndpoint)
                    .font(.body)
                    .monospaced()
                Text("Resolution: 640x480 H.264 (placeholder only)")
                    .font(.footnote)
                    .foregroundStyle(.secondary)
            }
        }
        .padding()
    }
}
