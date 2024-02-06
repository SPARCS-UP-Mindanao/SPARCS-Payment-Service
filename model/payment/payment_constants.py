from enum import Enum


class DirectDebitChannels(str, Enum):
    BPI = 'BPI'
    UBP = 'UBP'
    RCBC = 'RCBC'
    CHINABANK = 'CHINABANK'


class EWalletChannels(str, Enum):
    GCASH = 'GCASH'
    PAYMAYA = 'PAYMAYA'
