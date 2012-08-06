# -*- coding: utf-8 -*-
from __future__ import print_function
import csv
import time
import datetime
import textwrap
import unicodedata


ROOM_IDX_MAP = {
    'Room 230': 1,
    'Room 433': 2,
    'Room 351a': 3,
    'Room 357': 4,
    'Room 452': 5,
    'Room 358': 6
}


def str2datetime(s):
    "convert %m/%d/%Y HH:MM:SS -> datetime object"
    return datetime.datetime(*time.strptime(s, '%m/%d/%Y %H:%M:%S')[:6])


class attrmapper(object):

    def __init__(self, target_object, keyvalues, filters={}):
        self._target_object = target_object
        self._keyvalues = keyvalues
        self._filters = filters

    def __getattr__(self, name):
        if name in self._keyvalues:
            value = self._target_object[self._keyvalues[name]]
            filter = self._filters.get(name, str)
            return filter(value)
        return super(attrmapper, self).__getattr__(name)


class TimeTableRows(object):

    COL_IDX_KEYS = {
        'start': "開始時刻",
        'end': "終了時刻",
        'track': "トラック",
        'room': "場所",
        'title_ja': "講演タイトル / Talk title",
        'title_en': "英語タイトル",
        'title_sphinx': "タイトルSphinx埋込",
        'lang': "講演言語 / Language of talk",
        'speaker': '掲載名 (英語の実氏名)',
        'abstract': '講演内容 / Abstract',
        'outline': '概要 / Outline',
        'language': '講演言語 / Language of talk',
        'type': '種別',
        'audience': '対象者 / Intended audience',
    }

    FILTERS = {
        'start': str2datetime,
        'end': str2datetime,
    }


    def __init__(self, rows):
        self._rows = list(rows)
        self.header = self._rows[0]
        self.col_idx_map = {}

        # 入力データの列名とindex値の対応付け
        for k, v in self.COL_IDX_KEYS.iteritems():
            self.col_idx_map[k] = self.header.index(v)

    def __iter__(self):
        return (attrmapper(x, self.col_idx_map, self.FILTERS) for x in self._rows[1:])


def make_timetables(rows, timetable1_filename, timetable2_filename):
    session_terms = [
        {'start': datetime.datetime(2012, 9, 15,  9, 00), 'end': datetime.datetime(2012, 9, 15,  9, 30), 'end2': datetime.datetime(2012, 9, 15,  9, 30)},
        {'start': datetime.datetime(2012, 9, 15,  9, 30), 'end': datetime.datetime(2012, 9, 15,  9, 45), 'end2': datetime.datetime(2012, 9, 15,  9, 45)},
        {'start': datetime.datetime(2012, 9, 15,  9, 45), 'end': datetime.datetime(2012, 9, 15, 10, 45), 'end2': datetime.datetime(2012, 9, 15, 10, 50)},
        {'start': datetime.datetime(2012, 9, 15, 11, 00), 'end': datetime.datetime(2012, 9, 15, 11, 45), 'end2': datetime.datetime(2012, 9, 15, 11, 50)},
        {'start': datetime.datetime(2012, 9, 15, 11, 45), 'end': datetime.datetime(2012, 9, 15, 13, 30), 'end2': datetime.datetime(2012, 9, 15, 13, 35)},
        {'start': datetime.datetime(2012, 9, 15, 13, 30), 'end': datetime.datetime(2012, 9, 15, 14, 15), 'end2': datetime.datetime(2012, 9, 15, 14, 20)},
        {'start': datetime.datetime(2012, 9, 15, 14, 30), 'end': datetime.datetime(2012, 9, 15, 15, 15), 'end2': datetime.datetime(2012, 9, 15, 15, 20)},
        {'start': datetime.datetime(2012, 9, 15, 15, 30), 'end': datetime.datetime(2012, 9, 15, 16, 15), 'end2': datetime.datetime(2012, 9, 15, 16, 20)},
        {'start': datetime.datetime(2012, 9, 15, 16, 30), 'end': datetime.datetime(2012, 9, 15, 17, 15), 'end2': datetime.datetime(2012, 9, 15, 17, 20)},
        {'start': datetime.datetime(2012, 9, 15, 17, 30), 'end': datetime.datetime(2012, 9, 15, 18, 30), 'end2': datetime.datetime(2012, 9, 15, 18, 35)},
        {'start': datetime.datetime(2012, 9, 15, 18, 30), 'end': datetime.datetime(2012, 9, 15, 18, 45), 'end2': datetime.datetime(2012, 9, 15, 18, 50)},

        {'start': datetime.datetime(2012, 9, 16,  9, 00), 'end': datetime.datetime(2012, 9, 16, 10, 00), 'end2': datetime.datetime(2012, 9, 16, 10, 00)},
        {'start': datetime.datetime(2012, 9, 16, 10, 00), 'end': datetime.datetime(2012, 9, 16, 10, 45), 'end2': datetime.datetime(2012, 9, 16, 10, 50)},
        {'start': datetime.datetime(2012, 9, 16, 11, 00), 'end': datetime.datetime(2012, 9, 16, 11, 45), 'end2': datetime.datetime(2012, 9, 16, 11, 50)},
        {'start': datetime.datetime(2012, 9, 16, 11, 45), 'end': datetime.datetime(2012, 9, 16, 14, 00), 'end2': datetime.datetime(2012, 9, 16, 14, 00)},
        {'start': datetime.datetime(2012, 9, 16, 14, 00), 'end': datetime.datetime(2012, 9, 16, 15, 00), 'end2': datetime.datetime(2012, 9, 16, 15, 00)},
        {'start': datetime.datetime(2012, 9, 16, 15, 15), 'end': datetime.datetime(2012, 9, 16, 16, 00), 'end2': datetime.datetime(2012, 9, 16, 16, 5)},
        {'start': datetime.datetime(2012, 9, 16, 16, 00), 'end': datetime.datetime(2012, 9, 16, 16, 45), 'end2': datetime.datetime(2012, 9, 16, 16, 45)},
        {'start': datetime.datetime(2012, 9, 16, 16, 45), 'end': datetime.datetime(2012, 9, 16, 17, 30), 'end2': datetime.datetime(2012, 9, 16, 17, 35)},
        {'start': datetime.datetime(2012, 9, 16, 17, 45), 'end': datetime.datetime(2012, 9, 16, 18, 30), 'end2': datetime.datetime(2012, 9, 16, 18, 45)},
        {'start': datetime.datetime(2012, 9, 16, 18, 45), 'end': datetime.datetime(2012, 9, 16, 19, 00), 'end2': datetime.datetime(2012, 9, 16, 19, 00)},
    ]

    writers = {
        datetime.date(2012,9,15): csv.writer(open(timetable1_filename, 'wb')),
        datetime.date(2012,9,16): csv.writer(open(timetable2_filename, 'wb')),
    }

    time_index = 0
    cols = [''] * 7
    results = {}
    for row in rows:
        term = session_terms[time_index]
        if term['end'] <= row.start:
            results[term['start']] = cols
            cols = [''] * 7
            time_index += 1
            if len(session_terms) <= time_index:
                break
            term = session_terms[time_index]
        if row.end <= term['start']:
            continue

        cols[0] = '{0[start]:%H:%M} - {0[end]:%H:%M}'.format(term)

        data = cols[ROOM_IDX_MAP.get(row.room, 1)]
        if (data):
            data += '\n\n{0:%H:%M} '.format(row.start)

        if row.title_sphinx:
            data += row.title_sphinx
        else:
            data += ':ref:`session-{0:%d-%H%M}-{1}`'.format(
                row.start,
                row.room.replace(' ', '')
            )
        if row.end > term['end']:
            #休憩時間に食い込むセッション
            data += ' (till {0:%H:%M})'.format(row.end)
        if row.room:
            cols[ROOM_IDX_MAP[row.room]] = data
        else:
            cols[1:] = [data] * 6
            if row.start.day == 16:
                cols[ROOM_IDX_MAP['Room 230']] = ''

    for t in sorted(results):
        writers[t.date()].writerow(results[t])


