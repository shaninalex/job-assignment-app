import { createAction, props } from "@ngrx/store";
import { RegistrationPayload } from "../../models";

export const ActionRegisterStart = createAction(
    "[account] register start",
    props<{ payload: RegistrationPayload }>(),
)