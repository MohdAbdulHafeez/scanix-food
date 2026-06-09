class RateLimiter:

    def __init__(
        self,
        per_minute: int,
    ):

        self.per_minute = per_minute