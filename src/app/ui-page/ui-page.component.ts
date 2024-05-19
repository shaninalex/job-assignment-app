import { Component } from '@angular/core';
import { Skill } from '../types';

@Component({
  selector: 'app-ui-page',
  templateUrl: './ui-page.component.html'
})
export class UiPageComponent {
    selectedSkills(selected: Skill[]) {
        console.log(selected)
    }
}
