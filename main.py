import nextcord, random, openpyxl
from nextcord.ext import commands
from nextcord import File, ButtonStyle
from nextcord.ui import Button, View
import openpyxl
from openpyxl import load_workbook
from dotenv import load_dotenv
import os

#변수 선언
load_dotenv()

bot = commands.Bot(command_prefix="/", intents=nextcord.Intents.all())

IDNum = 1
STNum = 2
TOKEN = os.getenv("DISCORD_TOKEN")
dir = os.getenv("DIR")
Pcolum = ["A","B","C","D","E","F","G","H","I","J"]
GM_role = 1421049224321044480
Sid = 1360509644442697849

#본 온라인 확인
@bot.event
async def on_ready():
    print(f'준비완료 {bot.user}')

#플레이어를 데이터에 추가 및 기초 스텟 설정
@bot.slash_command(guild_ids=[Sid], name="플레이어추가", description="플레이어를 추가합니다")
async def slash2(ctx:nextcord.Interaction, 사용자명: nextcord.Member=nextcord.SlashOption(description="추가할 유저의이름을 선택해주세요."), 최대hp: int=nextcord.SlashOption(description="플레이어의 최대HP를 적어주세요."), 최대정신력: int=nextcord.SlashOption(description="플레이어의 최대정신력을 적어주세요.")):
    global IDNum
    global dir
    global Sid
    PN = 사용자명.display_name
    count = 0

    excel = load_workbook(dir)

    excel_ws = excel['Sheet']

    if IDNum == 4:
        await ctx.send('플레어는 최대 4명만 추가 할수있습니다.',ephemeral=True)
    elif IDNum < 4:
        for i in range(2,7):
            cell = excel_ws.cell(row=i,column=1).value
            if cell == PN:
                await ctx.send(f'{사용자명.display_name}님은 이미 추가된 플레이어입니다.',ephemeral=True)
                count += 1
                break
        if count == 0:
            excel_ws[f'A{IDNum + 1}'] = PN
            excel_ws[f'B{IDNum + 1}'] = 1
            excel_ws[f'C{IDNum + 1}'] = 최대hp
            excel_ws[f'D{IDNum + 1}'] = 최대hp
            excel_ws[f'E{IDNum + 1}'] = 최대정신력
            excel_ws[f'F{IDNum + 1}'] = 최대정신력
            excel_ws[f'G{IDNum + 1}'] = False
            excel_ws[f'B{1}'] = "MP"
            excel_ws[f'C{1}'] = "최대HP"
            excel_ws[f'D{1}'] = "현재HP"
            excel_ws[f'E{1}'] = "최대정신력"
            excel_ws[f'F{1}'] = "현재정신력"
            excel_ws[f'G{1}'] = "isDEAD"
            await ctx.response.send_message(f'{PN}님이 플레이어로 추가 되었습니다.',ephemeral=True)
            IDNum += 1

    excel.save(dir)

