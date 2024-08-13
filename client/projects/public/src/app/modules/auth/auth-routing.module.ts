import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthComponent } from './auth.component';
import { RegisterComponent } from './containers/register/register.component';
import { LoginComponent } from './containers/login/login.component';

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
