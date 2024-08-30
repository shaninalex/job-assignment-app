export interface Account {
    ID: string
    email: string
}

export interface RegistrationPayload {
    name: string
    email: string
    password: string
    password_confirm: string
    type: "company" | "candidate"
    companyName?: string
}
