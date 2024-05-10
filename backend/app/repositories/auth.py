import logging

from app import models
from sqlalchemy import update, insert, delete, select
from app.db import log, RecordNotFound


class AuthRepository:
    def __init__(self, connection):
        self.conn = connection
    
    def refresh(self):
        """
        Refreshes the authentication token.
        """
        raise NotImplementedError("refresh method must be implemented in subclasses")
    
    def login(self, payload: models.LoginPayload) -> models.JWTTokenResponse:
        """
        Logs in the user.
        Parameters
        ----------
        payload : LoginPayload
            Validated user login payload
        Returns
        -------
        list
            signed JWT access/refresh tokens packed in JWTTokenResponse type
        """
        logging.info(f"process authorization for {payload.email}")
        response: models.JWTTokenResponse = models.JWTTokenResponse(token="", refresh="")
        return response
        