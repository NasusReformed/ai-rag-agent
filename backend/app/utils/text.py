from typing import Iterable


def format_context(sources: list[dict], memory: Iterable[dict]) -> str:
    memory_lines = [f"{item['role']}: {item['content']}" for item in memory]
    source_lines = [
        f"[score={source['score']:.3f}] {source['content']}"
        for source in sources
    ]
    return "\n".join(["Memory:"] + memory_lines + ["", "Sources:"] + source_lines)
