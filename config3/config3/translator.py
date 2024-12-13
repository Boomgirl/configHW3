import json
import sys
import re
# команда запуска: python3 translator.py test.txt <primer.json

def parse_json(input_json):
    try:
        # Удаляем многострочные комментарии из JSON для парсинга
        clean_json = re.sub(r'/\*(.*?)\*/', '', input_json, flags=re.DOTALL)
        data = json.loads(clean_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка в формате JSON: {e}")

    return data

def process_data(data, comments):
    constants = {}
    output_lines = []

    # Добавляем комментарии в выходные строки
    for comment in comments:
        formatted_comment = f"<# {comment.strip()} #>"
        output_lines.append(formatted_comment)

    # Обработка констант
    for constant in data.get("constants", []):
        name = constant.get("name")
        value = constant.get("value")
        if isinstance(value, list):  # Если значение - это массив
        	#print(value)
            value = "(" + ", ".join(map(str, value)) + ")"
        output_lines.append(name + " = " + str(value))
        constants[name] = value

    # Обработка значений
    values = data.get("values", [])
    formatted_values = []  # Для хранения форматированных значений
    for value in values:
        if isinstance(value, str) and value.startswith("^["):
            const_name = value[2:-1]  # Убираем ^[ и ]
            if const_name in constants:
                formatted_values.append(str(constants[const_name]))
            else:
                raise ValueError(f"Неизвестная константа: {const_name}")
        elif isinstance(value, (int, float)):
            formatted_values.append(str(value))
            print(value)
        elif isinstance(value, list):  # Если значение - это массив
        	#print(value)
            formatted_array = "(" + ", ".join(map(str, value)) + ")"
            print(value)
            formatted_values.append(formatted_array)
        else:
            raise ValueError(f"Недопустимое значение: {value}")

    # Добавляем значения в выходные строки
    output_lines.extend(formatted_values)

    return output_lines

def write_output(output_lines, file_path):
    with open(file_path, 'w') as f:
        for line in output_lines:
            f.write(line + "\n")  # Запись без лишних пустых строк

def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <путь_к_выходному_файлу>")
        sys.exit(1)

    output_file = sys.argv[1]

    # Чтение JSON с входа
    input_data = sys.stdin.read()

    # Находим все многострочные комментарии
    comments = re.findall(r'/\*(.*?)\*/', input_data, flags=re.DOTALL)

    # Парсинг JSON
    data = parse_json(input_data)

    # Обработка данных
    output_lines = process_data(data, comments)

    # Запись результата в файл
    write_output(output_lines, output_file)
    
if __name__ == '__main__':
	main()
