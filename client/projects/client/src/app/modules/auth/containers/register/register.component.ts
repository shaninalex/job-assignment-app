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
    formTab: "candidate" | "company" = "candidate";
    constructor(private fb: FormBuilder, private store: Store<AppState>) { }

    ngOnInit() {
        this.form = this.fb.group({
            email: ['', [Validators.required, Validators.email]],
            password: ['', Validators.required],
            password_confirm: ['', Validators.required, confirmPasswordValidator('password')],
        });

        this.companyForm = this.fb.group({
            name: ['', [Validators.required]],
        });
    }

    submit(): void {
        if (!this.form.valid) return
        if (this.formTab === 'candidate') {
            this.store.dispatch(ActionRegisterAccountStart({
                payload: {
                    email: this.form.controls['email'].value,
                    password: this.form.controls['password'].value,
                    password_confirm: this.form.controls['password_confirm'].value,
                }
            }))
        } else if (this.formTab === 'company') {
            this.store.dispatch(ActionRegisterCompanyStart({
                payload: {
                    name: this.companyForm.controls['name'].value,
                }
            }))
        }
    }

    changeFormTab(tab: "candidate" | "company") {
        this.formTab = tab;
    }
}
