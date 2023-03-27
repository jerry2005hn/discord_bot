import discord
from discord.ext import commands
import json

class MyCog(commands.Cog):
    def __init__(self,client):
        self.client=client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("MyCog.py is ready!")
    
    @commands.command()
    async def embed(self,ctx):
        embed_message=discord.Embed(title="Title of embed",description="Description of embed",color=discord.Color.green())
        embed_message.set_author(name=f"Requested by {ctx.author.mention}",icon_url=ctx.author.avatar)
        embed_message.set_thumbnail(url=ctx.guild.icon)
        embed_message.set_image(url=ctx.guild.icon)
        embed_message.add_field(name="Field name",value="Field value",inline=False)
        embed_message.set_footer(text="This is the footer",icon_url=ctx.author.avatar)
        await ctx.send(embed=embed_message)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
            if count > 100:
                await ctx.send(embed = discord.Embed(color=discord.Color.red(), title=f"My limit is 100 message"))
            if count <= 100:
                await ctx.channel.purge(limit=count + 1)
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx,member:discord.Member,*,modreason):
        await ctx.guild.kick(member)
        conf_embed=discord.Embed(title="Success!",color=discord.Color.green())
        conf_embed.add_field(name="Kicked:",value=f"{member.mention} has been kicked from the server by {ctx.author.mention}.",inline=False)
        conf_embed.add_field(name="Reason:",value=modreason,inline=False)
        await ctx.send(embed=conf_embed)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx,member:discord.Member,*,modreason):
        await ctx.guild.ban(member)
        conf_embed=discord.Embed(title="Success!",color=discord.Color.green())
        conf_embed.add_field(name="Banned:",value=f"{member.mention} has been banned from the server by {ctx.author.mention}.",inline=False)
        conf_embed.add_field(name="Reason:",value=modreason,inline=False)
        await ctx.send(embed=conf_embed)
    
    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx,userID):
        user=discord.Object(id=userID)
        await ctx.guild.unban(user)
        conf_embed=discord.Embed(title="Success!",color=discord.Color.green())
        conf_embed.add_field(name="Unbanned:",value=f"<@{userID}> has been unbanned from the server by {ctx.author.mention}.",inline=False)
        await ctx.send(embed=conf_embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmuterole(self,ctx,role:discord.Role):
        with open("cogs/jsonfiles/mutes.json","r") as f:
            mute_role=json.load(f)
            mute_role[str(ctx.guild.id)]=role.name
        with open("cogs/jsonfiles/mutes.json","w") as f:
            json.dump(mute_role,f,indent=4)
        conf_embed=discord.Embed(title="Success!",color=discord.Color.green())
        conf_embed.add_field(name="Mute role has been set!", value=f"The mute role has been changed to '{role.mention}' for this guild. All members who are muted will be equipped this role.")
        await ctx.send(embed=conf_embed)
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self,ctx,member:discord.Member):
        with open("cogs/jsonfiles/mutes.json","r") as f:
            role=json.load(f)
            mute_role=discord.utils.get(ctx.guild.roles,name=role[str(ctx.guild.id)])
        await member.add_roles(mute_role)
        conf_embed=discord.Embed(title="Success!",color=discord.Color.green())
        conf_embed.add_field(name="Muted", value=f"The {member.mention} has been muted by {ctx.author.mention}.",inline=False)
        await ctx.send(embed=conf_embed)
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self,ctx,member:discord.Member):
        with open("cogs/jsonfiles/mutes.json","r") as f:
            role=json.load(f)
            mute_role=discord.utils.get(ctx.guild.roles,name=role[str(ctx.guild.id)])
        await member.remove_roles(mute_role)
        conf_embed=discord.Embed(title="Success!",color=discord.Color.green())
        conf_embed.add_field(name="Unmuted", value=f"The {member.mention} has been unmuted by {ctx.author.mention}.",inline=False)
        await ctx.send(embed=conf_embed)
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        with open("cogs/jsonfiles/autorole.json","r") as f:
            auto_role=json.load(f)
        join_role=discord.utils.get(member.guild.roles,name=auto_role[str(member.guild.id)])
        await member.add_roles(join_role)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def joinrole(self,ctx, role:discord.Role):
        with open("cogs/jsonfiles/autorole.json","r") as f:
            auto_role=json.load(f)
        auto_role[str(ctx.guild.id)]=str(role.name)
        with open("cogs/jsonfiles/autorole.json","w") as f:
            json.dump(auto_role,f,indent=4)
        conf_embed=discord.Embed(color=discord.Color.green())
        conf_embed.add_field(name="Success!",value=f"The automatic role for this guild/server has been set to {role.mention}.")
        conf_embed.set_footer(text=f"Action taken by {ctx.author.name}.")
        await ctx.send(embed=conf_embed)
async def setup(client):
    await client.add_cog(MyCog(client))