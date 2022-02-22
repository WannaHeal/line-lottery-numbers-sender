from typing import List


class Receiver:
    user_id: str
    is_global: bool

    def __init__(self, user_id: str, is_global: bool) -> None:
        self.user_id = user_id
        self.is_global = is_global


class ReceiverRepository:
    receivers: List[Receiver]

    def __init__(self) -> None:
        self.receivers = []

    def add(self, user_id: str, is_global: bool = True):
        self.receivers.append(Receiver(user_id, is_global))


receiver_repository = ReceiverRepository()
