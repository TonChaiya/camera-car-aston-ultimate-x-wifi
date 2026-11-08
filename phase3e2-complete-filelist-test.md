# PHASE 3E-2 — Complete File List Request Verification

## VERIFIED_FROM_APK

Exact method body evidence was found in:

- [sources/com/tima/app/common/devices/mstar/device/DeviceApi.java](sources/com/tima/app/common/devices/mstar/device/DeviceApi.java#L11-L49)
- [sources/com/tima/app/common/devices/mstar/device/beans/DeviceRequest.java](sources/com/tima/app/common/devices/mstar/device/beans/DeviceRequest.java#L6-L58)
- [sources/com/tima/app/common/devices/mstar/device/beans/FileListResponse.java](sources/com/tima/app/common/devices/mstar/device/beans/FileListResponse.java#L16-L55)
- [sources/com/tima/app/mstar/helper/DrCallbackImpl.java](sources/com/tima/app/mstar/helper/DrCallbackImpl.java#L136-L170)

### Exact request builder

From DeviceApi.getFileList:

- `CGI_URL = "cgi-bin/Config.cgi?"`
- `ACTION = "action="`
- `PROPERTY = "property="`
- `str` is the action value passed in.
- `typeToString(i2)` converts type values to `Normal`, `Event`, `Park`, `Photo`, etc.
- appends exactly:
  - `&action=<str>`
  - `&property=<typeToString(i2)>`
  - `&format=all`
  - `&count=<i4>`
  - `&from=<i3>`
  - `&backward=`

Therefore the exact URL pattern is:

`http://<deviceIP>/cgi-bin/Config.cgi?action=<str>&property=<typeToString(i2)>&format=all&count=<i4>&from=<i3>&backward=`

### Exact actions used by the app

From DeviceRequest and DrCallbackImpl:

- `DeviceRequest.ACTION_DIR = "dir"`
- `DeviceRequest.ACTION_REAR_DIR = "reardir"`
- when camera is front: `str = DeviceRequest.ACTION_DIR`
- when camera is rear: `str = DeviceRequest.ACTION_REAR_DIR`

So the valid calls derived directly from code are:

- `http://<deviceIP>/cgi-bin/Config.cgi?action=dir&property=Normal&format=all&count=999&from=0&backward=`
- `http://<deviceIP>/cgi-bin/Config.cgi?action=reardir&property=Normal&format=all&count=999&from=0&backward=`

### Exact response structure

From FileListResponse.parse:

- XML root contains repeated `<file>` nodes
- field extraction is:
  - `name`
  - `size`
  - `time`
  - `<format time="...">`
- then MediaFile is populated as:
  - `mediaFile.name`
  - `mediaFile.path`
  - `mediaFile.url`
  - `mediaFile.size`
  - `mediaFile.time`
  - `mediaFile.duration`
  - `mediaFile.thumb`

This is the exact metadata carried by the file list.

## VERIFIED_FROM_LIVE_CAMERA

The live camera responses captured during the read-only check were:

### Recording status before

`0 OK`

`Camera.Record.Available=0`
`Camera.Record.Remaining=513`
`Camera.Record.Start=-17958`
`Camera.Record.TS=0`
`Camera.Record.Total=17961`

### Incomplete requests rejected

The earlier live checks using only:

- `action=dir`
- `action=reardir`

returned:

- `701 Illegal Parameter`

This matches the code finding that those actions are only valid when the complete parameter set is present.

### Stop condition

Because the camera rejected the incomplete form, no further parameter fuzzing or repeated requests were made.

No unsafe actions were performed:
- no `action=set`
- no delete / format / reset
- no UI mode change
- no recording stop
- no file download

## Limit

The exact live XML file-list payload for a valid front/rear request was not returned in this session because the camera rejected the invalid incomplete requests and the stop rule was triggered before any further experimentation.

The verified result is therefore:

- The request format is proven from APK code.
- The live device rejected incomplete directory requests.
- The exact successful file-list payload remains unconfirmed live because additional parameter mutations were not allowed.
