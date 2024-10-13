import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Actions, createEffect, ofType } from "@ngrx/effects";
import { ActionRegisterAccountStart, ActionRegisterCompanyStart, ActionLoginAccountStart } from "./account.actions";
import { exhaustMap, of } from "rxjs";
import { LoginResponse, RegistrationPayload } from "../../models";
import { ApiResponse } from "../../models/response";


@Injectable()
export class AccountEffects {
    loginStart$ = createEffect(() => this.actions$.pipe(
        ofType(ActionLoginAccountStart.type),
        exhaustMap(({ payload }) => {
            this.http.post<ApiResponse<LoginResponse>>("api/v1/auth/login", payload).subscribe({
                next: response => {
                    console.log(response.data.token)
                    console.log(response.data.user.id)
                },
                error: error => {

                },
                complete: () => {
                    console.log("request execution complete action")
                }
            })
            return of({ type: "[account] register continues..." })
        })
    ));

    registerStart$ = createEffect(() => this.actions$.pipe(
        ofType(ActionRegisterAccountStart.type),
        exhaustMap(({ payload }) => {
            console.log(payload)
            this.http.post("api/v1/auth/register", payload).subscribe({
                next: response => {

                },
                error: error => {

                },
                complete: () => {
                    console.log("request execution complete action")
                }
            })
            return of({ type: "[account] register continues..." })
        })
    ));

    registerCompanyStart$ = createEffect(() => this.actions$.pipe(
        ofType(ActionRegisterCompanyStart.type),
        exhaustMap(({ payload }) => {
            console.log(payload)
            this.http.post("api/v1/auth/register", payload).subscribe({
                next: response => {

                },
                error: error => {

                },
                complete: () => {
                    console.log("request execution complete action")
                }
            })
            return of({ type: "[account] register continues..." })
        })
    ));

    constructor(
        private actions$: Actions,
        private http: HttpClient,
    ) { }
}
