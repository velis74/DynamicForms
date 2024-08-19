import calendar
import sys

from collections import namedtuple
from datetime import date, datetime, timedelta
from enum import IntEnum
from typing import List, Optional, Set, Tuple, Union

from django.utils.translation import gettext_lazy as _
from versio.version import Version
from versio.version_scheme import Pep440VersionScheme


def locale_weekdays():
    return ["ho"] + [_(day).lower()[:2] for day in calendar.day_abbr]


def locale_adjectives():
    return (
        _("1st")[:3],
        _("first")[:3],
        _("2nd")[:3],
        _("second")[:3],
        _("3rd")[:3],
        _("third")[:3],
        _("4th")[:3],
        _("fourth")[:3],
        _("5th")[:3],
        _("fifth")[:3],
        _("last")[:3],
    )


class Pattern(IntEnum):
    """
    cutoff date if the date of the occurrence AFTER which we're modifying the recurrence. Any occurrences before
    cutoff date are left out of the generated intervals

    Daily:
      { every: int }
      - repeat every n days
    Weekly:
      { every: int, weekdays: List[str] }
      - every: repeat every n-th week
      - weekdays: list of two-character day codes for monday - sunday + holiday
      - TODO: holidays are ADDED to result set. There is currently no support to only include weekdays that
          are also holidays or to exclude weekdays that are holidays
    Monthly:
      { days: List[int|Union[weekday_modifier: Enum(first, last, second, third, fourth), weekday: str]] }
      - days is a list of days in a month when this event is recurring
      - the days can be specified as integers (e.g. 1, 15, 23) or with a modifier (e.g. first we, 3rd thu, last fr)
    Yearly:
      { dates: List[Tuple[int, int]] }
      - dates is a list of (day, month). in a year when the event occurs
    """

    Daily = 1
    Weekly = 2
    Monthly = 3
    Yearly = 4


def date_range(start_at, end_at: datetime, cutoff_at: Optional[datetime], pattern: Pattern, params: dict):
    if pattern == Pattern.Daily:
        return date_range_daily(start_at, end_at, cutoff_at, params["every"])
    if pattern == Pattern.Weekly:
        return date_range_weekly(start_at, end_at, cutoff_at, params["every"], params["weekdays"], params["holidays"])
    if pattern == Pattern.Monthly:
        return date_range_monthly(start_at, end_at, cutoff_at, params["days"])
    if pattern == Pattern.Yearly:
        return date_range_yearly(start_at, end_at, cutoff_at, params["dates"])


def date_range_daily(start_at, end_at: datetime, cutoff_at: Optional[datetime], every: int):
    """
    Returns generator with dates matching the given criteria
    :param start_at: timestamp to start with
    :param end_at: timestamp to end with (inclusive)
    :param cutoff_at: only return instances greater or equal to cutoff (modifying the interval from this point forward)
    :param every: every n days
    :return: Iterable[datetime] - iterator with timestamps where time of day is always same and dates are determined as
      per above
    """
    cutoff_at = cutoff_at or start_at
    current_result = start_at
    while current_result <= end_at:
        if current_result >= cutoff_at:
            yield current_result
        current_result += timedelta(days=every)


_ISOCldr = namedtuple("ISOCalendar", ["year", "week", "weekday"])


def ISOCalendar(tpl: tuple):
    if Version(f"{sys.version_info.major}.{sys.version_info.minor}", scheme=Pep440VersionScheme) >= Version(
        "3.9", scheme=Pep440VersionScheme
    ):
        return tpl
    return _ISOCldr(*tpl)


def date_range_weekly(
    start_at, end_at: datetime, cutoff_at: Optional[datetime], every: int, weekdays: List[str], holidays: Set[date]
):
    cutoff_at = cutoff_at or start_at
    current_result = start_at
    prev_iso_calendar = ISOCalendar(current_result.date().isocalendar())
    week_no = 0
    weekdays = set(dict(zip(locale_weekdays(), range(8)))[day] for day in map(lambda x: x[:2].lower(), weekdays))
    do_holidays = 0 in weekdays
    weekdays.discard(0)

    matching = True
    while current_result <= end_at:
        if matching and current_result >= cutoff_at:
            yield current_result  # first instance always matches
        current_result += timedelta(days=1)
        iso_calendar = ISOCalendar(current_result.date().isocalendar())
        if iso_calendar.week != prev_iso_calendar.week:
            week_no += 1
        prev_iso_calendar = iso_calendar
        # weekly schedule only matches every n weeks and on selected weekdays
        matching = week_no % every == 0 and iso_calendar.weekday in weekdays
        if do_holidays and current_result.date() in holidays:
            matching = True


def date_range_monthly(
    start_at, end_at: datetime, cutoff_at: Optional[datetime], days: List[Union[int, Tuple[str, str]]]
):
    cutoff_at = cutoff_at or start_at
    current_result = start_at

    def uniform_date(d: Union[int, Tuple[str, str]]):
        if isinstance(d, str) and len(d.split(" ")) == 2:
            d = d.split(" ")
        if isinstance(d, (tuple, list)):
            modifier = dict(zip(locale_adjectives(), map(lambda x: str(x // 2 + 1), range(11))))[d[0][:3].lower()]
            weekday = dict(zip(locale_weekdays()[1:], map(str, range(1, 8))))[d[1]]
            return modifier + weekday
        elif isinstance(d, str):
            return int(d)
        elif isinstance(d, int):
            return d

    def uniformise_date(d: date):
        # d is date
        modifier = (d.day - 1) // 7 + 1
        weekday = d.isoweekday()
        res = [f"{modifier}{weekday}"]
        next_month = (d.replace(day=1) + timedelta(days=32)).replace(day=1)
        if next_month - d < timedelta(days=8):
            res.append(f"6{weekday}")
        res.append(d.day)
        return set(res)

    days = set(map(uniform_date, days))
    while current_result <= end_at:
        if current_result >= cutoff_at and (
            uniformise_date(current_result.date()).intersection(days) or current_result == start_at
        ):
            yield current_result
        current_result += timedelta(days=1)


def date_range_yearly(start_at, end_at: datetime, cutoff_at: Optional[datetime], dates: List[Tuple[int, int]]):
    # TODO: there should also be an option to specify "wednesday of n-th ISO week"
    # TODO: what about the moon, as in easter? or holidays?
    cutoff_at = cutoff_at or start_at
    current_result = start_at
    current_year = None
    dates = [(int(d), int(m)) for d, m in dates]
    year = set()

    def build_year(yr):
        def get_date(day, month, y):
            try:
                return date(y, month, day)
            except:
                return None

        return set([val for val in map(lambda d: get_date(d[0], d[1], yr), dates) if val is not None])

    while current_result <= end_at:
        if current_result.year != current_year:
            year = build_year(current_result.year)
        if current_result >= cutoff_at and (current_result.date() in year or current_result == start_at):
            yield current_result
        current_result += timedelta(days=1)
