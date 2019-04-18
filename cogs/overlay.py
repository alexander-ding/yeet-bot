""" The cog class where the core overlay functionality is defined
"""
from discord.ext import commands
from cogs.base import Base
from utils.web import get_image

# setup for Dlib
import dlib
from dlib_models import download_model, download_predictor, load_dlib_models
download_model()
download_predictor()
from dlib_models import models

# all the little packages
from pathlib import Path
from PIL import Image
from imutils import face_utils
from io import BytesIO
import numpy as np
import cv2
from math import floor

overlay_usage = "Overlays the set filter over all faces in the input image. Image must have the suffix jpg, jpeg, or png.\nUsage: !yeet <urL> or !yeet, attaching an image to the message."
class Overlay(Base):
    def __init__(self, bot):
        super().__init__(bot)
        # get the Dlib models down
        load_dlib_models()
        self.face_detect = models["face detect"]
        self.face_rec_model = models["face rec"]
        self.shape_predictor = models["shape predict"]

    @commands.command(name='yeet',
                    description=overlay_usage,
                    brief="Overlays the set filter over all faces in the input image.",
                    aliases=['overlay'],
                    pass_context=True)
    async def overlay(self, context):
        # parsing command
        command_comps = str(context.message.content).strip().split()
        # needs to be either !yeet <url> or !yeet with attachment
        if len(command_comps) > 2:
            await self.say(context, overlay_usage)
            return

        url = command_comps[-1]
        
        # if there is attachment, get attachment url
        if len(context.message.attachments) > 0:
            ok, err, new_url = self.get_attachment_url(context)
            if not ok:
                await self.say(context, err)
                return
            url = new_url
        else:
            # if no url, then return usage
            if len(command_comps) == 1:
                await self.say(context, overlay_usage)
                return
        print(url)
        ok, err, background = get_image(url)
        if not ok:
            await self.say(context, err)
            return

        username = str(context.message.author)
        settings = self.bot.get_cog("Settings").settings
        foreground = settings[username].get_foreground_image()
        
        try:
            io_buffer = self.apply_overlay(background, foreground, settings[username])
        except Exception as e:
            await self.say(context, "Error overlaying! Sorry mate")
            print("Error: ", e)
            return
        await self.bot.send_file(context.message.channel, io_buffer, filename="new.jpeg")

    def get_orientation(self, img, rect):
        """ Get the orientation of the face (circled by the rect
            in the image) in degrees, clockwise
            The current method is quite faulty and a little iffy
            so perhaps I'll fix
        """
        shape = self.shape_predictor(np.array(img), rect)
        shape = face_utils.shape_to_np(shape)

        # grab the outlines of each eye from the input image
        leftEye = shape[36:42]
        rightEye = shape[42:48]

        # compute the center of mass for each eye
        leftEyeCenter = leftEye.mean(axis=0).astype("int")
        rightEyeCenter = rightEye.mean(axis=0).astype("int")

        dY = leftEyeCenter[1] - rightEyeCenter[1] 
        dX = leftEyeCenter[0] - rightEyeCenter[0]
        angle = np.rad2deg(np.arctan2(dY, dX)) 
        return angle+180


    def apply_overlay(self, background, foreground, settings):
        """ The actual function doing the math of overlaying foreground over
            all faces found in background with the supplied settings
        """

        # turn into RGB first
        if np.array(background).shape[-1] == 4:
            background = Image.fromarray(np.array(background)[:,:,:3])

        detections = list(self.face_detect(np.array(background)))
        for detection in detections:
            angle = self.get_orientation(background, detection)
            width_after = detection.width()*settings.width_ratio
            height_after = detection.height()*settings.height_ratio

            foreground_resized = foreground.resize((floor(width_after), floor(height_after)), Image.BICUBIC)
            foreground_resized = foreground_resized.rotate(-angle)

            left_after = detection.left()-detection.width()*(settings.width_ratio-1)/2
            left_after += settings.x_shift*width_after

            top_after = detection.top()-detection.height()*(settings.height_ratio-1)/2
            top_after += settings.y_shift*height_after
            try:
                background.paste(foreground_resized, (floor(max(0, left_after)), 
                                                    floor(max(0, top_after))), 
                                foreground_resized)
            except:
                background.paste(foreground_resized, (floor(max(0, left_after)), 
                                                    floor(max(0, top_after))))
                            
        io_buffer = BytesIO()
        background.save(io_buffer, "JPEG")
        io_buffer.seek(0)
        return io_buffer

def setup(bot):
    bot.add_cog(Overlay(bot))