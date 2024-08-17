import { AccountEffects, accountReducer, AccountState } from "./account";

export interface AppState {
    account: AccountState
}

export const reducers = {
    account: accountReducer,
}

export const effects = [
    AccountEffects
]