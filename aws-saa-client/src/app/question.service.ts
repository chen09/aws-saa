import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable, Subject} from 'rxjs';
import {QuestionResponse} from './Entity/question-response';
import {environment} from '../environments/environment';
import _ from 'lodash';

@Injectable({
    providedIn: 'root'
})
export class QuestionService {
    private limitSubject = new Subject<number>();
    public titleObservable = this.limitSubject.asObservable();

    constructor(private http: HttpClient) {
    }

    getQuestions(limit): Observable<QuestionResponse> {
        const params = new HttpParams().set('limit', limit);
        return this.http.get<QuestionResponse>(environment.questions_url, {params});
    }

    getLimit(): number {
        let limit: string = localStorage.getItem('limit');
        console.log(limit);
        if (limit == null || limit.length === 0) {
            console.log(environment.limit);
            limit = `${environment.limit}`;
            console.log(limit);
            localStorage.setItem('limit', limit);
        }
        return _.toNumber(limit);
    }

    setLimit(limit: number) {
        localStorage.setItem('limit', _.toString(limit));
    }

    limitChanged(limit: number) {
        this.limitSubject.next(limit);
    }
}
