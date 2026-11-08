# ASTON Ultimate X WiFi Camera Research Repository

This repository holds reverse-engineering evidence, phase reports, app foundation source code, and local analysis artifacts for the ASTON Ultimate X WiFi camera project.

## Purpose

- Gather and preserve evidence for camera API behavior.
- Review and document safe, read-only app foundation work for an iOS interface.
- Maintain a research archive without damaging original evidence files.

## Current project structure

- [ios-app](ios-app) — SwiftUI app foundation and tests.
- [docs](docs) — structured documentation and status summaries.
- [resources](resources) — extracted camera configuration or support materials.
- [scratch](scratch) — local analysis scripts and investigative utilities.
- [tools](tools) — supporting tooling such as ffmpeg and jadx.
- [artifacts](artifacts) — captured or generated evidence outputs.

## Development status

The current state is intentionally conservative:

- Live camera requests are documented as stubbed and disabled in the app foundation.
- No real firmware, SD card, or device writes are performed.
- No dependency installation or live camera connection is allowed in this phase.
- The repository is organized for safe review and GitHub push preparation, not for production device execution.

## Phase reports

- [docs/phases/phase1](docs/phases/phase1)
- [docs/phases/phase2](docs/phases/phase2)
- [docs/phases/phase3](docs/phases/phase3)
- [docs/phases/phase4](docs/phases/phase4)

## Important constraints

- No Git commit or push is performed here.
- No live camera traffic or firmware modification is allowed.
- No app feature development beyond the existing foundation is added during this phase.
- Xcode or iPhone build success is not claimed unless verified on macOS.
