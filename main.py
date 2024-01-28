import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

tasks = {}


@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')


@bot.command(name='help')
async def help_command(ctx):
  embed = discord.Embed(title='Help Menu', color=0x2b71ec)
  embed.set_author(
      name='Pomodoro Buddy',
      icon_url=
      'https://media.discordapp.net/attachments/1200681000729055262/1200843764307087390/ZJ6QVJaOdFAiRAAg0j8P8BJLQVApTylgAAAAASUVORK5CYII.png'
  )
  embed.add_field(
      name='__**STATS :**__',
      value=
      f'> **📊 Bot in servers:** {len(bot.guilds)}\n> **🟢 Bot Ping:** {round(bot.latency * 1000)}ms\n>',
      inline=False)
  embed.add_field(name='__**COMMANDS :**__', value='\u200b', inline=False)

  embed.add_field(
      name='▶️  Study',
      value=
      '`addtask`, `deletetask`, `viewtasks`, `cleartasks`, `startstudying`',
      inline=True)

  embed.add_field(
      name='▶️  Music',
      value='`play`, `history`, `volume`, `pause`, `resume`, `skip`',
      inline=True)

  embed.add_field(
      name='▶️  Chatgpt',
      value=
      '`@Pomodoro Buddy ~ Mention the bot for asking questions to ChatGPT`',
      inline=True)
  embed.set_thumbnail(
      url=
      'https://media.discordapp.net/attachments/1200681000729055262/1200843764307087390/ZJ6QVJaOdFAiRAAg0j8P8BJLQVApTylgAAAAASUVORK5CYII.png'
  )

  embed.set_image(url='https://media.discordapp.net/attachments/1118491800949243946/1201024883329613834/Screenshot_2024-01-28_101220-transformed.png')

  await ctx.send(embed=embed)


@bot.command(name='addtask')
async def add_task(ctx, task_name, priority):
  try:
    priority = int(priority)
    tasks[task_name] = priority
    embed = discord.Embed(
        title="Task Added",
        description=f"Task: {task_name}\nPriority: {priority}",
        color=discord.Color.green())
    await ctx.send(embed=embed)
  except ValueError:
    embed = discord.Embed(
        title="Error",
        description=
        "Invalid priority. Please provide a valid integer for priority.",
        color=discord.Color.red())
    await ctx.send(embed=embed)


@bot.command(name='deletetask')
async def delete_task(ctx, task_name):
  if task_name in tasks:
    del tasks[task_name]
    embed = discord.Embed(
        title="Task Deleted",
        description=f"Task: {task_name} deleted successfully.",
        color=discord.Color.green())
    await ctx.send(embed=embed)
  else:
    embed = discord.Embed(title="Error",
                          description="That task does not exist!",
                          color=discord.Color.red())
    await ctx.send(embed=embed)


@bot.command(name='viewtasks')
async def view_tasks(ctx):
  embed = discord.Embed(title='Task List',
                        description='List of tasks',
                        color=discord.Color.blue())
  for task, priority in tasks.items():
    embed.add_field(name=task, value=f'Priority: {priority}', inline=False)
  await ctx.send(embed=embed)


@bot.command(name='cleartasks')
async def clear_tasks(ctx):
  tasks.clear()
  embed = discord.Embed(title="Tasks Cleared",
                        description="All tasks have been cleared.",
                        color=discord.Color.green())
  await ctx.send(embed=embed)


async def start_study_timer(ctx, message):

  embed = discord.Embed(title="Study Timer",
                        description="Time Remaining: 25:00",
                        color=discord.Color.blue())
  embed.set_footer(text="React with ⏸️ to pause or ⏹️ to stop.")
  timer_message = await message.channel.send(embed=embed)


  await timer_message.add_reaction('⏸️')
  await timer_message.add_reaction('⏹️')

  t = 1500
  paused = False
  while t > 0:
    mins, secs = divmod(t, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    embed = discord.Embed(title="Study Timer",
                          description=f"Time Remaining: {timer}",
                          color=discord.Color.blue())
    embed.set_footer(text="React with ⏸️ to pause or ⏹️ to stop.")
    await timer_message.edit(embed=embed)

    try:
      reaction, user = await bot.wait_for(
          'reaction_add',
          timeout=1.0,
          check=lambda r, u: r.message.id == timer_message.id and u != bot.user
      )
      if reaction.emoji == '⏸️':
        paused = not paused
        if paused:
          await timer_message.add_reaction('⏯️') 
          await message.channel.send("Timer paused. Click ⏯️ to resume.")
        else:
          await timer_message.remove_reaction('⏯️',
                                              bot.user) 
      elif reaction.emoji == '⏹️':
        await timer_message.clear_reactions()
        await timer_message.edit(content="Timer stopped.")
        return
    except asyncio.TimeoutError:
      pass

    if not paused:
      await asyncio.sleep(0.25)
      t -= 1

  await ctx.send(f"{ctx.author.mention}, time's up for your study session!"
                 ) 

  
  await asyncio.sleep(300)
  await ctx.send(
      f"{ctx.author.mention}, your 5-minute break is over! Time to get back to studying!"
  )


@bot.command(name='startstudying')
async def start_studying(ctx):
  study_message = await ctx.send(
      "Let's start studying! Get ready for a 25-minute session.")
  await start_study_timer(ctx, study_message)


bot.run(
    'MTIwMDEwMzI0MzQ0ODA2NjA1OQ.G9fTjG.pO8nplmAIFiH8Ul0h8Fak3wjMLOtN9JsoGo1ws')
