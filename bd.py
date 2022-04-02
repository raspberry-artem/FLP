import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection('E:\Work\YCHEBA\sqlite\sqlite2')
cursor = connection.cursor()

#Изначальная структура таблиц переделана в угоду реляционным бд

cursor.execute('''DROP TABLE IF EXISTS competitions;''')
cursor.execute('''DROP TABLE IF EXISTS teams;''')
cursor.execute('''DROP TABLE IF EXISTS results;''')
cursor.execute('''DROP TABLE IF EXISTS competitions_teams;''')

cursor.execute('''CREATE TABLE competitions
               (id integer, rang text, kind text, year integer, country text)''')

cursor.execute('''CREATE TABLE teams
               (id integer, name text, country text)''')

cursor.execute('''CREATE TABLE results
               (id_winner integer, id_looser integer)''')

cursor.execute('''CREATE TABLE competitions_teams
               (id_competition integer, id_team integer)''')

cursor.execute('''INSERT INTO competitions
                VALUES
                (0,  'Low',    'Basketball', 1987, 'Finland'),
                (1,  'Medium', 'Basketball', 1988, 'Turkey'),
                (2,  'High',   'Swim',       1989, 'England'),
                (3,  'Low',    'Basketball', 1990, 'England'),
                (4,  'Medium', 'Basketball', 1991, 'Ukraine'),
                (5,  'High',   'Swim',       1992, 'Russia'),
                (6,  'Low',    'Volleyball', 1993, 'England'),
                (7,  'Medium', 'Chess',      1994, 'Poland'),
                (8,  'High',   'Chess',      1995, 'Russia'),
                (9,  'Low',    'Volleyball', 1996, 'Belarus'),
                (10, 'Medium', 'Chess',      1997, 'England'),
                (11, 'High',   'Chess',      1998, 'China'),
                (12, 'Low',    'Basketball', 1999, 'Germany'),
                (13, 'Medium', 'Basketball', 2000, 'Russia'),
                (14, 'High',   'Swim',       2001, 'Poland')''')

cursor.execute('''INSERT INTO teams
               VALUES
               (0, 'Bears', 'Russia'),
               (1, 'Cats', 'Russia'),
               (2, 'Dogs',  'England'),
               (3, 'Rats',  'China'),
               (4, 'Boars', 'England'),
               (5, 'Sharks', 'Turkey'),
               (6, 'Stars', 'USA'),
               (7, 'Lions', 'Poland'),
               (8, 'Coyotes', 'USA'),
               (9, 'Squirrels', 'Russia'),
               (10, 'Wolfs', 'Ukraine'),
               (11, 'Elks', 'Russia'),
               (12, 'Snakes', 'Russia'),
               (13, 'Horses', 'Turkey'),
               (14, 'Dolphins', 'Russia'),
               (15, 'Whales', 'England'),
               (16, 'Crocodiles', 'Egypt'),
               (17, 'Cangaroos', 'Ukraine'),
               (18, 'Raccoons', 'Canada'),
               (19, 'Hyenes', 'Mexico'),
               (20, 'Llamas', 'Australia'),
               (21, 'Meerkats', 'Turkey'),
               (22, 'Gazelles', 'Germany'),
               (23, 'Lynxes', 'Egypt'),
               (24, 'Tigers', 'USA'),
               (25, 'Eagles', 'USA'),
               (26, 'Owls', 'Ukraine'),
               (27, 'Spiders', 'Australia'),
               (28, 'Pandas', 'China'),
               (29, 'Foxes', 'Turkey')''')

cursor.execute('''INSERT INTO results
                VALUES
               (0,4),(0,7),(0,21),
               (4,7),(4,24),(4,17),
               (7,21),(7,24),
               (17,0),(17,7),
               (24,0),
               (5,6),
               (6,14),(6,15),
               (16,5),
               (1,2),
               (2,3),
               (8,10),(8,13),
               (18,19),
               (19,22),
               (23,27),
               (12,20),
               (26,25),(26,29),
               (28,29)''')

