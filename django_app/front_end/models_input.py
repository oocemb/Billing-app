class PaymentHistory:
    def __init__(
        self,
        product_id,
        payment_method,
        purchase_date,
        coupon,
        price,
        product_type,
        is_refund,
        is_recurrent,
    ):
        self.coupon = coupon
        self.product_id = product_id
        self.payment_method = payment_method
        self.purchase_date = purchase_date
        self.price = price
        self.product_type = product_type
        self.is_refund = is_refund
        self.is_recurrent = is_recurrent
        self.title = ""
