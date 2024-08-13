import discord
from validators import is_valid_age_range, is_valid_gender, is_valid_language, is_valid_skillLevel, is_valid_gameType
from find_partners import find_gaming_partners
from database_helper import add_user


# Code adapted from https://www.youtube.com/watch?v=AGEpzKqnTvU&list=PLhSv6ICUmoIfdh2s-JdXQFbC0Sc3uGpww&index=1&t=48s\ 
class FormModal(discord.ui.Modal, title="Personal Information Form"):
    ageRange = discord.ui.TextInput(label="Your age range", placeholder="Type one of the following options: '13-19', '20-39', '40-59', '+60'", required=True, style=discord.TextStyle.long)
    gender = discord.ui.TextInput(label="Your gender", placeholder="Type one of the following options: 'Male', 'Female', 'Other'", required=True, style=discord.TextStyle.long)
    languages = discord.ui.TextInput(label="Languages you speak (separate with ',')", placeholder="'English', 'Chinese', 'Spanish', 'Portuguese', 'Russian', 'French', 'German', 'Italian', 'Romanian'", required=True, style=discord.TextStyle.long)
    skillLevel = discord.ui.TextInput(label="Your skill level", placeholder="Type one of the following options: 'Beginner', 'Intermediate', 'Advanced', 'Expert' or 'Proficient'", required=True, style=discord.TextStyle.long)
    preferredGameType = discord.ui.TextInput(label="Your preferred game type (separate with ',')", placeholder="Sandbox, Strategy, Shooter, MOBA, RPG, Simulation, Puzzlers, Action-adventure, Survival, Platformer", required=True, style=discord.TextStyle.long)

    # Function that is called when the user submits the form
    async def on_submit(self, interaction: discord.Interaction):
        
        # Add languages and game type to lists
        languages_list = [string.strip() for string in self.languages.value.split(',')] # Splits the languages into a list
        preferredGameType_list = [string.strip() for string in self.preferredGameType.value.split(',')] # Splits the game types into a list
       
        # Ensure all the strings are lowercase before the verifications
        gender = self.gender.value.lower()
        languages_list = [language.lower() for language in languages_list]
        skillLevel = self.skillLevel.value.lower()
        preferredGameType_list = [gameType.lower() for gameType in preferredGameType_list]
        
        # Validate all the fields
        if not is_valid_age_range(self.ageRange.value): # If the age range is not valid
            await interaction.response.send_message(f"{interaction.user.mention} Form not submitted. Invalid Age Range.", ephemeral=True)
        elif not is_valid_gender(gender): # If the age range is not valid
            await interaction.response.send_message(f"{interaction.user.mention} Form not submitted. Invalid Gender.", ephemeral=True)
        elif not is_valid_language(languages_list): # If the age range is not valid
            await interaction.response.send_message(f"{interaction.user.mention} Form not submitted. Invalid Language.", ephemeral=True)
        elif not is_valid_skillLevel(skillLevel): # If the age range is not valid
            await interaction.response.send_message(f"{interaction.user.mention} Form not submitted. Invalid Skill Level.", ephemeral=True)
        elif not is_valid_gameType(preferredGameType_list): # If the age range is not valid
            await interaction.response.send_message(f"{interaction.user.mention} Form not submitted. Invalid Preferred Game Type.", ephemeral=True)
        else:
            # Call the add_use function to add an user and their form's responses into the database
            await add_user(interaction.user.id, interaction.user.name, self.ageRange.value, gender, languages_list, skillLevel, preferredGameType_list)
            
            #Call the algorithms to get the possible gaming partners
            [first_algorithm_results_string, second_algorithm_results_string, third_algorithm_results_string] = await find_gaming_partners(interaction.user.id)
            
            await interaction.response.send_message(    
                f"""{interaction.user.mention} Thank you for submitting your Personal Information Form!

            {first_algorithm_results_string}
            {second_algorithm_results_string}
            {third_algorithm_results_string}
            """,
                ephemeral=True
            )
        