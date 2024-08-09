import { Component } from '@angular/core';
import { UiService } from '@ui';

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html'
})
export class HomeComponent {
    constructor(private ui: UiService) {
        this.ui.title.next("Home - JSA")
    }
}
