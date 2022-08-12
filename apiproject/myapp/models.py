from django.db import models
from django.db import models
import numpy as np
from rest_framework import serializers
from datetime import datetime, date
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import pandas as pd
from django.urls import path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from django.conf import settings


class Contact(models.Model):
    Description = models.CharField(max_length=200)
    Picture = models.ImageField(upload_to='covers/', blank=True)
    #Output = models.ImageField(upload_to='new/', blank=True)

    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)

        if self.Picture:
            pic = Image.open(self.Picture.path)
            pic = pic.resize((1066, 1048), Image.ANTIALIAS)
            bigsize = (pic.size[0] * 3, pic.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(pic.size, Image.ANTIALIAS)
            pic.putalpha(mask)

            output = ImageOps.fit(pic, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            output.save('output.png')

            font = ImageFont.truetype("OpenSans-Semibold.ttf", size=200)
            template = Image.open('media/new.jpg')
            template.paste(pic, (540, 200), pic)
            template.save('newpic.png')
            im = Image.open('newpic.png')
            ss = Image.open('media/new.jpg')
            im.paste(ss, (0,0), ss)
            draw = ImageDraw.Draw(im)
            draw.text((450, 1856), str(self.Description), font=font, fill='saddlebrown')
            im.save(self.Picture.path)

    def __str__(self):
        return self.Description

# Create your models here.

