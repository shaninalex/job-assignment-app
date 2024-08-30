
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CompanyRootComponent } from './company.component';
import { OverviewComponent } from './containers/overview/overview.component';
import { JobsComponent } from './containers/jobs/jobs.component';
import { CompanySettingsComponent } from './containers/settings/settings.component';
import { CompanyNotificationsComponent } from './containers/notifications/company-notifications.component';
import { CompJobDetailComponent } from './containers/jobs/components/job-detail/job-detail.component';
import { FeedbacksComponent } from './containers/feedbacks/feedbacks.component';
import { FeedbackDetailComponent } from './containers/feedbacks/components/feedback-detail/feedback-detail.component';

const routes: Routes = [
    {
        path: "",
        component: CompanyRootComponent,
        children: [
            {
                path: "",
                component: OverviewComponent
            },
            {
                path: "jobs",
                component: JobsComponent
            },
            {
                path: "jobs/:id",
                component: CompJobDetailComponent
            },
            {
                path: "settings",
                component: CompanySettingsComponent
            },
            {
                path: "notifications",
                component: CompanyNotificationsComponent
            },
            {
                path: "feedbacks",
                component: FeedbacksComponent
            },
            {
                path: "jobs/:id/feedback/:id",
                component: FeedbackDetailComponent
            }
        ]
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class CompanyRoutingModule { }
