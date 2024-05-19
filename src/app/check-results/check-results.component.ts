import { Component } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-check-results',
  templateUrl: './check-results.component.html',
})
export class CheckResultsComponent {
    searchForm = this.fb.group({
        submission_id: new FormControl("", Validators.required)  // TODO: should be uuid type
    });

    constructor(private fb: FormBuilder) {}

    submit() {
        if (this.searchForm.valid) {
            console.log(this.searchForm.value);
        }
    }
}
