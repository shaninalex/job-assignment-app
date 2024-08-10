
import { Component } from '@angular/core';

@Component({
    selector: 'p-root',
    template: `
<div class="container mb-4 mx-auto px-5">
    <p-navbar />
</div>
<router-outlet />
`
})
export class PublicRootComponent {

}
