import {Component, Input, OnInit} from '@angular/core';
import {ModalController, NavParams} from '@ionic/angular';

@Component({
    selector: 'app-test',
    templateUrl: './remarks.component.html',
    styleUrls: ['./remarks.component.scss'],

})
export class RemarksComponent implements OnInit {

    @Input() remarks: string;

    constructor(navParams: NavParams, private modalCtrl: ModalController) {
        console.log(navParams.get('remarks'));
    }

    ngOnInit() {
    }

    dismiss() {
        this.modalCtrl.dismiss();
    }
}
