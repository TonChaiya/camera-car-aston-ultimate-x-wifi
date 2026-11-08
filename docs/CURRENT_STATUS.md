# Current Status

This repository contains an evidence-first reverse engineering and app-foundation project for the ASTON Ultimate X WiFi camera. The current working status is intentionally conservative and written to match the checkpoint reports already present in the workspace.

## Confirmed

- The Android APK and decompiled artifacts were analyzed to establish a camera CGI contract and file-list conventions.
- The iOS SwiftUI foundation project exists under [../ios-app](../ios-app).
- The project keeps mock-preview mode separate from live camera mode.
- The XML file-list parser was hardened to reject malformed XML and invalid file paths.
- Data collection and API analysis remain read-only and no live camera connection is permitted in this phase.

## Unverified

- Any real Xcode build or iPhone execution remains unverified because there is no macOS/Xcode toolchain in this environment.
- Any live camera download or RTSP pathway remains a stub and not a production implementation.
- Real network calls to a physical camera were not executed in this repo organization phase.

## Planned next steps

1. Validate the Swift package or Xcode project in a macOS environment.
2. Complete device or mock-data integration after strict runtime verification.
3. Continue app development only after the current safety constraints are met.
