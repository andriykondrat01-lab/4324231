"""
Приклад: Соціальна мережа
==========================
Знаходимо ступені знайомства між людьми (як LinkedIn або Facebook).
"""

from collections import deque


def find_connection_degree(network: dict, person_a: str, person_b: str):
    """
    Знаходить найкоротший ланцюжок знайомств між двома людьми.

    Наприклад:
        Олег знає Андрія
        Андрій знає Богдана
        Отже: Олег → Андрій → Богдан (2 ступені)
    """
    if person_a not in network or person_b not in network:
        return None, None

    if person_a == person_b:
        return 0, [person_a]

    visited = {person_a}
    queue = deque([[person_a]])

    while queue:
        path = queue.popleft()
        current = path[-1]

        for friend in network.get(current, []):
            new_path = path + [friend]

            if friend == person_b:
                return len(new_path) - 1, new_path

            if friend not in visited:
                visited.add(friend)
                queue.append(new_path)

    return -1, None  # Не зв'язані


def find_friends_of_friends(network: dict, person: str, depth: int = 2) -> dict:
    """
    Знаходить всіх людей у межах заданої кількості ступенів.
    Повертає {людина: ступінь_знайомства}
    """
    visited = {person: 0}
    queue = deque([person])

    while queue:
        current = queue.popleft()
        current_depth = visited[current]

        if current_depth >= depth:
            continue

        for friend in network.get(current, []):
            if friend not in visited:
                visited[friend] = current_depth + 1
                queue.append(friend)

    del visited[person]  # Прибираємо самого себе
    return visited


def suggest_friends(network: dict, person: str) -> list:
    """
    Пропонує нових друзів (друзі друзів, з якими ще не знайомий).
    """
    direct_friends = set(network.get(person, []))
    direct_friends.add(person)

    suggestions = {}
    for friend in network.get(person, []):
        for fof in network.get(friend, []):  # Friend Of Friend
            if fof not in direct_friends:
                suggestions[fof] = suggestions.get(fof, 0) + 1

    # Сортуємо за кількістю спільних друзів
    return sorted(suggestions.items(), key=lambda x: x[1], reverse=True)


# ──────────────────────────────────────────────
# Демонстрація
# ──────────────────────────────────────────────

if __name__ == "__main__":
    # Соціальна мережа студентів
    network = {
        "Олег":    ["Андрій", "Марія", "Іван"],
        "Андрій":  ["Олег", "Богдан", "Катерина"],
        "Марія":   ["Олег", "Богдан", "Ліна"],
        "Іван":    ["Олег", "Петро"],
        "Богдан":  ["Андрій", "Марія", "Тарас"],
        "Катерина":["Андрій"],
        "Ліна":    ["Марія", "Тарас"],
        "Петро":   ["Іван", "Тарас"],
        "Тарас":   ["Богдан", "Ліна", "Петро"],
    }

    print("=" * 55)
    print("  👥 СОЦІАЛЬНА МЕРЕЖА — аналіз зв'язків")
    print("=" * 55)

    # Ступені знайомства
    pairs = [
        ("Олег", "Тарас"),
        ("Олег", "Катерина"),
        ("Іван", "Ліна"),
    ]

    print("\n🔗 Ступені знайомства:")
    for a, b in pairs:
        degree, path = find_connection_degree(network, a, b)
        chain = " → ".join(path) if path else "немає зв'язку"
        print(f"  {a} ↔ {b}: {degree} ступені")
        print(f"    Ланцюжок: {chain}")

    # Друзі в межах 2 ступенів
    print("\n🌐 Коло знайомств Олега (до 2 ступенів):")
    circle = find_friends_of_friends(network, "Олег", depth=2)
    for person, degree in sorted(circle.items(), key=lambda x: x[1]):
        label = "Прямий друг" if degree == 1 else "Друг друга"
        print(f"  {person}: {label} ({degree}° )")

    # Рекомендації друзів
    print("\n💡 Рекомендації нових друзів для Олега:")
    suggestions = suggest_friends(network, "Олег")
    for person, mutual in suggestions[:3]:
        print(f"  {person} — {mutual} спільних друзів")
