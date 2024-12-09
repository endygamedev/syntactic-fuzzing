import re

whitespace = re.compile(r'\s*')
string_pattern = re.compile(r'"((?:\\.|[^"\\])*)"')
number_pattern = re.compile(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?')

def parse(json_string: str):
    json_string = json_string.strip()
    result, _ = _parse_value(json_string, 0)
    return result

def _parse_value(json_string: str, idx: int):
    idx = _skip_whitespace(json_string, idx)

    if json_string[idx] == '"':
        return _parse_string(json_string, idx)
    elif json_string[idx] == '{':
        return _parse_object(json_string, idx)
    elif json_string[idx] == '[':
        return _parse_array(json_string, idx)
    elif json_string[idx] in '-0123456789':
        return _parse_number(json_string, idx)
    elif json_string[idx:idx + 4] == 'true':
        return True, idx + 4
    elif json_string[idx:idx + 5] == 'false':
        return False, idx + 5
    elif json_string[idx:idx + 4] == 'null':
        return None, idx + 4
    else:
        raise ValueError(f'Unexpected character at index {idx}')

def _parse_string(json_string: str, idx: int):
    match = string_pattern.match(json_string, idx)
    if not match:
        raise ValueError(f'Invalid string at index {idx}')
    return match.group(1), match.end()

def _parse_number(json_string: str, idx: int):
    match = number_pattern.match(json_string, idx)
    if not match:
        raise ValueError(f'Invalid number at index {idx}')
    number_str = match.group(0)
    if '.' in number_str or 'e' in number_str or 'E' in number_str:
        return float(number_str), match.end()
    else:
        return int(number_str), match.end()

def _parse_object(json_string: str, idx: int):
    obj = {}
    idx += 1
    idx = _skip_whitespace(json_string, idx)

    if json_string[idx] == '}':
        return obj, idx + 1

    while True:
        idx = _skip_whitespace(json_string, idx)
        key, idx = _parse_string(json_string, idx)
        idx = _skip_whitespace(json_string, idx)
        
        if json_string[idx] != ':':
            raise ValueError(f'Missing colon at index {idx}')
        idx += 1

        idx = _skip_whitespace(json_string, idx)
        value, idx = _parse_value(json_string, idx)
        obj[key] = value

        idx = _skip_whitespace(json_string, idx)
        if json_string[idx] == '}':
            return obj, idx + 1

        if json_string[idx] != ',':
            raise ValueError(f'Missing comma at index {idx}')
        idx += 1

def _parse_array(json_string: str, idx: int):
    array = []
    idx += 1
    idx = _skip_whitespace(json_string, idx)

    if json_string[idx] == ']':
        return array, idx + 1

    while True:
        idx = _skip_whitespace(json_string, idx)
        value, idx = _parse_value(json_string, idx)
        array.append(value)

        idx = _skip_whitespace(json_string, idx)
        if json_string[idx] == ']':
            return array, idx + 1

        if json_string[idx] != ',':
            raise ValueError(f'Missing comma at index {idx}')
        idx += 1

def _skip_whitespace(json_string: str, idx: int):
    match = whitespace.match(json_string, idx)
    return match.end()
