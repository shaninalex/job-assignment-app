import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
    {
        path: "",
        loadChildren: () => import("./modules/public/public.module").then(m => m.PublicModule),
    },
    {
        path: "auth",
        loadChildren: () => import("./modules/auth/auth.module").then(m => m.AuthModule),
        // TODO: if not authenticated only,
    },
    {
        path: "dashboard",
        loadChildren: () => import("./modules/dashboard/dashboard.module").then(m => m.DashboardModule),
        // canMatch: [CanMatchRoute],
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
