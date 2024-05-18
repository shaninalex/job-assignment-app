import { Injectable } from "@angular/core";
import { version } from '../../../package.json';

@Injectable({
    providedIn: 'root'
})
export class AppService {
    public version: string = version;
}