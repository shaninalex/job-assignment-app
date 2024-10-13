export interface ApiResponse<T> {
    message: string[]
    success: boolean
    error: any
    data: T
}
