import sqlite3
from .schemas import *

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()


def create_tables():
    cur.execute("""
create table if not exists dialogs  (
    id integer primary key autoincrement not null,
    text text not null,
    next_dialog_id integer,
    
    FOREIGN KEY(next_dialog_id) REFERENCES dialogs(id)
);
""")
    conn.commit()

    cur.execute("""
create table if not exists choices (
    id integer primary key autoincrement not null,
    choice varchar(256) not null,
    cur_dialog_id integer not null,
    next_dialog_id integer not null,
    
    FOREIGN KEY(cur_dialog_id) REFERENCES dialogs(id),
    FOREIGN KEY(next_dialog_id) REFERENCES dialogs(id)
)
""")
    conn.commit()

    cur.execute("""
create table if not exists checkpoints (
    id integer primary key autoincrement not null,
    yandex_user_id integer not null,
    dialog_checkpoint_id integer default 0 not null,

    FOREIGN KEY(dialog_checkpoint_id) REFERENCES dialogs(id)
)
""")
    conn.commit()

    cur.execute("""
    create table if not exists achievements (
        id integer primary key autoincrement not null,
        yandex_user_id integer not null,
        achievement varchar(256) not null
    )
    """)
    conn.commit()


def get_dialog_by_id(id: int) -> Dialog | None:
    cur.execute('select * from dialogs where id = ?', [id])
    resp = cur.fetchone()

    if not resp:
        return

    return Dialog(resp)


def get_choices_by_dialog_id(id: int) -> list[Choice] | None:
    cur.execute('select * from choices where cur_dialog_id = ?', [id])
    resp = cur.fetchall()
    arr = []

    if not resp:
        return

    for choice in resp:
        arr.append(Choice(choice))

    return arr


def set_user_checkpoint(yandex_user_id: int, dialog_id: int):
    cur.execute('select id from checkpoints where yandex_user_id = ?', [yandex_user_id])
    checkpoint_id = cur.fetchone()

    if checkpoint_id:
        cur.execute('update checkpoints set dialog_checkpoint_id = ? where yandex_user_id = ?', [dialog_id, yandex_user_id])
    else:
        cur.execute('insert into checkpoints(yandex_user_id, dialog_checkpoint_id) values (?, ?)', [yandex_user_id, dialog_id])

    conn.commit()


def get_user_checkpoint(yandex_user_id: int) -> Checkpoint | None:
    cur.execute('select * from checkpoints where yandex_user_id = ?', [yandex_user_id])
    resp = cur.fetchone()

    if not resp:
        return

    return Checkpoint(resp)


def add_user_achievement(yandex_user_id: int, achievement: str):
    cur.execute('insert into achievements(yandex_user_id, achievement) values (?, ?)', [yandex_user_id, achievement])
    conn.commit()


def get_achievements_by_yandex_user_id(yandex_user_id: int) -> list[Achievement] | None:
    cur.execute('select * from achievements where yandex_user_id = ?', [yandex_user_id])
    resp = cur.fetchall()
    arr = []

    if not resp:
        return

    for choice in resp:
        arr.append(Achievement(choice))

    return arr
