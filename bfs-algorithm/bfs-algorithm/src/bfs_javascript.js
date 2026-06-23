/**
 * Пошук у ширину (Breadth-First Search) — реалізація на JavaScript
 * =================================================================
 */

// ──────────────────────────────────────────────
// 1. Базовий BFS — обхід графу
// ──────────────────────────────────────────────

function bfs(graph, start) {
  /**
   * Базовий обхід графу в ширину.
   * @param {Object} graph - граф у вигляді списку суміжності
   * @param {string} start - початкова вершина
   * @returns {string[]} - порядок відвідування вершин
   */
  const visited = new Set([start]);
  const queue = [start];
  const order = [];

  while (queue.length > 0) {
    const vertex = queue.shift(); // Беремо з початку черги
    order.push(vertex);
    console.log(`  Відвідуємо: ${vertex}`);

    for (const neighbor of graph[vertex]) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor); // Додаємо в кінець черги
      }
    }
  }

  return order;
}


// ──────────────────────────────────────────────
// 2. BFS з пошуком найкоротшого шляху
// ──────────────────────────────────────────────

function bfsShortestPath(graph, start, end) {
  /**
   * Пошук найкоротшого шляху між двома вершинами.
   * @returns {string[]|null} - масив вершин шляху або null
   */
  if (start === end) return [start];

  const visited = new Set([start]);
  const queue = [[start]]; // Зберігаємо ШЛЯХИ

  while (queue.length > 0) {
    const path = queue.shift();
    const vertex = path[path.length - 1]; // Остання вершина в шляху

    for (const neighbor of graph[vertex]) {
      const newPath = [...path, neighbor];

      if (neighbor === end) {
        return newPath; // Знайшли найкоротший шлях!
      }

      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(newPath);
      }
    }
  }

  return null; // Шлях не існує
}


// ──────────────────────────────────────────────
// 3. BFS з відстанями
// ──────────────────────────────────────────────

function bfsDistances(graph, start) {
  /**
   * Обчислює мінімальну відстань від start до всіх інших вершин.
   * @returns {Object} - {вершина: відстань}
   */
  const distances = { [start]: 0 };
  const queue = [start];

  while (queue.length > 0) {
    const vertex = queue.shift();

    for (const neighbor of graph[vertex]) {
      if (!(neighbor in distances)) {
        distances[neighbor] = distances[vertex] + 1;
        queue.push(neighbor);
      }
    }
  }

  return distances;
}


// ──────────────────────────────────────────────
// 4. Перевірка чи граф зв'язний
// ──────────────────────────────────────────────

function isConnected(graph) {
  const vertices = Object.keys(graph);
  if (vertices.length === 0) return true;

  const visited = new Set([vertices[0]]);
  const queue = [vertices[0]];

  while (queue.length > 0) {
    const vertex = queue.shift();
    for (const neighbor of graph[vertex]) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor);
      }
    }
  }

  return visited.size === vertices.length;
}


// ──────────────────────────────────────────────
// Демонстрація
// ──────────────────────────────────────────────

const graph = {
  A: ["B", "C"],
  B: ["A", "D", "E"],
  C: ["A", "D"],
  D: ["B", "C", "F"],
  E: ["B"],
  F: ["D"],
};

console.log("=".repeat(50));
console.log("  ДЕМОНСТРАЦІЯ BFS");
console.log("=".repeat(50));

// 1. Базовий обхід
console.log("\n🔍 1. Обхід графу з вершини 'A':");
const order = bfs(graph, "A");
console.log(`  Порядок: ${order.join(" → ")}`);

// 2. Найкоротший шлях
console.log("\n🗺️  2. Найкоротший шлях A → F:");
const path = bfsShortestPath(graph, "A", "F");
console.log(`  Шлях: ${path.join(" → ")}`);
console.log(`  Довжина: ${path.length - 1} ребер`);

// 3. Відстані
console.log("\n📏 3. Відстані від вершини 'A':");
const distances = bfsDistances(graph, "A");
Object.entries(distances)
  .sort()
  .forEach(([v, d]) => console.log(`  A → ${v}: ${d} крок(ів)`));

// 4. Зв'язність
console.log(`\n🔗 4. Граф зв'язний: ${isConnected(graph)}`);

console.log("\n" + "=".repeat(50));

module.exports = { bfs, bfsShortestPath, bfsDistances, isConnected };
