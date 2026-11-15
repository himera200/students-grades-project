def ask (prompt: str, allow_empty: bool = False) -> str:
    while True:
        value = input(f"{prompt}: ").strip()
        if value or allow_empty:
            return value
        print("Поле не может быть пустым")


def ask_optional(prompt: str) -> str | None:
    value = input(f"{prompt} (Enter - пропустить): ").strip()
    return value or None


def ask_int(prompt: str, min_value: int | None = None,
            max_value: int | None = None) -> int:
    while True:
        raw = input(f"{prompt}: ").strip()
        try:
            value = int(raw)
        except ValueError:
            print("Нужно ввести целое число")
            continue
        if min_value is not None and value < min_value:
            print(f"Число должно быть не меньше {min_value}")
            continue
        if max_value is not None and value > max_value:
            print(f"Число должно быть не больше {max_value}")
            continue
        return value


def ask_choice(prompt: str = "Выберите действие") -> str:
    return input(f"{prompt}: ").strip()


def confirm(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (д/н): ").strip().lower()
        if answer in ("д", "да", "y", "yes"):
            return True
        if answer in ("н", "нет", "n", "no"):
            return False
        print("Введите «д» или «н»")


def print_header(title: str) -> None:
    print(f"\n===== {title} =====")


def print_table(headers: list[str], rows: list[list]) -> None:
    if not rows:
        print("Нет данных")
        return
    text_rows = [["" if c is None else str(c) for c in row] for row in rows]
    widths = [max(len(headers[i]), *(len(r[i]) for r in text_rows))
              for i in range(len(headers))]

    def line(cells):
        return " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells))

    print(line(headers))
    print("-+-".join("-" * w for w in widths))
    for row in text_rows:
        print(line(row))


def run(action, *args):
    """Вызывает сервис и возвращает результат; при ValueError печатает ошибку."""
    try:
        return action(*args)
    except ValueError as e:
        print(f"\nОшибка: {e}")
        return None


def do(action, success_message: str, *args) -> bool:
    """Для действий без результата: печатает успех или ошибку."""
    try:
        action(*args)
    except ValueError as e:
        print(f"\nОшибка: {e}")
        return False
    print(f"\n{success_message}")
    return True