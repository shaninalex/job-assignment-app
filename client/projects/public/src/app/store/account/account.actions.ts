import { createAction, props } from "@ngrx/store";
import { RegistrationPayload } from "../../models";
import { RegistrationCompanyPayload } from "../../models/company";

export const ActionRegisterAccountStart = createAction(
    "[account] register account start",
    props<{ payload: RegistrationPayload }>(),
)

export const ActionRegisterCompanyStart = createAction(
    "[account] register company start",
    props<{ payload: RegistrationCompanyPayload }>(),
)