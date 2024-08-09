
import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { CandidateRootComponent } from "./candidate.component";
import { CandidateRoutingModule } from "./candidate-routing.module";

@NgModule({
    declarations: [
        CandidateRootComponent
    ],
    imports: [
        CommonModule,
        CandidateRoutingModule
    ],
})
export class CandidateModule { }
