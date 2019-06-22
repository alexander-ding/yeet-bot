from cogs.base import Base
import discord
from discord.ext import commands

guilds_usage = "Returns the number of guilds I am in."
class Info(Base):
    @commands.command(name="guilds",
                      description=guilds_usage,
                      brief=guilds_usage,
                      pass_context=True)
    async def guilds(self, context):
        author = str(context.message.author)
        number_guilds = len(self.bot.guilds)
        await self.say(context, "This bot is in {} guilds. Spread me! Infect them all!".format(number_guilds))

def setup(bot):
    bot.add_cog(Info(bot))