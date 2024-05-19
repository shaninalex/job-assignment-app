export interface ApiResponse<T> {
    data: T
    message: string
    success: boolean
}

export interface Position {
    id: number
    name: string
    description: string
    created_at?: string
    skills: Skill[]
}

export interface Skill {
    id?: number
    name: string
}

export interface LoginPayload {
    email: string
    password: string
}

export interface ApplyPayload {
    name: string
    email: string
    phone: string
    about: string
    position_id: number
    skills: Skill[]
}

export interface Candidate {
    id: number
    name: string
    email: string
    phone: string
    about: string
    submitted: boolean
    position: Position
    created_at: string
    skills: Skill[]
}

export interface ErrorItem {
    error_message: string
    field?: string
    details?: string
}

export interface User {
    id: number
    email: string
    created_at: string
}
