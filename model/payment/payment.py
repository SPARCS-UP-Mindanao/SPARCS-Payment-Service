from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Extra, Field

from model.payment.payment_constants import DirectDebitChannels, EWalletChannels


class DirectDebitPaymentIn(BaseModel):
    class Config:
        extra = Extra.forbid

    amount: float = Field(..., title='Amount')
    givenNames: str = Field(..., title='Given Names')
    surname: str = Field(..., title='Surnames')
    email: EmailStr = Field(..., title='Email')
    channelCode: DirectDebitChannels = Field(..., title='Channel Code')
    successReturnUrl: str = Field(..., title='Success Return URL')
    failureReturnUrl: str = Field(..., title='Failure Return URL')


class PaymentRequestOut(BaseModel):
    class Config:
        extra = Extra.ignore

    createDate: datetime = Field(..., title='Updated Date')
    paymentUrl: str = Field(..., title='Payment URL')
    paymentRequestId: str = Field(..., title='Payment Request ID')
    referenceId: str = Field(..., title='Reference ID')


class EWalletPaymentIn(BaseModel):
    class Config:
        extra = Extra.forbid

    successReturnUrl: str = Field(..., title='Success Return URL')
    failureReturnUrl: str = Field(..., title='Failure Return URL')
    cancelReturnUrl: Optional[str] = Field(None, title='Cancel Return URL')
    referenceId: str = Field(..., title='Reference ID')
    amount: float = Field(..., title='Amount')
    channelCode: EWalletChannels = Field(..., title='Channel Code')