#특정 플레이어의 HP를 변경
@bot.slash_command(guild_ids=[Sid], name="hp", description="HP를 변경합니다.")
async def slash2(ctx:nextcord.Interaction, 사용자명: nextcord.Member=nextcord.SlashOption(description="변경할 플레이어를 골라주세요."), 값: int=nextcord.SlashOption(description="변경할 값을 적어주세요.")):
    global dir
    global GM_role
    global Sid
    excel = load_workbook(dir)
    excel_ws = excel['Sheet']

    count = 0
    for i in range(2,7):
            cell = excel_ws.cell(row=i,column=1).value
            if cell == 사용자명.display_name:
                count = i
                break
    if count == 0:
        await ctx.send('등록되지 않은 플레이어입니다',ephemeral=True)
    else:
        role_ids = [role.id for role in ctx.user.roles]
        if GM_role in role_ids:
            cal = (excel_ws[f'D{count}'].value or 0) + 값
            Mhp = excel_ws[f'C{count}'].value or 0
            isDEAD = excel_ws[f'G{count}'].value
            if isDEAD == True:
                await ctx.send(f'{excel_ws.cell(row=count, column=1).value}님은 행동 불능상태입니다.',ephemeral=True)
            else:
                if cal > Mhp:
                    await ctx.send(f'최대hp보다 커질수 없습니다.',ephemeral=True)
                else:
                    if cal <= 0:
                        excel_ws[f'G{count}'].value = True
                        await ctx.channel.send(f'**``《 {excel_ws.cell(row=count, column=1).value} 》님이 쓰러졌습니다.``**')
                        excel_ws[f'D{count}'].value = 0
                    else:
                        excel_ws[f'D{count}'].value = cal
                        await ctx.send(f'{excel_ws.cell(row=count, column=1).value}님의 HP값이 {excel_ws.cell(row=count, column=4).value}으로 변경되었습니다.',ephemeral=True)
                        if 값 < 0: 
                            await ctx.channel.send(f"**``{excel_ws.cell(row=count, column=1).value}님의 체력이 '{값 * -1}' 만큼 감소했습니다.``**")
                        else:
                            await ctx.channel.send(f"**``{excel_ws.cell(row=count, column=1).value}님의 체력이 '{값}' 만큼 증가했습니다.``**")
        else:
            await ctx.send('GM 권한이 없습니다.',ephemeral=True)
    excel.save(dir)

#특정 플레이어의 MP를 변경
@bot.slash_command(guild_ids=[Sid], name="mp", description="MP를 변경합니다.")
async def slash2(ctx:nextcord.Interaction, 사용자명: nextcord.Member=nextcord.SlashOption(description="변경할 플레이어의 번호를 적어주세요."), 값: int=nextcord.SlashOption(description="변경할 값을 적어주세요.")):
    global IDNum
    global dir
    global GM_role
    global Sid
    excel = load_workbook(dir)
    excel_ws = excel['Sheet']
    
    count = 0
    for i in range(2,7):
            cell = excel_ws.cell(row=i,column=1).value
            if cell == 사용자명.display_name:
                count = i
                break
    if count == 0:
        await ctx.send('등록되지 않은 플레이어입니다',ephemeral=True)
    else:
        role_ids = [role.id for role in ctx.user.roles]
        if GM_role in role_ids:
            excel_ws[f'B{count}'] = (excel_ws[f'B{count}'].value or 0) + 값
            await ctx.send(f'{excel_ws.cell(row=count, column=1).value}님의 MP값이 {excel_ws.cell(row=count, column=2).value}으로 변경되었습니다.',ephemeral=True)
            await ctx.channel.send(f"**``{excel_ws.cell(row=count, column=1).value}님의 남은 토큰:``**{" <:To:1360529966357549252>" * (excel_ws.cell(row=count, column=2).value or 0)}")
        else:
            await ctx.send('GM 권한이 없습니다.',ephemeral=True)
    excel.save(dir)

#특정 플레이어의 SP를 변경
@bot.slash_command(guild_ids=[Sid], name="sp", description="정신력을 변경합니다.")
async def slash2(ctx:nextcord.Interaction, 사용자명: nextcord.Member=nextcord.SlashOption(description="변경할 플레이어의 번호를 적어주세요."), 값: int=nextcord.SlashOption(description="변경할 값을 적어주세요.")):
    global IDNum
    global dir
    global GM_role
    global Sid
    excel = load_workbook(dir)
    excel_ws = excel['Sheet']
    
    count = 0
    for i in range(2,7):
            cell = excel_ws.cell(row=i,column=1).value
            if cell == 사용자명.display_name:
                count = i
                break
    if count == 0:
        await ctx.send('등록되지 않은 플레이어입니다',ephemeral=True)
    else:
        role_ids = [role.id for role in ctx.user.roles]
        if GM_role in role_ids:
            Msp = excel_ws[f'E{count}'].value or 0
            cal = (excel_ws[f'F{count}'].value or 0) + 값
            if cal > Msp:
                await ctx.send(f'최대sp보다 커질수 없습니다.',ephemeral=True)
            else:
                if cal < 0:
                    excel_ws[f'F{count}'] = 0
                    await ctx.send(f'{excel_ws.cell(row=count, column=1).value}님의 SP값이 {excel_ws.cell(row=count, column=6).value}으로 변경되었습니다.',ephemeral=True)
                else:
                    excel_ws[f'F{count}'] = cal
                    await ctx.send(f'{excel_ws.cell(row=count, column=1).value}님의 SP값이 {excel_ws.cell(row=count, column=6).value}으로 변경되었습니다.',ephemeral=True)
                    if 값 < 0:
                        await ctx.channel.send(f"**``{excel_ws.cell(row=count, column=1).value}님의 정신력이 '{값 * -1}' 만큼 감소했습니다.``**")
                    else:
                        await ctx.channel.send(f"**``{excel_ws.cell(row=count, column=1).value}님의 정신력이 '{값}' 만큼 증가했습니다.``**")

        else:
            await ctx.send('GM 권한이 없습니다.',ephemeral=True)
    excel.save(dir)

