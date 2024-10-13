import { createAction, props } from "@ngrx/store";
import { LoginPayload, RegistrationPayload } from "../../models";

export const ActionLoginAccountStart = createAction(
    "[account] login account start",
    props<{ payload: LoginPayload }>(),
)

export const ActionRegisterAccountStart = createAction(
    "[account] register account start",
    props<{ payload: RegistrationPayload }>(),
)

export const ActionRegisterCompanyStart = createAction(
    "[account] register company start",
    props<{ payload: RegistrationPayload }>(),
)