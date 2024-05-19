import { Component, Input } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Skill } from '../types';
import { ApiSkillsService } from '../services/skills.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-apply',
  templateUrl: './apply.component.html'
})
export class ApplyComponent {
    positionId: number;
    skills: Skill[];

    form = this.fb.group({
        name: new FormControl("", Validators.required),
        email: new FormControl("", [Validators.required, Validators.email]),
        phone: new FormControl("", Validators.required),  // TODO: phone pattern
        about: new FormControl("", [
            Validators.required, Validators.maxLength(250)]),
        skills: new FormControl<Skill[] | null>([])
    });

    constructor(
        private fb: FormBuilder,
        private router: ActivatedRoute,
        private skillsService: ApiSkillsService
    ) {
        // TODO: get position id from url
        // TODO: before rendering component check if position with given id is exists 
        //        use Resolvers: https://angular.io/api/router/ResolveFn
        // TODO: Yes it call api request every time you open modal
        
        // I'll refactor this with ngrx later
        this.skillsService.list().subscribe({
            next: results => this.skills = results.data
        })
    }

    submit() {
        if (this.form.valid) {
            // TODO: this should be in ApplyPayload type
            const payload = {
                ...this.form.value,
                position_id: this.positionId,
                skills: [],
            }
            console.log(payload);
        } else {
            console.log(this.form.errors);
        }
    }
}
