from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from discord_webhook import DiscordWebhook
from config import *
logtime = datetime.datetime.now()
timenow = logtime.strftime("%c")

log = open("log.txt", "a")

log.write("Start at " + timenow + "\n")

driver = webdriver.Chrome(PATH)
driver.get("https://online.ncbal.com/")
username = driver.find_element_by_name("UserName")
password = driver.find_element_by_name("Password")

#login Credentials
username.send_keys(un)
password.send_keys(pw)

login = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[1]/div/div[2]/form/div/div[5]/div[2]/div/button")

#click
login.click()

question = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[1]/div/div[2]/form/div/div[2]/div/h3").text
secq = driver.find_element_by_name("SecurityQuestionAnswer")

#log write
log.write("Security question was " + question +  "\n")

#security questionn 1
if question == qes1:
    secq.send_keys(ans1)
    print("A")

#security question 2
if question == qes2:
    secq.send_keys(ans2)
    print("B")

#security question 3
if question == qes3:
    secq.send_keys(ans3)
    print("C")

qsubmit = driver.find_element_by_id("AnswerQuestion")
qsubmit.click()

sleep(5)

#function to clean info
def clean(string):
    new = string.replace(",", "")
    num = float(new)
    print(num)
    return num

xcdamt = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div/div/div/div[2]/table/tfoot/tr[2]/td[4]").text
usdamt = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div/div/div/div[2]/table/tfoot/tr[1]/td[4]").text

log.write("xcd aammout is " + xcdamt + "\n")
log.write("usd aammout is " + usdamt + "\n")

readxcd = open("xcd.txt", "r")
readusd = open("usd.txt", "r")
oldxcd = readxcd.read()
oldusd = readusd.read()

xcdamt = clean(xcdamt)
usdamt = clean(usdamt)
oldusd = clean(oldusd)
oldxcd = clean(oldxcd)

if oldxcd > xcdamt:
    chng = oldxcd - xcdamt
    xcdtrans = "XCD+SUB+" + str(chng)
else:
    chng = xcdamt - oldxcd
    xcdtrans = "XCD+ADD+" + str(chng)

if oldusd > usdamt:    
    chng = oldxcd - usdamt
    usdtrans = "USD+SUB+" + str(chng)
else:    
    chng = usdamt - oldusd
    usdtrans = "USD+ADD+" + str(chng)

xcdamt = str(xcdamt)
usdamt = str(usdamt)
oldusd = str(oldusd)
oldxcd = str(oldxcd)


if not xcdamt == oldxcd:
    messge = xcdamt + " Is your new XCD balance"
    wtsmsg = xcdamt + "+Is+your+new+XCD+balance"
    wtsmsgg = xcdtrans

    #discord webhook
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/816492789307146240/VXFchUIUUEioJkVry7UiFTsTyxzIav6P8-6VsFZ5tzkOaDOQiTaoB7nQsA_pyYyUHT4L', content=messge)
    response = webhook.execute()
    #url for callmebot api
    urls = "https://api.callmebot.com/whatsapp.php?" + whtsappnum + "&text=" + wtsmsg + "&" + whtsappapi   
    urlss = "https://api.callmebot.com/whatsapp.php?" + whtsappnum + "&text=" + wtsmsgg + "&" + whtsappapi
    f = open("xcd.txt", "w")
    f.write(xcdamt)
    f.close()
    driver.get(urlss)
    driver.get(urls)
    log.write("xcd ammout sent via whatsapp" + "\n")

sleep(30)

if not usdamt == oldusd:
    messge = usdamt + " Is your new USD balance"
    wtsmsg = usdamt + "+Is+your+new+USD+balance"
    wtsmsgg = usdtrans
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/816492789307146240/VXFchUIUUEioJkVry7UiFTsTyxzIav6P8-6VsFZ5tzkOaDOQiTaoB7nQsA_pyYyUHT4L', content=messge)
    response = webhook.execute()
    driver.get("https://api.callmebot.com/whatsapp.php?phone=+12645839999&text=" + wtsmsgg + "&" + whtsappapi)    
    driver.get("https://api.callmebot.com/whatsapp.php?phone=+12645839999&text=" + wtsmsg + "&" + whtsappapi)
    f = open("usd.txt", "w")
    f.write(usdamt)
    f.close()
    log.write("usd ammout sent via whatsapp" + "\n")

driver.close()

log.write("Finished " + timenow + "\n")
log.close()
quit()
