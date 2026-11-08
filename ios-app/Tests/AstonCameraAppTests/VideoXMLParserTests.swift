import XCTest
@testable import AstonCameraApp

final class VideoXMLParserTests: XCTestCase {
    func testFrontVideoParser() throws {
        let xml = """
        <Normal>
          <file>
            <name>/SD/Normal/F/FILE261108-112713-068376F.TS</name>
            <format>BAD</format>
            <size>148701184</size>
            <attr>RW</attr>
            <time>2026-11-08 11:27:13</time>
          </file>
        </Normal>
        """

        let parser = VideoXMLParser(camera: .front)
        let videos = parser.parse(data: xml.data(using: .utf8)!)

        XCTAssertEqual(videos.count, 1)
        XCTAssertEqual(videos[0].camera, .front)
        XCTAssertTrue(videos[0].sizeBytes > 0)
    }

    func testRearVideoParser() throws {
        let xml = """
        <Normal>
          <file>
            <name>/SD/Normal/R/FILE261108-112713-068376R.TS</name>
            <format>BAD</format>
            <size>148701184</size>
            <attr>RW</attr>
            <time>2026-11-08 11:27:13</time>
          </file>
        </Normal>
        """

        let parser = VideoXMLParser(camera: .rear)
        let videos = parser.parse(data: xml.data(using: .utf8)!)

        XCTAssertEqual(videos.count, 1)
        XCTAssertEqual(videos[0].camera, .rear)
        XCTAssertEqual(videos[0].name, "/SD/Normal/R/FILE261108-112713-068376R.TS")
    }

    func testParserRejectsInvalidFilePath() throws {
        let xml = """
        <Normal>
          <file>
            <name>http://evil.example/SD/Normal/F/FILE.TS</name>
            <format>BAD</format>
            <size>148701184</size>
            <attr>RW</attr>
            <time>2026-11-08 11:27:13</time>
          </file>
        </Normal>
        """

        let parser = VideoXMLParser(camera: .front)
        let videos = parser.parse(data: xml.data(using: .utf8)!)

        XCTAssertTrue(videos.isEmpty)
    }

    func testParserReturnsFailureForMalformedXML() throws {
        let xml = "<Normal><file><name>/SD/Normal/F/FILE.TS</name>"
        let parser = VideoXMLParser(camera: .front)
        let result = parser.parseValidated(data: xml.data(using: .utf8)!)

        XCTAssertThrowsError(try result.get())
    }

    func testParserReturnsEmptyListForNoValidEntries() throws {
        let xml = "<Normal></Normal>"
        let parser = VideoXMLParser(camera: .front)
        let result = parser.parseValidated(data: xml.data(using: .utf8)!)

        XCTAssertThrowsError(try result.get())
    }
}
