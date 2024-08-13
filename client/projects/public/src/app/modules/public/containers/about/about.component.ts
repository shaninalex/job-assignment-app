import { Component } from '@angular/core';
import { UiService } from '@ui';

@Component({
    selector: 'app-about',
    templateUrl: './about.component.html'
})
export class AboutComponent {
    constructor(private ui: UiService) {
        this.ui.title.next("About - JSA")
    }
}
