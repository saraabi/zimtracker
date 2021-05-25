from django.core.management.base import BaseCommand, CommandError
from zimtracker.functions import update_vessels

class Command(BaseCommand):
    help = 'Updates information on all vessels'

    def handle(self, *args, **options):
        try:
            vessels = update_vessels()
        except Exception as error:
            self.stdout.write(self.style.ERROR(error))
            return
        if hasattr(vessels, 'meta'):
            if vessels.meta['TOTAL_RESULTS'] > 0:
                self.stdout.write(self.style.SUCCESS(
                    'Successfully updated {} vessels'.format(
                        vessels.meta['TOTAL_RESULTS'])))
            else:
                self.stdout.write(self.style.SUCCESS(
                    'No updated information available'))
        return