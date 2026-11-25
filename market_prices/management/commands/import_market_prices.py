
from django.core.management.base import BaseCommand, CommandError

from market_prices.services import (
    fetch_market_prices,
    AgmarknetAPIError,
)
from market_prices.importers import import_market_price_records


class Command(BaseCommand):

    help = 'Import or refresh agricultural market prices from Agmarknet.'

    def add_arguments(self, parser):

        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Number of records to fetch per API request.'
        )

        parser.add_argument(
            '--offset',
            type=int,
            default=0,
            help='Starting record offset.'
        )

        parser.add_argument(
            '--all',
            action='store_true',
            help='Fetch records in batches until no more records are available.'
        )

    def handle(self, *args, **options):

        limit = options['limit']
        offset = options['offset']
        import_all = options['all']

        if limit < 1:
            raise CommandError('--limit must be greater than zero.')

        if offset < 0:
            raise CommandError('--offset cannot be negative.')

        total_created = 0
        total_updated = 0
        total_skipped = 0
        total_received = 0

        self.stdout.write('Starting Agmarknet market-price import...')

        while True:

            self.stdout.write(
                f'Fetching records: offset={offset}, limit={limit}'
            )

            try:
                records = fetch_market_prices(
                    limit=limit,
                    offset=offset
                )

            except AgmarknetAPIError as exc:
                raise CommandError(
                    f'Agmarknet import failed: {exc}'
                ) from exc

            if not records:
                self.stdout.write('No more records available.')
                break

            result = import_market_price_records(records)

            total_received += result['total_received']
            total_created += result['created']
            total_updated += result['updated']
            total_skipped += result['skipped']

            self.stdout.write(
                f"Batch completed: "
                f"{result['created']} created, "
                f"{result['updated']} updated, "
                f"{result['skipped']} skipped."
            )

            for error in result['errors']:
                self.stdout.write(
                    self.style.WARNING(
                        f"Record {error['record']}: {error['error']}"
                    )
                )

            if not import_all:
                break

            offset += len(records)

            if len(records) < limit:
                break

        self.stdout.write('')
        self.stdout.write('Agmarknet import finished.')
        self.stdout.write(f'Total received: {total_received}')
        self.stdout.write(f'Created: {total_created}')
        self.stdout.write(f'Updated: {total_updated}')
        self.stdout.write(f'Skipped: {total_skipped}')
