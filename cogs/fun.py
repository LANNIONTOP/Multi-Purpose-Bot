import discord
import datetime
import random
import aiohttp
import requests
import pyfiglet
import os
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def owo(self, ctx, *, msg):

        vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

        def last_replace(s, old, new):
            li = s.rsplit(old, 1)
            return new.join(li)

        def text_to_owo(text):
            """ Converts your text to OwO """
            smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

            text = text.replace('L', 'W').replace('l', 'w')
            text = text.replace('R', 'W').replace('r', 'w')

            text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
            text = last_replace(text, '?', '? owo')
            text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

            for v in vowels:
                if 'n{}'.format(v) in text:
                    text = text.replace('n{}'.format(v), 'ny{}'.format(v))
                if 'N{}'.format(v) in text:
                    text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))

            return text

        await ctx.send(text_to_owo(msg))
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def meme(self, ctx):
        embed=discord.Embed(
            title = "LOL",
            color = 0x00FFFF
        )

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)  
                
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def anime(self, ctx):
        response = requests.get("https://shiro.gg/api/images/neko")

        realResponse = response.json()

        embed = discord.Embed(
            title = "uwu",
            color = 0xFFC0CB
        )
        embed.set_image(url = realResponse['url'])

        await ctx.send(embed = embed)                

    ≈≈≈

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['randomname'])
    async def random_name(self, ctx):
        await ctx.message.reply(requests.get("https://nekos.life/api/v2/name").json()['name'])
        
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['simpfor'])
    async def simp_for(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.send(f"Please enter a user you want simp for.")
            return

        embed = discord.Embed(title = "New Simp", description = f"{ctx.author.mention} just simped for {user.mention}.", color = 0xFFC0CB)
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.message.reply(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['dadjoke', 'joke', 'ramjoke', 'ram_joke'])
    async def dad_joke(self, ctx):
        url = "https://joke3.p.rapidapi.com/v1/joke"

        headers = {
            'x-rapidapi-host': "joke3.p.rapidapi.com",
            'x-rapidapi-key': os.environ.get("RAPID_API_KEY")
            }

        response = requests.request("GET", url, headers=headers)
        joke = response.json()

        await ctx.message.reply(joke['content'])

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def quote(self, ctx):
        results = requests.get('https://type.fit/api/quotes').json()
        num = random.randint(1, 1500)
        content = results[num]['text']
        await ctx.message.reply(content)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def say(self, ctx, *, msg = None):
        filter = ['@here', '@everyone', '<@&', '<@!']

        for word in filter:
            if msg.count(word) > 0:
                await ctx.message.reply(f"Sorry, I won't ping anyone. Try something else.")
                return

        if msg == None:
            await ctx.message.reply(f"Please enter a message that you want me to say.")
        else:
            await ctx.message.reply(msg)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['meow', 'simba', 'cats'])
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title = "Meow!", color = 0x00FF0C)
                    embed.set_image(url = data['file'])

                    await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['dogs'])
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title = "Woof!", color = 0x00FF0C)
                    embed.set_image(url = data['url'])

                    await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def advice(self, ctx):
        url = "https://api.adviceslip.com/advice"
        response = requests.get(url)
        advice = response.json()
        real_advice = advice['slip']['advice']
        await ctx.message.reply(real_advice)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def ascii(self, ctx, *, text = None):
        if text == None:
            await ctx.message.reply(f"Please enter some text.")
        else:
            if len(pyfiglet.figlet_format(text)) > 2000:
                await ctx.message.reply(f"Text too long. Please enter short text.")
            else:
                await ctx.message.reply(f"```{pyfiglet.figlet_format(text)}```")


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def fox(self, ctx):
        url = "https://randomfox.ca/floof/"
        response = requests.get(url)
        fox = response.json()

        embed = discord.Embed(color = 0x00FFFF)
        embed.set_image(url = fox['image'])
        await ctx.message.reply(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def mock(self, ctx, *,text=None):

        if text == None:
            await ctx.message.reply("Please enter some text!")
        else:

            filter = ['@here', '@everyone', '<@&', '<@!']

            for word in filter:
                if text.count(word) > 0:
                    await ctx.message.reply(f"Sorry, I won't ping anyone. Try something else.")
                    return

            res = ""
            for c in text:
                chance = random.randint(0,1)
                if chance:
                    res += c.upper()
                else:
                    res += c.lower()
            await ctx.message.reply(res)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["atc"])
    async def aesthetic(self, ctx, *, args=None):
        if args == None:
            await ctx.send("Invalid args. Correct usage: `&atc <msg> | [mode]`. Mode can be b (bold), i (italic), or n (none).")
            return

        if args.count(" | ") == 0:
            m = "n"
        else:
            m = args[-1]

        s = ""
        if m == "b":
            s += "**"
        elif m == "i":
            s += "_"

        msg = "".join(args.split(" | ")[0])
        args = args.split(" | ")[:-1]
        for c in msg:
            s += c + " "
        if m == "b":
            s += "**"
        elif m == "i":
            s += "_"

        await ctx.message.reply(s)

def setup(client):
    client.add_cog(Fun(client))