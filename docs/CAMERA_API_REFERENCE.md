# Camera API Reference

This document summarizes only the APIs and behaviors that are explicitly supported by the project reports in the workspace. It intentionally avoids claiming anything that was not observed or documented in the analysis reports.

## Confirmed / documented

- Camera status and file-list endpoints are referenced in the project reports and treated as read-only.
- File list responses are expected to be XML with a root element of `Normal`.
- Valid file paths must begin with `/SD/` and remain inside the camera storage tree.
- Path traversal patterns such as `..` and remote URLs are rejected.
- The app foundation clearly separates live mode and mock mode.

## Unverified

- Real camera HTTP requests were not executed during the current safety phase.
- Any live video download, RTSP streaming, or firmware mutation path remains outside the verified scope.
- Production endpoint details beyond the analysis evidence remain unconfirmed.

## Evidence source

See the phase reports under [phases](phases) and the app files under [../ios-app](../ios-app).
