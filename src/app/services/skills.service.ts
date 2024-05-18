import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { Skill, ApiResponse } from "../types";

const api_endpoints = {
    base: '/api/public/skills'
}

@Injectable({
    providedIn: 'root'
})
export class ApiSkillsService {
    constructor(private http: HttpClient) { }

    public list(): Observable<ApiResponse<Skill[]>> {
        return this.http.get<ApiResponse<Skill[]>>(api_endpoints.base)
    }

    public get(id: number): Observable<ApiResponse<Skill>> {
        return this.http.get<ApiResponse<Skill>>(`${api_endpoints.base}/${id}`)
    }

    // auth required
    public create(payload: Skill): Observable<ApiResponse<Skill>> {
        return this.http.post<ApiResponse<Skill>>(api_endpoints.base, payload)
    }

    // auth required
    public patch(id: number, payload: Skill): Observable<ApiResponse<Skill>> {
        return this.http.patch<ApiResponse<Skill>>(`${api_endpoints.base}/${id}`, payload)
    }

    // auth required
    public delete(id: number): Observable<ApiResponse<null>> {
        return this.http.get<ApiResponse<null>>(`${api_endpoints.base}/${id}`)
    }
}