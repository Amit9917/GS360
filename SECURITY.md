# Security Policy

## Reporting a Vulnerability

We take the security of GS360 seriously. If you believe you have found a security vulnerability, please report it to us as soon as possible.

**Do not open a public issue.** Please email your findings to security@jinacode.systems.

Include as much detail as possible to help us reproduce and address the issue:
- Type of issue (e.g., path traversal, IDOR, cross-tenant leak).
- The component affected (Frontend, Backend, DeepTutor core).
- Steps to reproduce.
- Potential impact.

## Our Commitment

- We will acknowledge your report within 48 hours.
- We will provide an estimated timeframe for a fix.
- We will notify you once the vulnerability has been patched.
- We will give credit to the researcher (if desired) in our security advisories.

## Security Architecture

GS360 implements several mandatory security layers:
- **Path Isolation**: All file operations are scoped to a `UserNamespace` with strict realpath validation.
- **Index Isolation**: User private data is stored in physically separate vector indices.
- **Request-Level Auth**: User identity is extracted from JWT claims, never from request bodies.
- **Audit Logging**: All sensitive operations are logged for forensic review.

Please refer to the implementation plan for detailed security specs.
