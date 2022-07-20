

class ChargeStatus:
    """Represents possible statuses of a payment.

    The following statuses are possible:
    - NOT_CHARGED - no funds were take off the customer founding source yet.
    - PARTIALLY_CHARGED - funds were taken off the customer's funding source,
    partly covering the payment amount.
    - FULLY_CHARGED - funds were taken off the customer founding source,
    partly or completely covering the payment amount.
    - PARTIALLY_REFUNDED - part of charged funds were returned to the customer.
    - FULLY_REFUNDED - all charged funds were returned to the customer.
    """

    NOT_CHARGED = "not-charged"
    PENDING = "pending"
    PARTIALLY_CHARGED = "partially-charged"
    FULLY_CHARGED = "fully-charged"
    PARTIALLY_REFUNDED = "partially-refunded"
    FULLY_REFUNDED = "fully-refunded"
    REFUSED = "refused"
    CANCELLED = "cancelled"

    CHOICES = [
        (NOT_CHARGED, "Not charged"),
        (PENDING, "Pending"),
        (PARTIALLY_CHARGED, "Partially charged"),
        (FULLY_CHARGED, "Fully charged"),
        (PARTIALLY_REFUNDED, "Partially refunded"),
        (FULLY_REFUNDED, "Fully refunded"),
        (REFUSED, "Refused"),
        (CANCELLED, "Cancelled"),
    ]


class TransactionKind:
    """Represents the type of a transaction.

    The following transactions types are possible:
    - AUTH - an amount reserved against the customer's funding source. Money
    does not change hands until the authorization is captured.
    - VOID - a cancellation of a pending authorization or capture.
    - CAPTURE - a transfer of the money that was reserved during the
    authorization stage.
    - REFUND - full or partial return of captured funds to the customer.
    """

    EXTERNAL = "external"
    AUTH = "auth"
    CAPTURE = "capture"
    CAPTURE_FAILED = "capture_failed"
    ACTION_TO_CONFIRM = "action_to_confirm"
    VOID = "void"
    PENDING = "pending"
    REFUND = "refund"
    REFUND_ONGOING = "refund_ongoing"
    REFUND_FAILED = "refund_failed"
    REFUND_REVERSED = "refund_reversed"
    CONFIRM = "confirm"
    CANCEL = "cancel"
    # FIXME we could use another status like WAITING_FOR_AUTH for transactions
    # Which were authorized, but needs to be confirmed manually by staff
    # eg. Braintree with "submit_for_settlement" enabled
    CHOICES = [
        (EXTERNAL, "External reference"),
        (AUTH, "Authorization"),
        (PENDING, "Pending"),
        (ACTION_TO_CONFIRM, "Action to confirm"),
        (REFUND, "Refund"),
        (REFUND_ONGOING, "Refund in progress"),
        (CAPTURE, "Capture"),
        (VOID, "Void"),
        (CONFIRM, "Confirm"),
        (CANCEL, "Cancel"),
    ]
