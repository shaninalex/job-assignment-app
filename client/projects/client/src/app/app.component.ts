import { Component } from '@angular/core';
import { version } from '../../../../package.json';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
})
export class AppComponent {
    version: string = version;
}
