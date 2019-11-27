import {Component, Input, OnInit} from '@angular/core';
import {NavParams} from '@ionic/angular';

@Component({
    selector: 'app-test',
    templateUrl: './test.component.html',
    styleUrls: ['./test.component.scss'],
})
export class TestComponent implements OnInit {

    @Input() remarks: string;

    constructor(navParams: NavParams) {
        console.log(navParams.get('remarks'));
    }

    ngOnInit() {
    }

}
