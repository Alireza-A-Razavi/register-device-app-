class ProductType:
    """Represents the type of a product that the user has bought.

    The following product types are possible:
    - NORMAL -
    - PLUGIN - 
    - OTHER
    """

    NORMAL = "normal"
    PLUGIN = "plugin"
    OTHER = "other"
    # FIXME we could use another status like WAITING_FOR_AUTH for transactions
    # Which were authorized, but needs to be confirmed manually by staff
    # eg. Braintree with "submit_for_settlement" enabled
    CHOICES = [
        (NORMAL, "معمولی"),
        (PLUGIN, "پلاگین"),
        (OTHER, "دیگر"),
    ]
