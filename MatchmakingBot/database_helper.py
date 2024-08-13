import aiosqlite

# Function to add a user to the database
async def add_user(user_id, username, age_range, gender, languages, skill_level, game_types):
    db = await aiosqlite.connect('database.db')

    # Insert user into 'users' table
    cursor = await db.execute('''
        INSERT INTO users (user_id, username, age_range, gender, skill_level)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, age_range, gender, skill_level))
    await db.commit()
    
    # Insert user's languages into 'user_language' table
    for language in languages:
        cursor = await db.execute('''
            INSERT INTO user_language (user_id, language_id)
            VALUES (?, (
                SELECT languages_id FROM languages WHERE languages_name = ?
            ))
        ''', (user_id, language))
    await db.commit()
    
    # Insert user's preferred game types into 'user_game_type' table
    for game_type in game_types:
        cursor = await db.execute('''
            INSERT INTO user_game_type (user_id, game_type_id)
            VALUES (?, (
                SELECT game_type_id FROM game_types WHERE game_type_name = ?
            ))
        ''', (user_id, game_type))
    
    await db.commit()
    await cursor.close()
    await db.close()

async def get_user_by_id(user_id):
    db = await aiosqlite.connect('database.db')
    
    # Execute a SELECT query to retrieve the user information based on user_id
    cursor = await db.execute('''
        SELECT * FROM users WHERE user_id = ?
    ''', (user_id,))
    
    # Fetch the result
    user = await cursor.fetchone()
    
    # Check if the user was found
    if user:
        # Convert the tuple to a dictionary for easier manipulation
        user_data = {
            "user_id": user[0],
            "username": user[1],
            "age_range": user[2],
            "gender": user[3],
            "skill_level": user[4],
        }
        
        # Get the user's languages
        cursor = await db.execute('''
            SELECT l.languages_name FROM languages l
            INNER JOIN user_language ul ON l.languages_id = ul.language_id
            WHERE ul.user_id = ?
        ''', (user_id,))
        languages = [language[0] for language in await cursor.fetchall()]
        user_data['languages'] = languages
        
        # Get the user's game types
        cursor = await db.execute('''
            SELECT gt.game_type_name FROM game_types gt
            INNER JOIN user_game_type ugt ON gt.game_type_id = ugt.game_type_id
            WHERE ugt.user_id = ?
        ''', (user_id,))
        game_types = [game_type[0] for game_type in await cursor.fetchall()]
        user_data['game_types'] = game_types
    else:
        user_data = None
        
    await db.commit()
    await cursor.close()
    await db.close()
    
    return user_data

# Function to update an user's information
async def update_user(user):
    db = await aiosqlite.connect('database.db')

    # Update the user's information (age_range, gender and skill_level) in the 'users' table
    cursor = await db.execute('''
        UPDATE users
        SET age_range = ?,
            gender = ?,
            skill_level = ?
        WHERE user_id = ?
    ''', (user['age_range'], user['gender'], user['skill_level'], user['user_id']))

    # Delete the user's existing language preferences from the 'user_language' table
    cursor = await db.execute('''
        DELETE FROM user_language
        WHERE user_id = ?
    ''', (user['user_id'],))

    # Insert the user's updated language preferences into the 'user_language' table
    for language in user['languages']:
        cursor = await db.execute('''
            INSERT INTO user_language (user_id, language_id)
            VALUES (?, (
                SELECT languages_id FROM languages WHERE languages_name = ?
            ))
        ''', (user['user_id'], language))
    await db.commit()
    
    # Delete the user's existing game type preferences from the 'user_game_type' table
    cursor = await db.execute('''
        DELETE FROM user_game_type
        WHERE user_id = ?
    ''', (user['user_id'],))
    await db.commit()
    
    # Insert the user's updated game type preferences into the 'user_game_type' table
    for game_type in user['game_types']:
        cursor = await db.execute('''
            INSERT INTO user_game_type (user_id, game_type_id)
            VALUES (?, (
                SELECT game_type_id FROM game_types WHERE game_type_name = ?
            ))
        ''', (user['user_id'], game_type))
    
    await db.commit()
    await cursor.close()
    await db.close()
    
# Function to get the user's results from the first, second and third algorithms
async def get_results(user_id):
    db = await aiosqlite.connect('database.db')

    results = {
        "first_algorithm": [],
        "second_algorithm": [],
        "third_algorithm": []
    }

    # Function to get usernames for a given list of partner_ids
    async def get_usernames(partner_ids):
        if not partner_ids: # If there are no partner IDs
            return []
        placeholders = ','.join('?' for _ in partner_ids) # Create a string of question marks for the SQL query according to the number of partner IDs
        cursor = await db.execute(f'''
            SELECT username FROM users
            WHERE user_id IN ({placeholders})
        ''', partner_ids)
        return [f"@{row[0]}" for row in await cursor.fetchall()]

    # Fetch partner IDs for the first algorithm
    cursor = await db.execute('''
        SELECT partner_id FROM user_partners_first_algorithm
        WHERE user_id = ?
    ''', (user_id,))
    first_algorithm_partner_ids = [row[0] for row in await cursor.fetchall()]
    results["first_algorithm"] = await get_usernames(first_algorithm_partner_ids)

    # Fetch partner IDs for the second algorithm
    cursor = await db.execute('''
        SELECT partner_id FROM user_partners_second_algorithm
        WHERE user_id = ?
    ''', (user_id,))
    second_algorithm_partner_ids = [row[0] for row in await cursor.fetchall()]
    results["second_algorithm"] = await get_usernames(second_algorithm_partner_ids)

    # Fetch partner IDs for the third algorithm
    cursor = await db.execute('''
        SELECT partner_id FROM user_partners_third_algorithm
        WHERE user_id = ?
    ''', (user_id,))
    third_algorithm_partner_ids = [row[0] for row in await cursor.fetchall()]
    results["third_algorithm"] = await get_usernames(third_algorithm_partner_ids)

    await db.commit()
    await cursor.close()
    await db.close()

    # Format the results as a string
    formatted_results = []
    if results["first_algorithm"]:
        formatted_results.append("Results from the 1st algorithm: " + ', '.join(results["first_algorithm"]))
    if results["second_algorithm"]:
        formatted_results.append("Results from 2nd algorithm: " + ', '.join(results["second_algorithm"]))
    if results["third_algorithm"]:
        formatted_results.append("Results from3rd algorithm: " + ', '.join(results["third_algorithm"]))
    if not formatted_results: # If there are no results
        formatted_results.append("No results found.")
    return '\n'.join(formatted_results) 
