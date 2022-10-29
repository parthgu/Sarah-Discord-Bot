import os
import discord
import openai
from keep_alive import keep_alive
import requests
import json

intents = discord.Intents.all()

client = discord.Client(intents=intents)
openai.api_key = os.environ['OPEN_AI_KEY']


def getRandomCompliment():
  response = requests.get("https://complimentr.com/api")
  json_data = json.loads(response.text)
  compliment = json_data['compliment']
  return compliment


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  m = message.content
  if message.author == client.user:
    return
  if message.content.startswith('!hello'):
    await message.channel.send('Hello ' + message.author.name + ", " +
                               getRandomCompliment())
  elif message.content.startswith('!help'):
    await message.channel.send(
      'I will respond to you if you start your sentence with "!"')
  elif message.content.startswith('!'):
    response = openai.Completion.create(model="text-curie-001",
                                        prompt=m[1:],
                                        temperature=0,
                                        max_tokens=65)
    await message.channel.send(response.choices[0].text)


keep_alive()
client.run(os.environ['TOKEN'])
