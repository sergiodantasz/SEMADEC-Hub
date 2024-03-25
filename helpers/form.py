def set_attr(field, name, value) -> None:
    field.widget.attrs[name] = value


def set_placeholder(field, value) -> None:
    set_attr(field, 'placeholder', value)
