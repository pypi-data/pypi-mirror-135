class ClientPaymentSDKError(Exception):
    def __init__(self, message, errors=None):
        super(ClientPaymentSDKError, self).__init__(message)
        self.errors = errors or {}


class RequestError(ClientPaymentSDKError):
    pass


class PassedTypeError(ClientPaymentSDKError):
    pass


class InternalServerError(ClientPaymentSDKError):
    pass


class MatchKeyError(ClientPaymentSDKError):
    pass


class SignatureVerificationError(ClientPaymentSDKError):
    pass


class ParseResponseError(ClientPaymentSDKError):
    pass