import aiosqlite

async def first_algorithm(user_id):
    db = await aiosqlite.connect('database.db')
    
    # Delete existing matches for the user from 'user_partners_first_algorithm' table
    await db.execute('''
        DELETE FROM user_partners_first_algorithm
        WHERE user_id = ?
    ''', (user_id,))
    await db.commit()
    
    # Gets the demographic information (age and gender) for the given user
    cursor = await db.execute('''
        SELECT age_range, gender
        FROM users
        WHERE user_id = ?
    ''', (user_id,))
    
    user_demographics = await cursor.fetchone()
    age_range, gender = user_demographics
        
    # Gets the languages for the given user
    target_user_languages = f'''
        SELECT language_id
        FROM user_language
        WHERE user_id = {user_id}
    '''
    
    # Query that gets users with matching age_range, gender, and at least one language in common, 
    # excluding the given user, 
    # ordered by the number of common languages
    query = f'''
        SELECT u.user_id, u.username
        FROM users u
        JOIN user_language ul ON u.user_id = ul.user_id
        WHERE u.age_range = ? 
            AND u.gender = ? 
            AND ul.language_id IN ({target_user_languages}) 
            AND u.user_id != ? 
        GROUP BY u.user_id
        ORDER BY COUNT(ul.language_id) DESC
        LIMIT 10
    '''
    cursor = await db.execute(query, (age_range, gender, user_id))
    potential_matches = await cursor.fetchall()
    
    # If there are no potential matches based on demographic information we try to match using the languages in common
    if not potential_matches:  
        # Query that gets users with at least one language in common, excluding the given user, 
        # ordered by the number of common languages
        query = '''
        SELECT u.user_id, u.username
        FROM users u
        JOIN user_language ul ON u.user_id = ul.user_id
        WHERE ul.language_id IN (
            SELECT language_id
            FROM user_language
            WHERE user_id = ?
        )
        AND u.user_id != ?
        GROUP BY u.user_id
        ORDER BY COUNT(ul.language_id) DESC
        LIMIT 10
        '''
        cursor = await db.execute(query, (user_id, user_id))
        potential_matches = await cursor.fetchall()
        
    if not potential_matches:  # If there are no potential matches based on language
        # Query that gets 10 users with matching age_range, excluding the given user
        query = '''
            SELECT u.user_id, u.username
            FROM users u
            WHERE u.age_range = ? 
                AND u.user_id != ? 
            GROUP BY u.user_id
            ORDER BY RANDOM()
            LIMIT 10
        '''
        cursor = await db.execute(query, (age_range, user_id))
        potential_matches = await cursor.fetchall()
        
    if not potential_matches:  # If there are no potential matches based on age range
        # Query to get users with the same gender, excluding the given user
        query = '''
            SELECT u.user_id, u.username
            FROM users u
            WHERE u.gender = (
                SELECT gender
                FROM users
                WHERE user_id = ?
            )
            AND u.user_id != ?
            GROUP BY u.user_id
            ORDER BY RANDOM()
            LIMIT 10
        '''
        cursor = await db.execute(query, (user_id, user_id))
        potential_matches = await cursor.fetchall()
    
    if not potential_matches: # If there are no potential matches based on gender
        # Query to get users with matching game types, excluding the given user
        query = '''
            SELECT u.user_id, u.username
            FROM users u
            JOIN user_game_type ug ON u.user_id = ug.user_id
            WHERE ug.game_type_id IN (
                SELECT game_type_id
                FROM user_game_type
                WHERE user_id = ?
            )
            AND u.user_id != ?
            GROUP BY u.user_id
            ORDER BY COUNT(ug.game_type_id) DESC
            LIMIT 10
        '''
        cursor = await db.execute(query, (user_id, user_id))
        potential_matches = await cursor.fetchall()
        
        # Loop through the potential_matches and put matches with the same skill level as the user first in the list
        potential_matches_with_same_skill = []
        potential_matches_with_different_skill = []

        for match in potential_matches:
                potential_match_user_id, potential_matche_username = match
                # Get the skill level of the matched user
                cursor = await db.execute('''
                    SELECT skill_level
                    FROM users
                    WHERE user_id = ?
                ''', (user_id,))
                user_skill_level = (await cursor.fetchone())[0]

                cursor = await db.execute('''
                    SELECT skill_level
                    FROM users
                    WHERE user_id = ?
                ''', (potential_match_user_id,))
                potential_match_skill_level = (await cursor.fetchone())[0]

                # Check if the skill level matches the user's skill level
                if potential_match_skill_level == user_skill_level:
                    potential_matches_with_same_skill.append((potential_match_user_id, potential_matche_username))
                else:
                    potential_matches_with_different_skill.append((potential_match_user_id, potential_matche_username))

        # Combine the lists, putting matches with the same skill level first
        matching_users = potential_matches_with_same_skill + potential_matches_with_different_skill
        
        for match in matching_users:  # For each potential match
            partner_id = match[0]  # The partner's user ID 

            # Adds the user Id and corresponding partners Ids into the 'user_partners_first_algorithm' table
            cursor = await db.execute('''
                INSERT INTO user_partners_first_algorithm (user_id, partner_id)
                VALUES (?, ?)
            ''', (user_id, partner_id))
        
        await cursor.close()
        await db.close()    
        
        # Convert the list of usernames with "@" prefix into a comma-separated string
        matching_usernames = [f"@{user[1]}" for user in matching_users]
        matching_usernames_string = ', '.join(matching_usernames)
        return matching_usernames_string

    
    # Gets the game types for the given user
    target_user_game_types = f'''
        SELECT game_type_id
        FROM user_game_type
        WHERE user_id = {user_id}
    '''

    # Filter the potential_matches based on matching game types
    matching_users = []
    for match in potential_matches:  # For each user in the initial potential_matches
        matched_user_id, username = match
        cursor = await db.execute(f'''
            SELECT COUNT(*)
            FROM user_game_type
            WHERE user_id = ? AND game_type_id IN ({target_user_game_types})
        ''', (matched_user_id,))
        common_game_types_count = (await cursor.fetchone())[0]
        
        # Add the username and the count of common game types to the list
        matching_users.append((matched_user_id, username, common_game_types_count))

    # Sort the list by the number of common game types in descending order
    sorted_matching_users = sorted(matching_users, key=lambda x: x[2], reverse=True)
    
    for match in sorted_matching_users:  # For each potential match
        partner_id = match[0]  # The partner's user ID 

        # Adds the user Id and corresponding partners Ids into the 'user_partners_first_algorithm' table
        cursor = await db.execute('''
            INSERT INTO user_partners_first_algorithm (user_id, partner_id)
            VALUES (?, ?)
        ''', (user_id, partner_id))
    
    await db.commit()
    await cursor.close()
    await db.close()
    
    if sorted_matching_users:
        # Convert the list of usernames with "@" prefix into a comma-separated string
        return ', '.join([f"@{user[1]}" for user in sorted_matching_users])
    return ""
