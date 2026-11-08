# ASTON Ultimate X iOS Foundation

This folder contains a SwiftUI-based foundation for a lightweight iOS app that targets the ASTON Ultimate X WiFi 2K camera.

## Scope

This foundation is intentionally isolated from the reverse-engineering workspace and is limited to:
- a clean SwiftUI app structure
- network access to the confirmed camera endpoints
- XML parsing for front/rear recorded file lists
- mock data and unit tests
- a safe download manager designed for `Range`-based resume behavior
- a protocol-based RTSP player abstraction

No production downloads, no camera state changes, and no code copied from the APK are included here.

## Prerequisites

- macOS with Xcode 15.4 or newer
- Swift 6 toolchain
- iOS 17+ deployment target

## Build on macOS

1. Open the folder in Xcode or run:
   ```bash
   cd ios-app
   xcodebuild -scheme AstonCameraApp -project AstonCameraApp.xcodeproj build
   ```
2. If using a Swift Package style setup in Xcode, select the executable target and an iPhone simulator.

## App architecture

- Network: `CameraAPIClient`
- Models: `CameraStatus`, `RecordedVideo`
- Services: `DownloadManager`, `RTSPPlayerAdapter`
- Views: `DashboardView`, `LiveView`, `GalleryView`, `VideoDetailView`

## Camera endpoints used

- Status:
  `GET /cgi-bin/Config.cgi?action=get&property=Camera.Preview.MJPEG.status.record`
- Front list:
  `GET /cgi-bin/Config.cgi?action=dir&property=Normal&format=all&count=999&from=0&backward=`
- Rear list:
  `GET /cgi-bin/Config.cgi?action=reardir&property=Normal&format=all&count=999&from=0&backward=`

## Important constraints

This project intentionally does not:
- send `action=set` or other state-changing commands
- change UI mode or stop recording
- modify firmware or SD card contents
- begin a live-view implementation for rear camera beyond an adapter abstraction
- claim an app build succeeded without a real Xcode verification run

## Testing

The included tests are mock-based and validate:
- status parsing
- XML list parsing
- range-request generation for downloads

## Notes

This is a foundation only. Real media playback and actual download behavior must be validated on a real macOS/Xcode environment before shipping.