#모든 플레이어의 HP를 변경
@bot.slash_command(guild_ids=[Sid], name="ahp", description="전체 플레이어의 HP를 변경합니다.")
async def slash2(ctx:nextcord.Interaction, 값: int=nextcord.SlashOption(description="변경할 값을 적어주세요.")):

    global dir
    global GM_role
    global Sid

    excel = load_workbook(dir)
    excel_ws = excel['Sheet']

    role_ids = [role.id for role in ctx.user.roles]
    if GM_role in role_ids:
        for i in range(2,6):
            cal = (excel_ws[f'D{i}'].value or 0) + 값
            Mhp = (excel_ws[f'C{i}'].value or 0)
            if cal > Mhp:
                excel_ws[f'D{i}'].value = Mhp
            elif cal <= 0:
                if excel_ws[f'A{i}'].value != None:
                    excel_ws[f'G{i}'].value = True
                    excel_ws[f'D{i}'].value = 0
                    await ctx.channel.send(f'**``《 {excel_ws.cell(row=i, column=1).value} 》님이 쓰러졌습니다.``**')
            else:
                excel_ws[f'D{i}'].value = cal
    else:   
        await ctx.send('GM 권한이 없습니다.',ephemeral=True)

    if 값 < 0: 
        await ctx.channel.send(f"**``모두의 체력이 '{값 * -1}' 만큼 감소했습니다.``**")
    else:
        await ctx.channel.send(f"**``모두의 체력이 '{값}' 만큼 증가했습니다.``**")
    excel.save(dir)

#모든 플레이어의 MP를 변경   
@bot.slash_command(guild_ids=[Sid], name="amp", description="전체 플레이어의 MP를 변경합니다.")
async def slash2(ctx:nextcord.Interaction, 값: int=nextcord.SlashOption(description="변경할 값을 적어주세요.")):
    global dir
    global GM_role
    global Sid

    excel = load_workbook(dir)
    excel_ws = excel['Sheet']

    role_ids = [role.id for role in ctx.user.roles]
    if GM_role in role_ids:
        for i in range(2,6):
            cal = (excel_ws.cell(row=i, column=2).value or 0) + 값
            if cal < 0:
                excel_ws[f'B{i}'].value = 0
            else:
                excel_ws[f'B{i}'].value = cal
    else:   
        await ctx.send('GM 권한이 없습니다.',ephemeral=True)
    if 값 < 0: 
        await ctx.channel.send(f"**``모두의 토큰이 '{값 * -1}' 만큼 감소했습니다.``**")
    else:
        await ctx.channel.send(f"**``모두의 토큰이 '{값}' 만큼 증가했습니다.``**")
    excel.save(dir)

