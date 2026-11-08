# PHASE 3E — Front/Rear Recorded File List Verification

Status: read-only live verification was attempted and completed with explicit camera responses.

## LIVE RESULTS

### 1) Recording status before directory tests

HTTP GET:
- `http://192.72.1.1/cgi-bin/Config.cgi?action=get&property=Camera.Record.*`

Result:
- `0 OK`
- `Camera.Record.Available=0`
- `Camera.Record.Remaining=513`
- `Camera.Record.Start=-17958`
- `Camera.Record.TS=0`
- `Camera.Record.Total=17961`

### 2) Front directory list test

HTTP GET:
- `http://192.72.1.1/cgi-bin/Config.cgi?action=dir`

Result:
- `701 Illegal Parameter`

### 3) Rear directory list test

HTTP GET:
- `http://192.72.1.1/cgi-bin/Config.cgi?action=reardir`

Result:
- `701 Illegal Parameter`

### 4) Recording status after directory tests

HTTP GET:
- `http://192.72.1.1/cgi-bin/Config.cgi?action=get&property=Camera.Record.*`

Result:
- `0 OK`
- `Camera.Record.Available=0`
- `Camera.Record.Remaining=473`
- `Camera.Record.Start=-54622`
- `Camera.Record.TS=0`
- `Camera.Record.Total=54624`

## VERIFIED_FROM_LIVE_CAMERA

- The camera accepted the read-only status query.
- The camera rejected both directory-list requests with `701 Illegal Parameter`.
- The directory actions `dir` and `reardir` were not accepted by this device in this state.
- No file-list XML payload was returned.
- Recording status remained readable and no unsafe action was issued.

## CONCLUSION

The live verification shows that the action values `dir` and `reardir` are not valid for this camera in the current state, even though the status endpoint is valid.

This means the file-list API for the front/rear recorded files is not confirmed from live HTTP in this environment, and no further request should be sent without a valid device-specific parameter set.

No unsafe actions were performed: no `action=set`, no delete/format, no UI-mode change, no recording stop, and no file download.
