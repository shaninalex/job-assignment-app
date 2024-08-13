import { Component, Input, forwardRef } from "@angular/core";
import { ControlValueAccessor, FormControl, FormGroup, NG_VALUE_ACCESSOR } from "@angular/forms";
import { passwordStrength, Result } from "check-password-strength";

@Component({
    selector: "ui-input-password",
    templateUrl: "./input-password.component.html",
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => InputPasswordComponent),
            multi: true
        }
    ]
})
export class InputPasswordComponent implements ControlValueAccessor {
    @Input() parentForm: FormGroup;
    @Input() fieldName: string;
    @Input() label: string;
    @Input() isRequired: boolean
    @Input() checkStrength: boolean = false;

    value: string;
    isDisabled: boolean;
    changed: (value: string) => void
    touched: () => void;

    private _type: "text" | "password" = "password";
    private _passwordStrength: Result<string> | null = null;

    get passwordStrength(): Result<string> | null {
        return this._passwordStrength;
    }

    get type(): string {
        return this._type
    }

    get control(): FormControl {
        return this.parentForm.get(this.fieldName) as FormControl;
    }

    toggleVisible(): void {
        if (this._type === 'text') {
            this._type = 'password'
        } else {
            this._type = 'text'
        }
    }

    onChange(event: Event): void {
        const value: string = (<HTMLInputElement>event.target).value;
        if (this.checkStrength) {
            this._passwordStrength = passwordStrength(value);
        }
        this.changed(value);
    }

    writeValue(value: any): void {
        this.value = value
    }

    registerOnChange(fn: any): void {
        this.changed = fn;
    }

    registerOnTouched(fn: any): void {
        this.touched = fn
    }

    setDisabledState(isDisabled: boolean): void {
        this.isDisabled = isDisabled;
    }
}
