import json
import requests
import random
import html
import discord
from discord.ui import View, Button

def get_info_willfry(category):
  response = requests.get(f"https://api.trivia.willfry.co.uk/questions?categories={category}&limit=1")

  json_data = json.loads(response.text)

  return json_data

def get_info_opentdb(level, topic):

  if topic == "gk":
    category = 9

  elif topic == "s&n":
    category = 17
  
  elif topic == "s&c":
    category = 18
  
  elif topic == "s&m":
    category = 19

  elif topic == "myth":
    category = 20

  elif topic == "geography":
    category = 22

  elif topic == "history":
    category = 23
  
  elif topic == "anime":
    category = 31

  response = requests.get(f"https://opentdb.com/api.php?amount=1&category={category}&difficulty={level}&type=multiple")

  json_data = json.loads(response.text)

  json_data["results"][0]["question"] = html.unescape(json_data["results"][0]["question"])

  json_data["results"][0]["correct_answer"] = html.unescape(json_data["results"][0]["correct_answer"])

  json_data["results"][0]["incorrect_answers"][0] = html.unescape(json_data["results"][0]["incorrect_answers"][0])
  
  json_data["results"][0]["incorrect_answers"][1] = html.unescape(json_data["results"][0]["incorrect_answers"][1])
  
  json_data["results"][0]["incorrect_answers"][2] = html.unescape(json_data["results"][0]["incorrect_answers"][2])

  # category = 'music'
  # api_url = 'https://api.api-ninjas.com/v1/trivia?category={}'.format(category)
  # response = requests.get(api_url, headers={'X-Api-Key': 'a30SaguL/wnOSlAb+VmSzQ==I0OfE64CE1DxgnUP'})
  # if response.status_code == requests.codes.ok:
  #     print(response.text)
  # else:
  #     print("Error:", response.status_code, response.text)

  return json_data



########################################################################

with open("sp_data.json", "r") as f:
  set_preferencer = json.load(f)

def set_preference(difficulty, topic, user):
  str(user)
  set_preferencer[f"{user}"] = [f"{difficulty}", f"{topic}"]

  with open("sp_data.json", "w") as f:
    json.dump(set_preferencer, f)

########################################################################

with open("levels_data.json", "r") as f:
  candy = json.load(f)

def deposit(user, candy_amount):
  if str(user) not in candy:
    candy[str(user)] = candy_amount
  
  else:
    candy[str(user)] = candy[str(user)] + candy_amount

  with open("levels_data.json", "w") as f:
    json.dump(candy, f)

def show_candy(user):
  if user not in candy:
    return "not there"
  else:
    return candy[str(user)]

########################################################################    

help_embed = discord.Embed(title="Commands",
  description="Commands on TriviaBot",
  colour=discord.Colour.from_rgb(0, 255, 132))

help_embed.add_field(
  name='-Q',
  value=
  f"Get a question with the format\n`-Q [level] [topic]`\n IT IS NOT POSSIBLE TO JUST DO -Q WITHOUT HAVING FIRST SET A PREFERENCE. ",
  inline=False  
)

help_embed.add_field(
  name='-pref',
  value=
  f"Set a preference so you don't have to type in the full command. Format:\n`-setPref [difficulty] [topic]`",
  inline=False
)

help_embed.add_field(
  name='-list',
  value = f"List of all the topics and difficulties currently available at the moment.",
  inline = False
)

help_embed.add_field(
  name='-candy',
  value = f"This will show how much candy you have ONLY if you have answered one or more questions. **Difficulty Ramping**:\nEasy - 1 candy\nMedium - 3 candies\nHard - 5 candies",
  inline = False
)

###############################################################

list_embed = discord.Embed(title="Topics & Difficulties",
  description="List of Topics & Difficulties",
  colour=discord.Color.from_rgb(140, 54, 173))

list_embed.add_field(
  name = "Difficulties",
  value = f"""- Hard\n- Medium\n - Easy""",
  inline = False  
)

list_embed.add_field(
  name = "Topics",
  value = 
f"""
- Geography
- History
- GK (General Knowledge)
- S&N (Science & Nature)
- S&C(Science and Computers)
- S&M(Science & Math)
- Myth(Mythology)
- Anime (Enterainment: Japanese Anime & Manga)
""",
  inline = False
)

##############################################################################################################################

