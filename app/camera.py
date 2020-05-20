from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import datetime
import random
from firebase_admin import credentials, firestore
import uuid
from sense_hat import SenseHat
#from sense_emu import SenseHat
import pygame
from dotenv import firestoreCreds

sense = SenseHat()
def pingSensehat():
    X = [255, 0, 0]  # Red
        
    question_mark = [
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X
    ]

    sense.set_pixels(question_mark)
    time.sleep(0.5)
    sense.clear()


def pushData():
    ts = datetime.datetime.now().timestamp()
    
    timestamp = time.strftime('%H:%M:%S - %e/%m/%g')
    
    test = str(uuid.uuid1())
    COLLECTION = 'securepi'
    DOCUMENT = 'info'
    
        
    cred = credentials.Certificate(firestoreCreds)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    info = {
    u'latest_timestamp': timestamp
    }

    data = {
    u'timestamp': timestamp,
    u'spottedDate' : ts
    }
    


    db.collection(COLLECTION).document(DOCUMENT).set(info)
    db.collection('data').document(test).set(data)

    colors = [1752220,3066993,3447003,10181046,15844367,15105570,15158332,8359053,3426654,1146986,16580705,10038562]

    discordUrl = "https://discordapp.com/api/webhooks/710873217702690966/qWSLvbmBBKPsiu-cf8nxKrhyWqIXozQNM3ub1MiduRJvc9hU8zjr6brQsSuiPVGXoV6q"
    webhook = DiscordWebhook(url=discordUrl)
    embed = DiscordEmbed(title='New Camera Alert!',  color=random.choice(colors))
    embed.set_author(name="IOT", url="https://www.arteveldehogeschool.be/canvas/login", icon_url="https://www.gramma.be/sites/gramma.be/files/styles/project_detail_large/public/projects/g_artev_logo_vierkant_lo_rgb.jpg?itok=8_jzni4C")
    embed.set_thumbnail(url='https://www.pngitem.com/pimgs/m/352-3521496_cctv-camera-png-16-channel-security-camera-system.png', height="40", width="40")
    embed.set_footer(text='Created by Wouter Janssens & Senne Wancour')
    
    
    embed.add_embed_field(name='Timestamp', value= ("Spotted at {0}".format(timestamp)) )
    webhook.add_embed(embed)
    response = webhook.execute()
    
    for x in range(0,3):
        pingSensehat()
        time.sleep(0.25)
        
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/Documenten/SecurePi/alarm.mp3")
    pygame.mixer.music.play()
    time.sleep(4)
        
pushData()