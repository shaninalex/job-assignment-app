import { Component, Input } from '@angular/core';
import { Position } from '../../types';
import { Router } from '@angular/router';

@Component({
  selector: 'app-position-item',
  templateUrl: './position-item.component.html'
})
export class PositionItemComponent {
    @Input() position: Position;

    constructor(private router: Router) {}
    apply() {
        this.router.navigate(['apply', this.position.id]);
    }
}
