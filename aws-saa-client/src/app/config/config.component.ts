import {Component, OnInit} from '@angular/core';
import {ActionSheetController} from '@ionic/angular';
import {QuestionService} from '../question.service';
import _ from 'lodash';
import {ActionSheetButton} from '@ionic/core/dist/types/components/action-sheet/action-sheet-interface';

@Component({
    selector: 'app-config',
    templateUrl: './config.component.html',
    styleUrls: ['./config.component.scss'],
})
export class ConfigComponent implements OnInit {
    limit;

    constructor(public questionService: QuestionService,
                public actionSheetController: ActionSheetController
    ) {
    }

    ngOnInit() {
        this.limit = this.questionService.getLimit();
    }

    async limitClick() {
        let buttonArray: ActionSheetButton[] = [];
        for (let i = 1; i < 9; i++) {
            buttonArray = _.concat(buttonArray,
                {
                    text: _.toString(i),
                    handler: () => {
                        this.questionService.setLimit(i);
                        this.limit = i;
                    }
                }
            );
        }

        const actionSheet = await this.actionSheetController.create({
            header: 'limit',
            buttons: buttonArray
        });
        await actionSheet.present();
    }
}
