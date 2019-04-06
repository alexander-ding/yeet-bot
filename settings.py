from pathlib import Path
from PIL import Image
path_images = Path("pictures")

class Setting:
    def __init__(self, foreground="_default_.png", width_ratio=1, height_ratio=1, x_shift=0, y_shift=0, rotation=0):
        self.foreground = foreground
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.rotation = rotation
    
    def get_foreground_image(self):
        return Image.open(path_images / self.foreground)
    
    def __str__(self):
        return self.foreground
    
    def __repr__(self):
        return self.__str__()