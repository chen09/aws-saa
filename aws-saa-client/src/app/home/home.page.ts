import {Component} from '@angular/core';
import {QuestionService} from '../question.service';

@Component({
    selector: 'app-home',
    templateUrl: 'home.page.html',
    styleUrls: ['home.page.scss'],
})
export class HomePage {

    constructor(public questionService: QuestionService) {
        this.questionService.test().subscribe(
            data => {
                console.log(data);
            },
            error => console.error(error),
            () => {
                console.log('done');
            }
        );
    }

}
