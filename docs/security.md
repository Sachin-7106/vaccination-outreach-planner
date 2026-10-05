# Security Architecture & Threat Model

## Overview
The Vaccination Outreach Planner enforces multi-layered security across authentication, authorization, data integrity, and operational oversight.

---

## 1. Authentication & JWT Token Architecture

1. **Password Hashing**: Passwords are saved as salted PBKDF2-SHA256 hashes (100,000 iterations) using standard library cryptographic functions.
2. **JWT Access Tokens**: Authenticated sessions issue signed HS256 JWT tokens containing `sub` (username), `role` (`ADMIN` or `CLINICIAN`), and `exp` (expiration timestamp).
3. **Header Transmission**: Clients present tokens via standard `Authorization: Bearer <token>` headers on all protected endpoints.

---

## 2. Role-Based Access Control (RBAC)

- **Backend Authoritative**: Frontend role labels are purely for user experience. All API endpoints re-verify permissions directly against the decoded JWT token.
- **Admin Privilege Scope**: Hard constraint overrides (`OVERRIDDEN`) and administrative audit operations strictly require `ADMIN` role claims (returning HTTP 403 Forbidden for Clinicians).

---

## 3. Concurrency Protection & Audit Integrity

- **Optimistic Locking**: State transitions from `PENDING` execute via single atomic `UPDATE ... WHERE status = 'PENDING'` queries.
- **Append-Only Audit Trail**: Review records are immutable; no DELETE or UPDATE API endpoints exist for historical audit entries.

---

## 4. Threat Mitigations

| Threat Vector | Severity | Mitigation Strategy |
|---|---|---|
| Role Spoofing in Client Requests | High | Identity & role claims extracted exclusively from validated JWT signatures. |
| Double-Review Race Conditions | Medium | Atomic state updates ensure exactly-once state finalization (HTTP 409). |
| Unjustified Hard Constraint Override | High | Backend rejects `OVERRIDDEN` requests lacking a non-empty `override_reason` (min 5 chars). |
| CORS Wildcard Exploitation | Medium | Configurable origin whitelist (`CORS_ORIGINS`) replaces wildcard `*` settings. |
