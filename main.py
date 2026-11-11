from converter import Converter


def main() -> None:
    print("Введите число (с точностью 1 знак после запятой).")
    print("Для выхода введите 'q' или пустую строку.\n")

    while True:
        raw = input("x = ").strip()

        if raw == "" or raw.lower() == "q":
            print("Выход.")
            break

        try:
            x = float(raw)
        except ValueError:
            print(f"Ошибка: '{raw}' не является числом. Попробуйте снова.\n")
            continue

        try:
            result = Converter.do(x)
            print(f"Converter.do({x}) = {result}\n")
        except ValueError as e:
            print(f"Исключение: {e}\n")


if __name__ == "__main__":
    main()