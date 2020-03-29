import requests
import json
from bs4 import BeautifulSoup
import discord
from discord.ext import commands


client = commands.Bot(command_prefix="L!")
client.remove_command("help")

#BOT TOKEN GOES HERE
token = ''

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"
}



stockx_api = 'https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query'

@client.event
async def on_ready():
    print(f"{client.user.name} Is Ready :)")
    print('-'*20)


@client.command(pass_context=True)
async def search(ctx, *args):


    parameter_result = '{}'.join(args)
    parameter_result = parameter_result.replace('{', '+')
    parameter_result = parameter_result.replace('}', '')

    data = {
        "params": f"query={parameter_result}&hitsPerPage=20&facets=*"
    }

    params = {
        'x-algolia-agent': 'Algolia for vanilla JavaScript 3.22.1',
        'x-algolia-api-key': '6bfb5abee4dcd8cea8f0ca1ca085c2b3',
        'x-algolia-application-id': 'XW7SBCT9V6',
    }

    response = requests.post(url=stockx_api, headers=headers, params=params, json=data)
    output = json.loads(response.text)
    stockx_name = output['hits'][0]['name']
    stockx_name = stockx_name.replace(" ", "+")


    r = requests.get(f'https://www.hypeanalyzer.com/webapi/product.php?q={stockx_name}&c=USD&a=67B2BBDBFC92BD86414FAEBA81429DFD')
    json_response = json.loads(r.text)
    product_name = json_response["product"]
    product_img = json_response["img"]
    product_numb_sales = json_response["sold"]
    product_retail = json_response["retail"]
    product_market_value = json_response["market_value"]
    product_release_date = json_response["release"]
    embed = discord.Embed(
        title = '',
        description = '',
        colour = 0x1ff274
    )
    embed.add_field(name='LuckyAIO Discord', value=f'[Join Here](http://discord.gg/xz2kTQ5)', inline=False)
    embed.set_footer(text='LuckyAIO x HypeAnalyzer ', icon_url='https://cdn.discordapp.com/attachments/575695619637903380/615941904504324232/luckyAIO.png')
    embed.set_image(url=product_img)
    embed.set_author(name=f'{product_name} - ${product_retail}')
    embed.add_field(name='Product Sales', value=product_numb_sales, inline=False)
    embed.add_field(name='Market Value', value=f'${product_market_value}', inline=False)
    embed.add_field(name='Release Date', value=product_release_date, inline=False)
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def topsearch(ctx):
    top_products = []
    r = requests.get(f'https://www.hypeanalyzer.com/webapi/top.php?c=USD&a=67B2BBDBFC92BD86414FAEBA81429DFD')
    
    top_products_json_response = json.loads(r.text)
    embed = discord.Embed(
        title = '',
        description = '',
        colour = 0x1ff274
    )
    embed.set_footer(text='LuckyAIO x HypeAnalyzer', icon_url='https://cdn.discordapp.com/attachments/575695619637903380/615941904504324232/luckyAIO.png')
    embed.set_author(name=f'Trending Products')
    embed.add_field(name='LuckyAIO Discord', value=f'[Join Here](http://discord.gg/xz2kTQ5)', inline=False)
    for product in top_products_json_response:
        top_products.append(product["product"])
        product_name = product["product"]
        product_market_value = product["market_value"]
        embed.add_field(name=product_name, value=f'${product_market_value}', inline=False)

    print(len(top_products))
    
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def help(ctx):
    help_embed = discord.Embed(
        title = '',
        description = '',
        colour = 0x1ff274
    )

    help_embed.set_author(name='LuckyAIO Help')
    help_embed.add_field(name='LuckyAIO Discord', value=f'[Join Here](http://discord.gg/xz2kTQ5)', inline=False)
    help_embed.add_field(name='L!search <product>', value='Returns Data on any sneaker')
    help_embed.add_field(name='L!topsearch', value='Returns Data on top trending sneakers', inline=False)
    help_embed.set_footer(text='LuckyAIO x HypeAnalyzer ', icon_url='https://cdn.discordapp.com/attachments/575695619637903380/615941904504324232/luckyAIO.png')

    await ctx.send(embed=help_embed)



client.run(token)
