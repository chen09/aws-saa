import {Language} from './language';
import {Choice} from './choice';
import {Answer} from './answer';

export class Question {
    // tslint:disable-next-line:variable-name
    question_id: string;
    // tslint:disable-next-line:variable-name
    language_id: string;
    question: string;
    remarks: string;
    language: Language;
    choices: Choice[];
    answers: Answer[];

}
