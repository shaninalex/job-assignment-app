import { NgModule } from "@angular/core";
import { ButtonModule } from 'primeng/button';
import { InputIconModule } from 'primeng/inputicon';
import { PanelModule } from 'primeng/panel';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { DividerModule } from 'primeng/divider';
import { TagModule } from 'primeng/tag';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';

@NgModule({
    imports: [
        ButtonModule,
        InputIconModule,
        PanelModule,
        ProgressSpinnerModule,
        DividerModule,
        TagModule,
        DialogModule,
        InputTextModule
    ],
    exports: [
        ButtonModule,
        InputIconModule,
        PanelModule,
        ProgressSpinnerModule,
        DividerModule,
        TagModule,
        DialogModule,
        InputTextModule
    ]
})
export class PrimeNgModule { }