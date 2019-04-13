""" The base class cog, with some common utility functions to inherit
"""

from discord.ext import commands

class Base:
    def __init__(self, bot):
        self.bot = bot
    
    async def say(self, context, msg):
        """ The client sends a message in response to the context, 
            mentioning the user who sent the command
        """
        return await self.bot.send_message(context.message.channel, "{} {}".format(msg, context.message.author.mention))

    def get_attachment_url(self, context):
        """ Gets an attachment from the message. Returns whether 
            the request was successful, a possible error string, and
            the url

            Returns
            -------
            (Bool, String, String)
        """
        return False, "Attachment is not yet supported.", None