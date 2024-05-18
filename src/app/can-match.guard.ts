import { CanMatchFn, Route, UrlSegment } from "@angular/router";
// import { inject } from "@angular/core";

export const CanMatchRoute: CanMatchFn = (route: Route, segments: UrlSegment[]) => {
    // for (let i = 0; i < segments.length; i++) {
    //     if (segments[i].path === 'admin') {
    //         return true
    //     }
    // }

    return true;
};
