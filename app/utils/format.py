import re


def snake_case(input_str: str) -> str:
    """Convert a string to snake_case.

    Args:
        - ``input_str`` (str): The input string to be converted.

    Returns:
        ``str``: The snake_case representation of the input string.
    """

    if re.match(r'^[a-z_]+$', input_str):
        return input_str
    snake_case_str = re.sub(
        r'[\sA-Z]', lambda x: '_' + x.group(0).lower(), input_str)
    snake_case_str = snake_case_str.lstrip('_')
    return snake_case_str
