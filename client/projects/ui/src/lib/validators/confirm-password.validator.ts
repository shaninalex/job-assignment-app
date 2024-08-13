import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';
import { Observable, of } from 'rxjs';

export function confirmPasswordValidator(passwordControlName: string): ValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
        const form = control.parent;
        if (!form) return of(null);

        const passwordControl = form.get(passwordControlName);
        if (passwordControl) {
            const passwordValue = passwordControl.value;
            const confirmPasswordValue = control.value;

            return passwordValue === confirmPasswordValue ? of(null) : of({ 'passwordMismatch': true });
        }

        return of(null)
    };
}
