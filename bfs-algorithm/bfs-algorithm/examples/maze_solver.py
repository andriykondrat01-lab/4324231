"""
Приклад: Розв'язання лабіринту за допомогою BFS
=================================================
BFS гарантує НАЙКОРОТШИЙ шлях від входу до виходу.

Символи лабіринту:
  '#' — стіна
  ' ' — прохід
  'S' — старт
  'E' — вихід
  '.' — шлях (виводиться після вирішення)
"""

from collections import deque


def solve_maze(maze: list[str]) -> tuple[list, int] | tuple[None, None]:
    """
    Знаходить найкоротший шлях через лабіринт.

    Args:
        maze: список рядків, де кожен рядок — ряд лабіринту

    Returns:
        (список координат шляху, довжина) або (None, None)
    """
    rows = len(maze)
    cols = len(maze[0])

    # Знаходимо позиції старту і виходу
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)

    if not start or not end:
        raise ValueError("Лабіринт повинен мати 'S' (старт) і 'E' (вихід)")

    # BFS
    visited = {start}
    queue = deque([[start]])

    # Чотири напрямки: вгору, вниз, вліво, вправо
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        path = queue.popleft()
        r, c = path[-1]

        if (r, c) == end:
            return path, len(path) - 1

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Перевіряємо межі та прохідність
            if (0 <= nr < rows and
                0 <= nc < cols and
                (nr, nc) not in visited and
                    maze[nr][nc] != '#'):
                visited.add((nr, nc))
                queue.append(path + [(nr, nc)])

    return None, None  # Виходу немає


def visualize_solution(maze: list[str], path: list) -> list[str]:
    """Малює вирішений лабіринт з позначеним шляхом."""
    maze_copy = [list(row) for row in maze]

    for r, c in path:
        if maze_copy[r][c] not in ('S', 'E'):
            maze_copy[r][c] = '·'

    return [''.join(row) for row in maze_copy]


# ──────────────────────────────────────────────
# Демонстрація
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  🏃 РОЗВ'ЯЗАННЯ ЛАБІРИНТУ через BFS")
    print("=" * 50)

    # Лабіринт 1: простий
    maze1 = [
        "##########",
        "#S       #",
        "# ##### ##",
        "# #   # ##",
        "# # # #  #",
        "#   # # ##",
        "##### #  #",
        "#     ## #",
        "# ##   # #",
        "#    # #E#",
        "##########",
    ]

    print("\n📍 Лабіринт (до вирішення):")
    for row in maze1:
        print(" ", row)

    path, steps = solve_maze(maze1)

    if path:
        solved = visualize_solution(maze1, path)
        print(f"\n✅ Шлях знайдено! Кроків: {steps}")
        print("\n📍 Вирішений лабіринт (· = шлях):")
        for row in solved:
            print(" ", row)
    else:
        print("\n❌ Шлях не існує!")

    print()

    # Лабіринт 2: кілька варіантів шляху (BFS знайде найкоротший)
    maze2 = [
        "#######",
        "#S    #",
        "### # #",
        "#   # #",
        "# ### #",
        "#     E",
        "#######",
    ]

    print("📍 Лабіринт 2 (BFS знаходить найкоротший шлях):")
    for row in maze2:
        print(" ", row)

    path2, steps2 = solve_maze(maze2)
    if path2:
        solved2 = visualize_solution(maze2, path2)
        print(f"\n✅ Найкоротший шлях: {steps2} кроків")
        for row in solved2:
            print(" ", row)

    print("\n" + "=" * 50)
