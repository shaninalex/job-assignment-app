import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Position, Skill } from '../types';
import { ApiSkillsService } from '../services/skills.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-apply',
  templateUrl: './apply.component.html'
})
export class ApplyComponent implements OnInit {
    position: Position;
    selectedSkills: Skill[];

    form = this.fb.group({
        name: new FormControl("", Validators.required),
        email: new FormControl("", [Validators.required, Validators.email]),
        phone: new FormControl("", Validators.required),  // TODO: phone pattern
        about: new FormControl("", [
            Validators.required, Validators.maxLength(250)]),
    });

    constructor(
        private fb: FormBuilder,
        private activatedRoute: ActivatedRoute
    ) { }

    ngOnInit() {
        this.activatedRoute.data.subscribe(({position}) => {
            this.position = position.data
        });
      }

    submit() {
        if (this.form.valid) {
            // TODO: this should be in ApplyPayload type
            const payload = {
                ...this.form.value,
                skills: this.selectedSkills,
                position_id: this.position.id,
            }
            console.log(payload);
        } else {
            console.log(this.form.errors);
        }
    }

    setSelectedSkills(selected: Skill[]) {
        this.selectedSkills = selected
    }

    setInputValue() {
        this.form.controls.name.setValue('New Name');
    }
}
