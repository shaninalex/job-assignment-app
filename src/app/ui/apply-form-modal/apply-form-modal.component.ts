import { Component, Input, inject } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-apply-form-modal',
  templateUrl: './apply-form-modal.component.html'
})
export class ApplyFormModalComponent {
	activeModal = inject(NgbActiveModal);

	@Input() positionId: number;
}
