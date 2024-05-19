import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AssignemntPageComponent } from './assignemnt-page/assignemnt-page.component';
import { CheckResultsComponent } from './check-results/check-results.component';
import { CanMatchRoute } from './can-match.guard';
import { ApplyComponent } from './apply/apply.component';

const routes: Routes = [
    {
        path: '',
        component: AssignemntPageComponent,
    },
    {
        path: 'results',
        component: CheckResultsComponent,
    },
    {
        path: 'apply/:id',
        component: ApplyComponent,
    },
    {
        path: "admin",
        loadChildren: () => import("./admin/admin.module").then(m => m.AdminModule),
        canMatch: [CanMatchRoute],
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
