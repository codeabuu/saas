from django.core.management.base import BaseCommand
from subscriptions import utils as subs_utils
from typing import Any
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--days-left", default=0, type=int)
        parser.add_argument("--days-ago", default=0, type=int)
        parser.add_argument("--clear-dangling", action="store_true", default=False)
        
    def handle(self, *args, **options: Any):
        days_left = options.get("days_left")
        days_ago = options.get("days_ago")
        clear_dangling = options.get("clear_dangling")
        if clear_dangling:
            print("clearing unused dangling active subs")
            subs_utils.clear_dangling_subs()
        else:
            print("syncing active subs...")
            done = subs_utils.refresh_users_subscriptions(
                active_only=True,
                days_ago=days_ago,
                days_left=days_left,
                verbose=True)
            if done:
                print("Done")