from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo, available_timezones

TZLikeType = str | ZoneInfo


class TzConverter:
    """Converts datetimes and date strings between a local timezone and UTC."""

    _default_tz = ZoneInfo("Asia/Jakarta")
    _datetime_formats = ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S")
    _local_tz = None

    def __init__(self, local_tz: TZLikeType = _default_tz) -> None:
        """Store the default local timezone used when a call doesn't override it."""
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

    def to_local_tz(self, dt: datetime, local_tz: TZLikeType | None = None) -> datetime:
        """Convert dt (naive datetimes are assumed UTC) to the local timezone."""
        dt = self._ensure_datetime(dt)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(
            self._coerce_tz(local_tz) if local_tz is not None else self._local_tz
        )

    def to_utc_tz(self, dt: datetime, local_tz: TZLikeType | None = None) -> datetime:
        """Convert dt (naive datetimes are assumed local) to UTC."""
        dt = self._ensure_datetime(dt)

        if dt.tzinfo is None:
            dt = dt.replace(
                tzinfo=self._coerce_tz(local_tz)
                if local_tz is not None
                else self._local_tz
            )
        return dt.astimezone(UTC)

    def now_local_tz(self, local_tz: TZLikeType | None = None) -> datetime:
        """Return the current time in the local timezone."""
        return datetime.now(
            self._coerce_tz(local_tz) if local_tz is not None else self._local_tz
        )

    def now_utc_tz(self) -> datetime:
        """Return the current time in UTC."""
        return datetime.now(UTC)

    def parse_str_to_utc_tz(
        self, value: str, local_tz: TZLikeType | None = None
    ) -> datetime:
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

        return self.to_utc_tz(dt, local_tz)

    def list_timezone(self) -> list[str]:
        """Return all available timezone names, sorted alphabetically."""
        timezones = available_timezones()

        return sorted(timezones)
