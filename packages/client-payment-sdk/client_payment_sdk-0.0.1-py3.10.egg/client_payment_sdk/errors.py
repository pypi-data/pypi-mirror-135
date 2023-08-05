class ClientPaymentSDKError(Exception):
    def __init__(self, response, message=None):
        self.response = response
        super(ClientPaymentSDKError, self).__init__(message or response.get('Message'))

class PaymentError(ClientPaymentSDKError):
    pass
