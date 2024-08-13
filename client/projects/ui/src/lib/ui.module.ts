import { NgModule } from '@angular/core';
import { UiComponent } from './ui.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { InputPasswordComponent, InputTextComponent } from './components';
import { CommonModule } from '@angular/common';


@NgModule({
    declarations: [
        UiComponent,
        InputTextComponent,
        InputPasswordComponent,
    ],
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
    ],
    exports: [
        UiComponent,
        InputTextComponent,
        InputPasswordComponent,
    ],

})
export class UiModule { }
