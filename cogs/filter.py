from cogs.base import Base
import discord
from discord.ext import commands

from utils.web import get_image
from PIL import Image

import numpy as np
import cv2

default_usage = "Sets current filter to the default image and defaults all settings"
clean_usage = "Cleans the current filter's background and adds an alpha layer (if not already existing). \nUsage: !clean"
set_usage = "Sets the current filter to the supplied image. \nUsage: !set <url> or !set, attaching an image as the new filter"
class Filter(Base):
    @commands.command(name="default",
                      description=default_usage,
                      brief=default_usage,
                      pass_context=True)
    async def default(self, context):
        settings = self.bot.get_cog("Settings")
        author = str(context.message.author)
        settings.get(author).default()
        with open("data/pictures/{}".format(settings.get(author).foreground), mode="rb") as fp:
            await self.say(context, "Filter set to default. Beautiful as always", discord.File(fp, filename="default.png"))

    @commands.command(name='set',
                description="Sets your custom filter to superimpose on people's faces. Pass a link or an attachment! A filter is stored for each user",
                brief="Sets image to replace faces",
                pass_context=True)
    async def set_filter(self, context):
        # parsing command
        command_comps = str(context.message.content).strip().split()
        # needs to be either !yeet <url> or !yeet with attachment
        if len(command_comps) > 2:
            await self.say(context, set_usage)
            return

        url = command_comps[-1]
        
        # if there is attachment, get attachment url
        if len(context.message.attachments) > 0:
            ok, err, new_url = self.get_attachment_url(context)
            if not ok:
                await self.say(context, err)
                return
            url = new_url
        
        # if no url, then return usage
        if len(command_comps) == 1:
            await self.say(context, set_usage)
            return
        
        username = str(context.message.author)
        ok, err, filter_image = get_image(url)
        if not ok:
            await self.say(context, err)
            return
        
        settings = self.bot.get_cog("Settings")

        image_filename = "{}.{}".format(username, filter_image.format)
        # save the actual image
        filter_image.save("data/pictures/{}".format(image_filename))
        # save to settings
        settings.get(username).foreground = image_filename

        await self.say(context, "Gotcha homie")

    @commands.command(name='what',
                description="Shows what your current filter is",
                brief="What is your current filter?",
                pass_context=True)
    async def what(self, context):
        settings = self.bot.get_cog("Settings")
        author = str(context.message.author)
        image_name = settings.get(author).foreground
        d = settings.get(author).jsonify()

        settings_str = ""

        for k in d.keys():
            if k != "foreground":
                settings_str += "{}: {}\n".format(k,d[k])
        
        with open("data/pictures/{}".format(image_name), mode="rb") as fp:
            await self.say(context, "This is your current filter, with settings:\n"+settings_str, discord.File(fp, "filter.{}".format(image_name.split(".")[-1])))

    @commands.command(name='clean',
                      description=clean_usage,
                      brief="Cleans the *rim* of your current filter",
                      pass_context=True)
    async def clean(self, context):
        settings = self.bot.get_cog("Settings")
        author = str(context.message.author)
        # only people who do not have the default image as the current filter can clean
        if not settings.exists(author) and settings.get(author).foreground != "_default_.png":
            await self.say(context, "Set a filter first with !set")
            return
        im = settings.get(author).get_foreground_image()
        im = self.clean_image(im)

        with open("data/pictures/{}.png".format(author), mode="wb") as fp:
            im.save(fp)
        settings.set_foreground(author, "{}.png".format(author))
        with open("data/pictures/{}.png".format(author), mode="rb") as fp:
            await self.say(context, "Cleaned it up for ya", file=discord.File(fp, "cleaned.png"))

    def clean_image(self, img):
        """ Just a helper function. Cleans image's background and adds a transparency
            layer if it doesn't already have one. 
        """
        if np.array(img).shape[2] == 3: # no transparency
            return self.remove_background(img)
        return self.replace_white_with_transparent(img)

    def replace_white_with_transparent(self, img):
        data = list(img.getdata())
        data_new = []
        for point in data:
            if point[0] == 255 and point[1] == 255 and point[2] == 255:
                data_new.append((255,255,255,0))
            else:
                data_new.append(point)

        img.putdata(data_new)
        return img

    def remove_background(self, img):
        """ Removes the background of the image and adds a transparency layer
        """
        BLUR = 15
        CANNY_THRESH_1 = 10
        CANNY_THRESH_2 = 40
        MASK_DILATE_ITER = 10
        MASK_ERODE_ITER = 10
    
        img = np.array(img)
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

        #-- Edge detection -------------------------------------------------------------------
        edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
        edges = cv2.dilate(edges, None)
        edges = cv2.erode(edges, None)

        #-- Find contours in edges, sort by area ---------------------------------------------
        contour_info = []
        _, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # Previously, for a previous version of cv2, this line was: 
        #  contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # Thanks to notes from commenters, I've updated the code but left this note
        for c in contours:
            contour_info.append((
                c,
                cv2.isContourConvex(c),
                cv2.contourArea(c),
            ))
        contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
        max_contour = contour_info[0]

        #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
        # Mask is black, polygon is white
        mask = np.zeros(edges.shape)
        cv2.fillConvexPoly(mask, max_contour[0], (255))

        #-- Smooth mask, then blur it --------------------------------------------------------
        mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
        mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
        mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)

        #-- Blend masked img into MASK_COLOR background --------------------------------------
        masked = np.concatenate((img, mask[:,:,np.newaxis]), axis=2).astype('uint8')
        return Image.fromarray(masked)

def setup(bot):
    bot.add_cog(Filter(bot))