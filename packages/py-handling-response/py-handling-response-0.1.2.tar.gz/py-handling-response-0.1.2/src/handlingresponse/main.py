from fastapi import HTTPException


class HandlingResponse:
    valid: bool
    data: dict
    error: str
    codeError: int
    defaultError: dict

    def __init__(self, valid, data=None, error=None, code_error=None):
        if valid and data is None:
            data = {"status": "ok"}

        self.data = data
        self.error = error
        self.codeError = code_error
        self.valid = valid

    def get(self, key):
        if self.data[key]:
            return self.data[key]
        return False

    def get_error_response(self):
        code_error = self.codeError if self.codeError != '' else '520'
        error = self.error if self.error != '' else self.get_default_errors(code_error)
        return HTTPException(status_code=code_error, detail=error)

    @staticmethod
    def get_default_errors(code):
        errors_dict = {
            "404": "not_found",
            "401": "invalid_token",
            "500": "internal_server_error",
            "520": "unknown_error",
        }
        return errors_dict[code]
