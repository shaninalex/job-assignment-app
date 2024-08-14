import { Component, forwardRef, Input } from '@angular/core';
import { ControlValueAccessor, FormControl, FormGroup, NG_VALUE_ACCESSOR } from '@angular/forms';
import { v4 as uuid } from "uuid";


@Component({
    selector: 'ui-input-text',
    templateUrl: './input-text.component.html',
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => InputTextComponent),
            multi: true
        }
    ]
})
export class InputTextComponent implements ControlValueAccessor {
    @Input() parentForm: FormGroup;
    @Input() fieldName: string;
    @Input() type: string;
    @Input() label: string;
    @Input() isRequired: boolean

    id: string = uuid();
    value: string;
    changed: (value: string) => void;
    touched: () => void;
    isDisabled: boolean = false;

    get control(): FormControl {
        return this.parentForm.get(this.fieldName) as FormControl;
    }

    onChange(event: Event): void {
        const value: string = (<HTMLInputElement>event.target).value;
        this.changed(value)
    }

    writeValue(value: any): void {
        this.value = value
    }

    registerOnChange(fn: any): void {
        this.changed = fn
    }

    registerOnTouched(fn: any): void {
        this.touched = fn
    }

    setDisabledState(isDisabled: boolean): void {
        this.isDisabled = isDisabled
    }
}
