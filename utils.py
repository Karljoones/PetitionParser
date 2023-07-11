def generate_two_column_table_row(column_one_content: str, column_two_content: str):
    return f"<tr><td>{column_one_content}</td><td>{column_two_content or ''}</td></tr>"

def generate_two_column_table_header(header_one: str, header_two: str):
    return f"<tr><th>{header_one}</th><th>{header_two}</th></tr>"

def generate_three_column_table_row(column_one_content: str, column_two_content: str, column_three_content: str):
    return f"<tr><td class='third'>{column_one_content}</td><td class='third'>{column_two_content or ''}</td><td class='third'>{column_three_content or ''}</td></tr>"

def generate_three_column_table_header(header_one: str, header_two: str, header_three: str):
    return f"<tr><th>{header_one}</th><th>{header_two}</th><th>{header_three}</th></tr>"

def format_number(number: int):
    return "{:,}".format(number)

def format_percentage(number: float):
    return f"{number}%"

def calculate_percentage(number: int, total: int, format: bool = True):
    if (format == True):
        return format_percentage(round((number / total) * 100, 2))
    else:
        return round((number / total) * 100, 2)
    
def convert_to_table(content: str):
    return f"<table>{content}</table>"

def convert_to_accordion(title: str, content: str):
    return f"<button class='accordion'>{title}</button><div class='panel'>{content}</div>"