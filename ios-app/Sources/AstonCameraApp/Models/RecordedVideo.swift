import Foundation

public enum CameraSide: String, Codable, CaseIterable {
    case front = "front"
    case rear = "rear"
}

public enum CameraNetworkConstants {
    public static let cameraHost = "192.72.1.1"
    public static let cameraScheme = "http"
    public static let cameraBaseURL = URL(string: "http://192.72.1.1")!
}

public struct RecordedVideo: Identifiable, Equatable, Hashable {
    public let id: String
    public let name: String
    public let path: String
    public let url: URL
    public let sizeBytes: Int64
    public let timeText: String
    public let camera: CameraSide
    public let attribute: String
    public let format: String
    public let isZeroByte: Bool

    public var displayName: String {
        name.split(separator: "/").last.map(String.init) ?? name
    }

    public var fileSizeDescription: String {
        ByteCountFormatter.string(fromByteCount: sizeBytes, countStyle: .file)
    }
}

public enum MockData {
    public static let recordedVideos: [RecordedVideo] = [
        RecordedVideo(
            id: "front-1",
            name: "/SD/Normal/F/FILE261108-112713-068376F.TS",
            path: "/SD/Normal/F/FILE261108-112713-068376F.TS",
            url: URL(string: "http://192.72.1.1/SD/Normal/F/FILE261108-112713-068376F.TS")!,
            sizeBytes: 148_701_184,
            timeText: "2026-11-08 11:27:13",
            camera: .front,
            attribute: "RW",
            format: "BAD",
            isZeroByte: false
        ),
        RecordedVideo(
            id: "rear-1",
            name: "/SD/Normal/R/FILE261108-112713-068376R.TS",
            path: "/SD/Normal/R/FILE261108-112713-068376R.TS",
            url: URL(string: "http://192.72.1.1/SD/Normal/R/FILE261108-112713-068376R.TS")!,
            sizeBytes: 148_701_184,
            timeText: "2026-11-08 11:27:13",
            camera: .rear,
            attribute: "RW",
            format: "BAD",
            isZeroByte: false
        )
    ]
}
