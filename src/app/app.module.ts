import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { PrimeNgModule } from './primeng.module';

import { AssignemntPageComponent } from './assignemnt-page/assignemnt-page.component';
import { CheckResultsComponent } from './check-results/check-results.component';
import { HeaderComponent } from './ui/header/header.component';
import { FooterComponent } from './ui/footer/footer.component';
import { PositionItemComponent } from './ui/position-item/position-item.component';
import { ApplyFormModalComponent } from './ui/apply-form-modal/apply-form-modal.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


@NgModule({
    declarations: [
        AppComponent,
        AssignemntPageComponent,
        CheckResultsComponent,
        HeaderComponent,
        FooterComponent,
        PositionItemComponent,
        ApplyFormModalComponent
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        AppRoutingModule,
        ReactiveFormsModule,
        BrowserAnimationsModule,
        PrimeNgModule,
        FormsModule,
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
