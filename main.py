import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

trigger = ["chato", "chata", "fak", "bug", "agotada", "sad", "lata", "fome"]

starter_buenaonda = [
  "Animo!",
  "amigx, eri secx!",
  "Brilla.",
  "Igual ya es hora de un descanso uwu",
  "Weona vo podi!"
]

if "responding" not in db.keys():
  db["responding"] = True


def get_cat_fact():  # retorna un random fact sobre gatos
  response = requests.get(
      "https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=1")
  cat_fact = response.json()["text"]
  return cat_fact


def get_dog_fact():  # retorna un random fact sobre perros
  response = requests.get(
    "https://cat-fact.herokuapp.com/facts/random?animal_type=dog&amount=1")
  dog_fact = response.json()["text"]
  return dog_fact


def get_horse_fact():  # retorna un random fact sobre caballos
  response = requests.get(
    "https://cat-fact.herokuapp.com/facts/random?animal_type=horse&amount=1")
  horse_fact = response.json()["text"]
  return horse_fact


def update_buenaonda(buenaOnda_msg):  # Agrega frases buena onda desde el chat
  if "buenaOndas" in db.keys():
    buenaOndas = db["buenaOndas"]
    buenaOndas.append(buenaOnda_msg)
    db["buenaOndas"] = buenaOndas
  else:
    db['buenaOndas'] = [buenaOnda_msg]


def delete_buenaonda(index):  # Elimina frases de las agregadas desde el chat
  buenaOndas = db["buenaOndas"]
  if len(buenaOndas) > index:
    del buenaOndas[index]
    db["buenaOndas"] = buenaOndas

@client.event
async def on_ready():
  print('We are logged in as {0.user}'.format(client))

@client.event 
async def on_message(message):
  if message.author == client.user:   #ignora los mensajes del mismo bot
    return
  
  msg = message.content

  if msg.startswith('$cat'):    #Manda el fact cuando se mensiona en el chat
    fact = get_cat_fact()
    await message.channel.send(fact)

  if msg.startswith('$dog'):
    fact = get_dog_fact()
    await message.channel.send(fact)
  
  if msg.startswith('$horse'):
    fact = get_horse_fact()
    await message.channel.send(fact)

if db["responding"]:  #Solo hace las respuestas a msges sad si estan activadas
    options = starter_buenaonda

    if "buenaOndas" in db.keys():
      options = options + db["buenaOndas"]

    # manda las frases buena onda cuando se dice una palabra sad en el chat
    if any(word in msg for word in trigger):
      await message.channel.send(random.choice(options))
    elif "bot" in msg:
      await message.channel.send("Hola :)")
  
  if msg.startswith("$new"):
    buenaOnda_msg = msg.split("$new ", 1)[1]
    update_buenaonda(buenaOnda_msg)
    await message.channel.send("Se agrego el nuevo msge buena onda.")

  if msg.startswith("$del"):
    buenaOndas = []
    if "buenaOndas" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_buenaonda(index)
      buenaOndas = db["buenaOndas"]
    await message.channel.send(buenaOndas)

  if msg.startswith("$list"):
    buenaOndas = []
    if "buenaOndas" in db.keys():
      buenaOndas = db["buenaOndas"]
    await message.channel.send(buenaOndas)

  if msg.startswith("$responding"):
    
    if msg == "$responding" :
      if db["responding"]:
        await message.channel.send("Responding is on")
      else:
        await message.channel.send("Responding is off")
      return

    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true" or value.lower() == "1":
      db["responding"] = True
      await message.channel.send("Responding is on")
    elif value.lower() == "false" or value.lower() == "0":
      db["responding"] = False
      await message.channel.send("Responding is off")

  
keep_alive()
client.run(os.getenv('TOKEN'))