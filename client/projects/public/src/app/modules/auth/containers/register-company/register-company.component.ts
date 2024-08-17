import { Component, computed, signal } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngrx/store';
import { AppState } from '../../../../store';
import { ActionRegisterCompanyStart } from '../../../../store/account';

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
        });
    }

    submit(): void {
        if (!this.form.valid) return
        this.store.dispatch(ActionRegisterCompanyStart({
            payload: {
                name: this.form.controls['name'].value,
            }
        }))
    }
}
