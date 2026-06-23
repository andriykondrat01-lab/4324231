"""
Юніт-тести для BFS алгоритму
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bfs_python import bfs, bfs_shortest_path, bfs_distances, is_connected


# ──────────────────────────────────────────────
# Тестовий граф
# ──────────────────────────────────────────────
#
#     A ── B ── E
#     |    |
#     C ── D ── F
#

GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'D'],
    'D': ['B', 'C', 'F'],
    'E': ['B'],
    'F': ['D'],
}


class TestBFS:
    """Тести базового BFS обходу"""

    def test_visits_all_vertices(self):
        order = bfs(GRAPH, 'A')
        assert set(order) == set(GRAPH.keys()), \
            "BFS повинен відвідати всі вершини"

    def test_start_vertex_is_first(self):
        order = bfs(GRAPH, 'A')
        assert order[0] == 'A', \
            "Перша відвідана вершина — стартова"

    def test_level_order(self):
        """Вершини рівня 1 мають передувати вершинам рівня 2"""
        order = bfs(GRAPH, 'A')
        # Сусіди A (рівень 1): B, C
        # Сусіди B і C (рівень 2): D, E, F
        idx = {v: i for i, v in enumerate(order)}
        assert idx['B'] < idx['D'], "B (рівень 1) перед D (рівень 2)"
        assert idx['C'] < idx['F'], "C (рівень 1) перед F (рівень 2)"

    def test_single_vertex(self):
        single = {'X': []}
        order = bfs(single, 'X')
        assert order == ['X']

    def test_linear_graph(self):
        linear = {'A': ['B'], 'B': ['C'], 'C': []}
        order = bfs(linear, 'A')
        assert order == ['A', 'B', 'C']


class TestShortestPath:
    """Тести пошуку найкоротшого шляху"""

    def test_path_exists(self):
        path = bfs_shortest_path(GRAPH, 'A', 'F')
        assert path is not None, "Шлях A→F існує"
        assert path[0] == 'A', "Шлях починається з A"
        assert path[-1] == 'F', "Шлях закінчується на F"

    def test_shortest_path_length(self):
        path = bfs_shortest_path(GRAPH, 'A', 'F')
        assert len(path) - 1 == 3, "Найкоротший шлях A→F має 3 ребра"

    def test_same_vertex(self):
        path = bfs_shortest_path(GRAPH, 'A', 'A')
        assert path == ['A']

    def test_direct_neighbor(self):
        path = bfs_shortest_path(GRAPH, 'A', 'B')
        assert len(path) - 1 == 1, "Сусіди на відстані 1"

    def test_no_path(self):
        disconnected = {
            'A': ['B'], 'B': ['A'],
            'C': ['D'], 'D': ['C'],
        }
        path = bfs_shortest_path(disconnected, 'A', 'C')
        assert path is None, "Шлях між різними компонентами не існує"

    def test_path_is_valid(self):
        """Перевіряємо що кожне ребро в шляху існує в графі"""
        path = bfs_shortest_path(GRAPH, 'A', 'F')
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            assert v in GRAPH[u], f"Ребро {u}→{v} повинно існувати"


class TestDistances:
    """Тести обчислення відстаней"""

    def test_distance_to_self_is_zero(self):
        distances = bfs_distances(GRAPH, 'A')
        assert distances['A'] == 0

    def test_distances_from_a(self):
        distances = bfs_distances(GRAPH, 'A')
        assert distances['B'] == 1  # A-B
        assert distances['C'] == 1  # A-C
        assert distances['D'] == 2  # A-B-D або A-C-D
        assert distances['E'] == 2  # A-B-E
        assert distances['F'] == 3  # A-B-D-F або A-C-D-F

    def test_all_reachable(self):
        distances = bfs_distances(GRAPH, 'A')
        assert len(distances) == len(GRAPH), \
            "Всі вершини досяжні"


class TestConnectivity:
    """Тести перевірки зв'язності"""

    def test_connected_graph(self):
        assert is_connected(GRAPH) is True

    def test_disconnected_graph(self):
        disconnected = {
            'A': ['B'], 'B': ['A'],
            'C': ['D'], 'D': ['C'],
        }
        assert is_connected(disconnected) is False

    def test_single_vertex_connected(self):
        assert is_connected({'A': []}) is True

    def test_empty_graph(self):
        assert is_connected({}) is True


# ──────────────────────────────────────────────
# Запуск тестів без pytest
# ──────────────────────────────────────────────

if __name__ == "__main__":
    test_classes = [TestBFS, TestShortestPath, TestDistances, TestConnectivity]
    total = passed = failed = 0

    print("=" * 50)
    print("  🧪 ЗАПУСК ТЕСТІВ")
    print("=" * 50)

    for cls in test_classes:
        print(f"\n📦 {cls.__name__}:")
        instance = cls()
        for name in [m for m in dir(cls) if m.startswith('test_')]:
            total += 1
            try:
                getattr(instance, name)()
                print(f"  ✅ {name}")
                passed += 1
            except AssertionError as e:
                print(f"  ❌ {name}: {e}")
                failed += 1
            except Exception as e:
                print(f"  💥 {name}: {type(e).__name__}: {e}")
                failed += 1

    print(f"\n{'=' * 50}")
    print(f"  Результат: {passed}/{total} пройшло", end="")
    print(f" | {'✅ Всі тести пройдено!' if failed == 0 else f'❌ {failed} провалено'}")
    print("=" * 50)
