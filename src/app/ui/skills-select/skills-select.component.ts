import { Component, ElementRef, EventEmitter, Output, ViewChild } from '@angular/core';
import { ApiSkillsService } from '../../services/skills.service';
import { Skill } from '../../types';

@Component({
    selector: 'app-skills-select',
    templateUrl: './skills-select.component.html'
})
export class SkillsSelectComponent {
    @ViewChild('searchInput') inputElement!: ElementRef;
    @Output() onSubmit: EventEmitter<Skill[]> = new EventEmitter<Skill[]>();
    searchPrompt: string = "";
    isLoading: boolean = true;
    skills: Skill[] = [];
    displayed: Skill[] = [];
    selected: Skill[] = [];

    constructor(private skillsService: ApiSkillsService) {
        this.skillsService.list().subscribe({
            next: results => {
                this.skills = results.data;
                this.displayed = this.skills;
                this.isLoading = false
            }
        })
    }

    create() { this.createSkill() }

    change($event: Event) {
        this.searchPrompt = ($event.target as HTMLInputElement).value;
        this.search(this.searchPrompt)
    }

    submit() {
        this.onSubmit.emit(this.selected);
    }

    addToSelected(idx: number) {
        // get skill form displayed list
        const selected = this.displayed[idx];
        // check if already exists in selected
        if (!this.selected.filter(s => s.name === selected.name).length) {
            // add it to selected if not
            this.selected.push(selected);
        }
    }

    removeFromSelected(idx: number) {
        this.selected = this.selected.filter(s => s.name !== this.selected[idx].name);
    }

    private search(text: string) {
        this.displayed = this.skills.filter(s => s.name.includes(text))
        console.log(this.displayed);
    }

    private createSkill() {
        if (this.searchPrompt.length) {
            const newSkill: Skill = { name: this.searchPrompt }
            this.skills.push(newSkill);
            this.selected.push(newSkill);
            this.searchPrompt = "";
            this.inputElement.nativeElement.value = '';
            this.displayed = this.skills;
        }
    }
}
