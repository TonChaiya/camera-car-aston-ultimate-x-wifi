import XCTest
@testable import AstonCameraApp

final class DownloadManagerTests: XCTestCase {
    func testRangeRequestUsesResumeHeader() throws {
        let manager = DownloadManager()
        let video = MockData.recordedVideos[1]

        let request = manager.makeRequest(for: video, offset: 4096)
        XCTAssertEqual(request.value(forHTTPHeaderField: "Range"), "bytes=4096-")
        XCTAssertEqual(request.url?.absoluteString, video.url.absoluteString)
    }

    func testResumeOffsetReadsLocalFileSize() throws {
        let manager = DownloadManager()
        let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent("resume-test.bin")
        let data = Data(repeating: 0x41, count: 4096)
        try data.write(to: tempURL)

        let offset = manager.resumeOffset(for: tempURL)
        XCTAssertEqual(offset, 4096)

        try FileManager.default.removeItem(at: tempURL)
    }

    func testPrepareRangeRequestUsesExistingFileOffset() throws {
        let manager = DownloadManager()
        let video = MockData.recordedVideos[0]
        let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent("prepare-range.bin")
        let data = Data(repeating: 0x42, count: 8192)
        try data.write(to: tempURL)

        let request = manager.prepareRangeRequest(for: video, localFileURL: tempURL)
        XCTAssertEqual(request.value(forHTTPHeaderField: "Range"), "bytes=8192-")

        try FileManager.default.removeItem(at: tempURL)
    }

    func testHTTPErrorHandlingIsRepresentedAtAPILevel() throws {
        let error = CameraAPIError.httpError(statusCode: 500, body: "Server error")
        XCTAssertNotNil(error.errorDescription)
        XCTAssertTrue(error.errorDescription!.contains("500"))
    }
}
