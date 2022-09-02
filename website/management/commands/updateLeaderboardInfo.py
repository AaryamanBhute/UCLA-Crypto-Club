from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from website.models import *
from website.utils import *
from decimal import Decimal

class Command(BaseCommand):
    help = 'Updates information for leaderboard display'

    def handle(self, *args, **kwargs):
        user_infos = UserInfo.objects.all()
        guest_user_infos = GuestUserInfo.objects.all()
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
            user_info.addPriceHistory(round(val, 2))
        for user_info in guest_user_infos:
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
            user_info.addPriceHistory(round(val, 2))
        return