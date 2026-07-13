import datetime as dt

_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class TimeWindow:
    def __init__(
        self, start: dt.datetime, end: dt.datetime, date_format: str = _DATE_FORMAT
    ):
        self.start = start
        self.end = end
        self.date_format = date_format

    def hourly_windows(self):
        cursor = self.start
        one_hour = dt.timedelta(hours=1)
        while cursor < self.end:
            window_end = min(cursor + one_hour - dt.timedelta(seconds=1), self.end)
            yield (
                cursor.strftime(self.date_format),
                window_end.strftime(self.date_format),
            )
            cursor += one_hour

    def daily_windows(self):
        cursor = self.start
        one_day = dt.timedelta(days=1)
        while cursor < self.end:
            window_end = min(cursor + one_day - dt.timedelta(seconds=1), self.end)
            yield (
                cursor.strftime(self.date_format),
                window_end.strftime(self.date_format),
            )
            cursor += one_day

    def weekly_windows(self):
        cursor = self.start
        one_week = dt.timedelta(weeks=1)
        while cursor < self.end:
            window_end = min(cursor + one_week - dt.timedelta(seconds=1), self.end)
            yield (
                cursor.strftime(self.date_format),
                window_end.strftime(self.date_format),
            )
            cursor += one_week

    def monthly_windows(self):
        cursor = self.start
        while cursor < self.end:
            next_year = cursor.year + cursor.month // 12
            next_month = cursor.month % 12 + 1
            window_start_of_next = cursor.replace(
                year=next_year,
                month=next_month,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
            window_end = min(window_start_of_next - dt.timedelta(seconds=1), self.end)
            yield (
                cursor.strftime(self.date_format),
                window_end.strftime(self.date_format),
            )
            cursor = window_start_of_next

    def time_windows(self):
        return {
            "hour": sum(1 for _ in self.hourly_windows()),
            "day": sum(1 for _ in self.daily_windows()),
            "week": sum(1 for _ in self.weekly_windows()),
            "month": sum(1 for _ in self.monthly_windows()),
        }
