---
name: nextjs-app-router
description: "Use when build Next.js App Router applications."
license: LicenseRef-Kayan-Owner-Terms
---
# nextjs-app-router

## Scope
Build Next.js App Router applications. Apply only when relevant to the requested task; inspect the existing project and installed versions first.

## Implementation workflow
1. Identify the affected boundaries, existing conventions, dependencies and failure modes.
2. Separate server and client components; authorize server actions; define caching explicitly.
3. Implement the smallest complete production change, preserving compatibility or documenting a migration.
4. Run typecheck build and route integration tests.

## Acceptance criteria
- The implementation satisfies the stated scope and the verification step above with recorded evidence.
- Error handling, authorization and data integrity are verified wherever applicable.
- No secrets are exposed; no external deployment, destructive operation or unrelated change is performed without explicit authorization.
- Report tests actually run, remaining risks and rollback or recovery procedure where applicable.

## Reference and provenance
Original Kayan-authored guidance, not copied from upstream. Consult the applicable version-specific official documentation before implementation. Starting reference: https://github.com/KAYANSTOR/kayan-skill
License: repository owner terms; see root LICENSE. No open-source license grant is implied.
