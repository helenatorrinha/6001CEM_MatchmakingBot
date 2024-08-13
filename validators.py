# Function to validate the age range input
def is_valid_age_range(age_range):
    valid_age_ranges = ['13-19', '20-39', '40-59', '+60']
    if age_range in valid_age_ranges:
        return True
    return False

# Function to validate the gender input
def is_valid_gender(gender):
    valid_gender = ['male', 'female', 'other']
    if gender in valid_gender:
        return True
    return False

# Function to validate the languages input
def is_valid_language(languages_list):
    valid_languages = ['english', 'chinese', 'spanish', 'portuguese', 'russian', 'french', 'german', 'italian', 'romanian']
    for language in languages_list:
        if not language in valid_languages:
            return False
    return True

# Function to validate the skill level input
def is_valid_skillLevel(skillLevel):
    valid_skillLevel = ['beginner', 'intermediate', 'advanced', 'expert', 'proficient']
    if skillLevel in valid_skillLevel:
        return True
    return False   
    
# Function to validate the game types input
def is_valid_gameType(preferredGameType_list):
    valid_preferredGameType = ['sandbox', 'strategy', 'shooter', 'moba', 'rpg', 'simulation', 'puzzlers', 'action-adventure', 'survival', 'platformer']
    for preferredGameType in preferredGameType_list:
        if not preferredGameType in valid_preferredGameType:
            return False
    return True
