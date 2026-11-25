---
name: docker-engineering
description: "Use when build minimal reproducible containers."
license: LicenseRef-Kayan-Owner-Terms
---
# docker-engineering

## Scope
Build minimal reproducible containers. Apply only when relevant to the requested task; inspect the existing project and installed versions first.

## Implementation workflow
1. Identify the affected boundaries, existing conventions, dependencies and failure modes.
2. Use multi stage builds nonroot user and pinned dependencies; exclude secrets.
3. Implement the smallest complete production change, preserving compatibility or documenting a migration.
4. Scan image and test health shutdown.

## Acceptance criteria
- The implementation satisfies the stated scope and the verification step above with recorded evidence.
- Error handling, authorization and data integrity are verified wherever applicable.
- No secrets are exposed; no external deployment, destructive operation or unrelated change is performed without explicit authorization.
- Report tests actually run, remaining risks and rollback or recovery procedure where applicable.

## Reference and provenance
Original Kayan-authored guidance, not copied from upstream. Consult the applicable version-specific official documentation before implementation. Starting reference: https://docs.github.com/actions
License: repository owner terms; see root LICENSE. No open-source license grant is implied.
