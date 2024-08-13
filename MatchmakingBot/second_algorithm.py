import aiosqlite

async def second_algorithm(user_id):
    db = await aiosqlite.connect('database.db')
    
    # Delete existing matches for the user from 'user_partners_second_algorithm' table
    cursor = await db.execute('''
        DELETE FROM user_partners_second_algorithm
        WHERE user_id = ?
    ''', (user_id,))
    await db.commit()
    
    # Gets the information (age, gender and skill level) for the given user
    cursor = await db.execute('''
        SELECT age_range, gender, skill_level FROM users WHERE user_id = ?
    ''', (user_id,))
    user_details = await cursor.fetchone()
    user_age_range, user_gender, user_skill_level = user_details

    # Gets the game types for the given user
    cursor = await db.execute('''
        SELECT game_type_id FROM user_game_type WHERE user_id = ?
    ''', (user_id,))
    user_game_types = set(row[0] for row in await cursor.fetchall())

     # Gets the languages for the given user
    cursor = await db.execute('''
        SELECT language_id FROM user_language WHERE user_id = ?
    ''', (user_id,))
    user_languages = set(row[0] for row in await cursor.fetchall())

    # Gets the potential partners ids without including the given user
    cursor = await db.execute('''
        SELECT user_id FROM users WHERE user_id != ?
    ''', (user_id,))
    potential_partner_ids = [row[0] for row in await cursor.fetchall()]
    
    if not potential_partner_ids:  # If there are no potential partners
        await db.close()
        return ""
    
    # Functionality to calculate the compatibility scores between the user and each potential partner
    partner_scores = {} # Dictionary to store the compatibility scores
    for partner_id in potential_partner_ids: # For each potential partner
        score = 0

        # Get the partner's informations (age, gender and skill level)
        cursor = await db.execute('''
            SELECT age_range, gender, skill_level FROM users WHERE user_id = ?
        ''', (partner_id,))
        partner_details = await cursor.fetchone()
        partner_age_range, partner_gender, partner_skill_level = partner_details

        # Score adjustments based on matching criteria
        if partner_age_range == user_age_range: # If the partner's age range is the same as the user
            score += 2 # Add 2 to the score
        if partner_gender == user_gender: # If the partner's gender is the same as the user
            score += 1 # Add 1 to the score
        if partner_skill_level == user_skill_level: # If the partner's skill level is the same as the user
            score += 2 # Add 2 to the score

        # Gets the game types for the possible partner
        cursor = await db.execute('''
            SELECT game_type_id FROM user_game_type WHERE user_id = ?
        ''', (partner_id,))
        partner_game_types = set(row[0] for row in await cursor.fetchall()) # Game types for the possible partner
    
        # Functionality to determine the if the game types of the user and potential partner match
        # For each game type in common we add 1 to the score
        game_type_matches = 0 # Counter for the matching game types
        for game_type in user_game_types: # For each game type of the user
            if game_type in partner_game_types: # If the game type is in the partner's game types
                game_type_matches += 1 # Add 1 to the count of matching game types
        score += game_type_matches # Add the count of matching game types to the score

        # Gets the languages for the possible partner
        cursor = await db.execute('''
            SELECT language_id FROM user_language WHERE user_id = ?
        ''', (partner_id,))
        partner_languages = set(row[0] for row in await cursor.fetchall())
        
        # Functionality to determine the if the languages of the user and potential partner match
        # For each language in common we add 1 to the score
        language_matches = 0 # Counter for the languages 
        for language in user_languages: # For each language of the user
            if language in partner_languages: # If the language is in the partner's languages
                language_matches += 1 # Add 1 to the count of matching languages
        score += language_matches # Add the count of matching languages to the score

        partner_scores[partner_id] = score # Adds the partner's id and respective score to partner_scores

    # Sort potential partners by their score in descending order
    sorted_partners = sorted(partner_scores.items(), key=lambda item: item[1], reverse=True)

    compatible_partners = []  # List to store the compatible partners
    for partner_id, score in sorted_partners[:5]:  # Limit to top 5
        # Gets the username of the potential partner
        cursor = await db.execute('''
            SELECT username FROM users WHERE user_id = ?
        ''', (partner_id,))
        username = (await cursor.fetchone())[0]
        compatible_partners.append({ # Adds the partner's username and score to the list
            'username': username,
            'compatibility_score': score
        })
        
        # Add the user id, partner id, and compatibility score to the user_partners_second_algorithm table
        cursor = await db.execute('''
            INSERT INTO user_partners_second_algorithm (user_id, partner_id, compatibility_score)
            VALUES (?, ?, ?)
        ''', (user_id, partner_id, score))

    await db.commit()
    await cursor.close()
    await db.close()

    # Convert the list to the desired string format (with "@" prefix and separated by commas)
    formatted_result = ', '.join([f"@{partner['username']} (score {partner['compatibility_score']})" for partner in compatible_partners])
    return formatted_result # Returns the formatted result
