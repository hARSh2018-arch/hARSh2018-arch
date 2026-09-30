import datetime
from typing import Dict, Any, Optional
from .theme import GraphTheme, LEETCODE_THEME, HACKERRANK_THEME
from .layout import (
    generate_calendar_days,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    CELL_SIZE,
)

def format_count_label(count: int, unit: str = "submission") -> str:
    if count == 1:
        return f"1 {unit}"
    return f"{count:,} {unit}s"

def build_contribution_svg(
    theme: GraphTheme,
    username: str,
    display_name: str,
    daily_counts: Dict[str, int],
    total_submissions: int,
    streak: int = 0,
    total_active_days: int = 0,
    solved_count: Optional[int] = None,
    easy_solved: Optional[int] = None,
    medium_solved: Optional[int] = None,
    hard_solved: Optional[int] = None,
    badges_count: Optional[int] = None,
    rank: Optional[int] = None,
    is_valid: bool = True,
    status_message: str = "OK",
    end_date: Optional[datetime.date] = None,
    period_label: Optional[str] = None,
    unit_name: str = "submission",
) -> str:
    grid_data = generate_calendar_days(daily_counts, end_date=end_date)
    cells = grid_data["cells"]
    month_labels = grid_data["month_labels"]
    weekday_labels = grid_data["weekday_labels"]
    window_total = grid_data["window_total"]
    active_in_window = grid_data["active_days_count"]

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    updated_str = now_utc.strftime("%b %d, %Y")

    display_total = window_total if window_total > 0 else total_submissions
    period_str = period_label or "in the last year"
    sub_title = f"{format_count_label(display_total, unit_name)} {period_str}"

    stats_tokens = []
    if streak > 0:
        stats_tokens.append(f"Streak: {streak}d")
    if active_in_window > 0:
        stats_tokens.append(f"Active: {active_in_window}d")
    elif total_active_days > 0:
        stats_tokens.append(f"Active: {total_active_days}d")

    if solved_count is not None and solved_count > 0:
        if easy_solved is not None and medium_solved is not None:
            stats_tokens.append(f"Solved: {solved_count} ({easy_solved}E / {medium_solved}M)")
        else:
            stats_tokens.append(f"Solved: {solved_count:,}")

    if badges_count is not None and badges_count > 0:
        stats_tokens.append(f"Badges: {badges_count}")
    if rank is not None and rank > 0:
        stats_tokens.append(f"Rank: #{rank:,}")

    sub_stats = " · ".join(stats_tokens) if stats_tokens else "Tracked via automated sync"

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" '
        f'width="100%" height="auto" role="img" aria-label="{theme.service_title} for {username}">'
    )

    svg_parts.append(f"""  <defs>
    <style>
      .card-bg {{
        fill: {theme.bg_color};
        stroke: {theme.card_border};
        stroke-width: 1px;
        rx: 6px;
        ry: 6px;
      }}
      .brand-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        font-size: 13px;
        font-weight: 600;
        fill: {theme.text_primary};
      }}
      .user-tag {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        font-size: 11px;
        font-weight: 500;
        fill: {theme.brand_color};
      }}
      .stats-primary {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        font-size: 12px;
        font-weight: 600;
        fill: {theme.text_primary};
        text-anchor: end;
      }}
      .stats-secondary {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        font-size: 10px;
        font-weight: 400;
        fill: {theme.text_muted};
        text-anchor: end;
      }}
      .label-text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        font-size: 10px;
        font-weight: 400;
        fill: {theme.text_muted};
      }}
      .legend-text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        font-size: 10px;
        font-weight: 400;
        fill: {theme.text_muted};
      }}
      .day-cell {{
        rx: 2px;
        ry: 2px;
        stroke: {theme.cell_stroke};
        stroke-width: 1px;
        transition: stroke 0.15s ease, stroke-width 0.15s ease;
      }}
      .day-cell:hover {{
        stroke: {theme.hover_stroke};
        stroke-width: 1.5px;
        cursor: pointer;
      }}
    </style>
  </defs>""")

    # Background Card
    svg_parts.append(
        f'  <rect x="0.5" y="0.5" width="{CANVAS_WIDTH - 1}" height="{CANVAS_HEIGHT - 1}" class="card-bg"/>'
    )

    # Header section
    header_y = 26
    svg_parts.append('  <!-- Header Left -->')
    svg_parts.append(f'  <g transform="translate(18, {header_y - 12})">')

    # Brand Icon
    if theme.icon_path:
        svg_parts.append(
            f'    <svg width="18" height="18" viewBox="0 0 24 24" fill="{theme.brand_color}">'
            f'<path d="{theme.icon_path}"/></svg>'
        )
    svg_parts.append(f'    <text x="24" y="10" class="brand-title">{theme.service_title}</text>')
    svg_parts.append(f'    <text x="24" y="22" class="user-tag">@{username}</text>')
    svg_parts.append('  </g>')

    # Header Right
    svg_parts.append('  <!-- Header Right -->')
    svg_parts.append(f'  <g transform="translate({CANVAS_WIDTH - 18}, {header_y - 2})">')
    svg_parts.append(f'    <text x="0" y="0" class="stats-primary">{sub_title}</text>')
    svg_parts.append(f'    <text x="0" y="13" class="stats-secondary">{sub_stats}</text>')
    svg_parts.append('  </g>')

    # Month Labels
    svg_parts.append('  <!-- Month Labels -->')
    svg_parts.append('  <g class="label-text">')
    for m in month_labels:
        svg_parts.append(f'    <text x="{m["x"]}" y="{m["y"]}">{m["text"]}</text>')
    svg_parts.append('  </g>')

    # Weekday Labels
    svg_parts.append('  <!-- Weekday Labels -->')
    svg_parts.append('  <g class="label-text" text-anchor="end">')
    for w in weekday_labels:
        svg_parts.append(f'    <text x="{w["x"]}" y="{w["y"]}">{w["text"]}</text>')
    svg_parts.append('  </g>')

    # Contribution Cells
    svg_parts.append('  <!-- Contribution Cells -->')
    svg_parts.append('  <g>')
    for cell in cells:
        if cell["is_future"]:
            continue

        c_fill = theme.levels[cell["level"]]
        c_count = cell["count"]
        c_date = cell["formatted_date"]

        if c_count == 0:
            tooltip = f"No {unit_name}s on {c_date}"
        elif c_count == 1:
            tooltip = f"1 {unit_name} on {c_date}"
        else:
            tooltip = f"{c_count} {unit_name}s on {c_date}"

        svg_parts.append(
            f'    <rect x="{cell["x"]}" y="{cell["y"]}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
            f'fill="{c_fill}" class="day-cell" data-date="{cell["date_str"]}" data-count="{c_count}">'
            f'<title>{tooltip}</title></rect>'
        )
    svg_parts.append('  </g>')

    # Footer Section
    footer_y = CANVAS_HEIGHT - 14
    svg_parts.append('  <!-- Footer Left: Sync Status -->')
    svg_parts.append(f'  <g transform="translate(18, {footer_y})">')
    status_dot_color = theme.brand_color if is_valid else "#f85149"
    svg_parts.append(f'    <circle cx="4" cy="-4" r="3" fill="{status_dot_color}"/>')
    status_label = f"Daily sync · {updated_str}" if is_valid else f"Status: {status_message}"
    svg_parts.append(f'    <text x="12" y="0" class="legend-text">{status_label}</text>')
    svg_parts.append('  </g>')

    # Footer Right: Legend
    legend_step = 13
    legend_total_width = 30 + (5 * legend_step) + 30
    legend_start_x = CANVAS_WIDTH - 18 - legend_total_width

    svg_parts.append('  <!-- Footer Right: Legend -->')
    svg_parts.append(f'  <g transform="translate({legend_start_x}, {footer_y})">')
    svg_parts.append('    <text x="0" y="0" class="legend-text">Less</text>')

    cur_x = 28
    for lvl, lvl_color in enumerate(theme.levels):
        svg_parts.append(
            f'    <rect x="{cur_x}" y="-8" width="{CELL_SIZE}" height="{CELL_SIZE}" '
            f'fill="{lvl_color}" class="day-cell">'
            f'<title>Level {lvl}</title></rect>'
        )
        cur_x += legend_step

    svg_parts.append(f'    <text x="{cur_x + 5}" y="0" class="legend-text">More</text>')
    svg_parts.append('  </g>')

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)
