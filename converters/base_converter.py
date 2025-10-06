def int_to_base(n: int, base: int) -> str:
    if not (2 <= base <= 36):
        raise ValueError("Основание должно быть от 2 до 36")
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sign = '-' if n < 0 else ''
    n = abs(n)
    res = ''
    while n:
        res = digits[n % base] + res
        n //= base
    return sign + res

def base_to_int(s: str, base: int) -> int:
    if not (2 <= base <= 36):
        raise ValueError("Основание должно быть от 2 до 36")
    return int(s, base)