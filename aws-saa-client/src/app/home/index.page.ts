import {Component, OnInit} from '@angular/core';
import {QuestionService} from '../question.service';
import {QuestionResponse} from '../Entity/question-response';
import {Question} from '../Entity/question';
import _ from 'lodash';
import {Choice} from '../Entity/choice';
import {AlertController, ModalController} from '@ionic/angular';
import {RemarksComponent} from './remarks/remarks.component';


@Component({
    selector: 'app-home',
    templateUrl: 'index.page.html',
    styleUrls: ['index.page.scss'],
})
export class IndexPage implements OnInit {
    limit = 3;
    inited = false;
    currentIndex = -1;
    questions: Question[] = [];
    question: Question = new Question();
    answers: boolean[] = [];
    isDisableAnswer = true;
    isDisableRemarks = true;

    constructor(public questionService: QuestionService,
                public alertController: AlertController,
                public modalController: ModalController) {

    }

    ngOnInit() {
        this.init();
    }

    init() {
        this.inited = false;
        this.currentIndex = -1;
        this.questions = [];
        this.question = new Question();
        this.isDisableAnswer = true;
        this.isDisableRemarks = true;

        this.questionService.getQuestions(this.limit).subscribe(
            (questionResponse: QuestionResponse) => {
                if (questionResponse.status !== 0) {
                    console.error('');
                    return;
                }
                const questions: Question[] = questionResponse.data.questions;
                if (_.size(questions) === 0) {
                    console.error('questions size is 0');
                    return;
                }
                this.currentIndex = 0;
                const question: Question = questions[this.currentIndex];

                this.questions = questions;
                this.question = question;
                this.inited = true;
                this.answers = _.fill(Array(_.size(this.questions)), false);
            },
            error => console.error(error),
            () => {
                console.log('done');
            }
        );
    }


    clickLeft($event) {
        if (!this.inited) {
            return;
        }
        if (this.currentIndex <= 0) {
            return;
        }
        this.currentIndex--;
        this.question = this.questions[this.currentIndex];
        this.choiceChanged();
        this.isDisableRemarks = true;
    }

    clickRight($event) {
        if (!this.inited) {
            return;
        }
        if (this.currentIndex > _.size(this.questions) - 1) {
            return;
        }
        this.currentIndex++;
        this.question = this.questions[this.currentIndex];
        this.choiceChanged();
        this.isDisableRemarks = true;
    }

    disableAnswer(): boolean {
        if (!this.inited) {
            return true;
        }
        for (const choice of this.question.choices) {
            if (choice.isChecked) {
                return false;
            }
        }
        return true;
    }

    disableClickLeft(): boolean {
        if (!this.inited) {
            return true;
        }
        return this.currentIndex <= 0;
    }

    disableClickRight(): boolean {
        if (!this.inited) {
            return true;
        }
        return this.currentIndex >= (_.size(this.questions) - 1);
    }

    choiceChanged() {
        this.isDisableAnswer = this.disableAnswer();
    }

    checkAnswer() {
        for (const answer of this.question.answers) {
            const tmp: Choice = _.find(this.question.choices, {choice_id: answer.choice_id});
            if (!tmp.isChecked) {
                this.answers[this.currentIndex] = false;
                return false;
            }
        }
        for (const choice of this.question.choices) {
            if (!choice.isChecked) {
                continue;
            }
            const tmp: Choice = _.find(this.question.answers, {choice_id: choice.choice_id});
            if (!tmp) {
                this.answers[this.currentIndex] = false;
                return false;
            }
        }
        this.answers[this.currentIndex] = true;
        return true;
    }

    clearChoice() {
        for (const choice of this.question.choices) {
            choice.isChecked = false;
        }
        this.choiceChanged();
    }

    isAllCorrect(): boolean {
        for (const answer of this.answers) {
            if (!answer) {
                return false;
            }
        }
        return true;
    }

    async presentOK() {
        const alert = await this.alertController.create({
            header: 'Ok',
            // subHeader: 'Subtitle',
            message: '<strong>Good</strong>',
            buttons: ['OK']
        });
        await alert.present();
    }

    async presentNG() {
        const alert = await this.alertController.create({
            header: 'NG',
            // subHeader: 'Subtitle',
            message: '<strong>Incorrect</strong>',
            buttons: ['Cancel']
        });

        await alert.present();

        await alert.onDidDismiss().then((data) => {
            this.clearChoice();
            this.isDisableRemarks = false;
        });
    }

    showRemarks() {
        this.presentModal();
        console.log('showRemarks');
    }

    async presentModal() {
        const modal = await this.modalController.create({
            component: RemarksComponent,
            componentProps: {
                remarks: this.question.remarks
            }
        });
        return await modal.present();
    }
}