cursor.execute('''INSERT INTO competitions_teams
                VALUES
                (0,0),(0,4),(0,7),(0,17),(0,21),(0,24),
                (1,0),(1,4),(1,7),(1,17),(1,21),(1,24),
                (2,5),(2,6),(2,14),(2,15),(2,16),
                (3,0),(3,4),(3,7),(3,17),(3,21),(3,24),
                (4,0),(4,4),(4,7),(4,17),(4,21),(4,24),
                (5,5),(5,6),(5,14),(5,15),(5,16),
                (6,1),(6,2),(6,3),(6,8),(6,10),(6,13),(6,18),(6,19),(6,22),(6,23),(6,27),
                (7,12),(7,20),(7,25),(7,26),(7,28),(7,29),
                (8,12),(8,20),(8,25),(8,26),(8,28),(8,29),
                (9,1),(9,2),(9,3),(9,8),(9,10),(9,13),(9,18),(9,19),(9,22),(9,23),(9,27),
                (10,12),(10,20),(10,25),(10,26),(10,28),(10,29),
                (11,12),(11,20),(11,25),(11,26),(11,28),(11,29),
                (12,0),(12,4),(12,7),(12,17),(12,21),(12,24),
                (13,0),(13,4),(13,7),(13,17),(13,21),(13,24),
                (14,5),(14,6),(14,14),(14,15),(14,16)
                
                
           ''')
print('competitions:')
for row in cursor.execute(
    '''SELECT * FROM competitions'''):
        print(row)
        
print('teams:')
for row in cursor.execute(
    '''SELECT * FROM teams'''):
        print(row)
        
print('results:')
for row in cursor.execute(
    '''SELECT * FROM results'''):
        print(row)

print('competitions_teams:')
for row in cursor.execute(
    '''SELECT * FROM competitions_teams'''):
        print(row)


        
#1. Найти год, в который участвовало максимальное число команд, в заданном виде спорта и в заданном ранге соревнований

print('№1:')

cursor.execute(
    '''
    CREATE TEMPORARY TABLE temp_table AS SELECT
        competitions.rang as rang,
        competitions.kind as kind,
        COUNT(competitions.id) as count
    FROM competitions
    INNER JOIN competitions_teams
    ON competitions.id = competitions_teams.id_competition
    GROUP BY competitions.rang, competitions.kind''')

for row in cursor.execute(
    '''
    SELECT 
        competitions.kind as kind,
        competitions.rang as rang,
        competitions.year as year,
        COUNT(competitions.id) as count
    FROM competitions
    INNER JOIN competitions_teams
    ON competitions.id = competitions_teams.id_competition
    INNER JOIN temp_table
    ON temp_table.count = count AND temp_table.rang = competitions.rang AND temp_table.kind = competitions.kind
    GROUP BY competitions.rang, competitions.kind
    ORDER BY competitions.kind,
        competitions.rang
    
    '''):
        print(row)
        
#2. Найти вид спорта, в котором выступает заданная команда

print('№2: ')

for row in cursor.execute(
    '''SELECT DISTINCT
        teams.name as name,
        competitions.kind as kind
    FROM competitions
    INNER JOIN competitions_teams
    ON competitions.id = competitions_teams.id_competition
    INNER JOIN teams
    ON competitions_teams.id_team = teams.id
    ORDER BY teams.name
    '''):
        print(row)

#3. Найти все команды, которые участвовали в Олимпийских играх по определенному виду спорта

print('№3: ')

for row in cursor.execute(
    '''SELECT DISTINCT
        competitions.kind as kind,
        teams.name as name,
        teams.country as country
    FROM competitions
    INNER JOIN competitions_teams
    ON competitions.id = competitions_teams.id_competition
    INNER JOIN teams
    ON competitions_teams.id_team = teams.id
    ORDER BY competitions.kind
    '''):
        print(row)

#4. Найти все команды, участвовавшие в соревнованиях в заданном году

print('№4: ')

for row in cursor.execute(
    '''SELECT DISTINCT
        competitions.year as year,
        teams.name as name,
        teams.country as country
    FROM competitions
    INNER JOIN competitions_teams
    ON competitions.id = competitions_teams.id_competition
    INNER JOIN teams
    ON competitions_teams.id_team = teams.id
    ORDER BY competitions.year
    '''):
        print(row)        

#5. Найти все команды определенной страны, у которых были выигрыши

print('№5: ')

for row in cursor.execute(
    '''SELECT DISTINCT
        teams.country as country,
        teams.name as name
    FROM teams
    INNER JOIN results
    ON teams.id = results.id_winner
    ORDER BY teams.country
    '''):
        print(row) 
