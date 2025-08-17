from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Extra, Field

from model.payment.payment_constants import DirectDebitChannels, EWalletChannels


class TransactionStatus(str, Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'


class PaymentTransactionIn(BaseModel):
    price: float = Field(None, title='Price')
    transactionStatus: TransactionStatus = Field(None, title='Transaction Status')
    eventId: Optional[str] = Field(None, title='Event ID')
    paymentRequestId: Optional[str] = Field(None, title='Payment Request ID')

    # Registration Data
    firstName: Optional[str] = Field(None, title='First Name')
    lastName: Optional[str] = Field(None, title='Last Name')
    contactNumber: Optional[str] = Field(None, title='Contact Number')
    careerStatus: Optional[str] = Field(None, title='Career Status')
    yearsOfExperience: Optional[str] = Field(None, title='Years of Experience')
    organization: Optional[str] = Field(None, title='Organization')
    title: Optional[str] = Field(None, title='Title')


class PaymentTransactionOut(PaymentTransactionIn):
    entryId: str = Field(..., title='Entry ID')


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
    eventId: Optional[str] = Field(None, title='Event ID')


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
    eventId: Optional[str] = Field(None, title='Event ID')
