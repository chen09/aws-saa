import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {IonicModule} from '@ionic/angular';
import {FormsModule} from '@angular/forms';
import {RouterModule} from '@angular/router';

import {IndexPage} from './index.page';
import {TestComponent} from './test/test.component';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        IonicModule,
        RouterModule.forChild([
            {
                path: '',
                component: IndexPage
            }
        ])
    ],
    declarations: [IndexPage, TestComponent],
    entryComponents: [TestComponent]
})
export class QuestionModule {
}
