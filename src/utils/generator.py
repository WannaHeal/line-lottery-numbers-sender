import logging
import random

from constants import (
    LOTTERY_NUMBER_AMOUNT,
    LOTTERY_NUMBER_RANGE_END,
    LOTTERY_NUMBER_RANGE_START,
    MESSAGE_CONTEXT,
)

logger = logging.getLogger(__name__)


def _generate_lottery_numbers_list():
    return sorted(
        random.sample(
            range(LOTTERY_NUMBER_RANGE_START, LOTTERY_NUMBER_RANGE_END + 1),
            LOTTERY_NUMBER_AMOUNT,
        )
    )


def get_lottery_numbers_message():
    return MESSAGE_CONTEXT.format(numbers=_generate_lottery_numbers_list())
