# -*- coding: utf-8 -*-
import json
from odoo.http import request
from odoo.tools import json_default
import datetime, jwt

SECRET_KEY = "Rasha_Secret_Key_777"
ALGORITHM = "HS256"


def generate_token(payload, expires_in_hours=24):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=expires_in_hours)
    payload.update(
        {
            "exp": expiry,
            "iat": datetime.datetime.utcnow(),
        }
    )

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, _("Token has expired")
    except jwt.InvalidTokenError:
        return False, _("Invalid token")


class ApiResponse:
    def __init__(
        self, success=True, message="", data=None, error=None, status_code=200
    ):
        self.success = success
        self.message = message
        self.data = data or {}
        self.error = error or {}
        self.status_code = status_code

    def to_json(self, token=None):
        headers = [("Content-Type", "application/json")]
        if token:
            headers.append(("Authorization", f"Bearer {token}"))

        return request.make_response(
            json.dumps(self.__dict__, sort_keys=True, indent=4, default=json_default),
            headers=headers,
            status=self.status_code,
        )
