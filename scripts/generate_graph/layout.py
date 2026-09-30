import datetime
from typing import Dict, List, Tuple, Optional

GRID_COLS = 53
GRID_ROWS = 7
CELL_SIZE = 10
CELL_GAP = 3
STEP = CELL_SIZE + CELL_GAP  # 13px

START_X = 44
START_Y = 52

CANVAS_WIDTH = 760
CANVAS_HEIGHT = 185

def compute_thresholds(non_zero_counts: List[int]) -> Tuple[int, int, int]:
    if not non_zero_counts:
        return (1, 2, 3)

    sorted_counts = sorted(non_zero_counts)
    n = len(sorted_counts)
    max_val = sorted_counts[-1]

    if max_val <= 4:
        return (1, 2, 3)

    q1 = max(1, sorted_counts[int(n * 0.25)])
    q2 = max(q1 + 1, sorted_counts[int(n * 0.50)])
    q3 = max(q2 + 1, sorted_counts[int(n * 0.75)])

    if q2 <= q1:
        q2 = q1 + 1
    if q3 <= q2:
        q3 = q2 + 1

    return (q1, q2, q3)

def get_level(count: int, thresholds: Tuple[int, int, int]) -> int:
    if count <= 0:
        return 0
    q1, q2, q3 = thresholds
    if count <= q1:
        return 1
    elif count <= q2:
        return 2
    elif count <= q3:
        return 3
    else:
        return 4

def generate_calendar_days(
    daily_counts: Dict[str, int],
    end_date: Optional[datetime.date] = None
):
    now_utc = datetime.datetime.now(datetime.timezone.utc).date()
    if end_date is None:
        end_date = now_utc

    today_dow = (end_date.weekday() + 1) % 7

    last_saturday = end_date + datetime.timedelta(days=(6 - today_dow))
    start_sunday = last_saturday - datetime.timedelta(days=(GRID_COLS * GRID_ROWS - 1))

    non_zero = []
    window_total = 0
    for i in range(GRID_COLS * GRID_ROWS):
        d = start_sunday + datetime.timedelta(days=i)
        if d <= end_date:
            c = daily_counts.get(d.strftime("%Y-%m-%d"), 0)
            if c > 0:
                non_zero.append(c)
                window_total += c

    thresholds = compute_thresholds(non_zero)

    cells = []
    month_labels = []

    # Map month labels matching GitHub's calendar columns exactly
    for col in range(GRID_COLS):
        sunday_of_week = start_sunday + datetime.timedelta(days=col * 7)
        month_label_for_col = None
        if col == 0:
            for day_off in range(7):
                cur_d = sunday_of_week + datetime.timedelta(days=day_off)
                if cur_d.day == 1:
                    month_label_for_col = cur_d.strftime("%b")
                    break
            if not month_label_for_col:
                month_label_for_col = sunday_of_week.strftime("%b")
        else:
            for day_off in range(7):
                cur_d = sunday_of_week + datetime.timedelta(days=day_off)
                if cur_d.day == 1 and cur_d <= end_date:
                    month_label_for_col = cur_d.strftime("%b")
                    break

        if month_label_for_col and col < GRID_COLS - 1:
            month_labels.append({
                "text": month_label_for_col,
                "x": START_X + col * STEP,
                "y": START_Y - 7,
            })

    for i in range(GRID_COLS * GRID_ROWS):
        d = start_sunday + datetime.timedelta(days=i)
        col = i // GRID_ROWS
        row = (d.weekday() + 1) % 7
        x = START_X + col * STEP
        y = START_Y + row * STEP

        date_str = d.strftime("%Y-%m-%d")
        formatted_date = d.strftime("%b %d, %Y")
        is_future = d > end_date
        count = 0 if is_future else daily_counts.get(date_str, 0)
        level = 0 if is_future else get_level(count, thresholds)

        cells.append({
            "col": col,
            "row": row,
            "x": x,
            "y": y,
            "date_str": date_str,
            "formatted_date": formatted_date,
            "count": count,
            "level": level,
            "is_future": is_future,
        })

    weekday_labels = [
        {"text": "Mon", "x": START_X - 8, "y": START_Y + 1 * STEP + 8},
        {"text": "Wed", "x": START_X - 8, "y": START_Y + 3 * STEP + 8},
        {"text": "Fri", "x": START_X - 8, "y": START_Y + 5 * STEP + 8},
    ]

    return {
        "cells": cells,
        "month_labels": month_labels,
        "weekday_labels": weekday_labels,
        "thresholds": thresholds,
        "window_total": window_total,
        "active_days_count": len(non_zero),
        "start_date": start_sunday,
        "end_date": end_date,
    }
