import random
import discord
import json
import requests
import io

from random import randint
from discord.ext import commands
from utils import lists, http, default, eapi, sfapi

processapi = eapi.processapi
processshowapi = eapi.processshowapi
search = sfapi.search


class ResultNotFound(Exception):
    """Used if ResultNotFound is triggered by e* API."""
    pass


class InvalidHTTPResponse(Exception):
    """Used if non-200 HTTP Response got from server."""
    pass


class Fun:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        answer = random.choice(lists.ballresponse)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    @staticmethod
    async def randomimageapi(ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")

        embed = discord.Embed(colour=249742)
        embed.set_image(url=r[endpoint])
        await ctx.send(embed=embed)

    @staticmethod
    async def textapi(ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")

        await ctx.send(f"{r[endpoint]}")

    @staticmethod
    async def factapi(ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")

        await ctx.send(f'**Did you know?** 🤔\n\n{r[endpoint]}')

    @staticmethod
    async def asciitext(ctx, url):
        try:
            with requests.get(url) as f:
                html = f.text
                await ctx.send(f"```\n{html}\n```")
        except InvalidHTTPResponse as e:
            print(e)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def cat(self, ctx):
        """ Posts a random cat """
        await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/meow', 'url')

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def dog(self, ctx):
        """ Posts a random dog """  # https://dog.ceo/api/breeds/image/random Fetch!
        await self.randomimageapi(ctx, 'https://random.dog/woof.json', 'url')

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def doggo(self, ctx):
        """ Posts a random dog """
        await self.randomimageapi(ctx, 'https://dog.ceo/api/breeds/image/random', 'message')

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def neko(self, ctx):
        """ Posts a random neko """
        await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/neko', 'url')

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def duck(self, ctx):
        """ Posts a random duck """
        await self.randomimageapi(ctx, 'https://random-d.uk/api/v1/random', 'url')

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def fox(self, ctx):
        """ Posts a random fox girl """
        await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/fox_girl', 'url')

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def rabbit(self, ctx):
        """ Posts a random rabbit """
        await self.randomimageapi(ctx, f'https://api.chewey-bot.ga/rabbit?auth={self.config.cheweyauth}', 'data')

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def snek(self, ctx):
        """ Does a heckin snek image """
        await self.randomimageapi(ctx, f'https://api.chewey-bot.ga/snake?auth={self.config.cheweyauth}', 'data')

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def otter(self, ctx):
        """ Posts a random otter """
        await self.randomimageapi(ctx, f'https://api.chewey-bot.ga/otter?auth={self.config.cheweyauth}', 'data')

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def birb(self, ctx):
        """ Posts a random birb """
        await self.randomimageapi(ctx, f'https://api.chewey-bot.ga/birb?auth={self.config.cheweyauth}', 'data')

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        numbers = random.randint(0, 100)
        decimals = random.randint(0, 9)

        if numbers == 100:
            decimals = 0

        await ctx.send(f"I'd rate {thing} a **{numbers}.{decimals} / 100**")

    @commands.command(aliases=['howhot', 'hot'])
    async def hotcalc(self, ctx, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        if user is None:
            user = ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command()
    async def e926(self, ctx, *args):
        """Searches e926 with given queries.
        Arguments:
        `*args` : list
        The quer(y/ies)"""
        msgtoedit = await ctx.send("Searching...")
        args = ' '.join(args)
        args = str(args)
        netloc = "e926"
        print("------")
        print("Got command with args: " + args)
        if "order:score_asc" in args:
            await ctx.send("I'm not going to fall into that one, silly~")
            return
        if "score:" in args:
            apilink = 'https://e926.net/post/index.json?tags=' + args + '&limit=320'
        else:
            apilink = 'https://e926.net/post/index.json?tags=' + args + ' score:>25&limit=320'
        try:
            await eapi.processapi(apilink)
        except ResultNotFound:
            await ctx.send("Result not found!")
            return
        except InvalidHTTPResponse:
            await ctx.send("We're getting invalid response from the API, please try again later!")
            return
        msgtoedit = await ctx.channel.get_message(msgtoedit.id)
        msgtosend = "Post link: `https://""" + netloc + """.net/post/show/""" + eapi.processapi.imgid + """/`\r\nArtist: `""" + eapi.processapi.imgartist + """`\r\nSource: `""" + eapi.processapi.imgsource + """`\r\nRating: """ + eapi.processapi.imgrating + """\r\nTags: `""" + eapi.processapi.imgtags + """` ...and more\r\nImage link: """ + eapi.processapi.file_link
        await msgtoedit.edit(content=msgtosend)

    @commands.command()
    async def yell(self, ctx, *, text: str):
        """ AAAAAAAAA!
        Everything you type after yell will of course, be yelled
        """
        t_upper = text.upper().replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"⬆️ {t_upper}")

    @commands.command()
    async def whisper(self, ctx, *, text: str):
        """ Shh
        Be quiet..
        """
        t_lower = text.lower().replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"⬇️ {t_lower}")

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def headpat(self, ctx):
        """Posts a random headpat from headp.at"""

        def url_to_bytes(url):
            data = requests.get(url)
            content = io.BytesIO(data.content)
            filename = url.rsplit("/", 1)[-1]
            return {"content": content, "filename": filename}

        pats = requests.get("http://headp.at/js/pats.json").json()
        pat = random.choice(pats)
        file = url_to_bytes("http://headp.at/pats/{}".format(pat))
        await ctx.send(file=discord.File(file["content"], file["filename"]))

    @commands.command()
    async def hug(self, ctx, user: discord.Member = None):
        """ Hug a user! """
        if user is None:
            user = ctx.author

        await ctx.send(f"💖 | **{ctx.author.name}** hugs **{user.name}**")

    @commands.command()
    async def cookie(self, ctx, user: discord.Member = None):
        """ Hug a user! """
        if user is None:
            user = ctx.author

        await ctx.send(f"🍪 | **{ctx.author.name}** gives **{user.name}** a cookie!")

    @commands.command()
    async def stab(self, ctx, user: discord.Member = None):
        """ Ssstab a perssson! """
        if user is None:
            user = ctx.author

        await ctx.send(f"🔪 | **{ctx.author.name}** stabbed **{user.name}** in the hand (How rude)!")

    @commands.command()
    async def pat(self, ctx, user: discord.Member = None):
        """ Headpats for all! """
        if user is None:
            user = ctx.author

        await ctx.send(f"<a:patkyutie:444890889513598986> | **{ctx.author.name}** pats **{user.name}** on the head!")

    @commands.command()
    async def nom(self, ctx, user: discord.Member = None):
        """ Nom a user! """
        if user is None:
            user = ctx.author

        await ctx.send(f"<a:WanTriggered:437201280918618112> | **{ctx.author.name}** nommed **{user.name}**'s arm!")

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def fact(self, ctx):
        """ sends a random fact """
        await self.factapi(ctx, 'https://nekos.life/api/v2/fact', 'fact')

    @commands.command()
    async def bamboozle(self, ctx):
        """ You just got bamboozled! """
        await ctx.send(f"**{ctx.author.name}** just got heckin' bamboozled!")

    @commands.command(hidden=True)
    async def highcontrastphotooffruitfloatingthreateninglyinthedark(self, ctx):
        """ .. """
        await ctx.send("https://i.imgur.com/gtm1VKQ.jpg")

    @commands.command(hidden=True)
    async def lighttheme(self, ctx):
        """ E """
        await ctx.send("Ew https://i.imgur.com/fbIE97N.png")

    @commands.command()
    @commands.guild_only()
    async def ship(self, ctx, user: discord.User, *, user2: discord.User=None):
        """Checks the shiprate for 2 users"""
        author = ctx.message.author
        if not user2:
            user2 = author
        if not user:
            await ctx.send("can't ship nothing y'know..")
        elif user.id == user2.id:
            await ctx.send("i-i can't ship the same person..")
        elif user.id == author.id and user2.id == author.id:
            await ctx.send(f"wow, you're in love with yourself, huh {ctx.author.name}?")
        elif user == self.bot.user and user2 == author or user2 == self.bot.user and user == author:
            blushes = ["m-me..? 0////0", "m-me..? >////<"]
            return await ctx.send(random.choice(blushes))

        else:
            n = randint(1, 100)
            if n == 100:
                bar = "██████████"
                heart = '💞'
            elif n >= 90:
                bar = "█████████."
                heart = '💕'
            elif n >= 80:
                bar = "████████.."
                heart = '😍'
            elif n >= 70:
                bar = "███████..."
                heart = '💗'
            elif n >= 60:
                bar = "██████...."
                heart = '❤'
            elif n >= 50:
                bar = '█████.....'
                heart = '❤'
            elif n >= 40:
                bar = "████......"
                heart = '💔'
            elif n >= 30:
                bar = "███......."
                heart = '💔'
            elif n >= 20:
                bar = "██........"
                heart = '💔'
            elif n >= 10:
                bar = "█........."
                heart = '💔'
            elif n < 10:
                bar = ".........."
                heart = '🖤'
            else:
                bar = ".........."
                heart = '🖤'
            name1 = user.name.replace(" ", "")
            name1 = name1[:int(len(name1) / 2):]
            name2 = user2.name.replace(" ", "")
            name2 = name2[int(len(name2) / 2)::]
            ship = discord.Embed(description=f"**{n}%** **`{bar}`** {heart}", color=ctx.me.colour)
            ship.title = f"{user.name} x {user2.name}"
            ship.set_footer(text=f"Shipname: {str(name1 + name2).lower()}")
            await ctx.send(embed=ship)

    @commands.command(aliases=['👏'])
    @commands.guild_only()
    async def emojify(self, ctx, emote, *, text_to_clap: str):
        """ 👏bottom👏text👏 """
        clapped_text = text_to_clap.replace("@everyone", f"{emote}everyone").replace("@here", f"{emote}here").replace(" ", f"{emote}")
        clapped_text = f"{emote}{clapped_text}{emote}"
        await ctx.send(clapped_text)

    @commands.command()
    async def owo(self, ctx):
        """Sends a random owo face"""
        owo = random.choice(lists.owos)
        await ctx.send(f"{owo} whats this~?")

    @commands.command()
    async def choose(self, ctx, *args):
        """Choose one of a lot arguments (Split with |) """
        args = ' '.join(args)
        args = str(args)
        choices = args.split('|')
        if len(choices) < 2:
            await ctx.send("You need to send at least 2 argument!")
            return
        await ctx.send(random.choice(choices))

    @commands.command()
    async def jpeg(self, ctx, urltojpeg: str):
        """ Does what it says on the can """
        if "http" not in urltojpeg:
            return ctx.send("Include a url you donk!")
        await self.randomimageapi(ctx, f'https://nekobot.xyz/api/imagegen?type=jpeg&url={urltojpeg}', 'message')

    @commands.command()
    async def deepfry(self, ctx, urltojpeg: str):
        """ Deepfries an image """
        if "http" not in urltojpeg:
            return ctx.send("Include a url you donk!")
        await self.randomimageapi(ctx, f'https://nekobot.xyz/api/imagegen?type=deepfry&image={urltojpeg}', 'message')

    @commands.command()
    async def clyde(self, ctx, clydetext: str):
        """ Makes Clyde say something """
        if clydetext is None:
            return ctx.send("Include some text you donk!")
        await self.randomimageapi(ctx, f'https://nekobot.xyz/api/imagegen?type=clyde&text={clydetext}', 'message')

    @commands.command()
    async def magik(self, ctx, intensity: str, imgtomagik: str):
        """ why don'T WE JUST RELAX AND TURn on THe rADIO? wOuLd You LIKE AM OR FM """
        if imgtomagik is None:
            return ctx.send("Include some text you donk!")
        if intensity not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            return ctx.send("Include an intensity to magik (1-10)")
        await self.randomimageapi(ctx, f'https://nekobot.xyz/api/imagegen?type=magik&image={imgtomagik}&intensity={intensity}', 'message')

    @commands.command(aliases=['ascii'])
    async def asciify(self, ctx, *, text: str):
        """ Test """
        texttoascii = text.replace(" ", "%20")
        await self.asciitext(ctx, f"http://artii.herokuapp.com/make?text={texttoascii}")


def setup(bot):
    bot.add_cog(Fun(bot))
