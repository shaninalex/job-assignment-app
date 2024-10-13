import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Actions, createEffect, ofType } from "@ngrx/effects";
import { ActionRegisterAccountStart, ActionRegisterCompanyStart } from "./account.actions";
import { exhaustMap, of } from "rxjs";
import { RegistrationPayload } from "../../models";


@Injectable()
export class AccountEffects {
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
