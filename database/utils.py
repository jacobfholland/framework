from sqlalchemy import or_, and_


def select_func(func):
    if func == or_ or func == and_:
        return func
    elif isinstance(func, str):
        if func == "and":
            return and_
        elif func == "or":
            return or_
    return and_
