import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { AuthRoutingModule } from "./auth-routing.module";
import { AuthComponent } from "./auth.component";
import { LoginComponent } from "./containers/login/login.component";
import { RegisterComponent } from "./containers/register/register.component";
import { ReactiveFormsModule } from "@angular/forms";
import { UiModule } from "@ui";
import { RegisterCompanyComponent } from "./containers/register-company/register-company.component";

@NgModule({
    declarations: [
        // -- pages
        LoginComponent,
        RegisterComponent,
        RegisterCompanyComponent,
        AuthComponent,
    ],
    imports: [
        CommonModule,
        AuthRoutingModule,
        ReactiveFormsModule,
        UiModule,
    ],
})
export class AuthModule { }
