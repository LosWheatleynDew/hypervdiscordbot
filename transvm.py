import discord
import subprocess
import asyncio
from datetime import datetime
from discord.ext import commands
import json

try: #get data from the json file
    with open('settings.json', 'r') as file:
        data = json.load(file)
    print("File data =", data)
    
except FileNotFoundError:
    print("Error: The file 'data.json' was not found.")
    

## important init DO NOT DELETE
intents = discord.Intents.default()
intents.message_content = True
curr_time = datetime #the current time the user will call it when needed

pre_Fstop = True #if this is false that means the user consented and should be ready to start the shutdown procedure
pre_BMreboot = 0 #0 is the normal value, 1 is a different user requesting consent 2 is the computer owner consent for reboot
pre_FMreboot = 0 #0 is normal, 1 is the user wanted it, 2 is waiting for the count
chanFMreboot = '' #This is the channel where the person wanted send

bot = commands.Bot(command_prefix="~", intents=intents)

#the name of the hyperV instance
vmname = data["vmname"]
##force otu abort

async def cynabortion(ctx):
    global vmname
    result = subprocess.run(["shutdown", "/a"], capture_output=True, text=True)
    chan = bot.get_channel(chanFMreboot) #tell the person who start the reboot that its aborted
    if result.stderr:
        await ctx.send('''```ansi
[1;2m[1;2m[1;31mWARNING AN EXCEPTION OCCURED[0m[0m[0m
```
```diff
-'''+ result.stderr + '''```''')
    elif result.stdout:
        await ctx.send("RESPONSE FROM SYSTEM >>\n" + "```" + result.stdout +"```")
    else:
        await ctx.send("**Reboot Aborted by <@" + str(ctx.message.author.id) + ">**")
        await chan.send("**Reboot Aborted by <@" + str(ctx.message.author.id) + ">**")


##end of abort

##force otu reboot
async def cynforce(ctx):
    global vmname
    result = subprocess.run(["shutdown", "/r", "/t", "60", "/f", "/c" , '"Mahiro is about to restart your pc! Send ~abort to abort"'], capture_output=True, text=True)

    if result.stderr:
        await ctx.send('''```ansi
[1;2m[1;2m[1;31mWARNING AN EXCEPTION OCCURED[0m[0m[0m
```
```diff
-'''+ result.stderr + '''```''')
    elif result.stdout:
        await ctx.send("RESPONSE FROM SYSTEM >>\n" + "```" + result.stdout +"```")
    else:
        await ctx.send("Starting 60 second countdown...")

#end of it


## finish
#start up function
async def startuparea(ctx):
    global vmname
    memchk = subprocess.run(["powershell.exe", "Get-VMMemory", vmname, "|", "Select-Object", "-ExpandProperty", "Startup"], capture_output=True, text=True)
    
    memchk = int((int(memchk.stdout) - 400000000)/1000000000) #first convert string to int then subtract 400 million then divide by 100 million then truncate the decimal 
    await ctx.send(f"Sending `Start-VM -Name {vmname}` command with " + str(memchk) + "gb of RAM...") 
    result = subprocess.run(["powershell.exe", "Start-VM", "-Name", vmname], capture_output=True, text=True)

    #print(result.stdout)
    #print(result.stderr)
    
    await asyncio.sleep(5)
    
    if result.stderr:# if detects err output first
        await ctx.send('''```ansi
[1;2m[1;2m[1;31mWARNING AN EXCEPTION OCCURED[0m[0m[0m
```
```diff
-'''+ result.stderr + '''```''')
        
    elif result.stdout:     #if theres something to be noted
        await ctx.send("RESPONSE FROM SYSTEM >>\n" + "```" + result.stdout +"```")
    else: #unless said
        await ctx.send("Assumed start up was successful... [Note startup can take up to 1 minute]\nIf Parsec isn't working try running the command again")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("SYS OK || ~helpy for VM commands-"))

#end of startup function
#force shutdown function

async def forceshutoff(ctx):
    global vmname
    await ctx.send(f'''
Sending `Stop-VM -Name {vmname} -TurnOff` command...
```diff
-Force shutdown init...
```''')
    result = subprocess.run(["powershell.exe", "Stop-VM", "-Name", vmname, "-TurnOff"], capture_output=True, text=True) 

    if result.stderr:
        await ctx.send('''```ansi
[1;2m[1;2m[1;31mWARNING AN EXCEPTION OCCURED[0m[0m[0m
```
```diff
-'''+ result.stderr + '''```''')
    elif result.stdout:     #if theres something to be noted
        await ctx.send("RESPONSE FROM SYSTEM >>\n" + "```" + result.stdout +"```")
    else: #unless said
        await ctx.send("System is now OFF")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("SYS Offline! || ~helpy for VM commands-"))
#end of force shutdown
#SAFE shutdown

