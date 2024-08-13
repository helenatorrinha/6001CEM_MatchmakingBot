import aiosqlite

async def third_algorithm(user_id):
    db = await aiosqlite.connect('database.db')
    
    # Delete existing matches for the user from 'user_partners_third_algorithm' table
    await db.execute('''
        DELETE FROM user_partners_third_algorithm
        WHERE user_id = ?
    ''', (user_id,))
    await db.commit()  # Commit right after deleting existing matches

    # Fetch the game types for the given user
    cursor = await db.execute('''
        SELECT game_type_id FROM user_game_type WHERE user_id = ?
    ''', (user_id,))
    user_game_types = set(row[0] for row in await cursor.fetchall())

    # Fetch potential partners' IDs, excluding the given user
    cursor = await db.execute('''
        SELECT user_id FROM users WHERE user_id != ?
    ''', (user_id,))
    potential_partner_ids = [row[0] for row in await cursor.fetchall()]
    
    if not potential_partner_ids:  # Check if there are potential partners
        await db.close()
        return ""
    
    partner_scores = {}  # Dictionary to store compatibility scores
    for partner_id in potential_partner_ids:
        # Fetch game types for the potential partner
        cursor = await db.execute('''
            SELECT game_type_id FROM user_game_type WHERE user_id = ?
        ''', (partner_id,))
        partner_game_types = set(row[0] for row in await cursor.fetchall())

        # Initialize compatibility score for this partner
        compatibility_score = 0

        # Calculate the compatibility score based on game type similarity
        for user_game_type in user_game_types:
            for partner_game_type in partner_game_types:
                # Check for direct match first (highest compatibility)
                if user_game_type == partner_game_type:
                    compatibility_score += 1  # or a higher value for exact matches
                else:
                    # Retrieve similarity score between different game types
                    cursor = await db.execute('''
                        SELECT similarity_score FROM game_type_similarity
                        WHERE game_type_id1 = ? AND game_type_id2 = ?
                        OR game_type_id1 = ? AND game_type_id2 = ?
                    ''', (user_game_type, partner_game_type, partner_game_type, user_game_type))
                    similarity_result = await cursor.fetchone()
                    if similarity_result:
                        compatibility_score += similarity_result[0]

        partner_scores[partner_id] = compatibility_score

    # Sort potential partners by their compatibility score in descending order
    sorted_partners = sorted(partner_scores.items(), key=lambda item: item[1], reverse=True)

    compatible_partners = []  # List to store compatible partners information
    for partner_id, score in sorted_partners[:5]:  # Limit to top 5
        # Fetch the username of the potential partner
        cursor = await db.execute('''
            SELECT username FROM users WHERE user_id = ?
        ''', (partner_id,))
        username = (await cursor.fetchone())[0]
        compatible_partners.append({
            'username': username,
            'compatibility_score': score
        })

        # Insert compatibility data into user_partners_third_algorithm table
        await db.execute('''
            INSERT INTO user_partners_third_algorithm (user_id, partner_id, compatibility_score)
            VALUES (?, ?, ?)
        ''', (user_id, partner_id, score))
        
    await db.commit()  # Ensure all inserts are committed before closing
    await db.close()

    # Format the result
    formatted_result = ', '.join([f"@{partner['username']} (score {partner['compatibility_score']})" for partner in compatible_partners])
    return formatted_result
