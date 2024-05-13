MAX_LEN_STRING = 13
BASE_36 = 36


def base36_to_int(string):
    """
    Преобразование строки base 36 в int.
    Для предотвращение перегрузки сервера отклонять запросы конвертации
    длинной более 13 символов.
    13 знаков достаточно для представления любового 64 битного числа.
    """
    if len(string) > MAX_LEN_STRING:
        raise ValueError('Длина входного значения base36 больше 13 символов.')
    return int(string, BASE_36)


def int_to_base36(integer_number: int):
    """Преобразование числа в строку."""
    char_set = '0123456789abcdefghijklmnopqrstuvwxyz'
    if integer_number < 0:
        raise ValueError('Отрицательное число для конвертации.')
    if integer_number < BASE_36:
        return char_set[integer_number]
    base36 = ''
    while integer_number != 0:
        integer_number, n = divmod(integer_number, BASE_36)
        base36 = char_set[n] + base36
    return base36
