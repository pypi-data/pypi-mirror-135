import os


def get_bool(key, default):
    """
    ### Description:

    Cast string to bool

    ### Args:

    `key`: the key to get from ENV variable

    `default`: value to return if key not in ENV variable

    ### Return:
    True/False (bool)
    """

    v = os.environ.get(key, default)
    if v in ["False", "0", False]:
        return False
    else:
        return True


class Config:
    """
    ### Description:

    Configuration class - define some variables used by package
    """

    ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
    AUTH_URL = os.environ.get("AUTH_SUPERWISE_URL", "https://auth.superwise.ai")
    SUPERWISE_HOST = os.environ.get("SUPERWISE_HOST", "portal.superwise.ai")
    POOLING_INTERVAL_SEC = 15
    LIST_DROP_DATA_COLS = ["model_id", "version_id"]
