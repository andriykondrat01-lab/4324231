"""
Пошук у ширину (Breadth-First Search) — реалізація на Python
=============================================================
Автор: навчальний матеріал
"""

from collections import deque


# ──────────────────────────────────────────────
# 1. Базовий BFS — обхід графу
# ──────────────────────────────────────────────

def bfs(graph: dict, start: str) -> list:
    """
    Базовий обхід графу в ширину.

    Args:
        graph: словник суміжності {вершина: [сусіди]}
        start: початкова вершина

    Returns:
        Список вершин у порядку відвідування
    """
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []

    while queue:
        vertex = queue.popleft()       # Беремо з початку черги
        order.append(vertex)
        print(f"  Відвідуємо: {vertex}")

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)   # Додаємо в кінець черги

    return order


# ──────────────────────────────────────────────
# 2. BFS з пошуком найкоротшого шляху
# ──────────────────────────────────────────────

def bfs_shortest_path(graph: dict, start: str, end: str) -> list | None:
    """
    Пошук найкоротшого шляху між двома вершинами.

    Args:
        graph: словник суміжності
        start: початкова вершина
        end:   кінцева вершина

    Returns:
        Список вершин що утворюють найкоротший шлях,
        або None якщо шлях не існує
    """
    if start == end:
        return [start]

    visited = {start}
    queue = deque([[start]])   # Зберігаємо ШЛЯХИ, а не просто вершини

    while queue:
        path = queue.popleft()
        vertex = path[-1]      # Остання вершина в поточному шляху

        for neighbor in graph[vertex]:
            new_path = path + [neighbor]

            if neighbor == end:
                return new_path         # Знайшли! Перший знайдений = найкоротший

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(new_path)

    return None  # Шлях не існує


# ──────────────────────────────────────────────
# 3. BFS з відстанями від початкової вершини
# ──────────────────────────────────────────────

def bfs_distances(graph: dict, start: str) -> dict:
    """
    Обчислення мінімальних відстаней від start до всіх вершин.

    Returns:
        Словник {вершина: відстань}
    """
    distances = {start: 0}
    queue = deque([start])

    while queue:
        vertex = queue.popleft()

        for neighbor in graph[vertex]:
            if neighbor not in distances:
                distances[neighbor] = distances[vertex] + 1
                queue.append(neighbor)

    return distances


# ──────────────────────────────────────────────
# 4. Перевірка чи граф зв'язний
# ──────────────────────────────────────────────

def is_connected(graph: dict) -> bool:
    """
    Перевіряє чи можна дістатися від будь-якої вершини до будь-якої іншої.
    """
    if not graph:
        return True

    start = next(iter(graph))
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) == len(graph)


# ──────────────────────────────────────────────
# Демонстрація
# ──────────────────────────────────────────────

if __name__ == "__main__":
    # Приклад графу:
    #
    #     A ── B ── E
    #     |    |
    #     C ── D ── F
    #
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'D'],
        'D': ['B', 'C', 'F'],
        'E': ['B'],
        'F': ['D'],
    }

    print("=" * 50)
    print("  ДЕМОНСТРАЦІЯ BFS")
    print("=" * 50)

    # 1. Базовий обхід
    print("\n🔍 1. Обхід графу з вершини 'A':")
    order = bfs(graph, 'A')
    print(f"  Порядок: {' → '.join(order)}")

    # 2. Найкоротший шлях
    print("\n🗺️  2. Найкоротший шлях A → F:")
    path = bfs_shortest_path(graph, 'A', 'F')
    print(f"  Шлях: {' → '.join(path)}")
    print(f"  Довжина: {len(path) - 1} ребер")

    # 3. Відстані
    print("\n📏 3. Відстані від вершини 'A':")
    distances = bfs_distances(graph, 'A')
    for vertex, dist in sorted(distances.items()):
        print(f"  A → {vertex}: {dist} крок(ів)")

    # 4. Зв'язність
    print(f"\n🔗 4. Граф зв'язний: {is_connected(graph)}")

    # 5. Незв'язний граф
    disconnected = {
        'A': ['B'],
        'B': ['A'],
        'C': ['D'],
        'D': ['C'],
    }
    print(f"   Незв'язний граф: {is_connected(disconnected)}")

    print("\n" + "=" * 50)
