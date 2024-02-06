from fastapi import APIRouter

from model.common import Message
from model.payment.payment import (
    CreateDirectDebitPaymentMethodIn,
    CreateDirectDebitPaymentMethodOut,
    DirectDebitPaymentIn,
    PaymentRequestOut,
)
from usecase.payment_usecase import PaymentUsecase

direct_debit_router = APIRouter()


@direct_debit_router.post(
    '/payment_method',
    response_model=CreateDirectDebitPaymentMethodOut,
    responses={
        400: {'model': Message, 'description': 'Bad request'},
        500: {'model': Message, 'description': 'Internal server error'},
    },
    summary='Create Direct Debit Payment Method',
)
@direct_debit_router.post(
    '/payment_method/',
    response_model=CreateDirectDebitPaymentMethodOut,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    include_in_schema=False,
)
def create_direct_debit_payment_method(
    create_direct_debit_payment_method_in: CreateDirectDebitPaymentMethodIn,
):
    payment_usecase = PaymentUsecase()
    return payment_usecase.create_direct_debit_payment_method(create_direct_debit_payment_method_in)


@direct_debit_router.post(
    '/payment_request',
    response_model=PaymentRequestOut,
    responses={
        400: {'model': Message, 'description': 'Bad request'},
        500: {'model': Message, 'description': 'Internal server error'},
    },
    summary='Pay with Direct Debit Payment Method',
)
@direct_debit_router.post(
    '/payment_request/',
    response_model=PaymentRequestOut,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    include_in_schema=False,
)
def direct_debit_payment_request(
    direct_debit_payment_request_in: DirectDebitPaymentIn,
):
    payment_usecase = PaymentUsecase()
    return payment_usecase.direct_debit_payment_request(direct_debit_payment_request_in)
