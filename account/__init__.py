class ProductPermissionType:
    """Represents the type of a product that the user has bought.

    The following product types are possible:
    - PRO -
    - NORMAL - 
    - ALL_IN_ONE
    - NOT_SET
    """

    PREMIUM = "premium"
    NORMAL = "normal"
    ALL_IN_ONE = "all-in-one"
    NOT_SET = "not-set"
    # FIXME we could use another status like WAITING_FOR_AUTH for transactions
    # Which were authorized, but needs to be confirmed manually by staff
    # eg. Braintree with "submit_for_settlement" enabled
    CHOICES = [
        (PREMIUM, "پرمیوم"),
        (NORMAL, "معمولی"),
        (ALL_IN_ONE, "آل این وان"),
        (NOT_SET, "خریداری نشده"),
    ]
