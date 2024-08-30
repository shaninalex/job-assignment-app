import { createAction, props } from "@ngrx/store";
import { RegistrationPayload } from "../../models";

export const ActionRegisterAccountStart = createAction(
    "[account] register account start",
    props<{ payload: RegistrationPayload }>(),
)

export const ActionRegisterCompanyStart = createAction(
    "[account] register company start",
    props<{ payload: RegistrationPayload }>(),
)