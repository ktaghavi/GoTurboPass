# Security Documentation

GoTurboPass Phase 1 security controls and PII handling guidelines.

---

## 1. PII Protection

### Sensitive Data Fields
- **CA Driver License Number** (full)
- **Date of Birth**
- **Password**

### Storage Rules

| Field               | Storage Method                          | Access                  |
|---------------------|-----------------------------------------|-------------------------|
| CA DL (full)        | bcrypt hash + salt (`ca_dl_hash`)       | Never displayed         |
| CA DL (last 4)      | Plaintext (`ca_dl_last4`)               | Certificate only        |
| Date of Birth       | Plaintext (DATE)                        | Backend only            |
| Password            | bcrypt hash (`password_hash`)           | Never displayed         |
| Email               | Plaintext                               | Authenticated users     |

### Logging Rules
**NEVER log these fields**:
- `caDlNumber` (full CA DL)
- `dob` (date of birth)
- `password`
- `ca_dl_hash`

**Audit logs automatically redact** PII fields via `AuditService._redact_pii()`.

---

## 2. Authentication & Authorization

### JWT Tokens
- **Algorithm**: HS256
- **Expiry**: 30 minutes (configurable via `JWT_ACCESS_TOKEN_EXPIRES`)
- **Storage**: In-memory only (frontend)
- **Refresh**: Not implemented in Phase 1

### Email Verification
- Required for STUDENT role before course access
- Phase 1 uses stub token generation (replace with `itsdangerous` in production)

### Roles (RBAC)
- `STUDENT`: Course access, certificate
- `INSTRUCTOR`: Inquiry management
- `ADMIN`: Full system access
- `REVIEWER`: Read-only demo account

---

## 3. Security Headers

### Content Security Policy (CSP)
```
default-src 'self';
script-src 'self';
style-src 'self' 'unsafe-inline';
img-src 'self' data:;
font-src 'self';
connect-src 'self' http://localhost:5173;
frame-ancestors 'none';
base-uri 'none';
```

### Additional Headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000` (production only)

---

## 4. Rate Limiting

| Endpoint Pattern | Limit             |
|------------------|-------------------|
| `/api/auth/*`    | 10 requests/min   |
| Global default   | 100 requests/hour |

Powered by **Flask-Limiter** with in-memory storage (Phase 1).

---

## 5. CORS

**Allowed Origins** (development):
- `http://localhost:5173`

**Production**: Update `FRONTEND_ORIGIN` in `.env` to production domain.

---

## 6. Input Validation

### Backend
- Email: `email-validator` library
- Passwords: Minimum 6 characters (Phase 1)
- CA DL: Required for STUDENT role

### Frontend
- HTML5 validation (required, email, date, minLength)
- Password confirmation matching

---

## 7. Error Handling

**Generic error messages** returned to client (no stack traces).

**Example**:
```json
{ "error": "Registration failed" }
```

**Internal errors** logged server-side only.

---

## 8. Idle Session Timeout

**Frontend**: 20-minute inactivity timeout (AuthContext)

**Events monitored**:
- `mousedown`, `keydown`, `scroll`, `touchstart`

**Action**: Automatic logout + JWT cleared from memory

---

## 9. Database Security

### Passwords
- **Hashing**: bcrypt with salt
- **Service**: `AuthService.hash_password()`

### CA Driver License
- **Hashing**: bcrypt with salt
- **Service**: `AuthService.hash_ca_dl()`
- **Last 4 Extraction**: `AuthService.extract_dl_last4()`

### SQL Injection Prevention
- **ORM**: SQLAlchemy 2.x with parameterized queries
- **No raw SQL** in Phase 1

---

## 10. Audit Logging

### Events Tracked (Phase 1)
- `REGISTER`: User registration
- `VERIFY_EMAIL`: Email verification
- `LOGIN`: Successful login

### Audit Log Fields
```python
{
  "event": "LOGIN",
  "student_id": 123,
  "user_id": 123,
  "ip": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "details": { "email": "user@example.com", "role": "STUDENT" },
  "created_at": "2025-11-07T12:34:56"
}
```

**PII Redaction**: `caDlNumber`, `dob`, `password` auto-redacted in `details`.

---

## 11. Backup & Recovery

See [BACKUP.md](./BACKUP.md) for PostgreSQL backup/restore procedures.

---

## 12. Production Checklist

Before deploying to production:

- [ ] Replace `JWT_SECRET` with cryptographically secure random string
- [ ] Enable HTTPS (TLS certificate)
- [ ] Update `FRONTEND_ORIGIN` to production domain
- [ ] Implement real email verification (replace stub with `itsdangerous`)
- [ ] Set up Redis for rate-limiting (replace in-memory)
- [ ] Enable `HSTS` header (Strict-Transport-Security)
- [ ] Configure database connection pooling
- [ ] Set up automated backups (see BACKUP.md)
- [ ] Review and harden CSP policy
- [ ] Implement rate limiting per user (not just IP)
- [ ] Add password strength requirements (8+ chars, complexity)
- [ ] Enable database SSL connections
- [ ] Configure firewall rules (allow only necessary ports)
- [ ] Set up monitoring & alerting (failed logins, errors)

---

## Contact Security Issues

**Email**: security@goturbopass.com (placeholder)
