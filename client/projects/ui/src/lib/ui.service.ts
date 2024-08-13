import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class UiService {
    public title: BehaviorSubject<string> = new BehaviorSubject<string>("loading...");
    constructor() {
        this.title.subscribe({
            next: (title: string) => {
                document.title = title;
            }
        })
    }
}
