from __future__ import annotations

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
