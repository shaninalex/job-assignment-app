export interface Account {
    ID: string
    email: string
}

export interface RegistrationPayload {
    email: string
    password: string
    password_confirm: string
}
