import { Component, inject, TemplateRef } from '@angular/core';
import { ApiPositionService } from '../services/position.service';
import { Position } from '../types';

import { ModalDismissReasons, NgbDatepickerModule, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ApplyFormModalComponent } from '../ui/apply-form-modal/apply-form-modal.component';

@Component({
    selector: 'app-assignemnt-page',
    templateUrl: './assignemnt-page.component.html',
})
export class AssignemntPageComponent {
    positions: Position[] = [];
	private modalService = inject(NgbModal);

    constructor(private positionsApi: ApiPositionService) {
        this.positionsApi.list().subscribe({
            next: results => { this.positions = results.data }
        })
    }

	open(positionId: number) {
		const modalRef = this.modalService.open(ApplyFormModalComponent, { size: 'xl' });
        modalRef.componentInstance.positionId = positionId;
	}

}
