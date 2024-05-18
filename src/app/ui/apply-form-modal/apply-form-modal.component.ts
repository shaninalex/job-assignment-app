import { Component, Input, inject } from '@angular/core';

@Component({
  selector: 'app-apply-form-modal',
  templateUrl: './apply-form-modal.component.html'
})
export class ApplyFormModalComponent {
	// activeModal = inject(NgbActiveModal);

	@Input() positionId: number;
}
