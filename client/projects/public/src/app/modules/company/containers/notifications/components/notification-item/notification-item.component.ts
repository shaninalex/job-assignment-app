import { Component, Input } from "@angular/core";

@Component({
    selector: "comp-notification",
    templateUrl: "./notification-item.component.html"
})
export class CompanyNotificationItemComponent {
    @Input() seen: boolean = false;
}