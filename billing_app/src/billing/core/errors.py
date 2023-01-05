from enum import Enum


class ErrorStatus(str, Enum):
    ITEMS_NOT_FOUND = "Items not found"
    SUBSCRIPTION_NOT_FOUND = "Subscription not found"
    MOVIES_NOT_FOUND = "Movies not found"
