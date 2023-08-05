from takeme.TakemeRequestor import TakemeRequestor
from takeme.RsaUtil import RsaUtil


class TakemeClient:

    def __init__(self, corporate_code, secret_key, is_production=False):
        self.request_takeme = TakemeRequestor(corporate_code, secret_key, is_production)

    def non_auth_call(self, body, endpoint):
        response = self.request_takeme.call_api_without_bearer(endpoint, body)

        if response.status_code != 200:
            raise ValueError(response.json())

        return response.json()

    def non_auth_call_with_pin(self, body, endpoint, pin):
        encrypted_pin = RsaUtil.encrypt(pin)
        response = self.request_takeme.call_api_without_bearer_and_pin(endpoint, body, encrypted_pin)

        if response.status_code != 200:
            raise ValueError(response.json())

        return response.json()

    def auth_call(self, body, endpoint, jwt):
        response = self.request_takeme.call_api_with_bearer(endpoint, body, jwt)

        if response.status_code != 200:
            raise ValueError(response.json())

        return response.json()

    def auth_call_with_pin(self, body, endpoint, jwt, pin):
        encrypted_pin = RsaUtil.encrypt(pin)
        response = self.request_takeme.call_api_with_bearer_and_pin(endpoint, body, jwt, encrypted_pin)

        if response.status_code != 200:
            raise ValueError(response.json())

        return response.json()

    def user_signup(self, full_name, email, phone_number):
        endpoint = "uaa/signup"
        body = {
            "full_name": full_name,
            "email": email,
            "phone_number": phone_number
        }

        self.non_auth_call(body, endpoint)

    def user_activation(self, email, phone_number, activation_code):
        endpoint = "uaa/activation"
        body = {
            "email": email,
            "phone_number": phone_number,
            "activation_code": activation_code,
        }

        response = self.non_auth_call(body, endpoint)

        return response.get("data")

    def user_prelogin(self, phone_number):
        endpoint = "uaa/prelogin"
        body = {
            "phone_number": phone_number,
        }

        self.non_auth_call(body, endpoint)

    def user_login(self, phone_number, login_code):
        endpoint = "uaa/login"
        body = {
            "phone_number": phone_number,
            "login_code": login_code,
        }

        response = self.non_auth_call(body, endpoint)

        return response.get("data").get("jwt")

    def user_save_pin(self, pin, jwt):
        endpoint = "user/save-pin"
        body = {
            "pin": RsaUtil.encrypt(pin)
        }

        self.auth_call(body, endpoint, jwt)

    def user_pre_forgot_pin(self, new_pin, jwt):
        endpoint = "user/pre-forgot-pin"
        body = {
            "pin": RsaUtil.encrypt(new_pin)
        }

        self.auth_call(body, endpoint, jwt)

    def user_confirm_forgot_pin(self, otp, jwt):
        endpoint = "user/forgot-pin"
        body = {
            "confirm_pin_code": otp
        }

        self.auth_call(body, endpoint, jwt)

    def user_change_pin(self, old_pin, new_pin, jwt):
        endpoint = "user/change-pin"
        body = {
            "old_pin": RsaUtil.encrypt(old_pin),
            "new_pin": RsaUtil.encrypt(new_pin)
        }

        self.auth_call(body, endpoint, jwt)

    def user_detail(self, jwt):
        endpoint = "user/check"
        body = None

        response = self.auth_call(body, endpoint, jwt)

        return response.get("data")

    def user_balance(self, jwt):
        endpoint = "user/check"
        body = None

        response = self.auth_call(body, endpoint, jwt)

        return response.get("data").get("balance")

    def user_transaction_history(self, jwt, offset=1, limit=10):
        endpoint = "transaction/?" + "page=" + str(offset) + "&limit=" + str(limit)
        body = None

        response = self.auth_call(body, endpoint, jwt)

        return response.get("data")

    def user_inquiry_bank_account(self, account_number, bank_code, jwt):
        endpoint = "transaction/account-holdername"
        body = {
            "account_number": account_number,
            "bank_code": bank_code
        }

        response = self.auth_call(body, endpoint, jwt)

        if not response.get("data").get("account_name"):
            raise ValueError("Invalid account number")
        else:
            return response.get("data")

    def set_bank_account(self, account_number, bank_code, jwt):
        response = self.user_inquiry_bank_account(account_number, bank_code, jwt)

        bank_account = {
            "name": response.get("account_name"),
            "account_number": response.get("account_number"),
            "bank_code": response.get("bank_name")
        }

        return bank_account

    def transfer_to_bank(self, bank_account, amount, pin, jwt):
        endpoint = "transaction/transfer/wallet"
        body = {
            "to_bank_account": bank_account,
            "type": "TRANSFER_TO_BANK",
            "notes": "",
            "amount": amount
        }

        response = self.auth_call_with_pin(body, endpoint, jwt, pin)

        return response.get("data")

    def aggregate_balance(self):
        endpoint = "corporate/aggregate-balance"
        body = None

        response = self.non_auth_call(body, endpoint)

        return response.get("data")

    def corporate_inquiry_bank_account(self, account_number, bank_code):
        endpoint = "corporate/account-holdername"
        body = {
            "account_number": account_number,
            "bank_code": bank_code
        }

        response = self.non_auth_call(body, endpoint)

        return response.get("data")

    def corporate_save_pin(self, pin):
        endpoint = "corporate/save-pin"
        body = {
            "pin": RsaUtil.encrypt(pin)
        }

        self.non_auth_call(body, endpoint)

    def corporate_pre_forgot_pin(self, new_pin):
        endpoint = "corporate/pre-forgot-pin"
        body = {
            "pin": RsaUtil.encrypt(new_pin)
        }

        self.non_auth_call(body, endpoint)

    def corporate_confirm_forgot_pin(self, otp):
        endpoint = "corporate/forgot-pin"
        body = {
            "confirm_pin_code": otp
        }

        self.non_auth_call(body, endpoint)

    def corporate_change_pin(self, old_pin, new_pin):
        endpoint = "user/change-pin"
        body = {
            "old_pin": RsaUtil.encrypt(old_pin),
            "new_pin": RsaUtil.encrypt(new_pin)
        }

        self.non_auth_call(body, endpoint)

    def corporate_topup_user(self, phone_number, amount):
        endpoint = "user/topup-user"
        body = {
            "phone_number": phone_number,
            "amount": amount
        }

        self.non_auth_call(body, endpoint)

    def corporate_deduct_user(self, phone_number, amount, pin):
        endpoint = "user/deduct-user"
        body = {
            "phone_number": phone_number,
            "amount": amount
        }

        self.non_auth_call_with_pin(body, endpoint, pin)