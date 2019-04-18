""" The base class cog, with some common utility functions to inherit
"""
import discord
from discord.ext import commands

class Base:
    def __init__(self, bot):
        self.bot = bot
        self.is_setup = False

    async def setup(self):
        """ Sets the status of the bot to display help text
        """
        help_text = "!help for more information"
        await self.bot.change_presence(game=discord.Game(name=help_text))
    
    async def say(self, context, msg):
        """ The client sends a message in response to the context, 
            mentioning the user who sent the command
        """
        # this is a workaround -- update as soon as any bot command is used
        # ideally I'd like to use the onstartup event, but there are some complications
        if not self.is_setup:
            await self.setup()
        return await self.bot.send_message(context.message.channel, "{} {}".format(msg, context.message.author.mention))

    def get_attachment_url(self, context):
        """ Gets an attachment from the message. Returns whether 
            the request was successful, a possible error string, and
            the url

            Returns
            -------
            (Bool, String, String)
        """
        if (len(context.message.attachments) == 0):
            return False, "No attachment found!", ""
        
        return True, None, str(context.message.attachments[0]['url'])