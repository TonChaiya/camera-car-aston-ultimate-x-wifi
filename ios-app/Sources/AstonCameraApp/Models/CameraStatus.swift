import Foundation

public enum CameraConnectionState: String, Codable, Equatable {
    case loading
    case connected
    case disconnected
    case error
}

public struct CameraStatus: Codable, Equatable {
    public let code: Int
    public let message: String
    public let isRecording: Bool

    public static let mock = CameraStatus(code: 0, message: "0 OK Camera.Preview.MJPEG.status.record=Recording", isRecording: true)

    public static func parseStatusResponse(_ raw: String) -> CameraStatus? {
        let cleaned = raw.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !cleaned.isEmpty else { return nil }

        let parts = cleaned.split(separator: " ", maxSplits: 2, omittingEmptySubsequences: true)
        guard parts.count >= 2 else { return nil }

        let codeValue = Int(parts[0]) ?? 0
        let statusText = String(parts[1])
        let lower = cleaned.lowercased()
        let recordingValue = lower.contains("recording") || lower.contains("record=on") || lower.contains("record=recording")

        let isRecording = statusText == "OK" || statusText.lowercased() == "success" ? recordingValue : false

        return CameraStatus(
            code: codeValue,
            message: cleaned,
            isRecording: isRecording
        )
    }
}
