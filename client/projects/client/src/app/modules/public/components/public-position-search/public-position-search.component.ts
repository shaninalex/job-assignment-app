import { Component, OnDestroy } from "@angular/core";
import { FormBuilder, FormControl, FormGroup, Validators } from "@angular/forms";
import { interval, Observable, Subject, switchMap, takeUntil, tap, throttle } from "rxjs";
import { HttpClient } from "@angular/common/http";
import { ApiResponse } from "../../../../models/response";
import { Position } from "../../../../models/position";


export interface LoginForm {
    search_query: FormControl<string>;
}

@Component({
    selector: "app-public-position-search",
    templateUrl: "./public-position-search.component.html"
})
export class PublicPositionSearchComponent implements OnDestroy {
    form: FormGroup<LoginForm> = this.fb.group<LoginForm>({
        search_query: new FormControl('', { nonNullable: true }),
    });
    positions$: Observable<Position[]>
    private destroy$ = new Subject<void>();
    
    constructor(private fb: FormBuilder, private http: HttpClient) {
        this.form.valueChanges
        .pipe(
            throttle(() => interval(500)),
            switchMap(() => {
                const { search_query } = this.form.getRawValue();
                const params = { title: search_query };
                return this.http.get<ApiResponse<Position[]>>(
                    '/api/v1/public/positions',
                    { params }
                );
            }),
            takeUntil(this.destroy$)
        )
        .subscribe({
            next: response => {
                this.positions$ = new Observable(observer => observer.next(response.data));
            },
            error: error => console.error(error),
        });
    }

    ngOnDestroy(): void {
        this.destroy$.next();
        this.destroy$.complete();
    }
}