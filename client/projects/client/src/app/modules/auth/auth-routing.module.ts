import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthComponent } from './auth.component';
import { RegisterComponent } from './containers/register/register.component';
import { LoginComponent } from './containers/login/login.component';
import { RegisterCompanyComponent } from './containers/register-company/register-company.component';

const routes: Routes = [
    {
        path: "",
        component: AuthComponent,
        children: [
            {
                path: "",
                component: LoginComponent 
            },
            {
                path: "register",
                component: RegisterComponent
            },
            {
                path: "register-company",
                component: RegisterCompanyComponent
            },
            {
                path: "login",
                redirectTo: "/auth"
            },
        ]
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class AuthRoutingModule { }
