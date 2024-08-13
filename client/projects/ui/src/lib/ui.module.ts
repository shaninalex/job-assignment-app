import { forwardRef, NgModule } from '@angular/core';
import { UiComponent } from './ui.component';
import { FormsModule, NG_VALUE_ACCESSOR, ReactiveFormsModule } from '@angular/forms';
import { TextInputComponent } from './components';
import { CommonModule } from '@angular/common';


@NgModule({
	declarations: [
		UiComponent,
		TextInputComponent,
	],
	imports: [
		CommonModule,
		FormsModule,
		ReactiveFormsModule,
	],
	exports: [
		UiComponent,
		TextInputComponent,
	],

})
export class UiModule { }
