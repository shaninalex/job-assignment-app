import { Component } from '@angular/core';
import { UiService } from '@ui';

@Component({
    selector: 'app-contacts',
    templateUrl: './contacts.component.html'
})
export class ContactsComponent {
    constructor(private ui: UiService) {
        this.ui.title.next("Contacts - JSA")
    }
}
