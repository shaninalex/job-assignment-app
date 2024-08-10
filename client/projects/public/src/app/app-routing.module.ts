import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
    {
        path: "",
        loadChildren: () => import("./modules/public/public.module").then(m => m.PublicModule),
        // TODO: if not authenticated only,
    },
    {
        path: "auth",
        loadChildren: () => import("./modules/auth/auth.module").then(m => m.AuthModule),
        // TODO: if not authenticated only,
    },
    {
        path: "company",
        loadChildren: () => import("./modules/company/company.module").then(m => m.CompanyModule),
    },
    {
        path: "app",
        loadChildren: () => import("./modules/candidate/candidate.module").then(m => m.CandidateModule),
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
