"""
Приклад: Симуляція веб-краулера
================================
Показує як Google обходить сторінки сайту за допомогою BFS.
Починаємо з головної сторінки і відвідуємо всі доступні сторінки.
"""

from collections import deque


# Симуляція структури сайту (сторінка -> список посилань)
WEBSITE = {
    "https://example.com/": [
        "https://example.com/about",
        "https://example.com/products",
        "https://example.com/blog",
    ],
    "https://example.com/about": [
        "https://example.com/",
        "https://example.com/team",
        "https://example.com/contacts",
    ],
    "https://example.com/products": [
        "https://example.com/",
        "https://example.com/products/laptops",
        "https://example.com/products/phones",
    ],
    "https://example.com/blog": [
        "https://example.com/",
        "https://example.com/blog/post-1",
        "https://example.com/blog/post-2",
    ],
    "https://example.com/team": [
        "https://example.com/about",
    ],
    "https://example.com/contacts": [
        "https://example.com/about",
    ],
    "https://example.com/products/laptops": [
        "https://example.com/products",
    ],
    "https://example.com/products/phones": [
        "https://example.com/products",
    ],
    "https://example.com/blog/post-1": [
        "https://example.com/blog",
        "https://example.com/blog/post-2",
    ],
    "https://example.com/blog/post-2": [
        "https://example.com/blog",
        "https://example.com/blog/post-1",
    ],
}


def crawl_website(start_url: str, max_depth: int = 3) -> dict:
    """
    Симуляція веб-краулера — обходить всі сторінки сайту через BFS.

    Args:
        start_url: початкова URL-адреса (головна сторінка)
        max_depth: максимальна глибина обходу

    Returns:
        Словник {url: глибина} для всіх знайдених сторінок
    """
    visited = {start_url: 0}
    queue = deque([(start_url, 0)])
    crawl_order = []

    print(f"🕷️  Починаємо сканування з: {start_url}")
    print(f"   Максимальна глибина: {max_depth}\n")

    while queue:
        url, depth = queue.popleft()
        crawl_order.append((url, depth))

        indent = "  " * depth
        print(f"{indent}[Рівень {depth}] {url}")

        if depth >= max_depth:
            continue

        # Отримуємо посилання зі сторінки (в реальності — HTTP запит + парсинг)
        links = WEBSITE.get(url, [])

        for link in links:
            if link not in visited:
                visited[link] = depth + 1
                queue.append((link, depth + 1))

    return visited


def build_sitemap(start_url: str) -> dict:
    """
    Будує карту сайту — структуру всіх сторінок і посилань.
    """
    visited = set()
    queue = deque([start_url])
    sitemap = {}

    while queue:
        url = queue.popleft()
        if url in visited:
            continue

        visited.add(url)
        links = WEBSITE.get(url, [])
        sitemap[url] = links

        for link in links:
            if link not in visited:
                queue.append(link)

    return sitemap


# ──────────────────────────────────────────────
# Демонстрація
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  🌐 ВЕБ-КРАУЛЕР — симуляція обходу сайту")
    print("=" * 55)
    print()

    start = "https://example.com/"
    discovered = crawl_website(start, max_depth=2)

    print(f"\n📊 Результат:")
    print(f"  Знайдено сторінок: {len(discovered)}")

    by_depth = {}
    for url, depth in discovered.items():
        by_depth.setdefault(depth, []).append(url)

    print("\n📑 Сторінки за рівнями:")
    for depth in sorted(by_depth.keys()):
        print(f"\n  Рівень {depth} ({len(by_depth[depth])} сторінок):")
        for url in by_depth[depth]:
            short = url.replace("https://example.com", "")
            print(f"    • {short or '/'}")

    print("\n" + "=" * 55)
    print("  💡 Саме так Google сканує мільярди сторінок!")
    print("=" * 55)
