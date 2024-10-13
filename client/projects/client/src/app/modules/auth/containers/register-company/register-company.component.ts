import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../store';
import { ActionRegisterCompanyStart } from '../../../../store/account';
import { confirmPasswordValidator } from '@ui';

@Component({
    selector: 'auth-register',
    templateUrl: "./register-company.component.html",
})
export class RegisterCompanyComponent {
    form: FormGroup;
    constructor(private fb: FormBuilder, private store: Store<AppState>) { }

    ngOnInit() {
        this.form = this.fb.group({
            name: ['', [Validators.required]],
            email: ['', [Validators.required, Validators.email]],
            password: ['', Validators.required],
            password_confirm: ['', Validators.required, confirmPasswordValidator('password')],
            company_name: ['', Validators.required],
        });
    }

    submit(): void {
        if (!this.form.valid) return
        this.store.dispatch(ActionRegisterCompanyStart({
            payload: {
                name: this.form.controls['name'].value,
                email: this.form.controls['email'].value,
                password: this.form.controls['password'].value,
                password_confirm: this.form.controls['password_confirm'].value,
                companyName: this.form.controls['company_name'].value,
            }
        }))
    }
}
