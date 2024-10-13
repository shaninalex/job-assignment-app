import { Component, computed, signal } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngrx/store';
import { confirmPasswordValidator } from '@ui';
import { AppState } from '../../../../store';
import { ActionRegisterAccountStart, ActionRegisterCompanyStart } from '../../../../store/account';

@Component({
    selector: 'auth-register',
    templateUrl: "./register.component.html",
})
export class RegisterComponent {
    form: FormGroup;
    companyForm: FormGroup;
    constructor(private fb: FormBuilder, private store: Store<AppState>) { }

    ngOnInit() {
        this.form = this.fb.group({
            name: ['', Validators.required],
            email: ['', [Validators.required, Validators.email]],
            password: ['', Validators.required],
            password_confirm: ['', Validators.required, confirmPasswordValidator('password')],
        });
    }

    submit(): void {
        if (!this.form.valid) return
        this.store.dispatch(ActionRegisterAccountStart({
            payload: {
                name: this.form.controls['name'].value,
                email: this.form.controls['email'].value,
                password: this.form.controls['password'].value,
                password_confirm: this.form.controls['password_confirm'].value,
            }
        }))
    }
}
