import re
import json

def clean_price(price_str):
    """
    Убирает пробелы и преобразует строку цены в float.
    Например: '1 200,00' -> 1200.00
    """
    price_str = price_str.replace(" ", "").replace(",", ".")
    return float(price_str)


def parse_receipt(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.splitlines()

    products = []
    prices = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Поиск строки с номером товара (например "1.")
        if re.match(r'^\d+\.$', line):
            # Название товара
            name = lines[i + 1].strip()

            # Строка с количеством и ценой
            qty_price_line = lines[i + 2].strip()

            # Общая стоимость товара (следующая строка)
            total_price_line = lines[i + 3].strip()

            # Извлекаем цену
            price_match = re.search(r'([\d\s]+,\d{2})', total_price_line)

            if price_match:
                price = clean_price(price_match.group(1))
                prices.append(price)

                products.append({
                    "name": name,
                    "price": price
                })

            i += 4
        else:
            i += 1

    # Итоговая сумма
    total_match = re.search(r'ИТОГО:\s*\n?\s*([\d\s]+,\d{2})', text)
    total_sum = clean_price(total_match.group(1)) if total_match else sum(prices)

    # Дата и время
    datetime_match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})', text)
    datetime_value = datetime_match.group(1) if datetime_match else None

    # Способ оплаты
    payment_match = re.search(r'(Банковская карта|Наличные)', text)
    payment_method = payment_match.group(1) if payment_match else "Не найдено"

    result = {
        "products": products,
        "prices": prices,
        "total_sum": total_sum,
        "calculated_sum": sum(prices),
        "datetime": datetime_value,
        "payment_method": payment_method
    }

    return result


if __name__ == "__main__":
    data = parse_receipt("raw.txt")
    print(json.dumps(data, indent=4, ensure_ascii=False))