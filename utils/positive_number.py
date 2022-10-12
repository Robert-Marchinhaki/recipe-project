def get_positive_number(value):
    try:
        number_positive = float(value)
    except ValueError:
        return False
    return number_positive > 0


if __name__ == '__main__':
    assert get_positive_number('10') is True
    assert get_positive_number('-10') is False
    assert get_positive_number('-0.75') is False
    assert get_positive_number('-2a') is False
    assert get_positive_number('abc') is False
