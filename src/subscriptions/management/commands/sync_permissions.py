from django.core.management.base import BaseCommand

from subscriptions import utils as subs_util
class Command(BaseCommand):

    def handle(self, *args, **options):
        subs_util.sysc_sub_group_permissions()