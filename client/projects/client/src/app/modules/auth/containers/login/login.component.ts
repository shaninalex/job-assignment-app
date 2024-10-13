
import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../store';
import { ActionLoginAccountStart } from '../../../../store/account';


export interface LoginForm {
    email: FormControl<string>;
    password: FormControl<string>;
}

export interface LoginPayload {
    email: string
    password: string
}

@Component({
    selector: 'auth-login',
    templateUrl: "./login.component.html",
})
export class LoginComponent {
    form: FormGroup<LoginForm> = this.fb.group<LoginForm>({
        email: new FormControl('peter@taylor-ltd.com', {
            nonNullable: true,
            validators: [Validators.required, Validators.email]
        }),
        password: new FormControl('password', {
            nonNullable: true,
            validators: Validators.required
        }),
    });;

    constructor(private fb: FormBuilder, private store: Store<AppState>) { }

    submit(): void {
        const payload = this.form.getRawValue()
        this.store.dispatch(ActionLoginAccountStart({ payload }))
    }
}
