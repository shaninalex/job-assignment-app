export interface LoginPayload {
    email: string
    password: string
}


export interface LoginResponse {
    token: string
    user: Account
}

export enum Role {
  CANDIDATE = "candidate",
  COMPANY_MEMBER = "company_member",
  COMPANY_ADMIN = "company_admin",
  COMPANY_HR = "company_hr",
}

export interface Account {
    id: string
    name: string
    email: string
    image: string
    social_accounts: any
    role: Role
}

export interface RegistrationPayload {
    name: string
    email: string
    password: string
    password_confirm: string
    companyName?: string
}
