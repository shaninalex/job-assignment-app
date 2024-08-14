import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { confirmPasswordValidator } from '@ui';

@Component({
    selector: 'auth-register',
    templateUrl: "./register.component.html",
})
export class RegisterComponent {
    form: FormGroup;

    constructor(private fb: FormBuilder) { }

    ngOnInit() {
        this.form = this.fb.group({
            email: ['', [Validators.required, Validators.email]],
            password: ['', Validators.required],
            password_confirm: ['', Validators.required, confirmPasswordValidator('password')],
        });
    }

    submit(): void {
        if (!this.form.valid) return

        // this.form.value
    }
}
