import {Pipe, PipeTransform} from '@angular/core';
import _ from 'lodash';
import {DomSanitizer} from '@angular/platform-browser';

@Pipe({
    name: 'pickHref'
})
export class PickHrefPipe implements PipeTransform {
    constructor(protected sanitizer: DomSanitizer) {
    }

    transform(value: any, ...args: any[]): any {
        return this.sanitizer.bypassSecurityTrustUrl(_.replace(value, /(http.*\s|http.*$)/g, '<a href=$1 >$1</a>'));
    }

}
