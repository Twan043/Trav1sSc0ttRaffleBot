import requests
import csv
import random
from threading import Thread
import time
from datetime import datetime
from colored import fg, attr
import random
from pyfiglet import Figlet
from discord_webhook import DiscordWebhook, DiscordEmbed, webhook
import json
from faker import Faker

def log(message, color):
    now = datetime.now().time()
    print(f'%s[{now}] [Travis Scott Raffle] [Task-{taskNum}] {message}%s' % (fg(color), attr(0)))


class Raffle:

    def __init__(self, taskJSON, taskNum):
        self.taskNum = taskNum
        self.email = taskJSON["email"]
        self.size = taskJSON["size"]

    def enter(self):
        s = requests.Session()
        log('Starting task', 45)

        while True:
         try:
             lines = open('proxies.txt').read().splitlines()
             proxy = random.choice(lines)
             split = proxy.split(':')
             good_format = (f'{split[2]}:{split[3]}@{split[0]}:{split[1]}')
             http_proxy = f"{good_format}"
             https_proxy = f"{good_format}"
             proxyDict = {
                          "http": f'http://{http_proxy}',
                          "https": f'http://{https_proxy}'}
         except Exception as e:
             print(e)
             log('Error getting proxies, you can only run with proxies, will be fixed soon', 196)
             time.sleep(10)
             exit()             
         else:
             break


        while True:
            try:
                response = s.get('https://shop.travisscott.com/', proxies=proxyDict)
            except Exception as e:
                print(e)
                time.sleep(delay)
            if response.status_code == 200:
                log('Succesfully got raffle page', 3)
                break

        while True:
            try:
                faker = Faker()
                first = faker.first_name()
                last = faker.last_name()
                zip = faker.postcode()
                n = '0000000000'
                while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
                    n = str(random.randint(10**9, 10**10-1))
                phone = n[:3] + '-' + n[3:6] + '-' + n[6:]
                response = s.get(f'https://f1eb5xittl.execute-api.us-east-1.amazonaws.com/fragment/submit?a=m&email={self.email}&first={first}&last={last}&zip={zip}&telephone={phone}&product_id=6732003639423&kind=shoe&size={self.size}', proxies=proxyDict)
            except Exception as e:
                print(e)
                time.sleep(delay)
            else:
                try:
                    if 'thanks' in response.text:
                        log('Succesfully entered raffle')
                        break
                except Exception as e:
                    print(e)
                    time.sleep(delay)

        log('Sending webhook', 45)
        web_hook = DiscordWebhook(url=f'{hook}', username='Travis Scott Raffle Bot')
        embed = DiscordEmbed(title=f'Succesfully entered raffle!', url=f'https://shop.travisscott.com/', color=65280)
        embed.add_embed_field(name='Email', value=f'{self.email}', inline=False)
        embed.add_embed_field(name='First Name', value=f'{first}', inline=False)
        embed.add_embed_field(name='Last Name', value=f'{last}', inline=False)
        embed.add_embed_field(name='Zip', value=f'{zip}', inline=False)
        embed.add_embed_field(name='Phone', value=f'{phone}', inline=False)
        embed.add_embed_field(name='Size', value=f'{self.size}', inline=False)
        embed.set_footer(text=f'made by twan#0002 {str(datetime.now())}', icon_url='https://cdn.discordapp.com/attachments/691974179226124298/860216509464444978/twanaio.jpg')
        web_hook.add_embed(embed)
        web_hook.execute()



with open('config.json') as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()
delay = int(jsonObject['delay'])
hook = jsonObject['webhook']


task_reader = csv.DictReader(open("travis.csv", 'r'))
for task in task_reader:
    if task_reader.line_num == 1:
        continue
    else:
        taskNum = str(task_reader.line_num - 1)
        Thread(target=Raffle(task, taskNum).enter).start()
