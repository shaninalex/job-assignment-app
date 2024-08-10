
import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { CompanyRootComponent } from "./company.component";
import { CompanyRoutingModule } from "./company-routing.module";
import { OverviewComponent } from "./containers/overview/overview.component";
import { CompanyNavbarComponent } from "./components/navbar/company-navbar.component";
import { CompanyNotificationsComponent } from "./containers/notifications/company-notifications.component";
import { CompanySettingsComponent } from "./containers/settings/settings.component";
import { CompJobItemComponent } from "./containers/jobs/components/job-item/job-item.component";
import { CompJobDetailComponent } from "./containers/jobs/components/job-detail/job-detail.component";
import { JobsComponent } from "./containers/jobs/jobs.component";

@NgModule({
    declarations: [
        // -- pages --
        CompanyRootComponent,
        OverviewComponent,
        CompanyNotificationsComponent,
        CompanySettingsComponent,
        JobsComponent,

        // -- components --
        CompanyNavbarComponent,
        CompJobItemComponent,
        CompJobDetailComponent,
    ],
    imports: [
        CommonModule,
        CompanyRoutingModule
    ],
})
export class CompanyModule { }
