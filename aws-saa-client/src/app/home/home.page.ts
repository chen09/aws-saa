import {Component} from '@angular/core';
import {QuestionService} from '../question.service';
import {QuestionResponse} from '../Entity/question-response';
import {Question} from '../Entity/question';
import _ from 'lodash';

@Component({
    selector: 'app-home',
    templateUrl: 'home.page.html',
    styleUrls: ['home.page.scss'],
})
export class HomePage {

    constructor(public questionService: QuestionService) {
        this.questionService.test().subscribe(
            (questionResponse: QuestionResponse) => {
                // console.log(questionResponse);
                if (questionResponse.status !== 0) {
                    console.error('');
                    return;
                }
                const questions: Question[] = questionResponse.data.questions;

                if (_.size(questions) === 0) {
                    console.error('questions size is 0');
                    return;
                }
                const question: Question = questions[0];
                console.log(question);


            },
            error => console.error(error),
            () => {
                console.log('done');
            }
        );
    }

}
