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