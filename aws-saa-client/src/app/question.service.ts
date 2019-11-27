import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {QuestionResponse} from './Entity/question-response';

@Injectable({
    providedIn: 'root'
})
export class QuestionService {

    constructor(private http: HttpClient) {
    }

    getQuestions(): Observable<QuestionResponse> {
        return this.http.get<QuestionResponse>('http://127.0.0.1:5000/api/v1/questions');
    }
}
