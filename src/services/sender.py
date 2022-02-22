import logging

from linebot.exceptions import LineBotApiError

from bot.api import my_line_bot_api
from bot.receivers import receiver_repository
from constants import LINE_RECEIVER_ID
from utils.generator import get_lottery_numbers_message

logger = logging.getLogger(__name__)


def _verify_receiver_id():
    logger.debug(LINE_RECEIVER_ID)
    if LINE_RECEIVER_ID is None:
        error_message = "환경 변수 LINE_RECEIVER_ID가 설정되지 않았습니다"
        logger.error(error_message)
        my_line_bot_api.send_error_log_to_admin(error_message)
        pass
    receiver_id_list = LINE_RECEIVER_ID.split(",")
    for user_id in receiver_id_list:
        try:
            my_line_bot_api.get_user_profile(user_id)
            receiver_repository.add(user_id)
        except LineBotApiError:
            pass


def send_message_to_users():
    _verify_receiver_id()
    global_lottery_message = get_lottery_numbers_message()
    for receiver in receiver_repository.receivers:
        message = (
            global_lottery_message
            if receiver.is_global
            else get_lottery_numbers_message()
        )
        my_line_bot_api.send_single_message_to_user(receiver.user_id, message)
