# -*- coding: utf-8 -*-
import requests
from .exceptions import RequestError, InternalServerError, PassedTypeError, ParseResponseError
from .models import InitPaymentResponse, StatusPaymentResponse, BalanceResponse, \
    WithdrawalResponse, StatusWithdrawalResponse


class ClientPaymentSDK:
    """
    ClientPaymentSDK Class
    """
    URL = 'https://sbank.gogo.vc'

    def _request(self, url, method, data=None, headers=None):
        try:
            if method == 'get':
                response = requests.get(url, params=data, headers=headers)
            else:
                response = requests.post(url, data, headers=headers)

            if response.status_code == 400:
                error = response.json()
                code = error['code']
                message = error['message']

                raise RequestError(f'error code: {code}, message: {message}')
            elif response.status_code == 500:
                error = response.json()
                message = error['message']

                raise InternalServerError(f'message: {message}')
            elif response.status_code != 200:
                raise RequestError(f'Server not available: {response.status_code}')

            if response.headers['Content-Type'].find('application/json') != -1:
                return response.json()
            else:
                return response.content.decode('utf-8')
        except requests.ConnectionError as error:
            raise RequestError(error)

    def _get(self, url, data=None):
        return self._request(url, 'get', data)

    def _post(self, url, data=None):
        return self._request(url, 'post', data)

    def init(self, params):
        """
        Payment Initiation

        # Arguments
        params (dict)

        # Raises
        RequestError: If request does fail
        InternalServerError: If internal server error
        PassedTypeError: If passed value does not dict
        ParseResponseError: If response not suite for class structure

        # Returns
        InitPaymentResponse
        """
        endpoint = '/init'

        if not isinstance(params, dict):
            raise PassedTypeError('passed value must be dict')

        response = self._post(self.URL + endpoint, params)

        if 'status' not in response:
            raise ParseResponseError(f'Unable to parse response, response: {response}')

        if response['status'] == 'error':
            raise RequestError(response)

        return InitPaymentResponse(response)

    def status(self, params):
        """
        Get Payment Status

        # Arguments
        params (dict)

        # Raises
        RequestError: If request does fail
        InternalServerError: If internal server error
        PassedTypeError: If passed value does not dict
        ParseResponseError: If response not suite for class structure

        # Returns
        StatusPaymentResponse
        """
        endpoint = '/status'

        if not isinstance(params, dict):
            raise PassedTypeError('passed value must be dict')

        response = self._get(self.URL + endpoint, params)

        if 'status' not in response:
            raise ParseResponseError(f'Unable to parse response, response: {response}')

        if response['status'] == 'error':
            raise RequestError(response)

        return StatusPaymentResponse(response)

    def balance(self, params):
        """
        Get Merchant Balance

        # Arguments
        params (dict)

        # Raises
        RequestError: If request does fail
        InternalServerError: If internal server error
        PassedTypeError: If passed value does not dict
        ParseResponseError: If response not suite for class structure

        # Returns
        BalanceResponse
        """
        endpoint = '/balance'

        if not isinstance(params, dict):
            raise PassedTypeError('passed value must be dict')

        response = self._get(self.URL + endpoint, params)

        if 'status' not in response:
            raise ParseResponseError(f'Unable to parse response, response: {response}')

        if response['status'] == 'error':
            raise RequestError(response)

        return BalanceResponse(response)

    def withdrawal(self, params):
        """
        Withdrawal Initiation

        # Arguments
        params (dict)

        # Raises
        RequestError: If request does fail
        InternalServerError: If internal server error
        PassedTypeError: If passed value does not dict
        ParseResponseError: If response not suite for class structure

        # Returns
        WithdrawalResponse
        """
        endpoint = '/withdrawal_request'

        if not isinstance(params, dict):
            raise PassedTypeError('passed value must be dict')

        response = self._post(self.URL + endpoint, params)

        if 'status' not in response:
            raise ParseResponseError(f'Unable to parse response, response: {response}')

        if response['status'] == 'error':
            raise RequestError(response)

        return WithdrawalResponse(response)

    def withdrawal_status(self, params):
        """
        Get Withdrawal Status

        # Arguments
        params (dict)

        # Raises
        RequestError: If request does fail
        InternalServerError: If internal server error
        PassedTypeError: If passed value does not dict
        ParseResponseError: If response not suite for class structure

        # Returns
        StatusWithdrawalResponse
        """
        endpoint = '/withdrawal_request'

        if not isinstance(params, dict):
            raise PassedTypeError('passed value must be dict')

        response = self._get(self.URL + endpoint, params)

        if 'status' not in response:
            raise ParseResponseError(f'Unable to parse response, response: {response}')

        if response['status'] == 'error':
            raise RequestError(response)

        return StatusWithdrawalResponse(response)
