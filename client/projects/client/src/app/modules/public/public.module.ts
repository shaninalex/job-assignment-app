import { NgModule } from "@angular/core";
import { PublicRoutingModule } from "./public-routing.module";
import { CommonModule } from "@angular/common";
import { HomeComponent } from './containers/home/home.component';
import { AboutComponent } from './containers/about/about.component';
import { ContactsComponent } from './containers/contacts/contacts.component';
import { PublicNavbarComponent } from "./components/navbar/navbar.component";
import { PublicRootComponent } from "./public-root.component";
import { PublicPositionSearchComponent } from "./components/public-position-search/public-position-search.component";
import { ReactiveFormsModule } from "@angular/forms";
import { UiModule } from "@ui";
import { RouterModule } from "@angular/router";

@NgModule({
    declarations: [
        PublicRootComponent,
        // -- pages
        HomeComponent,
        AboutComponent,
        ContactsComponent,

        // -- components
        PublicNavbarComponent,
        PublicPositionSearchComponent
    ],
    imports: [
        CommonModule,
        RouterModule,
        PublicRoutingModule,
        ReactiveFormsModule,
        UiModule,
    ],
})
export class PublicModule { }
