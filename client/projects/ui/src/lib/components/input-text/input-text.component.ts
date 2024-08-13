import { Component, forwardRef, Input } from '@angular/core';
import { ControlValueAccessor, FormControl, FormGroup, NG_VALUE_ACCESSOR } from '@angular/forms';


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
    @Input() public parentForm: FormGroup;
    @Input() public fieldName: string;
    @Input() public type: string;
    @Input() public label: string;
    @Input() public isRequired: boolean

    public value: string;
    public changed: (value: string) => void;
    public touched: () => void;
    public isDisabled: boolean;

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
