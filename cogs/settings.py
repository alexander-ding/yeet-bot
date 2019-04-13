# TODO
from cogs.base import Base

from pathlib import Path
from PIL import Image
path_images = Path("pictures")


from collections import defaultdict

default = "_default_.png"
class Setting:
    default = default
    def __init__(self, foreground=default, width_ratio=1, height_ratio=1, x_shift=0, y_shift=0, rotation=0):
        self.foreground = foreground
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.rotation = rotation
    
    def get_foreground_image(self):
        return Image.open(path_images / self.foreground)
    
    @property
    def default_image_name(self):
        return Setting.default
    
    def __str__(self):
        return self.foreground
    
    def __repr__(self):
        return self.__str__()

class Settings(Base):
    def __init__(self, bot):
        # TODO: load settings file if existing
        super().__init__(bot)
        self.settings = defaultdict(Setting)

def setup(bot):
    bot.add_cog(Settings(bot))