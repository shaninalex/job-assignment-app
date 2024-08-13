import { Component, Input } from "@angular/core";

@Component({
    selector: "comp-feedback-item",
    templateUrl: "./feedback-item.component.html"
})
export class FeedbackItemComponent {
    @Input() seen: boolean = false;
}
