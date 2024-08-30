import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './containers/home/home.component';
import { ContactsComponent } from './containers/contacts/contacts.component';
import { AboutComponent } from './containers/about/about.component';
import { PublicRootComponent } from './public-root.component';

const routes: Routes = [
    {
        path: "",
        component: PublicRootComponent,
        children: [
            {
                path: "",
                component: HomeComponent
            },
            {
                path: "about",
                component: AboutComponent
            },
            {
                path: "contacts",
                component: ContactsComponent
            }
        ]
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class PublicRoutingModule { }
