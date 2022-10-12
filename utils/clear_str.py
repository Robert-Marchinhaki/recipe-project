from unidecode import unidecode


def cleaning_str(value: str):
    return unidecode(value.strip().replace(' ', '-').lower())


if __name__ == '__main__':
    test_str = cleaning_str('Tradução livre para todos    ')
    print(test_str)
