import Foundation

public enum VideoXMLParserError: LocalizedError {
    case invalidXML(String)
    case invalidRootElement(String)
    case invalidFilePath(String)

    public var errorDescription: String? {
        switch self {
        case .invalidXML(let message):
            return "Invalid XML: \(message)"
        case .invalidRootElement(let element):
            return "Unexpected XML root element: \(element)"
        case .invalidFilePath(let path):
            return "Invalid camera file path: \(path)"
        }
    }
}

public final class VideoXMLParser: NSObject, XMLParserDelegate {
    private let camera: CameraSide
    private var currentElement: String?
    private var currentText: String = ""
    private var rootElement: String?
    private var currentItem: RecordedVideoBuilder?
    private var parsedVideos: [RecordedVideo] = []
    public private(set) var lastError: VideoXMLParserError?

    public init(camera: CameraSide) {
        self.camera = camera
    }

    public func parse(data: Data) -> [RecordedVideo] {
        switch parseValidated(data: data) {
        case .success(let videos):
            return videos
        case .failure:
            return []
        }
    }

    public func parseValidated(data: Data) -> Result<[RecordedVideo], VideoXMLParserError> {
        parsedVideos.removeAll(keepingCapacity: true)
        currentElement = nil
        currentText = ""
        rootElement = nil
        currentItem = nil
        lastError = nil

        let parser = XMLParser(data: data)
        parser.delegate = self

        guard parser.parse() else {
            let error = VideoXMLParserError.invalidXML(parser.parserError?.localizedDescription ?? "unknown parser error")
            lastError = error
            return .failure(error)
        }

        if let root = rootElement, root != "Normal" {
            let error = VideoXMLParserError.invalidRootElement(root)
            lastError = error
            return .failure(error)
        }

        return .success(parsedVideos)
    }

    public func parser(_ parser: XMLParser, didStartElement elementName: String, namespaceURI: String?, qualifiedName qName: String?, attributes attributeDict: [String: String] = [:]) {
        if rootElement == nil {
            rootElement = elementName
        }

        currentElement = elementName
        currentText = ""

        if elementName == "file" {
            currentItem = RecordedVideoBuilder(camera: camera)
        }
    }

    public func parser(_ parser: XMLParser, foundCharacters string: String) {
        guard let element = currentElement else { return }
        let allowedFields: Set<String> = ["name", "size", "time", "format", "attr"]
        guard allowedFields.contains(element) else { return }

        currentText += string.trimmingCharacters(in: .whitespacesAndNewlines)
    }

    public func parser(_ parser: XMLParser, didEndElement elementName: String, namespaceURI: String?, qualifiedName qName: String?) {
        switch elementName {
        case "name":
            currentItem?.name = currentText
        case "size":
            currentItem?.sizeText = currentText.isEmpty ? "0" : currentText
        case "time":
            currentItem?.timeText = currentText
        case "format":
            currentItem?.format = currentText
        case "attr":
            currentItem?.attribute = currentText
        case "file":
            if let item = currentItem?.build() {
                parsedVideos.append(item)
            }
            currentItem = nil
        default:
            break
        }

        if currentElement == elementName {
            currentElement = nil
        }
        currentText = ""
    }

    public func parser(_ parser: XMLParser, parseErrorOccurred parseError: any Error) {
        lastError = .invalidXML(parseError.localizedDescription)
    }
}

private struct RecordedVideoBuilder {
    let camera: CameraSide
    var name: String = ""
    var sizeText: String = "0"
    var timeText: String = ""
    var format: String = ""
    var attribute: String = ""

    func build() -> RecordedVideo? {
        let sanitizedName = name.trimmingCharacters(in: .whitespacesAndNewlines)
        guard Self.isValidPath(sanitizedName) else {
            return nil
        }

        let size = Int64(sizeText) ?? 0
        let id = sanitizedName.replacingOccurrences(of: "/", with: "-")
        let safeURL = URL(string: "http://\(CameraNetworkConstants.cameraHost)\(sanitizedName)")
        let finalURL = safeURL ?? URL(string: "http://\(CameraNetworkConstants.cameraHost)")!

        return RecordedVideo(
            id: id,
            name: sanitizedName,
            path: sanitizedName,
            url: finalURL,
            sizeBytes: size,
            timeText: timeText,
            camera: camera,
            attribute: attribute,
            format: format,
            isZeroByte: size == 0
        )
    }

    private static func isValidPath(_ path: String) -> Bool {
        guard !path.isEmpty else { return false }
        guard path.hasPrefix("/SD/") else { return false }
        guard !path.contains("..") else { return false }
        guard !path.contains(" ") else { return false }
        guard !path.contains("http://") else { return false }
        guard !path.contains("https://") else { return false }

        let pattern = "^/SD/(?:Normal|.*?)/(?:F|R)/[A-Za-z0-9._-]+\\.(?:TS|ts)$"
        let regex = try? NSRegularExpression(pattern: pattern)
        let range = NSRange(location: 0, length: path.utf16.count)
        return regex?.firstMatch(in: path, options: [], range: range) != nil
    }
}
