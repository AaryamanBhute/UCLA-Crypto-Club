from .models import *
from .utils import *
from decimal import Decimal

def updateUserCashAmounts():
    user_infos = UserInfo.objects.all()
    for user_info in user_infos:
        amount = weeksSinceStart() * 10000
        if(user_info.added_cash < amount):
            balance = amount - user_info.added_cash
            user_info.addCash(balance)
            user_info.addAddedCash(balance)

def updateUserCashAmounts_hook(i):
    print("finished updating cash", i)

def updateUserPortfolioValues():
    user_infos = UserInfo.objects.all()
    for user_info in user_infos:
        asset_string = user_info.assets
        if(asset_string == ""):
            assets = []
        else:
            assets = asset_string.split(";")
        asset_ids = []
        asset_amts = []
        for asset in assets:
            ind = asset.find("/")
            asset_ids.append(asset[:ind])
            asset_amts.append(asset[ind+1:])
        assets_value = Decimal(0)
        infos = getInfos(asset_ids)['data']
        assetToVal = {}
        for info in infos:
            assetToVal[info['id']] = Decimal(info['priceUsd'])
        for asset_id, asset_amt in zip(asset_ids, asset_amts):
            assets_value += assetToVal[asset_id] * Decimal(asset_amt)
        val = assets_value + user_info.cash
        user_info.updateLeaderboardPortfolioValue(val)
        user_info.addPriceHistory(val)

def updateUserPortfolioValues_hook(i):
    print("finished updating leaderboard values", i)