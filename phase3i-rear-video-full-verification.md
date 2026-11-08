# PHASE 3I — Rear Camera Full Video Verification

## VERIFIED_FROM_LIVE_CAMERA

### 1) Recording status before download
- Status endpoint: `http://192.72.1.1/cgi-bin/Config.cgi?action=get&property=Camera.Preview.MJPEG.status.record`
- Result: `0 OK Camera.Preview.MJPEG.status.record=Recording`
- Conclusion: the camera was live and recording at the time of verification.

### 2) Rear file list confirmation
- Rear XML endpoint: `http://192.72.1.1/cgi-bin/Config.cgi?action=reardir&property=Normal&format=all&count=999&from=0&backward=`
- Confirmed target file in XML:
  - `/SD/Normal/R/FILE261108-112713-068376R.TS`
- Target file size from XML: `148699352` bytes (non-zero)
- The exact URL used for read/download was:
  - `http://192.72.1.1/SD/Normal/R/FILE261108-112713-068376R.TS`

### 3) Range-read confirmation
Latest PowerShell validation result for the exact target file:
- HTTP Status: `206 Partial Content`
- Content-Length: `4096`
- Content-Range: `bytes 0-4095/148699352`
- MPEG-TS sync prefix: `0x47`

This confirms that the rear file is accessible over HTTP and that the server supports Range requests for the exact file.

### 4) File saved to workspace
- Download target path: `artifacts/rear-video-verification/FILE261108-112713-068376R.TS`
- File was acquired as a single rear-camera target file for verification.

## UNVERIFIED

The following items are not yet proven by final decode output in this session, because no validated ffprobe/ffmpeg result was attached to the current message:

- Codec
- Resolution
- FPS
- Duration
- Audio codec
- FFmpeg decode result
- Direct comparison with front-camera file playback

These should be treated as still unverified until the file is profiled and decoded with the local FFmpeg tools in the workspace.

## SAFETY STATUS

No unsafe operations were performed in this phase:
- no `action=set`
- no delete / format / reset
- no UI mode change
- no recording stop
- no SD-card editing
- no firmware changes
- no extra endpoint probing beyond the confirmed rear-file URL

## FINAL CONCLUSION

The exact rear TS file was successfully verified as reachable and downloadable via the confirmed HTTP Range flow, and the camera remained in recording state during the test. The server responded with `206 Partial Content` and `Content-Range: bytes 0-4095/148699352`, which is strong live evidence that the rear recorded video is accessible from the camera over HTTP.

The only remaining gap is the final ffprobe/ffmpeg decode output, which is intentionally left as unverified in this report until the actual file is profiled on the local machine.
