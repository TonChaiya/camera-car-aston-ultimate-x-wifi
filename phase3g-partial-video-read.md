# PHASE 3G — Safe Front/Rear Video Partial Read Verification

## VERIFIED_FROM_LIVE_CAMERA

The following facts were directly confirmed from the live camera and the APK-derived method-body contract:

- Recording status endpoint returned: `0 OK Camera.Preview.MJPEG.status.record=Recording`
- Front file list request succeeded with XML: `http://192.72.1.1/cgi-bin/Config.cgi?action=dir&property=Normal&format=all&count=999&from=0&backward=`
- Rear file list request succeeded with XML: `http://192.72.1.1/cgi-bin/Config.cgi?action=reardir&property=Normal&format=all&count=999&from=0&backward=`
- The live XML listed matching front/rear file names such as:
  - `/SD/Normal/F/FILE261108-112713-068376F.TS`
  - `/SD/Normal/R/FILE261108-112713-068376R.TS`
- These are a matching timestamp pair and avoid the latest zero-byte file entries.

## RANGE_SUPPORTED / RANGE_IGNORED / UNKNOWN

This phase is intentionally limited to a safe partial read and the explicit custom-Range GET was not successfully captured in this tool environment.

- Front: UNKNOWN
- Rear: UNKNOWN

Reason:
- the browser-based request path blocked direct custom Range fetches by CORS policy
- the terminal execution path did not produce inspectable output in this environment
- therefore, the explicit `Range: bytes=0-4095` behavior remains unconfirmed by live capture in this session

The code evidence from the APK still indicates the client expects partial reads to be possible:
- [sources/com/tima/app/common/medialist/dao/Downloader.java](sources/com/tima/app/common/medialist/dao/Downloader.java#L49-L94) adds `Range: bytes=<offset>-` when a cached file exists
- [sources/com/tima/app/common/medialist/dao/Downloader.java](sources/com/tima/app/common/medialist/dao/Downloader.java#L89-L116) explicitly handles both 200 and 206 responses

However, that is code-level expectation, not live proof of server behavior.

## FILE_CONTENT_PREFIX

No payload prefix was captured from a live custom Range fetch in this session.

- Front file prefix: not captured
- Rear file prefix: not captured

This is because the requirement for a strict 4096-byte read was not executable through the available browser/terminal interfaces without violating the read-limits or exceeding the scope of the test.

## FRONT / REAR RESULT

- Front result: XML listing confirmed; partial binary prefix not captured
- Rear result: XML listing confirmed; partial binary prefix not captured

## NEXT_SAFE_STEP

The safe next step is to run the script in [scratch/phase3g_partial_video_read.py](scratch/phase3g_partial_video_read.py) on a machine that allows raw HTTP GET requests with custom headers and captures only the first 4096 bytes of each response.

The script is written to:
- check recording status first
- read only one front file and one rear file from the confirmed XML list
- send `Range: bytes=0-4095`
- read at most 4096 bytes
- record only HTTP status, Content-Type, Content-Length, Content-Range, Accept-Ranges, and a 32-byte hex prefix
- stop immediately if a timeout, error, or abnormal response appears
- confirm recording status again at the end

This is the only safe continuation path without downloading the full clip or modifying the device.

This report stays within verified evidence and does not claim Range support beyond the actual camera behavior observed in this session.
