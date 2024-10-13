import { Company } from "./company"

export interface Position {
    id: string,
    title: string
    description: string
    responsibilities: string
    requirements: string
    interview_stages: string
    offer: string
    company_id: string,
    remote: Remote,
    salary: SalaryType,
    hours: WorkingHours,
    travel: TravelRequired,
    status: PositionStatus,
    price_range: string
    created_at: Date
    updated_at: Date
    company: Company
}

export enum Remote {
    REMOTE = "remote",
    OFFICE = "office",
    PARTIAL = "partial",
}


export enum SalaryType {
    EXPERIENCE = "experience",
    STATIC = "static",
    HOURLY = "hourly",
    AGREEMENT = "agreement",
}


export enum WorkingHours {
    FULL_TIME = "full_time",
    PARTIAL = "partial",
}


export enum TravelRequired {
    REQUIRED = "required",
    NO_MATTER = "no_matter",
    HELP = "help",
}


export enum PositionStatus {
    ACTIVE = "active",
    HIDDEN = "hidden",
    CLOSED = "closed",
    REMOVED = "removed",
}
