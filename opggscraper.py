from unicodedata import decimal
import winsound
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np
import time
from sklearn.utils import resample


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


summonerName = input()

PATH = "C:\webdrivers\chromedriver.exe"
site = 'https://na.op.gg/summoners/na/' + summonerName.replace(" ", "%20")

# Argument options for Driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--log-level=3")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize driver and get site url
driver = webdriver.Chrome(PATH, options=options)
driver.get(site)
# time.sleep(5)

# Clicks Update button, if available
updateButton = driver.find_element_by_xpath('//button[text()="Update"]')

if updateButton.is_enabled():
    updateButton.click()
    time.sleep(5)

# Shows only Ranked Games
driver.find_element_by_xpath(
    '//*[@id="content-container"]/div[2]/div[1]/ul/li[2]/button').click()
time.sleep(5)


# RESULT =      driver.find_element_by_xpath(f"(//div[contains(@class, 'result')])[{gameNumber}]")
# NAME =        driver.find_element_by_xpath(f"(//*[@id='content-container']/div[2]/div[3]/li[{gameNumber}]/div/div[3]/ul[{team}]/li[{player}]/div[2]/a)")
# CHAMPION =    driver.find_element_by_xpath(f"(//*[@id='content-container']/div[2]/div[3]/li[{gameNumber}]/div/div[3]/ul[{team}]/li[{player}]/div[1]/img)")
# SHOW MORE =   driver.find_element_by_xpath('//*[@id="content-container"]/div[2]/button').click()

flag = True
gameNumber = 1

# Lists to hold results
championsPlayed = []
championsPlayedAgainst = []
gamesWon = []
gamesLost = []


while flag:
    if check_exists_by_xpath(f"(//div[contains(@class, 'result')])[{gameNumber}]"):
        result = driver.find_element_by_xpath(
            f"(//div[contains(@class, 'result')])[{gameNumber}]")

        # Tallies wins and losses based on result text
        if result.text == 'Victory':
            gamesWon.append(1)
            gamesLost.append(0)
        elif result.text == 'Defeat':
            gamesWon.append(0)
            gamesLost.append(1)
        else:
            gameNumber += 1
            continue

        championList = []

        for team in range(1, 3):
            for player in range(1, 6):
                name = driver.find_element_by_xpath(
                    f"(//*[@id='content-container']/div[2]/div[3]/li[{gameNumber}]/div/div[3]/ul[{team}]/li[{player}]/div[2]/a)")

                champion = driver.find_element_by_xpath(
                    f"(//*[@id='content-container']/div[2]/div[3]/li[{gameNumber}]/div/div[3]/ul[{team}]/li[{player}]/div[1]/img)")
                championName = champion.get_attribute("alt")
                if name.text == summonerName:
                    championName = '*' + championName

                championList.append(championName)

        # Searches champion list for entry with * and stores it as yourChampion
        for idx, num in enumerate(championList):
            if '*' in num:
                yourChampion = championList[idx]
                id = idx

        # Cascading if to determine position of enemy lane opponent
        if id == 0:
            enemyChampion = championList[5]
        elif id == 1:
            enemyChampion = championList[6]
        elif id == 2:
            enemyChampion = championList[7]
        elif id == 3:
            enemyChampion = championList[8]
        elif id == 4:
            enemyChampion = championList[9]
        elif id == 5:
            enemyChampion = championList[0]
        elif id == 6:
            enemyChampion = championList[1]
        elif id == 7:
            enemyChampion = championList[2]
        elif id == 8:
            enemyChampion = championList[3]
        elif id == 9:
            enemyChampion = championList[4]

        championsPlayed.append(yourChampion)
        championsPlayedAgainst.append(enemyChampion)

        # print(f'{gameNumber}, {result.text}, {yourChampion} | {enemyChampion}')
        print(f'Processing Game: {gameNumber}')

    # If game result not on screen, click "Show More" button. If "Show More" button is disabled, break out of while loop.
    else:
        if check_exists_by_xpath('//*[@id="content-container"]/div[2]/button'):
            driver.find_element_by_xpath(
                '//*[@id="content-container"]/div[2]/button').click()
            time.sleep(1)
            gameNumber -= 1
        else:
            break

    gameNumber += 1

zipped = zip(championsPlayed, championsPlayedAgainst, gamesWon, gamesLost)
zippedList = list(zipped)

df = pd.DataFrame(zippedList, columns=[
                  'Your Champ', 'Enemy Champ', 'Won', 'Lost'])


groupedMultiple = df.groupby(['Your Champ', 'Enemy Champ']).agg(
    GamesWon=('Won', 'sum'), GamesLost=('Lost', 'sum'))

groupedMultiple.loc[:, 'Total'] = groupedMultiple.sum(
    numeric_only=True, axis=1)

groupedMultiple['WinPercent'] = (
    groupedMultiple['GamesWon']/groupedMultiple['Total'] * 100)

groupedMultiple['WinPercent'] = groupedMultiple['WinPercent'].astype(
    float).round(1)

sorted_df = groupedMultiple.sort_values(
    by=['Your Champ', 'Total'], ascending=[True, False])


print(sorted_df.to_string())

with open('opggoutput.txt', 'w') as outfile:
    sorted_df.to_string(outfile)

print(f"Games Recorded: {len(championsPlayed)}")


driver.close()