def make_sphinx_heading(text, marker='='):
    t = text.decode('utf-8')  #TODO
    t_width = sum(unicodedata.east_asian_width(x) in 'WFA' and 2 or 1 for x in t)
    t += '\n' + (marker * t_width)
    return t.encode('utf-8')

SESSION_TEMPLATE_JA = """
{title_with_underline}
{abstract}

:発表者: {speaker}
:対象: {audience}
:言語: {language}
:日時: {datetime}
:場所: {room}
"""

def make_session(rows, template, type_=(), override_filters={}):
    sessions = []
    for row in rows:
        if not row.speaker:
            continue
        if row.type not in type_:
            continue

        params = dict(
            title_with_underline = make_sphinx_heading(row.title_ja),
            abstract = row.abstract,
            speaker = row.speaker,
            language = row.language,
            datetime = "{0.start:%m/%d %H:%M} - {0.end:%H:%M}".format(row),
            room = row.room,
            audience = row.audience,
        )

        for k in params:
            if k in override_filters:
                params[k] = override_filters[k](row)

        text = template.format(**params)
        sessions.append(text)

    return sessions



def make_sessions(rows, sessions_local_filename, sessions_global_filename):

    japanese_filters = {
        'language': lambda r: r.language.split('/')[0].strip(),
        'audience': lambda r: ' / '.join([x.split('/')[0].strip() for x in r.audience.split(',')]),
    }
    # 日本語 セッション(出力言語ではなく)
    with open(sessions_local_filename, 'wb') as f:
        sessions = make_session(rows, SESSION_TEMPLATE_JA, ('日本語',), japanese_filters)
        f.write('\n\n'.join(sessions))

    # 英語 セッション(出力言語ではなく)
    with open(sessions_global_filename, 'wb') as f:
        sessions = make_session(rows, SESSION_TEMPLATE_JA, ('英語',), japanese_filters)
        f.write('\n\n'.join(sessions))


def main(input_filename, timetable1_filename, timetable2_filename, sessions_local_filename, sessions_global_filename):
    reader = csv.reader(open(input_filename, 'rb'))
    rows = TimeTableRows(reader)
    make_timetables(rows, timetable1_filename, timetable2_filename)
    make_sessions(rows, sessions_local_filename, sessions_global_filename)


if __name__ == '__main__':
    main('records.csv', 'schedule1.csv', 'schedule2.csv', 'sessions-local.in', 'sessions-global.in')
