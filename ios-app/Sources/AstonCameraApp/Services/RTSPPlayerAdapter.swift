import Foundation
import SwiftUI

public protocol RTSPPlayerProviding {
    var endpoint: String { get }
    func play()
    func stop()
    func prepare() -> Bool
}

public final class RTSPPlayerAdapter: RTSPPlayerProviding {
    public let endpoint: String

    public init(endpoint: String) {
        self.endpoint = endpoint
    }

    public func prepare() -> Bool {
        endpoint.hasPrefix("rtsp://")
    }

    public func play() {
        // This foundation layer intentionally avoids assuming direct AVPlayer RTSP support.
    }

    public func stop() {
        // Stop handling is adapter-specific and intentionally left as a safe abstraction.
    }
}

public struct RTSPPlayerPlaceholder: View {
    public let endpoint: String

    public var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Live preview")
                .font(.headline)
            Text(endpoint)
                .font(.caption)
                .foregroundStyle(.secondary)
            Text("RTSP is isolated behind an adapter so direct AVPlayer assumptions are avoided.")
                .font(.footnote)
                .foregroundStyle(.secondary)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}
