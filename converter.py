class Converter:
    @staticmethod
    def do(x: float) -> int:
        if x == 0.0:
            raise ValueError("x must not be zero")

        if x >= 100.7:
            return 1000

        if x > 0.0:
            return int(x)

        if -30.4 <= x < 0.0:
            return int(x) - 5

        if x <= -30.5:
            return -2000

        # Для входа с точностью 1 знак после запятой эта ветка недостижима:
        # между -30.5 и -30.4 нет значений с одним знаком после запятой.
        raise ValueError(f"Unsupported value: {x}")