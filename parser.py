import re


def parse_variants(text: str) -> list[str]:
    """
    Парсит текст и возвращает список вариантов.
    
    Поддерживаемые разделители:
    - запятая
    - символ /
    - перенос строки
    
    Удаляет лишние пробелы и пустые строки.
    """
    if not text or not text.strip():
        return []
    
    result = []
    
    # Разделяем по переносам строк
    lines = text.split('\n')
    
    for line in lines:
        # В каждой строке разделяем по запятым или слэшам
        # Слэш может быть окружён пробелами: "фильм 1 / фильм 2"
        parts = re.split(r'\s*,\s*|\s*/\s*', line)
        
        for part in parts:
            cleaned = part.strip()
            if cleaned:  # Игнорируем пустые строки
                result.append(cleaned)
    
    return result


def split_teams(items: list[str]) -> tuple[list[str], list[str]]:
    """
    Случайно делит список участников на 2 команды.
    
    Если нечётное количество, разница между командами может быть 1 человек.
    """
    import random
    
    # Создаём копию списка и перемешиваем
    shuffled = items.copy()
    random.shuffle(shuffled)
    
    # Делим пополам
    mid = len(shuffled) // 2
    
    team1 = shuffled[:mid]
    team2 = shuffled[mid:]
    
    return team1, team2
