import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {PickHrefPipe} from './pick-href.pipe';


@NgModule({
    declarations: [PickHrefPipe],
    imports: [
        CommonModule
    ],
    exports: [
        PickHrefPipe
    ]
})
export class SharingModule {
}
