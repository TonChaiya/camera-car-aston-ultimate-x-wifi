import Foundation

public final class DownloadManager: NSObject, ObservableObject {
    public struct DownloadProgress: Identifiable {
        public let id: String
        public let percentage: Double
        public let totalBytes: Int64
        public let downloadedBytes: Int64
    }

    private let session: URLSession
    private var activeTasks: [String: URLSessionDownloadTask] = [:]

    public init(session: URLSession = .shared) {
        self.session = session
    }

    public func makeRequest(for video: RecordedVideo, offset: Int64 = 0, timeout: TimeInterval = 10) -> URLRequest {
        var request = URLRequest(url: video.url, cachePolicy: .reloadIgnoringLocalCacheData, timeoutInterval: timeout)
        if offset > 0 {
            request.setValue("bytes=\(offset)-", forHTTPHeaderField: "Range")
        }
        request.setValue("*/*", forHTTPHeaderField: "Accept")
        return request
    }

    public func fileSize(at url: URL) -> Int64? {
        guard let attributes = try? FileManager.default.attributesOfItem(atPath: url.path) else { return nil }
        return attributes[.size] as? Int64
    }

    public func resumeOffset(for fileURL: URL) -> Int64 {
        fileSize(at: fileURL) ?? 0
    }

    public func cancelDownload(for videoID: String) {
        activeTasks[videoID]?.cancel()
        activeTasks.removeValue(forKey: videoID)
    }

    public func prepareRangeRequest(for video: RecordedVideo, localFileURL: URL) -> URLRequest {
        let offset = resumeOffset(for: localFileURL)
        return makeRequest(for: video, offset: offset)
    }
}
