import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Position } from '../../types';

@Component({
  selector: 'app-position-item',
  templateUrl: './position-item.component.html'
})
export class PositionItemComponent {
    @Input() position: Position;
    @Output() onApply: EventEmitter<number> = new EventEmitter<number>()

    apply() {
        this.onApply.emit(this.position.id)
    }
}
