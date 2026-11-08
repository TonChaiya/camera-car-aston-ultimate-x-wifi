# PHASE 3D-2 — Exact File List API Extraction

Status: exact request extraction is limited by missing usable method-body decompilation. This report is based only on available APK DEX/class/string evidence and stops without guessing beyond code-backed facts.

## VERIFIED_FROM_CODE

### 1) Code-backed class and method names

The class-signature scan in [scratch/decompile_device_api.py](scratch/decompile_device_api.py#L1-L129) and the extracted artifact [scratch/target_classes_decompiled.json](scratch/target_classes_decompiled.json#L42525-L45650) show these relevant symbols are present in the APK:

- `DeviceApi`
- `DeviceHttpEngine`
- `DeviceRequest`
- `FileListResponse`
- `MediaFile`
- `MediaDataAccess`
- `CamIdResponse`
- `getFileList`
- `downloadFile`
- `doDownloadFile`

The string summary in [scratch/dex_summary.json](scratch/dex_summary.json#L1-L36) confirms the following constants also exist in code:

- `cgi-bin/Config.cgi?`
- `action=`
- `property=`
- `Camera.Preview.Source.1.Camid`
- `Camid=`
- `Camera.Preview.Source.Totals=2`
- `Before downloadFile:`
- `After downloadFile:`
- `MediaDataAccess->downloadFile->onError:`
- `downloadFiles`

### 2) Exact code-backed Request pattern

The DEX strings prove the request builder is CGI-style URL parameter encoding, not a freeform REST path:

- base path: `/cgi-bin/Config.cgi`
- params: `action=` and `property=`
- source-specific property keys: `Camera.Preview.Source.1.Camid`, `Camera.Preview.Source.2.Camid`

This is visible in [scratch/dex_summary.json](scratch/dex_summary.json#L1-L36), [scratch/target_classes_decompiled.json](scratch/target_classes_decompiled.json#L39274-L40560), and [scratch/target_classes_decompiled.json](scratch/target_classes_decompiled.json#L55380-L56760).

### 3) Code-backed download flow markers

The method names and log strings provide verified download flow indicators:

- `downloadFile`
- `doDownloadFile`
- `Before downloadFile:`
- `After downloadFile:`
- `Downloader->onResponse, code:`
- `Downloader->onFailure,exception:`
- `MediaDataAccess->downloadFile->onError:`

These are explicit code strings in the APK artifact and are the only download-related evidence available from the existing decompiled output.

### 4) Camera split evidence

The camera split is code-backed as source-id based, not as a UI mode switch:

- `Camera.Preview.Source.1.Camid`
- `Camera.Preview.Source.2.Camid`
- `CamIdResponse`
- `Camid=`
- `Camera.Preview.Source.Totals=2`

This is enough to say the app tracks front/rear identity through source IDs and camera IDs, not by a recorded-action or mode-change call.

## INFERRED

The following are strongly suggested by the code strings and are consistent with the project protocol, but they are not proven from an exact method body:

- The file-list request is likely in the form:
  - `GET /cgi-bin/Config.cgi?action=get&property=Camera.File.*`
- The source-specific query is likely:
  - `GET /cgi-bin/Config.cgi?action=get&property=Camera.Preview.Source.1.Camid`
  - `GET /cgi-bin/Config.cgi?action=get&property=Camera.Preview.Source.2.Camid`
- `FileListResponse` is likely a wrapper around a list of `MediaFile` items.
- `MediaFile` likely carries path/filename/timestamp/size/source metadata used by `downloadFile`.
- Front/rear separation is most likely based on `camId` / source ID rather than changing `UIMode` or stopping recording.

## UNKNOWN

The following remain unknown because no usable JADX method body was available in the workspace:

- Exact HTTP method used by `DeviceApi.getFileList` (`GET` vs `POST`), from method body
- Exact URL path beyond the CGI base string
- Exact query parameters and their concrete values for the real file-list request
- Exact field names and data types of `FileListResponse`
- Exact field names and data types of `MediaFile`
- Exact `DeviceRequest` construction and `DeviceHttpEngine` call chain from method body
- Exact `downloadFile` URL builder and request body from method body
- Exact front/rear directory or filename naming rule for recorded media

## Limitation / no JADX available

The environment check for decompilation tooling returned no usable `jadx` or `jadx-gui` executable.

The only available APK-decompile artifacts in this workspace are:

- [scratch/decompile_device_api.py](scratch/decompile_device_api.py#L1-L129)
- [scratch/dex_summary.json](scratch/dex_summary.json#L1-L36)
- [scratch/target_classes_decompiled.json](scratch/target_classes_decompiled.json#L42525-L45650)

Those files are sufficient to verify symbol names and static constants, but they are not enough to reconstruct the exact method bodies of `DeviceApi.getFileList` and `downloadFile` in full Java/Kotlin form. Therefore no exact endpoint or final request payload can be claimed beyond the code-backed CGI parameter pattern above.

## Conclusion

The exact file-list API endpoint is not proven from method-body decompilation in this environment. The strongest verified fact is that the APK uses a CGI-style URL query pattern tied to `action` and `property`, with source-ID data carried via `Camera.Preview.Source.*.Camid`, and the file download flow is built around `FileListResponse` → `MediaFile` → `downloadFile` → `Downloader`.

No further extraction is claimed beyond this evidence-based boundary.
