from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from discord_webhook import DiscordWebhook
from conf import *
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
login.click()

question = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[1]/div/div[2]/form/div/div[2]/div/h3").text
secq = driver.find_element_by_name("SecurityQuestionAnswer")

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

sleep(3)

xcdamt = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div/div/div/div[2]/table/tfoot/tr[2]/td[4]").text
usdamt = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div/div/div/div[2]/table/tfoot/tr[1]/td[4]").text

log.write("xcd aammout is " + xcdamt + "\n")
log.write("usd aammout is " + usdamt + "\n")

readxcd = open("xcd.txt", "r")
readusd = open("usd.txt", "r")
oldxcd = readxcd.read()
oldusd = readusd.read()

whtsappnum = "phone=+12645839999"
whtsappapi = "apikey=177844"

if not xcdamt == oldxcd:
    messge = xcdamt + " Is your new XCD balance"
    wtsmsg = xcdamt + "+Is+your+new+XCD+balance"
    #discord webhook
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/816492789307146240/VXFchUIUUEioJkVry7UiFTsTyxzIav6P8-6VsFZ5tzkOaDOQiTaoB7nQsA_pyYyUHT4L', content=messge)
    response = webhook.execute()
    #url for callmebot api
    urls = "https://api.callmebot.com/whatsapp.php?" + whtsappnum + "&text=" + wtsmsg + "&" + whtsappapi
    f = open("xcd.txt", "w")
    f.write(xcdamt)
    f.close()
    driver.get(urls)
    log.write("xcd ammout sent via whatsapp" + "\n")

if not usdamt == oldusd:
    messge = usdamt + " Is your new USD balance"
    wtsmsg = usdamt + "+Is+your+new+USD+balance"
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/816492789307146240/VXFchUIUUEioJkVry7UiFTsTyxzIav6P8-6VsFZ5tzkOaDOQiTaoB7nQsA_pyYyUHT4L', content=messge)
    response = webhook.execute()
    driver.get("https://api.callmebot.com/whatsapp.php?phone=+12645839999&text=" + wtsmsg + "&apikey=177844")
    f = open("usd.txt", "w")
    f.write(usdamt)
    f.close()
    log.write("usd ammout sent via whatsapp" + "\n")

driver.close()

log.write("Finished " + timenow + "\n")
log.close()
