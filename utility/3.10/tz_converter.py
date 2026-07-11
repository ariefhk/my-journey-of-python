from __future__ import annotations

import re
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo, available_timezones

TZLikeType = str | ZoneInfo


class TzConverter:
    """Converts datetimes and date strings between a local timezone and UTC."""

    _time_re = re.compile(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$")
    _default_tz = ZoneInfo("Asia/Jakarta")
    _datetime_formats = ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S")
    _local_tz: ZoneInfo

    def __init__(self, local_tz: TZLikeType = _default_tz) -> None:
        """Store the local timezone used by every conversion on this instance."""
        self._local_tz = self._coerce_tz(local_tz)

    @classmethod
    def _coerce_tz(cls, tz: TZLikeType) -> ZoneInfo:
        """Coerce a timezone name or ZoneInfo into a ZoneInfo instance."""
        if isinstance(tz, ZoneInfo):
            return tz
        return ZoneInfo(tz)

    @classmethod
    def _ensure_datetime(cls, dt: datetime) -> datetime:
        """Raise TypeError if dt is not a datetime instance."""
        if not isinstance(dt, datetime):
            raise TypeError(f"expected datetime, got {type(dt).__name__}")
        return dt

    @classmethod
    def _parse_wall_time(cls, time_str: str) -> time:
        """Parse 'HH:MM' or 'HH:MM:SS' with validation and clear errors.

        Seconds are optional (default 0) and validated to 0..59.
        """
        m = cls._time_re.match(time_str.strip())
        if not m:
            raise ValueError(f"invalid time string {time_str!r}, expected 'HH:MM'")
        hour, minute, second = int(m[1]), int(m[2]), int(m[3] or 0)
        try:
            return time(hour, minute, second)
        except ValueError as e:
            raise ValueError(f"invalid time string {time_str!r}: {e}") from None

    def to_local_tz(self, dt: datetime) -> datetime:
        """Convert dt (naive datetimes are assumed UTC) to the local timezone."""
        dt = self._ensure_datetime(dt)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(self._local_tz)

    def to_utc_tz(self, dt: datetime) -> datetime:
        """Convert dt (naive datetimes are assumed local) to UTC."""
        dt = self._ensure_datetime(dt)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=self._local_tz)
        return dt.astimezone(UTC)

    def now_local_tz(self) -> datetime:
        """Return the current time in the local timezone."""
        return datetime.now(self._local_tz)

    def now_utc_tz(self) -> datetime:
        """Return the current time in UTC."""
        return datetime.now(UTC)

    def parse_str_to_utc_tz(self, value: str) -> datetime:
        """Parse a 'YYYY-MM-DD HH:MM:SS' or 'YYYY/MM/DD HH:MM:SS' string in the local timezone and convert it to UTC."""
        for fmt in self._datetime_formats:
            try:
                dt = datetime.strptime(value, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError(
                f"expected format 'YYYY-MM-DD HH:MM:SS' or 'YYYY/MM/DD HH:MM:SS', got {value!r}"
            )

        return self.to_utc_tz(dt)

    def list_timezone(self) -> list[str]:
        """Return all available timezone names, sorted alphabetically."""
        timezones = available_timezones()

        return sorted(timezones)

    def shift_boundary_to_utc(
        self,
        business_date: date | datetime,
        time_str: str,
        day_offset: int,
    ) -> datetime:
        """
        Example — morning shift, business_date=2026-06-06, local tz "Asia/Jakarta" (UTC+7):
            open_time="15:00", open_day_offset=-1
            local date + offset  : 2026-06-05
            local datetime       : 2026-06-05 15:00:00+07:00
            returned (UTC)       : 2026-06-05 08:00:00+00:00
        """
        zone = self._local_tz

        if isinstance(business_date, datetime):
            if business_date.tzinfo is None:
                raise ValueError(
                    "business_date datetime must be timezone-aware; "
                    "pass a plain date if you only have a calendar date"
                )
            # Recover the calendar date in the pool's local timezone. Taking
            # .date() directly in UTC is off by one day for UTC+ zones when
            # the input is local midnight expressed in UTC (e.g. Jakarta
            # local midnight 2026-06-06 == 2026-06-05T17:00Z).
            local_date = business_date.astimezone(zone).date()
        else:
            local_date = business_date

        local_date += timedelta(days=day_offset)
        local_dt = datetime.combine(
            local_date, self._parse_wall_time(time_str), tzinfo=zone
        )
        return local_dt.astimezone(UTC)
