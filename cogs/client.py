import disnake
from disnake.ext import commands
from database import editdb as db
from disnake.ui import View
from disnake.enums import ButtonStyle
from random import randint

class ConfirmButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @disnake.ui.button(label="Подтвердить оплату", style=ButtonStyle.green, emoji="✅")
    async def confirmpayment(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.admin = inter.guild.get_role(db.getadmin())
        self.channel = inter.channel
        await store_msg.delete()
        await self.channel.send(content=self.admin.mention, embed=disnake.Embed(title="✅ Подтверждение оплаты", description=f"{inter.author.mention} подтвердил оплату товара\n**Название:** {productname}\n**Стоимость:** {productcost}₽\n**Коментарий:** {comm}", colour=disnake.Colour.green()))
    
    @disnake.ui.button(label="Назад", style=ButtonStyle.red, emoji="↩️")
    async def backtolist(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.view = ProductSelect()
        items = db.shopcatalog()
        msg = ""
        for item in items:
            msg += f"> 🔹 {item[0]} - **{item[1]}₽**\n"
        await store_msg.edit(content=inter.author.mention, embed=disnake.Embed(title="🌌 Каталог", description=msg, colour=disnake.Colour.from_rgb(47, 49, 54)), view=self.view)

class ProductSelect(View):
    @disnake.ui.select(
        placeholder="🌑 Выберите товар",
        options=[disnake.SelectOption(label=i, emoji="🌑") for i in open("catalog.txt").read().strip()[:-2].split("&&")]
    )

    async def select_callback(self, select, inter):
        select.disabled=True
        view=ConfirmButton()
        global comm
        comm = f"{randint(1,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}"
        global productname
        productname = select.values[0]
        global productcost
        productcost = db.getprice(select.values[0])

        await store_msg.edit(embed=disnake.Embed(title="📜 Форма оплаты", description=f'''
        **Название товара** {productname}
        **Стоимость:** {productcost}
        **QIWI:** {db.getqiwi()}
        **Комментарий к платежу:** {comm}
        **Бот не проверяет ваш платёж, нажимайте на кнопку подтверждения только после оплаты!**''', colour=disnake.Colour.from_rgb(47, 49, 54)), view=view)
        print(db.getprice(select.values[0]))


class Client_behavior(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(description="Открыть меню магазина")
    async def start(self, inter):
        await inter.response.send_message(embed=disnake.Embed(title="⏰ Создание канала", description="Канал с меню создаётся, подождите", colour=disnake.Colour.from_rgb(47, 49, 54)), ephemeral=True)
        self.adminrole = inter.guild.get_role(db.getadmin())
        self.guild = inter.guild

        self.channel = await inter.guild.create_text_channel(f"shop-{db.getnumber()}", category=inter.guild.get_channel(db.getcategory()))
        db.addnumber()

        #change permissions
        await self.channel.set_permissions(self.guild.default_role, read_messages=False)
        await self.channel.set_permissions(inter.author, read_messages=True, send_messages=True)
        await self.channel.set_permissions(self.adminrole, read_messages=True, send_messages=True)

        #send menu
        view = ProductSelect()
        items = db.shopcatalog()
        msg = ""
        for item in items:
            msg += f"> 🔹 {item[0]} - **{item[1]}₽**\n"
        global store_msg
        store_msg = await self.channel.send(content=inter.author.mention, embed=disnake.Embed(title="🌌 Каталог", description=msg, colour=disnake.Colour.from_rgb(47, 49, 54)), view=view)


def setup(bot):
    bot.add_cog(Client_behavior(bot))
    print("Client cog is loaded!")