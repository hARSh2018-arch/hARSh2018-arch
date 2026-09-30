from dataclasses import dataclass
from typing import List

@dataclass
class GraphTheme:
    name: str
    service_title: str
    brand_color: str
    levels: List[str]
    bg_color: str = "#0d1117"
    card_border: str = "#30363d"
    text_primary: str = "#e6edf3"
    text_muted: str = "#7d8590"
    cell_stroke: str = "rgba(255, 255, 255, 0.05)"
    hover_stroke: str = "#f0f6fc"
    icon_path: str = ""

# LeetCode: Warm Amber / Gold / LeetCode Orange palette
LEETCODE_THEME = GraphTheme(
    name="leetcode",
    service_title="LeetCode Contributions",
    brand_color="#ffa116",
    levels=[
        "#161b22",  # Level 0 (Empty)
        "#4a2800",  # Level 1
        "#874400",  # Level 2
        "#c76a00",  # Level 3
        "#ffa116",  # Level 4 (Peak LeetCode Orange)
    ],
    icon_path=(
        "M16.107 10.999c-.198-.002-.394.062-.55.191l-5.698 4.708a.86.86 0 0 "
        "0-.306.662c0 .252.11.492.306.662l5.698 4.708c.328.271.81.246 "
        "1.107-.058.297-.303.297-.783 0-1.087L11.532 16.56l5.132-4.238c.31-.256.347-.723.1-1.042a.846.846 "
        "0 0 0-.657-.281zm-8.214 0c-.198-.002-.394.062-.55.191L1.645 15.898a.86.86 0 0 "
        "0-.306.662c0 .252.11.492.306.662l5.698 4.708c.328.271.81.246 "
        "1.107-.058.297-.303.297-.783 0-1.087L3.318 16.56l5.132-4.238c.31-.256.347-.723.1-1.042a.846.846 "
        "0 0 0-.657-.281z"
    )
)

# HackerRank: Signature Bright HackerRank Emerald Green palette
HACKERRANK_THEME = GraphTheme(
    name="hackerrank",
    service_title="HackerRank Contributions",
    brand_color="#00ea64",
    levels=[
        "#161b22",  # Level 0 (Empty)
        "#0b381e",  # Level 1
        "#006832",  # Level 2
        "#0fa34e",  # Level 3
        "#00ea64",  # Level 4 (Vibrant HackerRank Green)
    ],
    icon_path=(
        "M8.2 2.5v19h3.6v-7.8h4.4v7.8h3.6v-19h-3.6v7.6h-4.4V2.5H8.2z"
    )
)
