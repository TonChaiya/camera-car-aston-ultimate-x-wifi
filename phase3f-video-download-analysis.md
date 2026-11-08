# PHASE 3F — Recorded Video Playback & Download API Analysis

## 1) Confirmed from code

### 1.1 File-list XML produces the download URL

The APK code builds the media URL directly from the XML `<name>` value and the camera HTTP prefix:

- [sources/com/tima/app/common/devices/mstar/device/beans/FileListResponse.java](sources/com/tima/app/common/devices/mstar/device/beans/FileListResponse.java#L16-L55)
- [sources/com/tima/app/common/devices/mstar/device/beans/MediaFile.java](sources/com/tima/app/common/devices/mstar/device/beans/MediaFile.java#L7-L40)

Relevant logic:

```java
String strFirstElementTextByTag = firstElementTextByTag(hVar, "name");
mediaFile.path = strFirstElementTextByTag;
mediaFile.url = DeviceKit.getHttpPrefix() + strFirstElementTextByTag;
```

This means the download URL is not guessed; it is built as:

`http://<camera-ip> + <name-from-XML>`

Examples from the live XML:
- `/SD/Normal/F/FILE261108-112940-068377F.TS`
- `/SD/Normal/R/FILE261108-112940-068377R.TS`

So the actual URL pattern is:

`http://192.72.1.1/SD/Normal/F/FILE261108-112940-068377F.TS`

and

`http://192.72.1.1/SD/Normal/R/FILE261108-112940-068377R.TS`

### 1.2 Download method is HTTP GET

The app’s downloader uses OkHttp with a normal Request.Builder, and only adds a Range header when resume is needed:

- [sources/com/tima/app/common/medialist/dao/Downloader.java](sources/com/tima/app/common/medialist/dao/Downloader.java#L22-L170)

Key code:

```java
Request.Builder builderUrl = new Request.Builder().tag(this.url).url(this.url);
StringBuilder sb = new StringBuilder();
sb.append("bytes=");
sb.append(this.file.length());
sb.append("-");
requestBuild = builderUrl.header(HttpHeaders.RANGE, sb.toString()).build();
```

and for the normal full download:

```java
requestBuild = new Request.Builder().tag(this.url).url(this.url).build();
```

This confirms the downloader uses GET for both full and resumed downloads. There is no evidence in the APK of a POST-based video download API.

### 1.3 Download flow from UI to file save

The real file download path is wired through MediaDataAccess:

- [sources/com/tima/app/common/medialist/dao/MediaDataAccess.java](sources/com/tima/app/common/medialist/dao/MediaDataAccess.java#L305-L359)
- [sources/com/tima/app/common/medialist/fragments/MediaListFragment.java](sources/com/tima/app/common/medialist/fragments/MediaListFragment.java#L783-L810)

Important logic:

```java
File file = new File(i.a(videoPath, mediaItem));
File file2 = new File(videoPath + mediaItem.name + ".tmp");
downloader.setup(mediaItem.url, file2, listener);
downloader.start();
```

This means:
- `mediaItem.url` is the exact remote clip URL
- the app writes to a temp file first
- on success it renames the temp file to the final local path

### 1.4 HTTP Range support is expected by the client

The client contains explicit resume-download logic:

```java
if (this.file.exists()) {
    Request.Builder builderUrl = new Request.Builder().tag(this.url).url(this.url);
    StringBuilder sb = new StringBuilder();
    sb.append("bytes=");
    sb.append(this.file.length());
    sb.append("-");
    requestBuild = builderUrl.header(HttpHeaders.RANGE, sb.toString()).build();
}
```

And it handles both full and partial responses:

```java
if (iCode == 200) {
    fileOutputStream = new FileOutputStream(..., false);
    length = 0;
} else if (iCode == 206) {
    length = this.file.length();
    fileOutputStream = new FileOutputStream(..., true);
}
```

This proves the app is designed to support ranged fetches and resume-downloads. However, this is only a client-side expectation. The APK does not contain a direct camera `Accept-Ranges` or `Content-Range` validation path; therefore, server-side Range support is expected but not proven solely from APK code.

## 2) Confirmed from live XML and metadata

From the live front/rear file-list responses already confirmed in [phase3e3-live-filelist-result.md](phase3e3-live-filelist-result.md):

- Front request succeeded: `action=dir&property=Normal&format=all&count=999&from=0&backward=`
- Rear request succeeded: `action=reardir&property=Normal&format=all&count=999&from=0&backward=`
- Both returned XML with `<Normal>` and several `<file>` entries
- The camera reported 10 files in both front and rear lists

### 2.1 Metadata observations

The XML examples show:

- front filename: `/SD/Normal/F/FILE261108-112940-068377F.TS`
- rear filename: `/SD/Normal/R/FILE261108-112940-068377R.TS`
- size values include both `0` and large byte counts such as `216203264`, `278986752`, `279052288`, etc.
- every shown example had `format` set to `BAD`
- `attr` values were `RW`
- `time` values were normal timestamp strings like `2026-11-08 11:29:40`

This means:
- the live camera does expose actual recorded-file metadata
- some entries are non-zero size and therefore likely real clips
- but the raw XML uses `format=BAD`, which does not match the parser’s expected `<format time="...">` shape described in [FileListResponse.java](sources/com/tima/app/common/devices/mstar/device/beans/FileListResponse.java#L16-L55)

So, based on the available live XML, we can confirm that `size > 0` entries exist, but we cannot confirm that every listed file is a valid playable media file because the XML’s `format` field is still marked `BAD` in the live responses.

## 3) Front/rear clip pairing logic

The naming pattern strongly indicates matching by the same timestamp and by camera letter marker `F` vs `R`:

- `/SD/Normal/F/FILE261108-112940-068377F.TS`
- `/SD/Normal/R/FILE261108-112940-068377R.TS`

Both share:
- same date/time stem: `261108-112940`
- same serial suffix: `068377`
- only `F` vs `R` differs

This is the most likely pairing key for front/rear correspondence. The same pattern appears across the rest of the XML entries, which suggests a deterministic front-vs-rear pair based on timestamp + serial.

## 4) What remains unconfirmed

These items are not proven by code alone and therefore remain for a future non-destructive test step:

- whether the camera honors `Range: bytes=...` for a partial `GET`
- whether every `size > 0` file is truly playable video or only a valid TS container artifact
- whether the raw `format=BAD` value is a camera quirk or a signal that the app intentionally ignores it and relies on the extension/path instead
- whether the `http://<camera>/...` file URL is directly playable in the app without extra auth or token headers

## 5) Safe next test design (not executed in this phase)

The next permitted test step, if the team decides to continue later, should be limited to read-only probing of one known valid file URL only, with no mutation or recording changes:

1. Choose one front file and one rear file from the XML with `size > 0` and a matching timestamp.
2. Issue a GET request for the exact remote URL with:
   - `Range: bytes=0-1048575` (first 1 MB)
   - no other endpoint changes
   - 3 second timeout
3. Read only response status, Content-Length, Accept-Ranges, and a short byte prefix from the first few KB.
4. Do not download to local storage.
5. Stop immediately on any 4xx/5xx, timeout, or abnormal response.

This would validate partial-read support without performing the actual video download or changing any camera state.

## 6) Bottom line

### Confirmed
- The APK builds the media URL directly from XML `<name>` values and the camera HTTP prefix.
- The downloader uses GET and supports resume via `Range: bytes=<offset>-`.
- The app handles both 200 and 206 responses.
- Front and rear XML file lists were verified live, each returning 10 entries.
- Matching `F`/`R` filenames share the same timestamp and serial base, which is consistent with front/rear pairing.

### Not yet confirmed
- Whether the camera actually honors HTTP Range on the exact file URLs.
- Whether every `size > 0` file is a valid playable video despite `format=BAD` in the raw XML.
- Whether a direct file GET can be consumed without an app-layer wrapper or additional metadata step.

This report is intentionally limited to code evidence and live XML metadata only; no actual playback or download was performed in this phase.
