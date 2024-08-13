import discord
from discord.ext import commands

class Greetings(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.channel_id = 1198647460361404507 # Id for the general text channel of the server
    
    # Function called when a user types !hello    
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello, I am the Matchmaking Bot.")    
        
    # Function called when a user types !goodbye
    @commands.command()
    async def goodbye(self, ctx):
        await ctx.send("Byebye.") 
    
 
    ### Beggining of the code adapted from https://www.youtube.com/watch?v=ksAtGCFxrP8&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=2     
            
    # Function called when a user joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(self.channel_id) # Channel id where the message is going to be sent
        
        if (self.check_channel(channel, self.channel_id)):
            await channel.send(f"Welcome to the server, {member.mention}. Would you like to find a perfect gaming partner? \U0001F3AE Use '/form' to fill the Personal Information Form and find gaming partners!") #\U0001F3AE is the unicode for the Video Game emoji
        
    # Function called when a user leaves the server
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(self.channel_id) #Channel id where the message is going to be sent
    
        if (self.check_channel(channel, self.channel_id)):
            await channel.send(f"Goodbye, {member.name}. \U0001F44B") #\U0001F44B is the unicode for the Waving Hand emoji    

    # Function to check if the channel exists    
    def check_channel (self, channel, channel_id):
        if channel: # If the variable channel contains something
            return True
        else: # Otherwise the channel does not exist
            print(f"Channel {channel_id} not found.") 
            return False        
    
    ### End of the code adapted from https://www.youtube.com/watch?v=ksAtGCFxrP8&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=2     
    
async def setup(client):
    await client.add_cog(Greetings(client))