from datetime import datetime

from pydantic import BaseModel, EmailStr, Extra, Field

from model.payment.payment_constants import DirectDebitChannels, EWalletChannels


class CreateDirectDebitPaymentMethodIn(BaseModel):
    class Config:
        extra = Extra.forbid

    given_names: str = Field(..., title='Given Names')
    surname: str = Field(..., title='Surnames')
    email: EmailStr = Field(..., title='Email')
    channel_code: DirectDebitChannels = Field(..., title='Channel Code')
    success_return_url: str = Field(..., title='Success Return URL')
    failure_return_url: str = Field(..., title='Failure Return URL')


class CreateDirectDebitPaymentMethodOut(BaseModel):
    class Config:
        extra = Extra.ignore

    allow_payment_url: str = Field(..., title='Allow Payment URL')
    customer_id: str = Field(..., title='Customer ID')
    payment_method_id: str = Field(..., title='Payment Method ID')
    reference_id: str = Field(..., title='Reference ID')
    create_date: datetime = Field(..., title='Updated Date')


class DirectDebitPaymentIn(BaseModel):
    class Config:
        extra = Extra.forbid

    payment_method_id: str = Field(..., title='Payment Method ID')
    callback_url: str = Field(..., title='Callback URL')
    reference_id: str = Field(..., title='Reference ID')
    amount: float = Field(..., title='Amount')


class PaymentRequestOut(BaseModel):
    class Config:
        extra = Extra.ignore

    create_date: datetime = Field(..., title='Updated Date')
    payment_url: str = Field(..., title='Payment URL')
    payment_request_id: str = Field(..., title='Payment Request ID')
    reference_id: str = Field(..., title='Reference ID')


class EWalletPaymentIn(BaseModel):
    class Config:
        extra = Extra.forbid

    success_return_url: str = Field(..., title='Success Return URL')
    failure_return_url: str = Field(..., title='Failure Return URL')
    reference_id: str = Field(..., title='Reference ID')
    amount: float = Field(..., title='Amount')
    channel_code: EWalletChannels = Field(..., title='Channel Code')
