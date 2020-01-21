import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';
import {QuestionResponse} from './Entity/question-response';
import { environment } from '../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class QuestionService {

    constructor(private http: HttpClient) {
    }

    getQuestions(limit): Observable<QuestionResponse> {
        const params = new HttpParams().set('limit', limit);
        return this.http.get<QuestionResponse>(environment.questions_url, {params});
    }
}
