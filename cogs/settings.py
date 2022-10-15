import disnake
from disnake.ext import commands
from disnake import Option
from database import editdb as db
from main import bot

class Bot_settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #settings information
    @commands.slash_command(description="Посмотреть настройки")
    async def assettings(self, inter):
        self.guild = self.bot.get_guild(inter.guild.id)
        self.role = self.guild.get_role(db.getadmin())
        
        await inter.response.send_message(embed=disnake.Embed(title="⚙️ Настройки", description=f'''
        **Роль администратора:** {self.role.mention if self.role is not None else 'Не установлена'}
        **Категория:** {"<#"+str(db.getcategory())+">" if db.getcategory() != -1 else 'Не установлена'}
        **Количество вызовов:** {db.getnumber()}
        **QIWI:** {db.getqiwi()}
        ''', colour=disnake.Colour.from_rgb(47, 49, 54)))
        options = db.shopcatalog()
        print(options)
    
    #set category
    @commands.slash_command(description="Добавить/изменить категорию каналов", options=[
        Option(
            name="category_id",
            description="ID категории для каналов",
            type=disnake.OptionType.channel,
            required=True
        )
    ])
    async def ascategory(self, inter, category_id: disnake.CategoryChannel):
        db.editcategory(category_id.id)
        await inter.response.send_message(embed=disnake.Embed(title="✅ Успешно", description=f"Выбрана категория {category_id.mention}", colour=disnake.Colour.green()), ephemeral=True)

    #set admin role
    @commands.slash_command(description="Добавить/изменить роль администратора",
    options=[
        Option(
            name="id_role",
            description="Роль администратора",
            type=disnake.OptionType.role,
            required=True
        )
    ])
    async def asadmin(self, inter, id_role: disnake.Role):
        db.editadmin(id_role.id)
        await inter.response.send_message(embed=disnake.Embed(title="✅ Успешно", description=f"Роль администратора установлена для {id_role.mention}", colour=disnake.Colour.green()), ephemeral=True)
    
    #add to shop
    @commands.slash_command(description="Добавить товар в магазин", options=[
        Option(
            name="name",
            description="Название товара",
            type=disnake.OptionType.string,
            required=True
        ),
        Option(
            name="price",
            description="Цена товара",
            type=disnake.OptionType.integer,
            required=True
        )
    ])
    async def asaddproduct(self, inter, name: str, price: int):
        if db.addproduct(name, price):
            bot.unload_extension("cogs.client")
            bot.load_extension("cogs.client")
            await inter.response.send_message(embed=disnake.Embed(title="✅ Успешно", description=f"Добавлен товар:\n**Название:** {name}\n**Цена:** {price}", colour=disnake.Colour.green()), ephemeral=True)
        else:
            await inter.response.send_message(embed=disnake.Embed(description="Такой товар уже существует", colour=disnake.Colour.red()), ephemeral=True)
    
    #delete product
    @commands.slash_command(description="Удалить товар", options=[
        Option(
            name="name",
            description="Название товара",
            type=disnake.OptionType.string,
            required=True
        )
    ])
    async def asremoveproduct(self, inter, name: str):
        if db.removeproduct(name):
            bot.unload_extension("cogs.client")
            bot.load_extension("cogs.client")
            await inter.response.send_message(embed=disnake.Embed(title="✅ Успешно", description=f"Товар с именем {name} удалён", colour=disnake.Colour.green()), ephemeral=True)
        else:
            await inter.response.send_message(embed=disnake.Embed(description="Товара с таким именем не существует", colour=disnake.Colour.red()), ephemeral=True)
    
    #shop catalog
    @commands.slash_command(description="Показать товары в магазине")
    async def shoplist(self, inter):
        items = db.shopcatalog()
        msg = ""
        count = 1
        for item in items:
            msg += f"{count}. {item[0]} - **{item[1]}₽**\n"
            count += 1
        await inter.response.send_message(embed=disnake.Embed(title="🌌 Каталог", description=msg, colour=disnake.Colour.from_rgb(47, 49, 54)))
    
    #edit qiwi
    @commands.slash_command(description="Установить/поменять реквизиты QIWI", options=[
        Option(
            name="value",
            description="Значение для реквизитов, здесь может быть любое значение",
            type=disnake.OptionType.string,
            required=True
        )
    ])
    async def asqiwi(self, inter, value: str):
        db.editqiwi(value)
        await inter.response.send_message(embed=disnake.Embed(title="✅ Успешно", description=f"Реквизиты установлены как {value}", colour=disnake.Colour.green()), ephemeral=True)
    
    #close command
    @commands.slash_command(description="Закрыть приватный канал")
    async def close(self, inter):
        await inter.channel.delete()
    
    #help command
    @commands.slash_command(description="📜 Описание команд")
    async def help(self, inter):
        await inter.response.send_message(embed=disnake.Embed(title="Список команд", description='''
        **/assetings** - Посмотреть текущие настройки бота
        **/asadmin** - Установить роль администрации
        **/ascategory** - Установить категорию для новых каналов
        **/asqiwi** - Установить реквизиты QIWI кошелька
        **/asaddproduct** - Добавить новый товар
        **/asremoveproduct** - Удалить товар
        **/shoplist** - Посмотреть текущий каталог товаров
        **/close** - Удалить канал с магазином (работает и с другими каналами)
        **/start** - Создать новый канал с меню
        ''', colour=disnake.Colour.from_rgb(47, 49, 54)), ephemeral=True)

def setup(bot):
    bot.add_cog(Bot_settings(bot))
    print("Settings is loaded!")