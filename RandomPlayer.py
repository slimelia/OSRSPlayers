#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
import pickle
import getpass
import schedule
import mechanicalsoup
from OSRS_Hiscores import Hiscores
from cohost.models.user import User
from cohost.models.block import MarkdownBlock


POST_TEMPLATE = """
<table style="text-align:center;max-width:30em;margin:auto">
    <thead>
        <tr>
            <th>{username}</th>
            <th></th>
            <th>Rank {rank}</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><img src="https://oldschool.runescape.wiki/images/Attack_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Attack icon" title="Attack"> {attack}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Hitpoints_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Hitpoints icon" title="Hitpoints"> {hitpoints}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Mining_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Mining icon" title="Mining"> {mining}</td>
        </tr>
        <tr>
            <td><img src="https://oldschool.runescape.wiki/images/Strength_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Strength icon" title="Strength"> {strength}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Agility_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Agility icon" title="Agility"> {agility}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Smithing_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Smithing icon" title="Smithing"> {smithing}</td>
        </tr>
        <tr>
            <td><img src="https://oldschool.runescape.wiki/images/Defence_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Defence icon" title="Defence"> {defence}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Herblore_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Herblore icon" title="Herblore"> {herblore}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Fishing_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Fishing icon" title="Fishing"> {fishing}</td>
        </tr>
        <tr>
            <td><img src="https://oldschool.runescape.wiki/images/Ranged_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Ranged icon" title="Ranged"> {ranged}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Thieving_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Thieving icon" title="Thieving"> {thieving}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Cooking_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Cooking icon" title="Cooking"> {cooking}</td>
        </tr>
        <tr>
            <td><img src="https://oldschool.runescape.wiki/images/Prayer_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Prayer icon" title="Prayer"> {prayer}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Crafting_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Crafting icon" title="Crafting"> {crafting}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Firemaking_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Firemaking icon" title="Firemaking"> {firemaking}</td>
        </tr>
        <tr>
            <td><img src="https://oldschool.runescape.wiki/images/Magic_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Magic icon" title="Magic"> {magic}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Fletching_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Fletching icon" title="Fletching"> {fletching}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Woodcutting_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Woodcutting icon" title="Woodcutting"> {woodcutting}</td>
        </tr>
        <tr>
            <td><img src="https://oldschool.runescape.wiki/images/Runecraft_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Runecraft icon" title="Runecraft"> {runecraft}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Slayer_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Slayer icon" title="Slayer"> {slayer}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Farming_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Farming icon" title="Farming"> {farming}</td>
        </tr>
        <tr>
            <td><img src="https://oldschool.runescape.wiki/images/Construction_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Construction icon" title="Construction"> {construction}</td>
            <td><img src="https://oldschool.runescape.wiki/images/Hunter_icon.png" style="display:inline;margin-top:0;margin-bottom:0" alt="Hunter icon" title="Hunter"> {hunter}</td><td>Total {total}</td>
        </tr>
    </tbody>
</table>
"""

class PlayerRandomiser:
    __TOP=80000
    __URL='https://secure.runescape.com/m=hiscore_oldschool/overall?table=0&page='
    __ROWMAX = 25
    __HISCORES_CLASS = 'personal-hiscores__row'
    __HTML_TAG_CONTAINING_USERNAME = 'a'

    def __init__(self):
        self.alreadyPostedUsers = self.__getAlreadyPosted()
    
    def __getAlreadyPosted(self):
        try:
            with open('usernames.pickle','rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return set()
    
    def __pickNewUser(self):
        row = random.randint(0,PlayerRandomiser.__ROWMAX-1)
        page = PlayerRandomiser.__URL+str(random.randint(1,PlayerRandomiser.__TOP))
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(page)
        fetchedUsername = str(browser.page.find_all(class_=PlayerRandomiser.__HISCORES_CLASS)[row].find(PlayerRandomiser.__HTML_TAG_CONTAINING_USERNAME).contents[0])
        return fetchedUsername.replace(u'\xa0', '_').replace(' ','_')
    
    def getRandomUser(self):
        while (username := self.__pickNewUser()) in self.alreadyPostedUsers:
            pass
        self.alreadyPostedUsers.add(username)
        with open('usernames.pickle','wb') as f:
            pickle.dump(self.alreadyPostedUsers, f)
        print(self.alreadyPostedUsers)
        return Hiscores(username)
        
def post(page):
    randomiser = PlayerRandomiser()
    hiscoreRecord = randomiser.getRandomUser()
    username = hiscoreRecord.username.replace('_',' ')
    
    
    blocks = [
        MarkdownBlock(POST_TEMPLATE.format(
            username=username,
            rank=hiscoreRecord.skill('total','rank'),
            attack=hiscoreRecord.skill('attack'),
            hitpoints=hiscoreRecord.skill('hitpoints'),
            mining=hiscoreRecord.skill('mining'),
            strength=hiscoreRecord.skill('strength'),
            agility=hiscoreRecord.skill('agility'),
            smithing=hiscoreRecord.skill('smithing'),
            defence=hiscoreRecord.skill('defense'), #Incorrectly spelled with an 's' in OSRS_Hiscores, just to keep me on my toes.
            herblore=hiscoreRecord.skill('herblore'),
            fishing=hiscoreRecord.skill('fishing'),
            ranged=hiscoreRecord.skill('ranged'),
            thieving=hiscoreRecord.skill('thieving'),
            cooking=hiscoreRecord.skill('cooking'),
            prayer=hiscoreRecord.skill('prayer'),
            crafting=hiscoreRecord.skill('crafting'),
            firemaking=hiscoreRecord.skill('firemaking'),
            magic=hiscoreRecord.skill('magic'),
            fletching=hiscoreRecord.skill('fletching'),
            woodcutting=hiscoreRecord.skill('woodcutting'),
            runecraft=hiscoreRecord.skill('runecrafting'), #Real ones know that the skill name is just 'Runecraft'. The OSRS_Hiscores library doesn't.
            slayer=hiscoreRecord.skill('slayer'),
            farming=hiscoreRecord.skill('farming'),
            construction=hiscoreRecord.skill('construction'),
            hunter=hiscoreRecord.skill('hunter'),
            total=hiscoreRecord.skill('total')
            ))
    ]
    page.post(f'Random OSRS User of the Day: {username}', blocks,tags=['cohost.py', 'bot','botchosting','The Cohost Bot feed','automated post','osrs','old school runescape','RuneScape'])
    return 0


if __name__ == '__main__':
    cohost = User.login(input("Cohost login username: "),getpass.getpass("Cohost password: "))
    # cohost = User.loginWithCookie(input('Cookie: '))
    page = cohost.getProject(input("Cohost page name: "))
    
    schedule.every().day.at("11:00","Europe/London").do(post, page=page)
    while True:
        schedule.run_pending()
        time.sleep(1)
        
        
    

    
