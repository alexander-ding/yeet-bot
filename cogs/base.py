""" The base class cog, with some common utility functions to inherit
"""
import discord
from discord.ext import commands

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def say(self, context, msg, file=None):
        """ The client sends a message in response to the context, 
            mentioning the user who sent the command
        """
        return await context.send("{} {}".format(msg, context.author.mention), file=file)

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