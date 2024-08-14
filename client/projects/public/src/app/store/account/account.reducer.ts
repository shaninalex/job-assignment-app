import { createReducer } from "@ngrx/store";
import { Account, RegistrationPayload } from "../../models";

export interface AccountState {
    account: Account | null
}

const initialState: AccountState = {
    account: null
}

export const accountReducer = createReducer<AccountState>(
    initialState,
)


