import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AssignemntPageComponent } from './assignemnt-page/assignemnt-page.component';
import { CheckResultsComponent } from './check-results/check-results.component';
import { CanMatchRoute } from './can-match.guard';
import { ApplyComponent } from './apply/apply.component';
import { UiPageComponent } from './ui-page/ui-page.component';
import { PositionRouteResolver } from './apply/apply-route.resolver';
import { NotFoundComponent } from './not-found/not-found.component';

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
        resolve: {position: PositionRouteResolver}
    },
    {
        path: 'ui',
        component: UiPageComponent,
    },
    {
        path: "admin",
        loadChildren: () => import("./admin/admin.module").then(m => m.AdminModule),
        canMatch: [CanMatchRoute],
    },
    {
        path: 'not-found',
        component: NotFoundComponent,
    },
    {
        path: '**',
        redirectTo: "not-found",
    },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
