from functions import triviaOptions, show_candy, set_preference, set_preferencer, help_embed, list_embed, question_logic, candy
import os
import discord
import random

client = discord.Bot(command_prefix="-")

global gameOn
gameOn = False

@client.event
async def on_ready():
  print('We are in as {0.user}'.format(client))
  game = discord.Game("-help")
  await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(ctx):  
  if "-help" in str(ctx.content).lower():
    await ctx.channel.send(embed=help_embed)

  if "-candy" in str(ctx.content).lower():
    if show_candy(str(ctx.author.id)) ==  "not there":
      await ctx.channel.send("Answer questions to gain candy!")
    
    else:
      embed = discord.Embed(title=f"{ctx.author}'s' Candy", description=f"You have {show_candy(str(ctx.author.id))} 🍭", colour=discord.Colour.from_rgb(1, 74, 35))

      await ctx.channel.send(embed=embed)

  if "-pref" in str(ctx.content).lower():
    trueDiffs = ["easy", "medium", "hard"]
    trueTopics = ["history", "geography", "gk", "s&n", "s&c", "s&m", "myth", "anime"]

    if str(ctx.content).lower().split()[1] in trueDiffs and str(ctx.content).lower().split()[2] in trueTopics:
      difficulty = str(ctx.content).lower().split()[1]
      topic = str(ctx.content).lower().split()[2]
      
      set_preference(difficulty, topic, str(ctx.author.id))
      await ctx.channel.send(f"Successfully set to `{difficulty} {topic}`")
    else:
      await ctx.channel.send("Invalid topic or difficulty. For a list of all topics and difficulties do -list")
      

  if "-list" in str(ctx.content).lower():
    await ctx.channel.send(embed=list_embed)

  if "-q" in str(ctx.content).lower():
    
    info = question_logic(ctx, user_id=str(ctx.author.id))
    
    if info == "No pref":
      await ctx.channel.send("Since you have not yet set a preference, try doing -q easy history. -list for more subjects and difficulties. If you want to set a preference, try something like -pref easy history. Then, each time, until you change your pref, you will get a easy history question when you enter -q.")
    else: 
      await ctx.channel.send(embed = info[0], view = info[1])

  if "-tb " in str(ctx.content).lower():
    disallowed_characters="<!@>"

    challenger = str(ctx.content).split()[1]

    for x in disallowed_characters:
      challenger = challenger.replace(x, "")

    global turn
    turn = 0

    global gameOn
    gameOn = True

    global tbBattleBetween
    tbBattleBetween = [str(ctx.author.id), challenger]

    global score
    score = [0, 0]

    tb_embed = discord.Embed(
      title= f"Trivia Battle",
      colour=discord.Colour.from_rgb(0, 255, 132)
      )
    
    tb_embed.add_field(name="Score", value=f"<@{ctx.author.id}>: 0 points\n{str(ctx.content).split()[1]}: 0 points")

    tb_embed.add_field(name="How to play", value=f"The person who entered the command -tb will always start first. Turns will alternate until one person wins by getting 5 questions right. If it is your turn, do -tbques to get a question. If you want to leave/give up, you have enter the command -resign, ending the game.")

    await ctx.channel.send(embed=tb_embed)

  if "-tbques" in str(ctx.content).lower():
    if gameOn:
      if str(ctx.author.id) != tbBattleBetween[turn % 2]:
        await ctx.channel.send("Not your turn")
      else:
        if turn % 2 == 0:
          info = question_logic(user_id=tbBattleBetween[0], tb=True)

          await ctx.channel.send(embed = info[0], view = info[1])

          turn += 1

        elif turn % 2 == 1:
          info = question_logic(user_id=tbBattleBetween[1], tb=True)
    
          await ctx.channel.send(embed = info[0], view = info[1])

          turn += 1
    else:
      await ctx.channel.send("No game has started")

  if "Correct" in str(ctx.content) or "Incorrect" in str(ctx.content) and ctx.author == client.user:
    if gameOn == False:
      return
    else:
      if "Correct" in str(ctx.content):
        score[turn %2 - 1] += 1

        await ctx.channel.send(f"The score is now <@{tbBattleBetween[0]}> {score[0]} - {score[1]} <@{tbBattleBetween[1]}>")

      if "Incorrect" in str(ctx.content):
        await ctx.channel.send(f"The score is now <@{tbBattleBetween[0]}> {score[0]} - {score[1]} <@{tbBattleBetween[1]}> (No change).")
    
    if score[0] == 5 or score[1] == 5:
      if score[0] == 5:
        winner = tbBattleBetween[0]
      elif score[1] == 5:
        winner = tbBattleBetween[1]

      await ctx.channel.send(f"Game over <@{winner}> is the winner!")
      
      gameOn = False  

  if "-resign" in str(ctx.content).lower():
    if gameOn:
      gameOn = False

      if tbBattleBetween[0] == str(ctx.author.id):
        winner = tbBattleBetween[1]

      if tbBattleBetween[1] == str(ctx.author.id):
        winner = tbBattleBetween[0]
        
      await ctx.channel.send(f"Game over <@{winner}> is the winner!")

    else:
      return
    
  if "-rankings" in str(ctx.content).lower():
    sorted_candy = {k: v for k, v in sorted(candy.items(), key=lambda item: item[1], reverse=True)}
 
    stringthing = ""

    x = 1

    for key in sorted_candy:

      stringthing += f"\n{x}) <@{key}> {sorted_candy[key]} 🍭"

      x += 1

    rankings = discord.Embed(
      title= f"Rankings",
      colour=discord.Colour.from_rgb(0, 123, 132)
      )

    rankings.add_field(name="Down the list", value = f"{stringthing}")

    await ctx.channel.send(embed=rankings)

client.run(#insert token here)

