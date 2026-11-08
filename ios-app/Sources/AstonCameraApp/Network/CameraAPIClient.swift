import Foundation

public enum CameraRuntimeMode {
    case mockPreview
    case liveCamera
}

public final class CameraAPIClient {
    public static let shared = CameraAPIClient()

    private let session: URLSession
    private let baseURL: URL
    private let runtimeMode: CameraRuntimeMode
    public var connectionState: CameraConnectionState = .disconnected

    public init(baseURL: URL = CameraNetworkConstants.cameraBaseURL, session: URLSession = .shared, runtimeMode: CameraRuntimeMode = .mockPreview) {
        self.baseURL = baseURL
        self.session = session
        self.runtimeMode = runtimeMode
    }

    public func fetchStatus() async throws -> CameraStatus {
        if runtimeMode == .mockPreview {
            connectionState = .connected
            return .mock
        }

        throw CameraAPIError.liveModeDisabled
    }

    public func fetchRecordedVideos(camera: CameraSide) async throws -> [RecordedVideo] {
        if runtimeMode == .mockPreview {
            connectionState = .connected
            return MockData.recordedVideos.filter { $0.camera == camera }
        }

        throw CameraAPIError.liveModeDisabled
    }

    private func makeRequest(path: String, queryItems: [URLQueryItem]) throws -> URLRequest {
        var components = URLComponents(url: baseURL.appendingPathComponent(path), resolvingAgainstBaseURL: false)
        components?.queryItems = queryItems

        guard let url = components?.url else {
            throw CameraAPIError.invalidURL
        }

        guard url.host == CameraNetworkConstants.cameraHost else {
            throw CameraAPIError.invalidHost(url.host ?? "unknown")
        }

        var request = URLRequest(url: url)
        request.timeoutInterval = 3
        request.cachePolicy = .reloadIgnoringLocalCacheData
        return request
    }
}

public enum CameraAPIError: LocalizedError {
    case invalidURL
    case invalidHost(String)
    case invalidStatusCode(Int)
    case invalidStatusBody
    case invalidXML(String)
    case missingHTTPResponse
    case httpError(statusCode: Int, body: String)
    case liveModeDisabled

    public var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Camera endpoint is invalid."
        case .invalidHost(let host):
            return "Camera host is not allowed: \(host). Only 192.72.1.1 is accepted."
        case .invalidStatusCode(let code):
            return "Camera returned an unexpected HTTP status: \(code)."
        case .invalidStatusBody:
            return "Camera response body could not be decoded."
        case .invalidXML(let message):
            return "The file list XML could not be parsed: \(message)"
        case .missingHTTPResponse:
            return "Camera did not return an HTTP response."
        case .httpError(let statusCode, let body):
            let trimmed = body.trimmingCharacters(in: .whitespacesAndNewlines)
            return "Camera returned HTTP \(statusCode): \(trimmed.isEmpty ? "no body" : trimmed)"
        case .liveModeDisabled:
            return "Live camera mode is intentionally disabled in this foundation phase."
        }
    }
}