async def shutoff(ctx):
    global vmname
    await ctx.send(f"Sending `Stop-VM -Name {vmname}` command...")
    result = subprocess.run(["powershell.exe", "Stop-VM", "-Name", vmname], capture_output=True, text=True)
    if result.stderr:
        await ctx.send('''```ansi
[1;2m[1;2m[1;31mWARNING AN EXCEPTION OCCURED[0m[0m[0m
```
```diff
-'''+ result.stderr + '''```''')
    elif result.stdout:     #if theres something to be noted
        await ctx.send("RESPONSE FROM SYSTEM >>\n" + "```" + result.stdout +"```")
    else: #unless said
        await ctx.send("System is now OFF")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("SYS Offline! || ~helpy for VM commands-"))
#end of safe shutdown
#set the memmory
async def setmemowy(ctx, intarg):
    global vmname
    result = subprocess.run(["powershell.exe", "Set-VMMemory", vmname, "-StartupBytes", str(intarg)+"GB"], capture_output=True, text=True)
    await ctx.send(f"Sending `Set-VMMemory {vmname} -StartupBytes "+str(intarg)+"GB` command...")

    if result.stderr:
        await ctx.send('''```ansi
[1;2m[1;2m[1;31mWARNING AN EXCEPTION OCCURED[0m[0m[0m
```
```diff
-'''+ result.stderr + '''```''')
    elif result.stdout:     #if theres something to be noted
        await ctx.send("RESPONSE FROM SYSTEM >>\n" + "```" + result.stdout +"```")
    else: #unless said
        await ctx.send("VM RAM set to " + str(intarg) + "gb")

async def oturebooty(ctx):
    await ctx.send("Sending `Restart-Computer -Force` command...")
    await ctx.send("Mahiro/OcTiU-I shutting down.. have a good night..")
    subprocess.run(["powershell.exe", "Restart-Computer", "-Force"])
    


#####################
#####################

# This is for the presence and status of machine
async def status_task():
    global vmname, pre_Fstop, pre_BMreboot, pre_FMreboot
    while(True):
        result = subprocess.run(["powershell.exe", "Get-VM", "-Name", vmname, "|", "Select-Object", "-ExpandProperty", "State"], capture_output=True, text=True)
        #print("statusofvm =", result.stdout)

        if result.stderr: #this is mainly used if something went VERY BAD
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("WARNING Exception occured! Check logs"))
            #print("EXCEPTION!!!", result.stderr)
  
        res = result.stdout #theres a getline at the end of the value taken from the command
        res = res.replace("\n", "") #so get rid of it or else the match case won't worky
        
        match res: #see if the status of the VM is either Off or Running
            case "Running":
                await bot.change_presence(status=discord.Status.online, activity=discord.Game("SYS OK || ~helpy for VM commands-"))
                #print("VM STAT", "ONLINE__")
            case "Off":
                await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("SYS Offline! || ~helpy for VM commands-"))
                #print("VM STAT", "OFFLINE__")
            case _:
                print("Invalid?")
        
        pre_Fstop = True #resets pre_Fstop if the user changes its mine on pulling the plug on the vm
        pre_BMreboot = 0 #resets pre_BMreboot if the user changes its mine on pulling the plug on the vm
        pre_FMreboot = 0 #resets if the user changes its mind on shutting down my pc
        await asyncio.sleep(60)

@bot.event #on ready used for initatal startup of the program NOT THE BOT ON DISCORD
async def on_ready():
    print("よし、行くぞ！")
    #await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Starting up..."))
    for server in bot.guilds:
        await bot.tree.sync(guild=discord.Object(id=server.id))
    bot.loop.create_task(status_task())
 
@bot.event #just when a message is sent and detected nothing else uwu
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message) #taisetsu, allows other commands from being read


@bot.hybrid_command(name='start', description="I du know is dis worky?")
async def startup(ctx):
    #print("######### Start Seq INIT ##########")
    await ctx.send('Acknowledged, Initializing starting sequence...')
    await startuparea(ctx)


@bot.hybrid_command(name="forcestop", description="Something must have gone terribly wrong. Pull the plug!")
async def fstop(ctx):
    global pre_Fstop
    if pre_Fstop:
        await ctx.send('Are you really sure you want to do this? \nAny Unsaved data **WILL** be lost, this is equivalent to pulling the plug\n[type ~forcestop again to force stop]')
        pre_Fstop = False
    else:
        pre_Fstop = True
        await forceshutoff(ctx)

@bot.hybrid_command(name="shutdown", description="A safer alternative to turning off the pc RECOMMENDED")
async def stopu(ctx):
    #print("######### Stop Seq INIT ###########")
    await ctx.send("Acknowledge, Initializing shutdown sequence..")
    await shutoff(ctx)

