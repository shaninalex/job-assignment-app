import { Component } from '@angular/core';

@Component({
    selector: 'auth-root',
    template: `
<div class="p-4">
    <div class="mt-20 mx-auto border rounded-lg p-4 max-w-md border-slate-400">
        <router-outlet />
    </div>
</div>
`,
})
export class AuthComponent {
}
