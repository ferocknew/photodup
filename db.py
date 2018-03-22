import sqlite3

from config import db_file

conn = sqlite3.connect(db_file)
cursor = conn.cursor()


def create_table():
    drop_table()
    cursor.executescript('''CREATE TABLE photo
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hash VARCHAR(50) NOT NULL,
        name TEXT NOT NULL,
        path TEXT NOT NULL,
        existed INTEGER DEFAULT 1
    );
    CREATE INDEX photo_hash_index
        ON photo (hash);
    CREATE INDEX photo_name_index
        ON photo (name);
    CREATE INDEX photo_path_index
        ON photo (path);
    ''')


def drop_table():
    cursor.execute('DROP TABLE IF EXISTS photo')


def commit_changes():
    conn.commit()


def insert_file(hash, name, path):
    cursor.execute('INSERT INTO photo (hash,name,path) VALUES (?,?,?)', (hash, name, path))


def is_existed(file_path):
    cursor.execute('SELECT COUNT(*) FROM photo WHERE path = ? AND existed = 1', (file_path,))
    row = cursor.fetchone()
    return row[0] != 0


def mark_deleted(file_path):
    cursor.execute('UPDATE photo SET existed=0 WHERE path = ?', (file_path,))
    conn.commit()


def find_duplicate():
    cursor.execute('''SELECT * FROM photo WHERE hash IN
                      (SELECT hash FROM photo GROUP BY hash HAVING count(*) > 1)''')
    rows = cursor.fetchall()
    return rows


def close_db():
    if conn is not None:
        conn.close()


if __name__ == '__main__':
    print('create photo.db ...')
    create_table()
    close_db()
    print('done!')