@bot.hybrid_command(name="setram", description="It sets the allowed memory for the vm?")
async def setm(ctx, arg):
    result = subprocess.run(["powershell.exe", "Get-VM", "-Name", vmname, "|", "Select-Object", "-ExpandProperty", "State"], capture_output=True, text=True)
    if result.stdout.replace("\n", "") == "Running": #check first to see if the system is running or else it will throw an error at you
        await ctx.send("You need to turn off the VM in order to change RAM") 
        return
    
    try: #first thing first is to try to see if you can convert the user arguments to an int for processing
        intarg = int(arg)
    except: #if you can't raise the exception then quit the function
        await ctx.send("Invalid argument! [Note: If you put GB at the end, remove it just put the value you want]\nExample:\n`~setram 8` set for 8gb of RAM")
        return #its not valid argument
    
    if intarg > 16 or intarg < 6: #allowed memory is  6 <= x <= 16
        await ctx.send("Maximum memory allowed 16GB and minimum of 6GB")
        return
    await ctx.send("Okay then.. setting value to " + str(intarg) + "gb")

    await setmemowy(ctx, intarg)

@bot.hybrid_command(name='reboot', value="Just do a shutdown and start up")
async def rebot(ctx):
    await ctx.send('okayy just gimmie a moment...')
    await shutoff(ctx)
    await ctx.send('Finish shutdown... Starting up...')
    await asyncio.sleep(5)
    await startuparea(ctx)
    await ctx.send("SYS reboot completed!")

@bot.hybrid_command(name='otureboot', description="Requires the host's consent! bare metal reboot")
async def nturebot(ctx):
    global pre_BMreboot
    match pre_BMreboot:
        case 0:
            await ctx.send("**Disclaimer!** This requires the host's approval. I need her approval before i'm able to rebooter her computer\ndo you wish to continue? [send ~otureboot to request for the host's consent]")
            pre_BMreboot = 1 #changes to the second stage
        case 1:
            await ctx.send("<@266032204243533825> requesting for restart of your pc. do you accept? [send ~otureboot]")
            pre_BMreboot = 2 #changes to the third stage
        case 2:
            if str(ctx.message.author.id) == '266032204243533825':
                await ctx.send("Authorized consent! rebooting OcTiU-I...")
                pre_BMreboot = 0 #resets back this area is when two parties consented for bare metal reboot
                await oturebooty(ctx)
            else:
                await ctx.send("Unauthorized consent! only <@266032204243533825> is allowed to accept")

@bot.hybrid_command(name='oturebootforce', description="Force the host's pc to reboot")
async def fnturebot(ctx):
    global pre_FMreboot, curr_time, chanFMreboot
    #await ctx.send(curr_time.now().hour)
    if curr_time.now().hour >= 19 or curr_time.now().hour <= 12:
        await ctx.send("I'm sorry but this command is only available between <t:1744916400:T>~<t:1744941600:T>")
        return

    match pre_FMreboot:
        case 0: #first warning
            await ctx.send("I'm sure the host will understand. Continue? [type command again]")
            pre_FMreboot = 1
        case 1: #second warning
            await ctx.send("This is your last warning, Are you really sure?\nThere will be a 1 minute wait before it restarts\n**Use ~abort to stop**\n**Type ~oturebootforce to restart**")
            pre_FMreboot = 2
        case 2: #start the reboot process
            await ctx.send("The host's PC will reboot in 1 minute **To abort restart type ~abort**")
            chanFMreboot = ctx.channel.id #get the channel id of where the user started the process
            await cynforce(ctx)

@bot.hybrid_command(name='abort', description="Abort the forced shutdown")
async def abortion(ctx):
    global chanFMreboot, pre_FMreboot
    #print(chanFMreboot)
    pre_FMreboot = 0
    await cynabortion(ctx)
 
    

@bot.hybrid_command(name='helpy', description="forgot commands? just go here!")
async def hellp(ctx):
    embed = discord.Embed(title="VM Commands", description="Commands related to the VM", colour=discord.Colour.pink(), type="rich")
    embed.set_author(name=bot.user.display_name)
    embed.set_thumbnail(url=bot.user.display_avatar)

    embed.add_field(name="start", value="it starts it?")
    embed.add_field(name="forcestop", value="Very dangerous, Pull the plug")
    embed.add_field(name="shutdown", value="Highly recommended")
    embed.add_field(name="setram", value="Change RAM size for VM from\n6gb <= n <= 16gb")
    embed.add_field(name="reboot", value="Does shutdown and start commands")
    embed.add_field(name="otureboot", value="Reboots the host's machine [aka bare metal reboot] **REQUIRES THE HOST'S CONSENT**")
    embed.add_field(name="oturebootforce", value="Reboots the host's machine without consent Only between 12:00~19:00")
    embed.add_field(name ="abort" , value="Abort the force reboot")
    await ctx.send(embed=embed)







































bot.run(data["token"])