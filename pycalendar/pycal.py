# coding: utf-8

import os
import codecs
import json
import calendar
from calendar import SUNDAY

import arrow
import click
from termcolor import colored, cprint
import requests

class PyCalendar(object):
    def __init__(self):
        self.holidays = {}

    def load_holidays(self, path):
        with codecs.open(path, encoding='utf-8') as f:
            self.holidays = json.load(f)

    def get_month_calendar(self, year, month, mark_today=True,
                           show_holidays=False):
        now = arrow.now()

        lines = []
        holidays = []

        cal = calendar.Calendar(firstweekday=SUNDAY)

        for week in cal.monthdatescalendar(year, month):
            line = []

            for date in week:
                color = None
                bg = None
                attrs = []

                if calendar.weekday(date.year, date.month, date.day) == SUNDAY:
                    color = 'red'

                if show_holidays and date.month == month:
                    date_key = '%d-%02d-%02d' % (date.year, date.month, date.day)
                    if date_key in self.holidays:
                        holidays.append(u'%d.%d %s' % (date.month, date.day,
                                                       self.holidays[date_key]))
                        color = 'red'

                if date.month != month:
                    attrs.append('dark')

                if mark_today:
                    if date == now.date():
                        if color:
                            bg = 'on_red'
                        else:
                            bg = 'on_white'

                        color = 'grey'

                line.append(colored(u'%2d' % date.day, color, bg, attrs))

            lines.append(u' '.join(line))

        if show_holidays:
            for idx, holiday in enumerate(holidays[:4]):
                lines[idx] += (u'  %s' % holiday)

        return '\n'.join(lines)

def get_holidays_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'holidays.json')

@click.command()
@click.option('-y', '--year', type=int,
              help='Show given year\'s calendar.')
@click.option('-m', '--month', type=int,
              help='Show given month\'s calendar.')
@click.option('-p', '--previous-month', is_flag=True,
              help='Show previous month\'s calendar.')
@click.option('-n', '--next-month', is_flag=True,
              help='Show next month\'s calendar.')
@click.option('-h', '--show-holidays', is_flag=True,
              help='Show month\'s holidays')
def main(year, month, previous_month, next_month, show_holidays):
    if (year or month) and (previous_month or next_month):
        cprint('Cannot mix --year/--month options with --previous-month/'
               '--next-month options.', 'red')
        return

    if previous_month and next_month:
        cprint('Cannot mix --previous-month option with --next-month option.',
               'red')
        return

    pycal = PyCalendar()
    holidays_file_path = get_holidays_file_path()
    if os.path.isfile(holidays_file_path):
        pycal.load_holidays(holidays_file_path)

    now = arrow.now()
    target_date = now.replace(year=year or now.year, month=month or now.month)
    if previous_month:
        target_date = target_date.replace(months=-1)
    elif next_month:
        target_date = target_date.replace(months=+1)

    print (u'%d년 %d월' % (target_date.year, target_date.month)).center(20)
    print '일 월 화 수 목 금 토'
    print pycal.get_month_calendar(target_date.year, target_date.month,
                                   show_holidays=show_holidays)

@click.command()
@click.option('-y', '--year', type=int,
              help='Fetch given year\'s holidays.')
def fetch_holidays(year):
    target_year = year or arrow.now().year

    url = 'https://apis.sktelecom.com/v1/eventday/days'
    params = {'type': 'h,i', 'year': target_year}
    headers = {'TDCProjectkey': '56fbad42-7012-4ba7-8941-6c3ec783b4ed'}
    r = requests.get(url, params=params, headers=headers)

    holidays = {}
    holidays_file_path = get_holidays_file_path()

    if os.path.isfile(holidays_file_path):
        with codecs.open(holidays_file_path, encoding='utf-8') as f:
            holidays.update(json.load(f))

    for holiday in r.json()['results']:
        year = int(holiday['year'])
        month = int(holiday['month'])
        day = int(holiday['day'])

        date_key = '%d-%02d-%02d' % (year, month, day)
        holidays[date_key] = holiday['name']

    with codecs.open(holidays_file_path, 'w', encoding='utf-8') as f:
        json.dump(holidays, f, ensure_ascii=False, indent=4, separators=(',', ': '))