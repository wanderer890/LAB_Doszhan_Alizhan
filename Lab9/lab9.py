import sqlite3
import re

# Исходные данные с исправленными синтаксическими ошибками из методички
students = [
    {'name': 'Aida', 'group': 'IS-24-01', 'score': 82, 'attendance': 91, 'email': 'aida@atu.edu.kz'},
    {'name': 'Miras', 'group': 'IS-24-01', 'score': 69, 'attendance': 88, 'email': 'miras@atu.edu.kz'},
    {'name': 'Dana', 'group': 'IS-24-02', 'score': 91, 'attendance': 96, 'email': 'dana@atu.edu.kz'},
    {'name': 'Timur', 'group': 'IS-24-02', 'score': 74, 'attendance': 62, 'email': 'timur_at_atu.kz'}, # Намеренно ошибочный email
    {'name': 'Aliya', 'group': 'IS-24-03', 'score': 87, 'attendance': 79, 'email': 'aliya@atu.edu.kz'},
    {'name': 'Arman', 'group': 'IS-24-03', 'score': 55, 'attendance': 72, 'email': 'arman@atu.edu.kz'}
]

print("--- Задание 1: Сравнение двух стилей ---")
passed_imperative = []
for student in students:
    if student['score'] >= 75:
        passed_imperative.append(student['name'])

passed_declarative = [
    student['name']
    for student in students
    if student['score'] >= 75
]

print("Императивный стиль:", passed_imperative)
print("Декларативный стиль:", passed_declarative)
print("Совпадают:", passed_imperative == passed_declarative)

print("\n--- Задание 2: Условия для коллекции ---")
has_excellent = any(s['score'] >= 90 for s in students)
all_attended = all(s['attendance'] >= 60 for s in students)
average = sum(s['score'] for s in students) / len(students) if students else 0

print('Есть отличник:', has_excellent)
print('Посещаемость всех не ниже 60%:', all_attended)
print('Средний балл:', round(average, 1))

# Изменяем посещаемость, чтобы all_attended стал False
students[5]['attendance'] = 50
all_attended_new = all(s['attendance'] >= 60 for s in students)
print('Посещаемость всех не ниже 60% (после изменения Арману):', all_attended_new)
students[5]['attendance'] = 72 # Возвращаем для дальнейших заданий

print("\n--- Задание 3: Проверка данных регулярными выражениями ---")
group_pattern = r'^[A-Z]{2}-\d{2}-\d{2}$'
email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

invalid_groups = [s['group'] for s in students if not re.fullmatch(group_pattern, s['group'])]
invalid_emails = [s['email'] for s in students if not re.fullmatch(email_pattern, s['email'])]

print('Ошибочные группы:', invalid_groups)
print('Ошибочные email:', invalid_emails)

# Исправление ошибочного адреса у Тимура
for s in students:
    if s['email'] == 'timur_at_atu.kz':
        s['email'] = 'timur@atu.edu.kz'

invalid_emails_fixed = [s['email'] for s in students if not re.fullmatch(email_pattern, s['email'])]
print('Ошибочные email (после исправления):', invalid_emails_fixed)

print("\n--- Задание 4: Создание базы SQLite ---")
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE students (
    name TEXT NOT NULL,
    group_name TEXT NOT NULL,
    score INTEGER NOT NULL,
    attendance INTEGER NOT NULL,
    email TEXT NOT NULL
)
''')

rows = [(s['name'], s['group'], s['score'], s['attendance'], s['email']) for s in students]
cursor.executemany('INSERT INTO students VALUES (?, ?, ?, ?, ?)', rows)
connection.commit()
print("Таблица создана, данные загружены через параметры '?'.")

print("\n--- Задание 5: Декларативные SQL запросы ---")
print("Выборка и сортировка:")
query1 = '''
SELECT name, score, attendance 
FROM students 
WHERE score >= 75 AND attendance >= 70 
ORDER BY score DESC
'''
for row in cursor.execute(query1):
    print(row)

print("\nГруппировка и агрегирование:")
query2 = '''
SELECT group_name, COUNT(*) AS student_count, ROUND(AVG(score), 1) AS average_score 
FROM students 
GROUP BY group_name 
HAVING AVG(score) >= 70 
ORDER BY average_score DESC
'''
for row in cursor.execute(query2):
    print(row)

print("\n--- Задание 6: Интегрированный результат ---")
query3 = '''
SELECT name, group_name, score, email 
FROM students 
WHERE score >= 70 AND attendance >= 70 
ORDER BY score DESC
'''
result = cursor.execute(query3).fetchall()

valid_result = [row for row in result if re.fullmatch(email_pattern, row[3])]

for place, row in enumerate(valid_result, start=1):
    name, group_name, score, email = row
    print(f'{place}. {name} | {group_name} | {score} | {email}')


print("\n--- Индивидуальный вариант (Вариант 1: Рейтинг отличников) ---")
# Добавим дополнительного отличника в нужную группу для наглядности
cursor.execute("UPDATE students SET score = 95 WHERE name = 'Aida'")

query_var1 = '''
SELECT name, group_name, score, email
FROM students
WHERE score >= 90 AND group_name = 'IS-24-01'
ORDER BY score DESC
'''
result_var1 = cursor.execute(query_var1).fetchall()

if not result_var1:
    print("Отличников в группе IS-24-01 не найдено.")
else:
    for row in result_var1:
        # Дополнительное требование: проверка домена
        if row[3].endswith('@atu.edu.kz'):
            print(f"Студент: {row[0]}, Оценка: {row[2]}, Email домен корректен: {row[3]}")
        else:
            print(f"Студент: {row[0]}, Оценка: {row[2]}, Некорректный домен: {row[3]}")

connection.close()