#모든 플레이어의 SP를 변경
@bot.slash_command(guild_ids=[Sid], name="asp", description="전체 플레이어의 SP를 변경합니다.")
async def slash2(ctx:nextcord.Interaction, 값: int=nextcord.SlashOption(description="변경할 값을 적어주세요.")):
    global dir
    global GM_role
    global Sid

    excel = load_workbook(dir)
    excel_ws = excel['Sheet']

    role_ids = [role.id for role in ctx.user.roles]
    if GM_role in role_ids:
        for i in range(2,6):
            cal = excel_ws.cell(row=i, column=6).value or 0 + 값
            Mhp = excel_ws.cell(row=i, column=5).value or 0
            if cal > Mhp:
                excel_ws[f'F{i}'].value = Mhp
            else:
                excel_ws[f'F{i}'].value = cal
    else:   
        await ctx.send('GM 권한이 없습니다.',ephemeral=True)
    if 값 < 0: 
        await ctx.channel.send(f"**``모두의 정신력이 '{값 * -1}' 만큼 감소했습니다.``**")
    else:
        await ctx.channel.send(f"**``모두의 정신력이 '{값}' 만큼 증가했습니다.``**")
    excel.save(dir)

#모든 플레이어의 정보를 출력
@bot.slash_command(guild_ids=[Sid], name="플레이어정보", description="플레이어들의 정보를 보여줍니다.")
async def slash(ctx:nextcord.Interaction):
    global IDNum
    global dir
    global GM_role
    global Sid
    excel = load_workbook(dir)
    excel_ws = excel['Sheet']
    pnum = 2
    snnum = 2
    P1 = excel_ws.cell(row=pnum, column=1).value
    pnum +=1
    P2 = excel_ws.cell(row=pnum, column=1).value
    pnum +=1
    P3 = excel_ws.cell(row=pnum, column=1).value
    pnum +=1
    P4 = excel_ws.cell(row=pnum, column=1).value
    pnum +=1
    P5 = excel_ws.cell(row=pnum, column=1).value

    S1 = excel_ws.cell(row=1, column=snnum).value
    snnum +=1
    S2 = excel_ws.cell(row=1, column=snnum).value
    snnum +=1
    S3 = excel_ws.cell(row=1, column=snnum).value
    snnum +=1
    S4 = excel_ws.cell(row=1, column=snnum).value
    snnum +=1
    S5 = excel_ws.cell(row=1, column=snnum).value

    pnum = 2
    snnum = 2
    #플레이어 1 값
    S1V1 = excel_ws.cell(row=pnum, column=snnum).value 
    snnum += 1
    S1V2 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S1V3 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S1V4 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S1V5 = excel_ws.cell(row=pnum, column=snnum).value

    pnum = 3
    snnum = 2
    #플레이어 2 값
    S2V1 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S2V2 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S2V3 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S2V4 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S2V5 = excel_ws.cell(row=pnum, column=snnum).value

    pnum = 4
    snnum = 2
    # 플레이어 3 값
    S3V1 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S3V2 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S3V3 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S3V4 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S3V5 = excel_ws.cell(row=pnum, column=snnum).value

    pnum = 5
    snnum = 2
    # 플레이어 4 값
    S4V1 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S4V2 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S4V3 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S4V4 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S4V5 = excel_ws.cell(row=pnum, column=snnum).value

    pnum = 6
    snnum = 2
    # 플레이어 5 값
    S5V1 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S5V2 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S5V3 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S5V4 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S5V5 = excel_ws.cell(row=pnum, column=snnum).value

    embed = nextcord.Embed(
        title='플레이어 정보',
        description='',
        color=nextcord.Color(0xFF0000)
        )
    embed.add_field(name='', value=f'『{P1}』님의 정보\n『{S1}:{S1V1}』\n『{S2}:{S1V2}』\n『{S3}:{S1V3}』\n『{S4}:{S1V4}』\n『{S5}:{S1V5}』\n\n『{P2}』님의 정보\n『{S1}:{S2V1}』\n『{S2}:{S2V2}』\n『{S3}:{S2V3}』\n『{S4}:{S2V4}』\n『{S5}:{S2V5}』\n\n『{P3}』님의 정보\n『{S1}:{S3V1}』\n『{S2}:{S3V2}』\n『{S3}:{S3V3}』\n『{S4}:{S3V4}』\n『{S5}:{S3V5}』\n\n『{P4}』님의 정보\n『{S1}:{S4V1}』\n『{S2}:{S4V2}』\n『{S3}:{S4V3}』\n『{S4}:{S4V4}』\n『{S5}:{S4V5}』\n\n『{P5}』님의 정보\n『{S1}:{S5V1}』\n『{S2}:{S5V2}』\n『{S3}:{S5V3}』\n『{S4}:{S5V4}』\n『{S5}:{S5V5}』')
    
    await ctx.send(embed=embed,ephemeral=True)
    excel.save(dir)

