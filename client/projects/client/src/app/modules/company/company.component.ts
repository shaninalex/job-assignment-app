import { Component } from '@angular/core';
import { UiService } from '@ui';

@Component({
    selector: 'company-root',
    template: `
<div class='container mx-auto px-4 mb-4'>
    <comp-navbar />
</div>
<div class="container px-4 mx-auto mb-4">
    <router-outlet />
</div>
`
})
export class CompanyRootComponent {
    constructor(private ui: UiService) {
        this.ui.title.next("Company")
    }
}
