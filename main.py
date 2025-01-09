import windowClass
import sqlite3

window = windowClass.hockeyTkinterWindow()

conn = sqlite3.connect('hockey_video.db')
cursor = conn.cursor()

# todo: references

cursor.execute('''
            CREATE TABLE IF NOT EXISTS Matches
            (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                home_team INTEGER NOT NULL REFERENCES Teams(ID),
                away_team INTEGER NOT NULL REFERENCES Teams(ID),
                date DATE,
                scheduled_pushback DATETIME,
                actual_pushback DATETIME,
                video_link TEXT,
                umpire_1 INTEGER REFERENCES People(ID),
                umpire_2 INTEGER REFERENCES People(ID)
            );''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS Teams
            (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                club_id INTEGER NOT NULL REFERENCES Clubs(ID),
                name TEXT NOT NULL,
                challenges INTEGER,
                successful_challenges INTEGER
            );''')

conn.commit()
