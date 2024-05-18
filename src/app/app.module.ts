import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ReactiveFormsModule } from '@angular/forms';
import { AssignemntPageComponent } from './assignemnt-page/assignemnt-page.component';
import { CheckResultsComponent } from './check-results/check-results.component';
import { HttpClientModule } from '@angular/common/http';
import { HeaderComponent } from './ui/header/header.component';
import { FooterComponent } from './ui/footer/footer.component';

@NgModule({
    declarations: [
        AppComponent,
        AssignemntPageComponent,
        CheckResultsComponent,
        HeaderComponent,
        FooterComponent
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        AppRoutingModule,
        ReactiveFormsModule
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