def question_logic(ctx = None, user = None, user_id = None, tb = False):
  if tb == True:
    hardness = "hard"
    subject = random.choice(["history", "geography", "gk", "s&n", "s&c", "s&m", "mythology", "anime"]) 
  
  else:
    e = str(ctx.content).lower()

    if len(str(ctx.content)) == 2 and str(ctx.author.id) not in set_preferencer:
      return "No pref"

    else:
      if len(str(ctx.content)) > 9:
        hardness = e.lower().split()[1]
        subject = e.lower().split()[2]

      elif str(ctx.author.id) in set_preferencer:
        hardness = set_preferencer[str(ctx.author.id)][0]
        subject = set_preferencer[str(ctx.author.id)][1]

  info = get_info_opentdb(hardness, subject)

  question = info["results"][0]["question"]
  correct = info["results"][0]["correct_answer"]
  a = info["results"][0]["incorrect_answers"]

  a.append(info["results"][0]["correct_answer"])
  random.shuffle(a)

  embed = discord.Embed(title=f"{question}", colour=0x11806a)

  embed.add_field(
      name='Answers',
      value=f"A. {a[0]}\nB. {a[1]}\nC. {a[2]}\nD. {a[3]}\n",
      inline=False)

  embed.set_footer(text=f"This is question is categorized under '{hardness} {subject}'")

  if a.index(correct) == 0:
    correct_location = "ans_choice_a"

  if a.index(correct) == 1:
    correct_location = "ans_choice_b"
  
  if a.index(correct) == 2:
    correct_location = "ans_choice_c"
  
  if a.index(correct) == 3:
    correct_location = "ans_choice_d"

  view = triviaOptions(user_id, correct, hardness, correct_location, tb=True)

  return [embed, view]   

########################################################################

class triviaOptions(View):
  def __init__(self, user_id, correct, hardness, correct_location, tb=False):
    super().__init__()
    self.user_id = user_id
    self.correct = correct
    self.hardness = hardness
    self.correct_location = correct_location
    self.tb = tb

  @discord.ui.button(emoji="🇦", style=discord.ButtonStyle.blurple, custom_id="ans_choice_a")
  async def a_button_callback(self, button, interaction):
    for x in self.children:
      x.disabled = True

    await interaction.response.edit_message(view=self)

    if interaction.data["custom_id"] == self.correct_location:

      if self.hardness == "easy":
        deposit(self.user_id, 1)
        the_amount_of_candy = 1
      
      if self.hardness == "medium":
        deposit(self.user_id, 3)
        the_amount_of_candy = 3

      if self.hardness == "hard":
        deposit(self.user_id, 5)
        the_amount_of_candy = 5

      await interaction.followup.send(f"Correct! You have earned {the_amount_of_candy} 🍭")

    else:
      await interaction.followup.send(f"Incorrect; the answer was {self.correct}.")

  @discord.ui.button(emoji="🇧", style=discord.ButtonStyle.blurple, custom_id="ans_choice_b")
  async def b_button_callback(self, button, interaction):
    for x in self.children:
      x.disabled = True

    await interaction.response.edit_message(view=self)

    if interaction.data["custom_id"] == self.correct_location:

      if self.hardness == "easy":
        deposit(self.user_id, 1)
        the_amount_of_candy = 1
      
      if self.hardness == "medium":
        deposit(self.user_id, 3)
        the_amount_of_candy = 3

      if self.hardness == "hard":
        deposit(self.user_id, 5)
        the_amount_of_candy = 5

      await interaction.followup.send(f"Correct! You have earned {the_amount_of_candy} 🍭")


    else:
      await interaction.followup.send(f"Incorrect; the answer was {self.correct}.")

  @discord.ui.button(emoji="🇨", style=discord.ButtonStyle.blurple, custom_id="ans_choice_c")
  async def c_button_callback(self, button, interaction):
    for x in self.children:
      x.disabled = True

    await interaction.response.edit_message(view=self)

    if interaction.data["custom_id"] == self.correct_location:

      if self.hardness == "easy":
        deposit(self.user_id, 1)
        the_amount_of_candy = 1
      
      if self.hardness == "medium":
        deposit(self.user_id, 3)
        the_amount_of_candy = 3

      if self.hardness == "hard":
        deposit(self.user_id, 5)
        the_amount_of_candy = 5

      await interaction.followup.send(f"Correct! You have earned {the_amount_of_candy} 🍭")

    else:
      await interaction.followup.send(f"Incorrect; the answer was {self.correct}.")

  @discord.ui.button(emoji="🇩", style=discord.ButtonStyle.blurple, custom_id="ans_choice_d")
  async def d_button_callback(self, button, interaction):
    for x in self.children:
      x.disabled = True

    await interaction.response.edit_message(view=self)

    if interaction.data["custom_id"] == self.correct_location:

      if self.hardness == "easy":
        deposit(self.user_id, 1)
        the_amount_of_candy = 1
      
      if self.hardness == "medium":
        deposit(self.user_id, 3)
        the_amount_of_candy = 3

      if self.hardness == "hard":
        deposit(self.user_id, 5)
        the_amount_of_candy = 5

      await interaction.followup.send(f"Correct! You have earned {the_amount_of_candy} 🍭")

    else:
      await interaction.followup.send(f"Incorrect; the answer was {self.correct}.")

  async def interaction_check(self, interaction) -> bool:
    if str(interaction.user.id) != self.user_id:
      await interaction.response.send_message("This question is not for you!", ephemeral=True)
      return False
    else:
      return True


###################################################################################################
