import os

LOTTERY_NUMBER_RANGE_START = 1
LOTTERY_NUMBER_RANGE_END = 45
LOTTERY_NUMBER_AMOUNT = 6

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_ADMIN_ID = os.environ.get("LINE_ADMIN_ID")
LINE_RECEIVER_ID = os.environ.get("LINE_RECEIVER_ID")

MESSAGE_CONTEXT = "이번 주 기계신님께서 점지해 주신 번호는 다음과 같습니다:\n{numbers}"
