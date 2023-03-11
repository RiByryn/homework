def search4vowels(phrase: str) -> set:
    """Возвращает булево значение в зависимости
    от присутствия дугих гласных."""
    vowels = set('aeiou')
    found = vowels.intersection(set(phrase))
    return bool(found)

def search4letters(phrase: str, letters: str='aeiou') -> set:
    """Возвращает множество букв из 'letters', найденных
    в указанной фразе."""
    return set(letters).intersection(set(phrase))
