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
    oldlimit;
    limit;

    constructor(public questionService: QuestionService,
                public actionSheetController: ActionSheetController
    ) {
    }

    ngOnInit() {
        this.limit = this.questionService.getLimit();
        this.oldlimit = this.limit;
    }

    async limitClick() {
        let buttonArray: ActionSheetButton[] = [];
        for (let i = 1; i < 16; i++) {
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

    menuOpen() {
        this.oldlimit = this.limit;
    }

    menuClosed() {
        if (this.oldlimit !== this.limit) {
            this.questionService.limitChanged(this.limit);
        }
    }
}
