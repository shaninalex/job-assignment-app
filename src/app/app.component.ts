import { Component } from '@angular/core';
import { FormArray, FormBuilder, FormControl, Validators } from '@angular/forms';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})
export class AppComponent {
    form = this.fb.group({
        "name": new FormControl("", Validators.required),
        "skills": this.fb.array<any>([])
    })

    constructor(
        private fb: FormBuilder
    ) { }

    get skills(): FormArray {
        return this.form.get("skills") as FormArray
    }

    addSkills() {
        console.log("add new row")
        const skillsForm = this.fb.group({
            "skill": new FormControl("", [Validators.required, Validators.minLength(3)]),
            "level": new FormControl("", [Validators.required, Validators.minLength(3)]),
        });
        this.skills.push(skillsForm);
    }

    removeSkill(index: number) {
        console.log("delete row:", index)
        this.skills.removeAt(index);
    }

    onSubmit() {
        console.log("form submitted")
        console.log(this.form);
    }
}
