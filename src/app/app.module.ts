import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AssignemntPageComponent } from './assignemnt-page/assignemnt-page.component';
import { CheckResultsComponent } from './check-results/check-results.component';
import { HeaderComponent } from './ui/header/header.component';
import { FooterComponent } from './ui/footer/footer.component';
import { PositionItemComponent } from './ui/position-item/position-item.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ApplyComponent } from './apply/apply.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SkillsSelectComponent } from './ui/skills-select/skills-select.component';
import { UiPageComponent } from './ui-page/ui-page.component';

@NgModule({
    declarations: [
        AppComponent,
        AssignemntPageComponent,
        CheckResultsComponent,
        HeaderComponent,
        FooterComponent,
        PositionItemComponent,
        ApplyComponent,
        SkillsSelectComponent,
        UiPageComponent
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        AppRoutingModule,
        ReactiveFormsModule,
        BrowserAnimationsModule,
        FormsModule,
        NgbModule,
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
