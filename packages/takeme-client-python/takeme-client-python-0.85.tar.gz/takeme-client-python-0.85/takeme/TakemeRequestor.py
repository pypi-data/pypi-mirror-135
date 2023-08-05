import requests
import uuid
import hmac
import json
import hashlib


class TakemeRequestor(object):

    BASE_URL_SANDBOX = "https://api.takeme.id/dev/api/v1/"
    BASE_URL_PRODUCTION = "https://api.takeme.id/api/v1/"

    def __init__(self, corporate_code, secret_key, is_production):
        self.corporate_code = corporate_code
        self.secret_key = secret_key
        self.method_post = "POST"
        self.method_get = "GET"

        if is_production:
            self.url = self.BASE_URL_PRODUCTION
        else:
            self.url = self.BASE_URL_SANDBOX

    def call_api_without_bearer(self, endpoint, body):

        data = json.dumps(body)
        request_id = uuid.uuid4()
        byte_key = bytes(self.secret_key, 'utf-8')
        byte_data = bytes(data, 'utf-8')
        signature = hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()
        headers = {
            "Accept-Language": "en",
            "corporate": self.corporate_code,
            "requestID": str(request_id),
            "signature": signature,
        }
        if body is not None:
            response = requests.post(self.url + endpoint, data=data, headers=headers)
            return response
        else:
            response = requests.get(self.url + endpoint, data=data, headers=headers)
            return response

    def call_api_without_bearer_and_pin(self, endpoint, body, pin):

        data = json.dumps(body)
        request_id = uuid.uuid4()
        byte_key = bytes(self.secret_key, 'utf-8')
        byte_data = bytes(data, 'utf-8')
        signature = hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()
        headers = {
            "Accept-Language": "en",
            "corporate": self.corporate_code,
            "requestID": str(request_id),
            "signature": signature,
            "x-transaction-code": pin,
        }
        if body is not None:
            response = requests.post(self.url + endpoint, data=data, headers=headers)
            return response
        else:
            response = requests.get(self.url + endpoint, data=data, headers=headers)
            return response

    def call_api_with_bearer(self, endpoint, body, jwt):

        data = json.dumps(body)
        request_id = uuid.uuid4();
        byte_key = bytes(self.secret_key, 'utf-8')
        byte_data = bytes(data, 'utf-8')
        signature = hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()
        headers = {
            "Accept-Language": "en",
            "corporate": self.corporate_code,
            "requestID": str(request_id),
            "signature": signature,
            "Authorization": "Bearer "+ jwt,
        }
        if body is not None:
            response = requests.post(self.url + endpoint, data=data, headers=headers)
            return response
        else:
            response = requests.get(self.url + endpoint, data=data, headers=headers)
            return response

    def call_api_with_bearer_and_pin(self, endpoint, body, jwt, pin):

        data = json.dumps(body)
        request_id = uuid.uuid4();
        byte_key = bytes(self.secret_key, 'utf-8')
        byte_data = bytes(data, 'utf-8')
        signature = hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()
        headers = {
            "Accept-Language": "en",
            "corporate": self.corporate_code,
            "requestID": str(request_id),
            "signature": signature,
            "Authorization": "Bearer "+ jwt,
            "x-transaction-code": pin,
        }
        if body is not None:
            response = requests.post(self.url + endpoint, data=data, headers=headers)
            return response
        else:
            response = requests.get(self.url + endpoint, data=data, headers=headers)
            return response

