from enum import Enum


class PaymentMethod(str, Enum):
    DIRECT_DEBIT = 'DIRECT_DEBIT'
    E_WALLET = 'E_WALLET'


class DirectDebitChannels(str, Enum):
    BPI = 'BPI'
    UBP = 'UBP'
    RCBC = 'RCBC'
    CHINABANK = 'CHINABANK'


class EWalletChannels(str, Enum):
    GCASH = 'GCASH'
    PAYMAYA = 'PAYMAYA'


class PaymentRequestConstants:
    SUCCESS_STATUSES = ('SUCCEEDED',)
    ERROR_STATUSES = (
        'CANCELED',
        'FAILED',
        'VOIDED',
        'EXPIRED',
        'UNKNOWN',
        'UNKNOWN_ENUM_VALUE',
    )
    PENDING_STATUSES = (
        'PENDING',
        'REQUIRES_ACTION',
        'AWAITING_CAPTURE',
    )
