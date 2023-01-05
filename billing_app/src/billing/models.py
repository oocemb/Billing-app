from enum import Enum

from piccolo.columns import (
    Varchar,
    Integer,
    Boolean,
    ForeignKey,
    UUID,
    JSON,
    Numeric,
    Timestamp,
    Date,
    BigSerial,
)
from piccolo.table import Table
from piccolo.columns.readable import Readable


class PAYMENT_STATUS(str, Enum):
    CREATED = "created"
    CONFIRMED_STEP1 = "ok_step1"
    CONFIRMED_STEP2 = "ok_step2"
    REJECTED = "rejected"
    REFUNDED = "refunded"
    ERROR = "error"


class PAYMENT_PROVIDER(str, Enum):
    ROBOKASSA = "robo"
    SBER = "sber"
    YOOKASSA = "yoka"


class STATUS(str, Enum):
    ENABLED = "on"
    DISABLED = "off"
    ARCHIVE = "arc"


class COUPON_TYPE(str, Enum):
    PERCENT = "per"
    ABSOLUTE = "abs"


class PAYMENT_TYPE(str, Enum):
    BUY = "buy"
    RENT = "rent"
    SUBSCRIBE = "subs"


class SUBSCRIBE_STATUS(str, Enum):
    NOT_STARTED = "not"
    ENABLED = "on"
    USER_CANCELED = "usr_cns"
    PAY_REJECTED = "pay_rej"
    SYS_TERMINATED = "sys_trm"


class Coupon(Table):
    id = UUID(primary_key=True)
    title = Varchar(length=20)
    discount = Numeric(digits=(8, 2))
    type = Varchar(length=3, choices=COUPON_TYPE)
    has_deadline = Boolean(default=False)
    deadline = Date()
    use_max_limit = Integer()
    use_counter = Integer()
    status = Varchar(length=3, choices=STATUS)
    duration_subscribe_months = Integer()
    created_at = Timestamp()
    updated_at = Timestamp()

    @classmethod
    def get_readable(cls):
        return Readable(template="%s - %s", columns=[cls.title, cls.discount])


class SubscriptionPlan(Table):
    id = UUID(primary_key=True)
    title = Varchar(length=100)
    level = Integer()
    price = Numeric(digits=(8, 2))
    status = Varchar(length=3, choices=STATUS)
    created_at = Timestamp()
    updated_at = Timestamp()

    @classmethod
    def get_readable(cls):
        return Readable(template="%s - %s", columns=[cls.title, cls.level])


class MoviePriceTier(Table):
    id = UUID(primary_key=True)
    title = Varchar(length=20)
    price = Numeric(digits=(8, 2))

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.title])


class Payment(Table):
    id = BigSerial(primary_key=True)
    external_order_id = Varchar(length=256, default="")
    user = UUID()
    price = Numeric(digits=(8, 2))
    price_original = Numeric(digits=(8, 2))
    payment_provider = Varchar(length=4, choices=PAYMENT_PROVIDER)
    meta_info = JSON()
    payment_type = Varchar(length=7, choices=PAYMENT_TYPE)
    content = UUID()
    status = Varchar(length=10, choices=PAYMENT_STATUS)
    parent_payment = Varchar(length=256, default="")
    coupon = ForeignKey(references=Coupon)
    is_auto_recurrent = Boolean(default=False)
    is_refund = Boolean(default=False)
    purchased_from_url = Varchar(length=255)
    created_at = Timestamp()
    updated_at = Timestamp()


class UserSubscribe(Table):
    id = UUID(primary_key=True)
    user = UUID()
    subscribe_plan = ForeignKey(references=SubscriptionPlan)
    pay_fail_counter = Integer()
    coupon = ForeignKey(references=Coupon)
    first_payment = ForeignKey(references=Payment)
    subscribe_status = Varchar(length=7, choices=SUBSCRIBE_STATUS)
    pay_meta_info = JSON()
    created_at = Timestamp()
    updated_at = Timestamp()
    terminated_at = Timestamp()
