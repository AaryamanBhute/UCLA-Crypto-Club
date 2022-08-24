from django.core.management.base import BaseCommand
from django.utils import timezone
from website.models import *
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add cash to each user if needed'

    def handle(self, *args, **kwargs):
        user_infos = UserInfo.objects.all()
        for user_info in user_infos:
            amount = weeksSinceStart() * 10000
            if(user_info.added_cash < amount):
                balance = amount - user_info.added_cash
                user_info.addCash(balance)
                user_info.addAddedCash(balance)
        return