#데이터의 모든 값을 초기화
@bot.slash_command(guild_ids=[1360509644442697849], name="초기화", description="플레이어들의 정보를 초기화합니다.")
async def slash2(ctx:nextcord.Interaction):
    global IDNum
    global dir
    global GM_role
    global Sid
    global Pcolum
    excel = load_workbook(dir)
    excel_ws = excel['Sheet']

    for i in range(10):
        for j in range(2,7):
            P = Pcolum[i]
            if P == "A" and excel_ws.cell(row=j,column=i+1).value != None:
                PI = ctx.guild.get_member_named(excel_ws.cell(row=j,column=i+1).value)
                excel_ws[f'{P}{j}'] = None
            else:
                excel_ws[f'{P}{j}'] = None
            excel.save(dir)

    await ctx.send("정보를 초기화했습니다.",ephemeral=True)
    IDNum = 1
    STNum = 2

    pnum = 2
    snnum = 2
    P1 = excel_ws.cell(row=pnum, column=1).value
    pnum +=1
    P2 = excel_ws.cell(row=pnum, column=1).value
    pnum +=1
    P3 = excel_ws.cell(row=pnum, column=1).value
    pnum +=1
    P4 = excel_ws.cell(row=pnum, column=1).value
    pnum +=1
    P5 = excel_ws.cell(row=pnum, column=1).value

    S1 = excel_ws.cell(row=1, column=snnum).value
    snnum +=1
    S2 = excel_ws.cell(row=1, column=snnum).value
    snnum +=1
    S3 = excel_ws.cell(row=1, column=snnum).value
    snnum +=1
    S4 = excel_ws.cell(row=1, column=snnum).value
    snnum +=1
    S5 = excel_ws.cell(row=1, column=snnum).value

    pnum = 2
    snnum = 2
    #플레이어 1 값
    S1V1 = excel_ws.cell(row=pnum, column=snnum).value 
    snnum += 1
    S1V2 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S1V3 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S1V4 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S1V5 = excel_ws.cell(row=pnum, column=snnum).value

    pnum = 3
    snnum = 2
    #플레이어 2 값
    S2V1 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S2V2 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S2V3 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S2V4 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S2V5 = excel_ws.cell(row=pnum, column=snnum).value

    pnum = 4
    snnum = 2
    # 플레이어 3 값
    S3V1 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S3V2 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S3V3 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S3V4 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S3V5 = excel_ws.cell(row=pnum, column=snnum).value

    pnum = 5
    snnum = 2
    # 플레이어 4 값
    S4V1 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S4V2 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S4V3 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S4V4 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S4V5 = excel_ws.cell(row=pnum, column=snnum).value

    pnum = 6
    snnum = 2
    # 플레이어 5 값
    S5V1 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S5V2 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S5V3 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S5V4 = excel_ws.cell(row=pnum, column=snnum).value
    snnum += 1
    S5V5 = excel_ws.cell(row=pnum, column=snnum).value

    embed = nextcord.Embed(
        title='플레이어 정보',
        description='',
        color=nextcord.Color(0xFF0000)
        )
    embed.add_field(name='', value=f'『{P1}』님의 정보\n『{S1}:{S1V1}』\n『{S2}:{S1V2}』\n『{S3}:{S1V3}』\n『{S4}:{S1V4}』\n『{S5}:{S1V5}』\n\n『{P2}』님의 정보\n『{S1}:{S2V1}』\n『{S2}:{S2V2}』\n『{S3}:{S2V3}』\n『{S4}:{S2V4}』\n『{S5}:{S2V5}』\n\n『{P3}』님의 정보\n『{S1}:{S3V1}』\n『{S2}:{S3V2}』\n『{S3}:{S3V3}』\n『{S4}:{S3V4}』\n『{S5}:{S3V5}』\n\n『{P4}』님의 정보\n『{S1}:{S4V1}』\n『{S2}:{S4V2}』\n『{S3}:{S4V3}』\n『{S4}:{S4V4}』\n『{S5}:{S4V5}』\n\n『{P5}』님의 정보\n『{S1}:{S5V1}』\n『{S2}:{S5V2}』\n『{S3}:{S5V3}』\n『{S4}:{S5V4}』\n『{S5}:{S5V5}』')
    
    await ctx.send(embed=embed,ephemeral=True)

