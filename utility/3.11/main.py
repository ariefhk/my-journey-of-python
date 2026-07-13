from __future__ import annotations

from datetime import date, datetime

from time_window import TimeWindow
from tz_converter import TzConverter

if __name__ == "__main__":
    converter = TzConverter()  # defaults to Asia/Jakarta

    now_local = converter.now_local_tz()
    now_utc = converter.now_utc_tz()
    print(f"now_local_tz(): {now_local}")
    print(f"now_utc_tz():   {now_utc}")

    parsed_utc = converter.parse_str_to_utc_tz("2026-07-11 15:00:00")
    print(f"parse_str_to_utc_tz('2026-07-11 15:00:00'): {parsed_utc}")

    back_to_local = converter.to_local_tz(parsed_utc)
    print(f"to_local_tz(parsed_utc): {back_to_local}")

    ny_converter = TzConverter("America/New_York")
    parsed_ny = ny_converter.parse_str_to_utc_tz("2026/07/11 08:00:00")
    print(
        f"parse_str_to_utc_tz('2026/07/11 08:00:00') for America/New_York: {parsed_ny}"
    )

    timezones = converter.list_timezone()
    print(f"list_timezone(): {len(timezones)} timezones, e.g. {timezones[:5]}")

    shift_open = converter.shift_boundary_to_utc(date(2026, 6, 6), "15:00", -1)
    print(f"shift_boundary_to_utc(2026-06-06, '15:00', -1): {shift_open}")

    start = datetime(2026, 1, 15, 10, 0, 0)
    end = datetime(2026, 1, 22, 10, 0, 0)
    tw = TimeWindow(start, end)
    print("HOURLY:", list(tw.hourly_windows())[:3])
    print("DAILY:", list(tw.daily_windows())[:3])
    print("WEEKLY:", list(tw.weekly_windows())[:3])
    print("MONTHLY:", list(tw.monthly_windows()))
    print("TIME WINDOW:", tw.time_windows())
