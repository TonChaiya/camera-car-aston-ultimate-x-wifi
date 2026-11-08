# PHASE 3D-3 — JADX Setup and Exact API Extraction

Status: blocked by environment. No usable JADX installation was completed in this workspace, so no method-body extraction from `DeviceApi.getFileList` or `downloadFile` could be verified.

## VERIFIED_FROM_METHOD_BODY

No method body was successfully decompiled or extracted with JADX in this session.

Evidence:
- Existing workspace tools folder currently contains only [tools/ffmpeg](tools/ffmpeg), not a [tools/jadx](tools/jadx) installation.
- No JVM/JADX binary was found in the checked environment and no portable install under the workspace was created.
- No APK decompilation output under an `apk-analysis/jadx-output` directory was produced.

Because of this, there is no code-backed `DeviceApi.getFileList` method body to cite, and no exact `downloadFile` method body to validate.

## INFERRED

The earlier APK artifact evidence from [scratch/dex_summary.json](scratch/dex_summary.json#L1-L36) and [scratch/target_classes_decompiled.json](scratch/target_classes_decompiled.json#L42525-L45650) still supports a narrow inference:

- The APK contains class symbols and string constants for:
  - `DeviceApi`
  - `DeviceHttpEngine`
  - `DeviceRequest`
  - `DeviceRequest` / CGI query builder
  - `FileListResponse`
  - `MediaFile`
  - `CamIdResponse`
  - `getFileList`
  - `downloadFile`
  - `doDownloadFile`
- The request pattern is still inferred as CGI-style:
  - `/cgi-bin/Config.cgi`
  - `action=`
  - `property=`
- Cam/front-rear split is still inferred as source-ID based via:
  - `Camera.Preview.Source.1.Camid`
  - `Camera.Preview.Source.2.Camid`
  - `CamIdResponse`

This remains inference only because it is not backed by a complete method-body decompilation.

## UNKNOWN

The following remain unknown because no actual JADX method-body extraction was achieved:

- Exact `DeviceApi.getFileList` method body
- Exact `DeviceHttpEngine` request construction logic
- Exact `DeviceRequest` URL object and headers
- Exact `downloadFile` URL builder and HTTP method
- Exact `FileListResponse` field names and data types
- Exact `MediaFile` schema and source-cam mapping
- Exact response JSON/XML structure for the video list
- Exact request/query values used by the real file-list API
- Whether the final API is `GET` or `POST` from code, not name-only clues

## Installation attempt status

The user explicitly approved installing the official portable JADX under the workspace only, but the terminal execution environment in this session was unable to complete the download and file creation steps. The workspace still has no [tools/jadx](tools/jadx) folder and no `jadx-output` result folder.

## Final conclusion

This phase is blocked by missing executable access to the required toolchain. Without a working JADX install and a successful decompilation of the APK, the exact file-list endpoint and exact response schema cannot be claimed from method bodies.

The correct result at this stage is: no verified method-body extraction, no exact API endpoint proven, and no final endpoint statement beyond the earlier artifact-level string evidence.
