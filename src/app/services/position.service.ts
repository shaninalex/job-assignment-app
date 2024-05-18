import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { Position, ApiResponse } from "../types";

const api_endpoints = {
    base: '/api/public/positions'
}

@Injectable({
    providedIn: 'root'
})
export class ApiPositionService {
    constructor(private http: HttpClient) { }

    public list(): Observable<ApiResponse<Position[]>> {
        return this.http.get<ApiResponse<Position[]>>(api_endpoints.base)
    }

    public get(id: number): Observable<ApiResponse<Position>> {
        return this.http.get<ApiResponse<Position>>(`${api_endpoints.base}/${id}`)
    }

    // auth required
    public create(payload: Position): Observable<ApiResponse<Position>> {
        return this.http.post<ApiResponse<Position>>(api_endpoints.base, payload)
    }

    // auth required
    public patch(id: number, payload: Position): Observable<ApiResponse<Position>> {
        return this.http.patch<ApiResponse<Position>>(`${api_endpoints.base}/${id}`, payload)
    }

    // auth required
    public delete(id: number): Observable<ApiResponse<null>> {
        return this.http.get<ApiResponse<null>>(`${api_endpoints.base}/${id}`)
    }
}