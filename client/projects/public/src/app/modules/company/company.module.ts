
import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { CompanyRootComponent } from "./company.component";
import { CompanyRoutingModule } from "./company-routing.module";

@NgModule({
    declarations: [
        CompanyRootComponent
    ],
    imports: [
        CommonModule,
        CompanyRoutingModule
    ],
})
export class CompanyModule { }
