from cogs.base import Base

import atexit
import json
from pathlib import Path
from PIL import Image

import discord
from discord.ext import commands

path_data = Path("data")
path_images = path_data / "pictures"


from collections import defaultdict

scale_usage = "Set width/height ratio to apply to filter.\nUsage: !scale [direction (x or y)] [scale]. Example: !scale x 1.5. Omitting direction applies scale to both x and y, like !scale 1.5. "
shift_usage = "Shift the filter by a fraction of the filter's own size\nUsage: !shift [direction (x or y)] [amount (size of filter)]. Example: !shift y -0.5. This shifts the filter on the y axis by half of the filter's height. "

default = "_default_.png"


class Setting:
    def __init__(self, foreground=default, width_ratio=1, height_ratio=1, x_shift=0, y_shift=0, rotation=0):
        self.foreground = foreground
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.x_shift = x_shift
        self.y_shift = y_shift

    def get_foreground_image(self):
        return Image.open(path_images / self.foreground).convert("RGBA")
    
    def jsonify(self):
        return {
            "foreground": self.foreground,
            "width_ratio": self.width_ratio,
            "height_ratio": self.height_ratio,
            "x_shift": self.x_shift,
            "y_shift": self.y_shift,
        }
    
    def default(self):
        self.__init__()

    def __str__(self):
        return self.foreground
    
    def __repr__(self):
        return self.__str__()

class Settings(Base):
    default = default
    def __init__(self, bot):
        super().__init__(bot)
        self.settings = defaultdict(Setting)
        self.load()
        self.save()
        atexit.register(self.save)
    
    @commands.command(name='scale',
                description=scale_usage,
                brief="Set width/height ratio to apply to filter.",
                pass_context=True)
    async def scale(self, context):
        cmds = str(context.message.content).split(" ")
        if len(cmds) not in [2,3]:
            await self.say(context, scale_usage)
            return

        try:
            scale = float(cmds[-1])
            assert(scale > 0)
        except:
            await self.say(context, "Last value must be a positive number")
            return

        if len(cmds) == 3:
            direction = cmds[1]
            if direction not in ["x", "y"]:
                await self.say(context, "Direction must be x or y")
                return
        else:
            direction = "x and y"

        settings = self.bot.get_cog("Settings")
        author = str(context.message.author)
        
        if "x" in direction:
            self.get(author).width_ratio = scale
        if "y" in direction:
            self.get(author).height_ratio = scale
        
        await self.say(context, "Direction {}'s scale set to {}".format(direction, scale))

    @commands.command(name='shift',
                description=shift_usage,
                brief="Shift the filter by a fraction of the filter's own size",
                pass_context=True)
    async def shift(self, context):
        cmds = str(context.message.content).split(" ")
        if len(cmds) != 3:
            await self.say(context, shift_usage)
            return

        try:
            displacement = float(cmds[-1])
        except:
            await self.say(context, "Last value must be a number")
            return

        direction = cmds[1]
        if direction not in ["x", "y"]:
            await self.say(context, "Direction must be x or y")
            return

        settings = self.bot.get_cog("Settings")
        author = str(context.message.author)
        
        if "x" in direction:
            self.get(author).x_shift = displacement
        if "y" in direction:
            self.get(author).y_shift = displacement
        
        await self.say(context, "Direction {} will now be displaced by {}*filter {}".format(direction, displacement, "width" if "x" in direction else "height"))

    def load(self):
        """ Loads the saved setting
        """
        # do nothing if settings file does not exist
        if not (path_data / "settings.json").exists():
            return

        with open(path_data / "settings.json", "r") as f:
            d = json.load(f)
            for key in d.keys():
                self.settings[key] = Setting(**d[key])

    def save(self):
        """ Saves the setting
        """
        with open(path_data / "settings.json", "w") as f:
            d = {}
            for key in self.settings.keys():
                d[key] = self.settings[key].jsonify()
            
            f.write(json.dumps(d))

    def get(self, user):
        return self.settings[user]
    
    def exists(self, user):
        return user in self.settings.keys()
    
    def set_foreground(self, user, foreground):
        self.settings[user].foreground = foreground

    @property
    def default_image_name(self):
        return Settings.default

def setup(bot):
    bot.add_cog(Settings(bot))