from usecase.payment_tracking_usecase import PaymentTrackingUsecase
from utils.logger import logger


def handler(event, context):
    """Payment tracking handler"""
    _ = context

    logger.info(f'Payment tracking handler event: {event}')

    payment_tracking_usecase = PaymentTrackingUsecase()
    payment_tracking_usecase.track_pending_payments()

    return {'statusCode': 200, 'body': 'Payment tracking handler completed'}
