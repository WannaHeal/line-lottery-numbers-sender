import logging

from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage

from constants import LINE_ADMIN_ID, LINE_CHANNEL_ACCESS_TOKEN

logger = logging.getLogger(__name__)


class MyLineBotApi:
    api: LineBotApi
    admin_id: str

    def __init__(self):
        self._verify_channel_access_token()
        self._verify_admin_id()

    def _verify_channel_access_token(self):
        """환경 변수로 들어온 `LINE_CHANNEL_ACCESS_TOKEN` 값을 검증한 후,
        `self.api`에 새로운 `LineBotApi` 오브젝트를 할당합니다.

        Raises:
            Exception: `LINE_CHANNEL_ACCESS_TOKEN` 값이 설정되지 않은 경우
            LineBotApiError: LINE API에서 에러가 발생한 경우
        """
        logger.debug(LINE_CHANNEL_ACCESS_TOKEN)
        if LINE_CHANNEL_ACCESS_TOKEN is None:
            logger.error("환경 변수 LINE_CHANNEL_ACCESS_TOKEN이 설정되지 않았습니다")
            raise Exception
        self.api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
        try:
            self.api.get_bot_info()
        except LineBotApiError as e:
            logger.error(f"환경 변수 LINE_CHANNEL_ACCESS_TOKEN 검증 중 에러가 발생했습니다: {e}")
            raise e

    def _verify_admin_id(self):
        """환경 변수로 들어온 `LINE_ADMIN_ID` 값을 검증한 후,
        `self.admin_id`에 admin ID를 할당합니다.

        Raises:
            Exception: `LINE_ADMIN_ID` 값이 설정되지 않은 경우
            LineBotApiError: LINE API에서 에러가 발생한 경우
        """
        logger.debug(LINE_ADMIN_ID)
        if LINE_ADMIN_ID is None:
            logger.error("환경 변수 LINE_ADMIN_ID가 설정되지 않았습니다")
            raise Exception
        self.admin_id = LINE_ADMIN_ID
        try:
            self.api.get_profile(self.admin_id)
        except LineBotApiError as e:
            logger.error(f"환경 변수 LINE_ADMIN_ID 검증 중 에러가 발생했습니다: {e}")
            raise e

    def send_error_log_to_admin(self, msg: str):
        """로직 실행 중 발생한 에러 메시지를 admin에게 전송합니다.

        Args:
            msg (str): 에러 메시지의 내용

        Raises:
            LineBotApiError: LINE API에서 에러가 발생한 경우
        """
        try:
            self.api.push_message(
                self.admin_id, TextSendMessage(f"봇 내부 로직 실행 중 에러가 발생했습니다: {msg}")
            )
        except LineBotApiError as e:
            logger.error(f"에러 로그 전송 중 에러가 발생했습니다: {e}")
            raise e

    def get_user_profile(self, user_id: str):
        """입력받은 `user_id`를 이용해 유저의 profile에 접근합니다.

        Args:
            user_id (str): LINE 회원의 유저 ID

        Raises:
            LineBotApiError: LINE API에서 에러가 발생한 경우
        """
        try:
            self.api.get_profile(user_id)
        except LineBotApiError as e:
            error_message = f"user_id 검증 중 에러가 발생했습니다: {e}"
            logger.error(error_message)
            self.api.push_message(self.admin_id, TextSendMessage(error_message))
            raise e

    def send_single_message_to_user(self, user_id: str, context: str):
        """유저 1명에게 텍스트 메시지를 전송합니다.

        Args:
            user_id (str): LINE 회원의 유저 ID
            context (str): LINE 회원에게 전송할 메시지의 본문

        Raises:
            LineBotApiError: LINE API에서 에러가 발생한 경우
        """
        try:
            self.api.push_message(user_id, TextSendMessage(context))
        except LineBotApiError as e:
            error_message = f"유저에게 메시지 전송 중 에러가 발생했습니다: {e}"
            logger.error(error_message)
            try:
                self.api.push_message(self.admin_id, TextSendMessage(error_message))
            except LineBotApiError as ee:
                logger.error(f"에러 로그 전송 중 에러가 발생했습니다: {ee}")
                raise ee
            raise e


my_line_bot_api = MyLineBotApi()
