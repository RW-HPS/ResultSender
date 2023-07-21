#!/bin/bash
#put your discord webhook here 
discord_webhook=https://discord.com/api/webhooks/1104425166366318724/sNM2A81tQdaboLkFlDvRlH8dMsL6RG66dTzAxHHM53IoVakCAKRdcK_dnDgoHAEBd8Cx

pkill screen
screen -S server -d -m
screen -S monitor -d -m
screen -r server -X stuff $"java -jar Server/RW-HPS-2.3.0-M3/StartServer/Server-All.jar\n"
screen -r monitor -X stuff $"python Server/send.py\n"
curl -i -H "Accept: application/json" -H "Content-Type:application/json" -X POST --data "{\"content\": \"Server restarted\"}" $discord_webhook