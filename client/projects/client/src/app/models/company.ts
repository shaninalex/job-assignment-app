export interface Company {
    id: string
    name: string,
    website: string,
    email: string,
    status: CompanyStatus,
    image_link?: string
}

export interface RegistrationCompanyPayload {
    name: string
}

export enum CompanyStatus {
    ACTIVE = "active",
    INACTIVE = "inactive",
    BANNED = "banned",
    PENDING = "pending",
}
