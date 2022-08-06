class ProductType:
    """Represents the type of a product that the user has bought.

    The following product types are possible:
    - PRO -
    - NORMAL - 
    - ALL_IN_ONE
    """

    PREMIUM = "premium"
    NORMAL = "normal"
    ALL_IN_ONE = "all-in-one"
    # FIXME we could use another status like WAITING_FOR_AUTH for transactions
    # Which were authorized, but needs to be confirmed manually by staff
    # eg. Braintree with "submit_for_settlement" enabled
    CHOICES = [
        (PREMIUM, "پرمیوم"),
        (NORMAL, "معمولی"),
        (ALL_IN_ONE, "آل این وان"),
    ]
