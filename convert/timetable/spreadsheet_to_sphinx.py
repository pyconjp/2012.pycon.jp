# -*- coding: utf-8 -*-
from __future__ import print_function
import csv
import time
import datetime

def str2datetime(s):
    "convert %m/%d/%Y HH:MM:SS -> datetime object"
    return datetime.datetime(*time.strptime(s, '%m/%d/%Y %H:%M:%S')[:6])


def main(input_filename, timetable1_filename, timetable2_filename):
    reader = csv.reader(open(input_filename, 'rb'))
    rows = list(reader)
    in_col_idx_keys = {
        'start': "開始時刻",
        'end': "終了時刻",
        'track': "トラック",
        'room': "場所",
        'title_ja': "講演タイトル / Talk title",
        'title_en': "英語タイトル",
        'title_sphinx': "タイトルSphinx埋込",
        'lang': "講演言語 / Language of talk",
    }
    in_col_idx_map = {}
    room_idx_map = {
        'Room 230': 1,
        'Room 433': 2,
        'Room 351a': 3,
        'Room 357': 4,
        'Room 452': 5,
        'Room 358': 6
    }
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

    # 入力データの列名とindex値の対応付け
    in_header = rows[0]
    for k, v in in_col_idx_keys.iteritems():
        in_col_idx_map[k] = in_header.index(v)

    time_table = {}
    for row in rows[1:]:
        start = row[in_col_idx_map['start']]
        start = str2datetime(start)
        tr = time_table[start] = time_table.get(start, {})
        tr[row[in_col_idx_map['room']]] = row

    # rename keys; data[start] -> data[start, end]
    time_table_keys = sorted(time_table)
    for start, end in zip(time_table_keys, time_table_keys[1:]+time_table_keys[:1]):
        if start.day != end.day:
            end = time_table[start].values()[0][in_col_idx_map['end']]
            end = str2datetime(end)
        time_table[start, end] = time_table.pop(start)

    # debug print
    #for t in sorted(time_table):
    #    rooms = time_table[t]
    #    room_names = sorted(room_idx_map, key=lambda k: room_idx_map[k])
    #    print(
    #        '{0[0]:%m/%d %H:%M} - {0[1]:%H:%M} {1}'.format(
    #            t, ' '.join([(x if x in rooms else (' ' * len(x))) for x in room_names])
    #        )
    #    )

    writers = {
        datetime.date(2012,9,15): csv.writer(open(timetable1_filename, 'wb')),
        datetime.date(2012,9,16): csv.writer(open(timetable2_filename, 'wb')),
    }

    time_index = 0
    cols = [''] * 7
    results = {}
    for start, end in sorted(time_table):
        term = session_terms[time_index]
        if term['end'] <= start:
            results[term['start']] = cols
            cols = [''] * 7
            time_index += 1
            if len(session_terms) <= time_index:
                break
            term = session_terms[time_index]
        if end <= term['start']:
            continue

        time_row = time_table[start, end]
        cols[0] = '{0[start]:%H:%M} - {0[end]:%H:%M}'.format(term)

        for room in time_row:
            if room and room not in room_idx_map:
                pass
            else:
                row = time_row[room]
                data = cols[room_idx_map.get(room, 1)]
                if (data):
                    data += '\n\n{0:%H:%M} '.format(start)

                if row[in_col_idx_map['title_sphinx']]:
                    data += row[in_col_idx_map['title_sphinx']]
                else:
                    data += ':ref:`session-{0:%d-%H%M}-{1}`'.format(
                        str2datetime(row[in_col_idx_map['start']]),
                        room.replace(' ', '')
                    )
                session_end = str2datetime(row[in_col_idx_map['end']])
                if session_end > term['end']:
                    #休憩時間に食い込むセッション
                    data += ' (till {0:%H:%M})'.format(session_end)
                if room:
                    cols[room_idx_map[room]] = data
                else:
                    cols[1:] = [data] * 6
                    if start.day == 16:
                        cols[room_idx_map['Room 230']] = ''

    for t in sorted(results):
        writers[t.date()].writerow(results[t])


if __name__ == '__main__':
    main('records.csv', 'schedule1.csv', 'schedule2.csv')
