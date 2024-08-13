import discord
from validators import is_valid_age_range, is_valid_gender, is_valid_language, is_valid_skillLevel, is_valid_gameType
from database_helper import update_user
from find_partners import find_gaming_partners

class UpdateFormModal(discord.ui.Modal):
    def __init__(self, user_data=None):
        super().__init__(title="Update Personal Information Form")
        self.add_item(discord.ui.TextInput(
            label="Your age range",
            default=user_data['age_range'] if user_data and 'age_range' in user_data else "Type one of the following options: '13-19', '20-39', '40-59', '+60'",
            placeholder = "Type one of the following options: '13-19', '20-39', '40-59', '+60'", 
            required=True,
            style=discord.TextStyle.long,
        ))
        self.add_item(discord.ui.TextInput(
            label="Your gender",
            default=user_data['gender'] if user_data and 'gender' in user_data else "Type one of the following options: 'Male', 'Female', 'Other'",
            placeholder= "Type one of the following options:'Male', 'Female', 'Other'",
            required=True,
            style=discord.TextStyle.long,
        ))
        self.add_item(discord.ui.TextInput(
            label="Languages you speak (separate with ',')",
            default=', '.join(user_data['languages']) if user_data and 'languages' in user_data else "English, Chinese, Spanish, Portuguese, Russian, French, German, Italian, Romanian",
            placeholder="'English', 'Chinese', 'Spanish', 'Portuguese', 'Russian', 'French', 'German', 'Italian', 'Romanian'",
            required=True,
            style=discord.TextStyle.long,
        ))
        self.add_item(discord.ui.TextInput(
            label="Your skill level",
            default=user_data['skill_level'] if user_data and 'skill_level' in user_data else "Type one of the following options: 'Beginner', 'Intermediate', 'Advanced', 'Expert' or 'Proficient'",
            placeholder="Type one of the following options: 'Beginner', 'Intermediate', 'Advanced', 'Expert' or 'Proficient'",
            required=True,
            style=discord.TextStyle.long,
        ))
        self.add_item(discord.ui.TextInput(
            label="Your preferred game type (separate with ',')",
            default=', '.join(user_data['game_types']) if user_data and 'game_types' in user_data else "Sandbox, Strategy, Shooter, MOBA, RPG, Simulation, Puzzlers, Action-adventure, Survival, Platformer",
            placeholder="Sandbox, Strategy, Shooter, MOBA, RPG, Simulation, Puzzlers, Action-adventure, Survival, Platformer",
            required=True,
            style=discord.TextStyle.long,
        ))
    # Function that is called when the user submits the form
    async def on_submit(self, interaction: discord.Interaction):
        age_range = ""
        gender = ""
        languages = ""
        skill_level = ""
        game_type = ""

        for item in self.children:  # Loop through all components added to the modal
            if item.label == "Your age range":
                age_range = item.value  # Access the value property of the TextInput
            elif item.label == "Your gender":
                gender = item.value
            elif item.label == "Languages you speak (separate with ',')":
                languages = item.value
            elif item.label == "Your skill level":
                skill_level = item.value
            elif item.label == "Your preferred game type (separate with ',')":
                game_type = item.value

        # Add languages and game type to lists
        languages_list = [string.strip() for string in languages.split(',')] # Splits the languages into a list
        preferredGameType_list = [string.strip() for string in game_type.split(',')] # Splits the game types into a list
       
        # Ensure all the strings are lowercase before the verifications
        gender = gender.lower()
        languages_list = [language.lower() for language in languages_list]
        skill_level = skill_level.lower()
        preferredGameType_list = [gameType.lower() for gameType in preferredGameType_list]
        
        # Validate all the fields
        if not is_valid_age_range(age_range): # If the age range is not valid
            await interaction.response.send_message(f"{interaction.user.mention} Update Form not submitted. Invalid Age Range.", ephemeral=True)
        elif not is_valid_gender(gender): # If the age range is not valid
            await interaction.response.send_message(f"{interaction.user.mention} Update Form not submitted. Invalid Gender.", ephemeral=True)
        elif not is_valid_language(languages_list): # If the age range is not valid
            await interaction.response.send_message(f"{interaction.user.mention} Update Form not submitted. Invalid Language.", ephemeral=True)
        elif not is_valid_skillLevel(skill_level): # If the age range is not valid
            await interaction.response.send_message(f"{interaction.user.mention} Update Form not submitted. Invalid Skill Level.", ephemeral=True)
        elif not is_valid_gameType(preferredGameType_list): # If the age range is not valid
            await interaction.response.send_message(f"{interaction.user.mention} Update Form not submitted. Invalid Preferred Game Type.", ephemeral=True)
        else: # If all the fields are valid
            user_data = {
                'user_id': interaction.user.id,  # Get user_id from interaction object
                'age_range': age_range,
                'gender': gender,
                'skill_level': skill_level,
                'languages': languages_list,  # This should be a list of language names
                'game_types': preferredGameType_list,  # This should be a list of game type names
            }
            await update_user(user_data) # Update the database with the new user data
            
            #Call the algorithms to get the possible gaming partners
            [first_algorithm_results_string, second_algorithm_results_string, third_algorithm_results_string] = await find_gaming_partners(interaction.user.id)
        
            await interaction.response.send_message(
                f"""{interaction.user.mention} Thank you for submitting your Updated Personal Information Form!

            {first_algorithm_results_string}
            {second_algorithm_results_string}
            {third_algorithm_results_string}""",
                ephemeral=True
            )
    
    