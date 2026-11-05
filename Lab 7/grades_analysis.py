"""
Лабораторная работа №7: Функциональная парадигма
Вариант 1: Анализ оценок
Студент: Досжан Алижан, Группа ТИИ25-21
"""

from typing import List, Dict, Any, Optional

# ==========================================
# ЧИСТОЕ ВЫЧИСЛИТЕЛЬНОЕ ЯДРО
# ==========================================

def validate_score(score: Any) -> float:
    """Проверяет корректность балла. Чистая функция."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError("Балл должен быть числом")
    if not 0 <= score <= 100:
        raise ValueError("Балл должен быть от 0 до 100")
    return float(score)

def validate_scores(scores: List[Any]) -> List[float]:
    """Возвращает новый список корректных значений, не изменяя исходный."""
    return [validate_score(score) for score in scores]

def calculate_average(scores: List[float]) -> Optional[float]:
    """Вычисляет среднее значение. Чистая функция."""
    return sum(scores) / len(scores) if scores else None

def calculate_median(scores: List[float]) -> Optional[float]:
    """Вычисляет медиану, возвращая результат без изменения исходного списка."""
    if not scores:
        return None
    sorted_scores = sorted(scores)
    n = len(sorted_scores)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_scores[mid - 1] + sorted_scores[mid]) / 2.0
    return sorted_scores[mid]

def admission_status(scores: List[float], threshold: float = 50.0) -> str:
    """Определяет статус допуска. Чистая функция."""
    avg = calculate_average(scores)
    if avg is None:
        return "нет данных"
    return "допущен" if avg >= threshold else "не допущен"

def recursive_max(values: List[float]) -> float:
    """Рекурсивный поиск максимума с явным базовым случаем."""
    if not values:
        raise ValueError("Последовательность пуста")
    if len(values) == 1:
        return values[0]
    
    tail_max = recursive_max(values[1:])
    return values[0] if values[0] > tail_max else tail_max

def build_report(name: str, scores: List[Any]) -> Dict[str, Any]:
    """Неизменяемое преобразование: возвращает новый словарь отчета."""
    checked = validate_scores(scores)
    return {
        "name": name.strip(),
        "scores": tuple(checked),
        "average": calculate_average(checked),
        "median": calculate_median(checked),
        "status": admission_status(checked),
        "maximum": recursive_max(checked) if checked else None,
    }

# ==========================================
# ИМПЕРАТИВНАЯ ОБОЛОЧКА
# ==========================================

def main():
    """Ввод и вывод отделены от вычислительного ядра."""
    source_scores = [80, 75.5, 90, 45, 100]
    
    print("--- Анализ успеваемости ---")
    try:
        report = build_report("Досжан Алижан", source_scores)
        for key, value in report.items():
            print(f"{key.capitalize()}: {value}")
            
        print("\nПроверка неизменяемости:")
        print(f"Исходный список: {source_scores}")
    except Exception as e:
        print(f"Ошибка обработки: {e}")

if __name__ == "__main__":
    main()