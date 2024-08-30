import { NgModule } from "@angular/core";
import { PublicRoutingModule } from "./public-routing.module";
import { CommonModule } from "@angular/common";
import { HomeComponent } from './containers/home/home.component';
import { AboutComponent } from './containers/about/about.component';
import { ContactsComponent } from './containers/contacts/contacts.component';
import { PublicNavbarComponent } from "./components/navbar/navbar.component";
import { PublicRootComponent } from "./public-root.component";

@NgModule({
    declarations: [
        PublicRootComponent,
        // -- pages
        HomeComponent,
        AboutComponent,
        ContactsComponent,

        // -- components
        PublicNavbarComponent
    ],
    imports: [
        CommonModule,
        PublicRoutingModule
    ],
})
export class PublicModule { }
