import { Component, forwardRef, Input } from '@angular/core';
import { ControlValueAccessor, FormControl, FormGroup, NG_VALUE_ACCESSOR } from '@angular/forms';


@Component({
    selector: 'ui-text-input',
    templateUrl: './text-input.component.html',
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => TextInputComponent),
            multi: true
        }
    ]
})
export class TextInputComponent implements ControlValueAccessor {
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

    public onChange(event: Event): void {
        const value: string = (<HTMLInputElement>event.target).value;
        this.changed(value)
    }

    public writeValue(value: any): void {
        this.value = value
    }

    public registerOnChange(fn: any): void {
        this.changed = fn
    }

    public registerOnTouched(fn: any): void {
        this.touched = fn
    }

    public setDisabledState(isDisabled: boolean): void {
        this.isDisabled = isDisabled
    }
}