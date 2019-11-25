import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Question} from './question';

@Injectable({
    providedIn: 'root'
})
export class QuestionService {

    constructor(private http: HttpClient) {
    }

    test(): Observable<Question> {
        return this.http.get<Question>('http://127.0.0.1:5000/api/v1/questions');
    }
}
