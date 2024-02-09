import os
from http import HTTPStatus
from uuid import uuid4

import xendit
from starlette.responses import JSONResponse
from xendit.apis import PaymentRequestApi

from model.payment.payment import (
    DirectDebitPaymentIn,
    EWalletPaymentIn,
    PaymentRequestOut,
)
from utils.logger import logger
from utils.utils import Utils


class PaymentUsecase:
    def __init__(self) -> None:
        xendit_api_key_name = os.environ.get('XENDIT_API_KEY_SECRET_NAME')
        self.__xendit_api_key = Utils.get_secret(xendit_api_key_name)

    def direct_debit_payment_request(self, in_data: DirectDebitPaymentIn) -> PaymentRequestOut:
        xendit.set_api_key(self.__xendit_api_key)

        api_client = xendit.ApiClient()

        api_instance = PaymentRequestApi(api_client)

        idempotency_key = str(uuid4())
        reference_id = str(uuid4())

        payment_method_parameters = {
            'type': 'DIRECT_DEBIT',
            'direct_debit': {
                'channel_code': in_data.channel_code,
                'channel_properties': {
                    'success_return_url': in_data.success_return_url,
                    'failure_return_url': in_data.failure_return_url,
                    'email': in_data.email,
                },
            },
            'reusability': 'ONE_TIME_USE',
        }

        payment_request_parameters = {
            'reference_id': reference_id,
            'amount': in_data.amount,
            'currency': 'PHP',
            'payment_method': payment_method_parameters,
            'enable_otp': False,
            'customer': {
                'reference_id': reference_id,
                'type': 'INDIVIDUAL',
                'individual_detail': {
                    'given_names': in_data.given_names,
                    'surname': in_data.surname,
                },
            },
        }

        try:
            # Create Payment Request
            api_response = api_instance.create_payment_request(
                idempotency_key=idempotency_key, payment_request_parameters=payment_request_parameters
            )

            return PaymentRequestOut(
                create_date=api_response.created,
                payment_url=api_response.actions[0].url,
                payment_request_id=api_response.id,
                reference_id=api_response.reference_id,
            )

        except xendit.XenditSdkException as e:
            message = f'Exception when calling PaymentRequestApi->create_payment_request: {e.errorMessage}'
            logger.info(message)

            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': message})

    def e_wallet_payment_request(self, in_data: EWalletPaymentIn) -> PaymentRequestOut:
        xendit.set_api_key(self.__xendit_api_key)

        api_client = xendit.ApiClient()
        api_instance = PaymentRequestApi(api_client)

        idempotency_key = str(uuid4())
        reference_id = in_data.reference_id

        payment_request_parameters = {
            'country': 'PH',
            'amount': in_data.amount,
            'currency': 'PHP',
            'reference_id': reference_id,
            'payment_method': {
                'type': 'EWALLET',
                'ewallet': {
                    'channel_properties': {
                        'success_return_url': in_data.success_return_url,
                        'failure_return_url': in_data.failure_return_url,
                        'cancel_return_url': in_data.cancel_return_url,
                    },
                    'channel_code': in_data.channel_code,
                },
                'reusability': 'ONE_TIME_USE',
            },
        }

        try:
            # Create Payment Request
            api_response = api_instance.create_payment_request(
                idempotency_key=idempotency_key, payment_request_parameters=payment_request_parameters
            )
            return PaymentRequestOut(
                create_date=api_response.created,
                payment_url=api_response.actions[0].url,
                payment_request_id=api_response.id,
                reference_id=api_response.reference_id,
            )

        except xendit.XenditSdkException as e:
            message = f'Exception when calling PaymentRequestApi->create_payment_request: {e.errorMessage}'
            logger.info(message)

            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': message})
