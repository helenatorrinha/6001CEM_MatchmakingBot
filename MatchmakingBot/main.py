import discord
from discord.ext import commands
import os
import asyncio
from Form import FormModal
from UpdateFormModal import UpdateFormModal

from apikeys import * #import bot's token

from database import create_database
from find_partners import find_gaming_partners
from database_helper import add_user, get_user_by_id, get_results

print("Starting bot...")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents) # Defines the commands' prefix

@client.event
async def on_ready(): # Event that is called when the bot is ready to receive commands (has finished logging in and setting things up)
    await client.tree.sync()
    print(f"Ready! Logged in as {client.user}")
    print("-----------------------------")
    # Check if 'database.db' exists, and if not, create the database
    if not os.path.exists('database.db'):
        print("Database not found, creating database...")
        create_database()
    else:
        print("Database already exists. Skipping creation.")
    
### Beggining of the code adapted from https://www.youtube.com/watch?v=rWfrdBAinvY&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=13

initial_extensions = []

for filename in os.listdir("./cogs"): # Loop to go through the files in the cogs folder
    if filename.endswith(".py"): # If the name of the file ends in .py
        initial_extensions.append("cogs." + filename[:-3]) 
 
@client.tree.command(name="form", description="Personal Information Form")   
async def form(interaction: discord.Interaction):
    user_data = await get_user_by_id(interaction.user.id)  # Get the user's data from the database
    if user_data:
        await interaction.response.send_message("You have already filled the Personal Information Form! Use /update to update your information", ephemeral=True) 
    else:
        await interaction.response.send_modal(FormModal())   

@client.tree.command(name="update", description="Update Personal Information Form")
async def form(interaction: discord.Interaction):
    user_data = await get_user_by_id(interaction.user.id)  # Get the user's data from the database
    if user_data:
        # If user data exists, initialize the modal with the user data
        await interaction.response.send_modal(UpdateFormModal(user_data=user_data))
    else:
        # If no user data is found
        await interaction.response.send_message("Update not available. You have filled the Personal Information Form before, please use the '/form' command to fill it.", ephemeral=True) 

@client.tree.command(name="results", description="Results of the algorithms")
async def results(interaction: discord.Interaction):
    user_data = await get_user_by_id(interaction.user.id)  # Get the user's data from the database
    if user_data:
        results = await get_results(interaction.user.id)
        await interaction.response.send_message(results, ephemeral=True)
    else:
        # If no user data is found
        await interaction.response.send_message("Results are not available. You have filled the Personal Information Form before, please use the '/form' command to fill it.", ephemeral=True) 

@client.tree.command(name="find_partners", description="Find the newest gaming partners")
async def find_partners(interaction: discord.Interaction):
    user_data = await get_user_by_id(interaction.user.id)  # Get the user's data from the database
    if user_data:
        #Call the algorithms to get the possible gaming partners
        [first_algorithm_results_string, second_algorithm_results_string, third_algorithm_results_string] = await find_gaming_partners(interaction.user.id)
        
        await interaction.response.send_message(
            f"""{interaction.user.mention} Here are your latest matches!

        {first_algorithm_results_string}
        {second_algorithm_results_string}
        {third_algorithm_results_string}""",
            ephemeral=True
        )
    else:
        # If no user data is found
        await interaction.response.send_message("Unable to find you gaming partners. You have filled the Personal Information Form before, please use the '/form' command to fill it.", ephemeral=True) 

async def main():
    for extension in initial_extensions:
        await client.load_extension(extension)
        
      
# Loads all the code in the files under the cogs folder    
if __name__ == "__main__":
    asyncio.run(main())
     
### End of the code adapted from https://www.youtube.com/watch?v=rWfrdBAinvY&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=13
     
        
# Bot's token that is used to run it  
client.run(BotToken) 