import sqlite3

# Function to create the database and fill the languages and game types tables 
def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create 'users' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            age_range TEXT,
            gender TEXT,
            skill_level TEXT
        )
    ''')

    # Create 'languages' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS languages (
            languages_id INTEGER PRIMARY KEY,
            languages_name TEXT UNIQUE
        )
    ''')

    # List with all the languages to add to the table
    languages_list = ['english', 'chinese', 'spanish', 'portuguese', 'russian', 'french', 'german', 'italian', 'romanian']

    # Loops through the list and adds the languages to the table
    for language in languages_list:
        cursor.execute('''
            INSERT OR IGNORE INTO languages (languages_name)
            VALUES (?)
        ''', (language,))

    # Create 'game_types' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_types (
            game_type_id INTEGER PRIMARY KEY,
            game_type_name TEXT UNIQUE
        )
    ''')
    
    # List with all the game types to add to the table
    game_types_list = ['sandbox', 'strategy', 'shooter', 'moba', 'rpg', 'simulation', 'puzzlers', 'action-adventure', 'survival', 'platformer']

    # Loops through the list and adds the game types to the table
    for game_type in game_types_list:
        cursor.execute('''
            INSERT OR IGNORE INTO game_types (game_type_name)
            VALUES (?)
        ''', (game_type,))
    
    # Create 'user_language' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_language (
            user_id INTEGER,
            language_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (language_id) REFERENCES languages(languages_id),
            PRIMARY KEY (user_id, language_id)
        )
    ''')
    
    # Create 'user_game_type' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_game_type (
            user_id INTEGER,
            game_type_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (game_type_id) REFERENCES game_types(game_type_id),
            PRIMARY KEY (user_id, game_type_id)
        )
    ''')
    
    # Create 'user_partners_first_algorithm' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_partners_first_algorithm (
            user_id INTEGER,
            partner_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (partner_id) REFERENCES users(user_id)
        )
    ''')
    
    # Create 'user_partners_second_algorithm' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_partners_second_algorithm (
            user_id INTEGER,
            partner_id INTEGER,
            compatibility_score INTEGER,
            PRIMARY KEY (user_id, partner_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (partner_id) REFERENCES users(user_id)
        )
    ''')

    # Create 'game_type_similarity' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_type_similarity (
        game_type_id1 INTEGER,
        game_type_id2 INTEGER,
        similarity_score INTEGER DEFAULT 1, 
        FOREIGN KEY (game_type_id1) REFERENCES game_types(game_type_id),
        FOREIGN KEY (game_type_id2) REFERENCES game_types(game_type_id),
        PRIMARY KEY (game_type_id1, game_type_id2)
    );
    ''')
    
    game_type_pairs = [
    (1, 6), #Sandbox (1) and Simulation (6)
    (1, 2), #Sandbox (1) and Strategy (2)
    (2, 4), #Strategy (2) and MOBA (4)
    (2, 1), #Strategy (2) and Sandbox (1)
    (2, 6), #Strategy (2) and Simulation (6)
    (3, 8), #Shooter (3) and Action-Adventure (8)
    (3, 4), #Shooter (3) and MOBA (4)
    (4, 2), #MOBA (4) and Strategy (2)
    (4, 3), #MOBA (4) and Shooter (3)
    (5, 8), #RPG (5) and Action-Adventure (8)
    (5, 9), #RPG (5) and Survival (9)
    (6, 1), #Simulation (6) and Sandbox (1)
    (6, 2), #Simulation (6) and Strategy (2)
    (7, 1), #Puzzlers (7) and Sandbox (1)
    (7, 2), #Puzzlers (7) and Strategy (2)
    (8, 5), #Action-Adventure (8) and RPG (5)
    (8, 3), #Action-Adventure (8) and Shooter (3)
    (8, 9), #Action-Adventure (8) and Survival (9)
    (9, 1), #Survival (9) and Sandbox (1)
    (9, 5), #Survival (9) and RPG (5)
    (9, 8), #Survival (9) and Action-Adventure (8)
    (10, 8) #Platformer (10) and Action-Adventure (8)
    ]

    for pair in game_type_pairs:
        cursor.execute('''
            INSERT INTO game_type_similarity (game_type_id1, game_type_id2)
            VALUES (?, ?)
        ''', pair)
        
    # Create 'user_partners_third_algorithm' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_partners_third_algorithm (
            user_id INTEGER,
            partner_id INTEGER,
            compatibility_score INTEGER,
            PRIMARY KEY (user_id, partner_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (partner_id) REFERENCES users(user_id)
        )
    ''')
        
    conn.commit()
    conn.close()

