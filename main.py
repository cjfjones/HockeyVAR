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

cursor.execute('''
            CREATE TABLE IF NOT EXISTS Clubs
            (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS People
            (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT,
                date_of_birth DATE,
                team INTEGER REFERENCES Teams(ID),
                is_umpire BOOLEAN
            );''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS Player_Appearances
            (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                match INTEGER REFERENCES Matches(ID),
                player INTEGER REFERENCES People(ID)
            );''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS Clips
            (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                file_name TEXT,
                match INTEGER REFERENCES Matches(ID),
                time_from_start DATETIME,
                length DECIMAL
            );''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS Frames
            (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                frame_num INTEGER NOT NULL,
                confidence DECIMAL,
                challenge BOOLEAN,
                clip INTEGER REFERENCES Clips(ID),
                is_foot BOOLEAN NOT NULL
            );''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS Challenges
            (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                frame_id INTEGER REFERENCES Frames(ID),
                challenger INTEGER REFERENCES People(ID),
                challenge_correct BOOLEAN
            );''')

conn.commit()
