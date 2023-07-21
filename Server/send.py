import os
import json
import time
import requests as req
from requests import get
from requests.structures import CaseInsensitiveDict
from discord_webhook import DiscordEmbed, DiscordWebhook
from datetime import datetime
from datetime import timedelta


#Script features:
#Server daily restart based on system time (this will fix bugs caused by running the server for too long)
#Server restart notification
#Post replay result to discord channel via webhook
#upload replay file to discord channel via webhook
#Send script error exceptions to discord channel via webhook

#replace with server folder name
serverVersion = "RW-HPS-2.3.0-M3"
#replace with the value from RW-HPS/StartServer/data/config.json 
AuthCookieValue = ""
#replace with your discord webhook
discord_wh = 'https://discord.com/api/webhooks/1131749935478489098/xKDL7i8xXlb4hFXTOgcnW_VwhBYvz2nxmqxNoajJE9_i77l6rFLThABkTT2WrxUfg0uz'
restart_time = "23:59:59"

keys = ['allPlayerList','winPlayerList','mapName','playerData','replayName']
keysToPrint = ["**Players:**\n","**Winners:**\n","**Chosen Map:**\n","**Player Stats:**\n","\n**Replay Name:**\n"]
count = 0

time.sleep(10)
while True:
    try:
        time.sleep(1)
        #make new cookie session after 1 day
        if (count%17000==0):
            url = "http://127.0.0.1:5000/HttpApi/api/AuthCookie?passwd=" + AuthCookieValue
            headers = CaseInsensitiveDict()
            resp = req.get(url)
            headers["Cookie"] = "HttpApi-Authentication="+resp.cookies['HttpApi-Authentication']
            print(headers)
        r = get('http://localhost:5000/HttpApi/api/get/event/GameOver',headers=headers)
        stringBuilder = ""
        count += 1
        print("Get game result #" + str(count))
        
        #time check for server reset, discord channel alert
        t1 = datetime.now()
        t2 = datetime.strptime(restart_time, "%H:%M:%S")
        timediff = t2 - t1
        timediff = timediff.seconds
        td = timedelta(seconds=timediff)

        message = "Server restart in "+str(timedelta(seconds=timediff))+"s."
        #Server sends countdown to server chat
        if(timediff < 11):
            print("say "+message)
            req.post("http://localhost:5000/HttpApi/api/post/run/ServerCommand", headers=headers, json={"RunCommand":"say "+message})
            if(timediff == 0):
                os.system("bash start.sh")
        
        #build message string
        response = r.text
        data = json.loads(response)
        data = json.loads(data["data"])
        if(len(data)>0):
            data = json.loads(data[0])
            print(data)
            matchTime = str(data['gameTime'])
            if(int(matchTime) < 60):
                continue
            replay = data['replayName']
            mapName = data['mapName']
            mapName = mapName.replace('_',' ')
            path = os.path.join(os.getcwd()+'/Server/'+ serverVersion +'/StartServer/data/replays/',replay)

            for i in range(len(keys)):
                if(i != 3):
                    stringBuilder += keysToPrint[i] 
                    temp = data[keys[i]]
                    if(i == 2 or i == 4):
                            stringBuilder += '`' 
                    for t in temp:
                        if(i != 2 and i != 4):
                            stringBuilder += '`' 
                        stringBuilder += str(t)
                        if(i != 2 and i != 4):
                            stringBuilder += "`\n"
                    if(i == 2 or i == 4):
                            stringBuilder += '`' 
            stringBuilder += '\n**Game time:**\n`'+ matchTime + 's`'
            print(stringBuilder)

            #payout ={
            #    'content': stringBuilder
            #}
            #req.post(URL,data=payout)

            time.sleep(10)
            webhook = DiscordWebhook(url=discord_wh)
            f = open(path, "rb")
            embed = DiscordEmbed(title= mapName, description=stringBuilder, color='03b2f8')
            webhook.add_embed(embed)
            webhook.add_file(file=f.read(), filename=replay)
            response = webhook.execute(remove_embeds=True)
            f.close()
            print("Replay uploaded to discord")
            os.remove(path)
            print("ReplayFile removed.")
    except Exception as error:
            req.post(discord_wh, {"content": "Error Exception: "+str(error)})
