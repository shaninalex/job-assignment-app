
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CandidateRootComponent } from './candidate.component';

const routes: Routes = [
    {
        path: "",
        component: CandidateRootComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class CandidateRoutingModule { }
