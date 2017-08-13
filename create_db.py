import sqlite3

def create_table(conn):
    c = conn.cursor()
    # star_info
    sql = '''
            create table star_info
            (
             star_info_id INTEGER PRIMARY KEY autoincrement,
             star_id varchar(20) not null,
             star_name VARCHAR(50) not null,
             star_description text
            )'''
    c.execute(sql)

    # star_image
    sql ='''
            create table star_image
            (
             star_image_id INTEGER PRIMARY KEY  autoincrement,
             star_id varchar(20) not null,
             image_id varchar(50) not null,
             image_feat_id varchar(50) not null,
             path varchar(50),
             FOREIGN KEY(star_image_id) REFERENCES star_info(star_id)
            )'''
    c.execute(sql)

    # video_info
    sql='''
          create table video_info
          (
            video_info_id INTEGER PRIMARY KEY autoincrement,
            video_name varchar(50) not null,
            year text,
            type varchar(20),
            star_id varchar(50),
            star_name varchar(50),
            link text
          )'''
    c.execute(sql)

    conn.commit()

def drop_table(conn):
    c = conn.cursor()

    drop_sql="drop table if exists "

    c.execute(drop_sql + 'images')
    c.execute(drop_sql + 'star_info')
    c.execute(drop_sql + 'star_image')
    c.execute(drop_sql + 'video_info')

    conn.commit()

if __name__=="__main__":
    conn = sqlite3.connect('facesearch.db')
    try:
        drop_table(conn)
        create_table(conn)
    except:
        conn.close()
    conn.close()