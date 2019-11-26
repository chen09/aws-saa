import {AuditData} from './audit-data';
import {Question} from './question';

export class QuestionResponse {
    auditData: AuditData;
    status: number;
    message: number;
    data: {
        questions: Question[];
    };
}
