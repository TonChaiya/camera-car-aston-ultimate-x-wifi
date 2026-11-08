import XCTest
@testable import AstonCameraApp

final class CameraStatusTests: XCTestCase {
    func testParsingRecordingStatus() throws {
        let raw = "0 OK Camera.Preview.MJPEG.status.record=Recording"
        let status = CameraStatus.parseStatusResponse(raw)

        XCTAssertNotNil(status)
        XCTAssertEqual(status?.code, 0)
        XCTAssertTrue(status?.isRecording == true)
    }

    func testParsingInvalidStatusReturnsNil() throws {
        let raw = ""
        XCTAssertNil(CameraStatus.parseStatusResponse(raw))
    }

    func testParsingErrorStatusReturnsFalseForRecording() throws {
        let raw = "1 ERROR Camera.Preview.MJPEG.status.record=Off"
        let status = CameraStatus.parseStatusResponse(raw)

        XCTAssertNotNil(status)
        XCTAssertEqual(status?.code, 1)
        XCTAssertFalse(status?.isRecording == true)
    }
}
