```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant UI as Browser / Sign-up UI
    participant VAL as Client Validation
    participant API as Auth API
    participant SVAL as Server Validation
    participant DB as User DB
    participant MAIL as Email Service
    participant OTP as OTP Service

    U->>UI: Open sign-up page
    U->>UI: Enter name, email, password<br/>Click "Create account"
    UI->>VAL: Validate inputs (format, password strength)
    alt Client validation fails
        VAL-->>UI: Errors (e.g., weak password)
        UI-->>U: Show inline errors
    else Client validation passes
        UI->>API: POST /register {name, email, password}
        API->>SVAL: Validate (email unique, policy checks)
        alt Email already in use
            SVAL-->>API: Conflict
            API-->>UI: 409 Email exists
            UI-->>U: Show "Email already registered"
        else Server validation passes
            API->>DB: Create user (status=pending, hashed pw, audit)
            DB-->>API: User id created
            API->>MAIL: Send verification link (token)
            MAIL-->>U: Verification email
            API-->>UI: 201 Created (pending verification)
            UI-->>U: Prompt to verify email
        end
    end

    rect rgb(245,245,245)
    note over U,MAIL: User checks inbox and clicks the verification link
    U->>UI: Open /verify?token=...
    UI->>API: GET /verify?token
    API->>DB: Lookup token & user
    alt Token invalid/expired
        DB-->>API: Not found / expired
        API-->>UI: 400/410 Error
        UI-->>U: Show "Link expired" + "Resend"
    else Token valid
        DB-->>API: Token OK
        API->>DB: Mark user verified (status=active)
        DB-->>API: Updated
        API-->>UI: 200 Verified + (optional) session/JWT
        UI-->>U: Show "Account verified" & redirect
    end
    end

    opt Optional 2FA on first login
        API->>OTP: Generate OTP (SMS/Email/App)
        OTP-->>U: Deliver code
        U->>UI: Enter OTP
        UI->>API: POST /mfa/verify {code}
        API-->>UI: 200 MFA success -> issue session/JWT
        UI-->>U: Redirect to dashboard
    end
