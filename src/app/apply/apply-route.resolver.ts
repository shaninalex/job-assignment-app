import { inject } from "@angular/core";
import { Position } from "../types";
import { ActivatedRouteSnapshot, Resolve, ResolveFn, Router, RouterStateSnapshot } from "@angular/router";
import { ApiPositionService } from "../services/position.service";
import { EmptyError, catchError, of } from "rxjs";
import { NONE_TYPE } from "@angular/compiler";


export function PositionRouteResolver(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
) {
    const id: number = parseInt(route.paramMap.get('id') as string);
    const router = inject(Router)
    return inject(ApiPositionService).get(id).pipe(
        catchError(e => {
            router.navigate(['/not-found'])
            return of(EmptyError);
        })
    );
}
