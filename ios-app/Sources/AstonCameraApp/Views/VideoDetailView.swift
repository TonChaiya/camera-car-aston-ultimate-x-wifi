import SwiftUI

struct VideoDetailView: View {
    let video: RecordedVideo

    var body: some View {
        Form {
            Section("File") {
                LabeledContent("Name", value: video.displayName)
                LabeledContent("Camera", value: video.camera.rawValue.capitalized)
                LabeledContent("Size", value: video.fileSizeDescription)
                LabeledContent("Time", value: video.timeText)
                LabeledContent("Format", value: video.format)
            }

            Section("Download") {
                Button("Download (mock)") {
                    // Intentional placeholder only; no actual file download in this phase.
                }
                .frame(maxWidth: .infinity)
            }
        }
        .navigationTitle("Details")
    }
}
