from django.core.management.base import BaseCommand
from django.utils import timezone
from website.models import *
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add cash to each user if needed'

    def handle(self, *args, **kwargs):
        user_infos = UserInfo.objects.all()
        amount = weeksSinceStart() * 10000
        for user_info in user_infos:
            user_info.updateAssets("")
            user_info.updateCash(amount)
            user_info.updateAddedCash(amount)
            user_info.updateLeaderboardPortfolioValue(amount)
            user_info.updatePriceHistory(str(round(float(amount), 2)))
        return