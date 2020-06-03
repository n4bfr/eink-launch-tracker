#!/usr/bin/python
# -*- coding:utf-8 -*-

#beta05 - make row count variable
#beta06 - detect number of rows and adjust rd apropriately to continue loop

import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime, timedelta
import csv

#launch = datetime(2020, 06, 30)

#variable row count - RD is RowDisplay
rd = 1

#begin main loop

#initialize and clear screen

while rd  < 999:
    epd = epd2in7.EPD()
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the Horizontal image
    Himage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)  # 255: clear the frame

    # Horizontal
    draw = ImageDraw.Draw(Himage)
    font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
    font20 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 22)
    font14 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 14)
    bmp = Image.open('/home/pi/launch/sx3x250.bmp')
    Himage.paste(bmp, (20,2))

    with open("/home/pi/launch/launchlist.csv") as launchdata:
        ld_reader = csv.reader(launchdata)
        rows = list(ld_reader)

#get rowcount for managing loop
        row_count = sum(1 for row in rows)


#parse data from RD row by type

    for line in rows[rd]:
        fields = line.split(";")
        ship = fields[0]
        payload = fields[1]
        when = fields[2]
        lyr = fields[3]
        lmo = fields[4]
        ldy = fields[5]
    launchdata.close()

# turn date info into interger so it can be processed by datetime
    lyri = int(lyr)
    lmoi = int(lmo)
    ldyi = int(ldy)

# convert SKD and NET
    if when == ' SKD':
	when1 = "Scheduled For:"
    else:
        when1 = "No Earlier Than"

#Calculate days until launch date

    ldate1 =  datetime(lyri, lmoi, ldyi)
    fromtoday = datetime.now()
    delta = ldate1 - fromtoday	
    tminus = "Launch in T - " + str(delta.days) + " days"

    draw.text((35,44), ship + payload, font = font24, fill = 0)
    draw.text((84,76), when1, font = font14, fill = 0)
    draw.text((70,96), str(ldate1.strftime("%d-%b-%Y")), font = font24, fill = 0)
    draw.rectangle((0, 127, 275, 155), fill = 0)
    draw.text((20, 129), tminus, font = font20, fill = 1)
    draw.text((20,160), 'Current Date: ', font = font14, fill = 0)
    draw.text((120,160), str(fromtoday.strftime("%d-%b-%Y %H:%M")) , font = font14, fill = 0)
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)
        
    epd.sleep()

#wait 15 seconds
    time.sleep(150)

# increment the row to display
    rd += 1

    if rd == (row_count):
        rd = 1

else:
    exit()