#전투를 종료하고 스텟을 초기화
@bot.slash_command(guild_ids=[Sid], name="전투종료",description="전투를 종료합니다.")
async def slash2(ctx:nextcord.Interaction):
    global IDNum
    global dir
    global Sid

    excel = load_workbook(dir)
    excel_ws = excel['Sheet']

    for i in range(2,6):
        excel_ws[f'B{i}'] = 1
        excel_ws[f'D{i}'] = excel_ws[f'C{i}'].value
        excel_ws[f'F{i}'] = excel_ws[f'E{i}'].value
        excel_ws[f'G{i}'] = False
    excel.save(dir)
    await ctx.send(f'전투를 종료하고 데이터를 초기화했습니다.',ephemeral=True)
    await ctx.channel.send(f'전투를 종료했습니다.')

#최댓값을 정한뒤 주사위 굴리기
@bot.slash_command(guild_ids=[1360509644442697849], name="roll", description="게임 진행에 필요한 주사위굴리기를 실행합니다 최대 값을 지정할수있습니다.")
async def slash2(ctx:nextcord.Interaction, 최대값: int=nextcord.SlashOption(description="주사위의 최대값을 적어주십시오 최소값은 1입니다.")):
    V = random.randint(1,최대값)
    await ctx.send(f'## 『{V}』')

#슬레시 없이 메세지를 보내는것으로 작동하는 스킬같은 명령어들        
@bot.event
async def on_message(msg:nextcord.Message):
    if msg.author.bot:
        return
    elif msg.content == "기본 공격":
        m = 1 #최솟값
        M = 10 #최댓값
        V = random.randint(m,M)
        await msg.channel.send(f'**``{V}의 피해를 입혔습니다.``**')
    elif msg.content == "참":
        m = 2 #최솟값
        M = 30 #최댓값
        V1 = random.randint(m,M)
        V2 = random.randint(m,M)
        V3 = random.randint(m,M)
        await msg.channel.send(f'**``{V1}의 피해를 입혔습니다.``**\n**``{V2}의 피해를 입혔습니다.``**\n**``{V3}의 피해를 입혔습니다.``**')
    elif msg.content == "상태 확인":
        global dir
        global Sid
        
        excel = load_workbook(dir)
        excel_ws = excel['Sheet']
        count = 0
        for i in range(2,7):
            cell = excel_ws.cell(row=i,column=1).value
            if msg.author.display_name== cell:
                count =+ 1
                column = i
                break

        if count == 0:
            await msg.channel.send("등록되지 않은 플레이어입니다.")
        else:
            isDEAD = excel_ws.cell(row=column,column=7).value
            Mhp = excel_ws.cell(row=column,column=3).value
            hp = excel_ws.cell(row=column,column=4).value
            Ms = excel_ws.cell(row=column,column=5).value
            s = excel_ws.cell(row=column,column=6).value
            mp = excel_ws.cell(row=column,column=2).value
            if isDEAD == True:
                await msg.channel.send(f'**``《 {cell} 》``** **``『행동 불능』``**{" <:To:1360529966357549252>"* int(mp or 0)}\n**``『체력』 ({hp}/{Mhp})``**\n**``『정신력』 ({s}/{Ms})``**')
            else:
                await msg.channel.send(f'**``《 {cell} 》``**{" <:To:1360529966357549252>"* int(mp or 0)}\n**``『체력』 ({hp}/{Mhp})``**\n**``『정신력』 ({s}/{Ms})``**')

#봇의 토큰
bot.run(TOKEN)       