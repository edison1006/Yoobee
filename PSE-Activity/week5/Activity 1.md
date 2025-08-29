```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant S as System

    U->>S: Open sign-up page
    U->>S: Enter name, email, password<br/>Click "Create account"

    alt Invalid input
        S-->>U: Show error message
    else Valid input
        alt Email already used
            S-->>U: Show "Email already registered"
        else Success
            S-->>U: Send verification email
            S-->>U: Show "Check your email to verify"
        end
    end
