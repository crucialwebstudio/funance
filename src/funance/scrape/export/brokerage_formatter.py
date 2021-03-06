import csv
import json
import os

from funance.common.paths import EXPORT_DIR
from funance.common.logger import get_logger

PREFIX = 'brokerage'

logger = get_logger('csv')


class CsvFormatter:
    HEADERS = ['account_name', 'ticker', 'date_acquired', 'num_shares', 'cost_per_share', 'total_cost', 'term']

    def __init__(self):
        pass

    def format(self):
        filenames = [
            f for f in os.listdir(EXPORT_DIR) if f.startswith(PREFIX) and f.endswith('.json')
        ]
        logger.debug(f"Found exported filenames: {filenames}")
        exported_filename = f'{EXPORT_DIR}/{PREFIX}.csv'
        with open(exported_filename, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.HEADERS)
            writer.writeheader()

            for filename in filenames:
                logger.info(f'Processing file {filename}')
                with open(f"{EXPORT_DIR}/{filename}", "r") as src_file:
                    data = json.load(src_file)
                    for a in data['accounts'].values():
                        for cb in a['cost_basis'].values():
                            for lot in cb['lots']:
                                writer.writerow(dict(
                                    ticker=cb['ticker'],
                                    date_acquired=lot['date_acquired'],
                                    num_shares=lot['num_shares'],
                                    cost_per_share=lot['cost_per_share'],
                                    total_cost=lot['total_cost'],
                                    account_name=a['account_name'],
                                    term=lot['term']
                                ))
        logger.info(f'Generated file: {exported_filename}')


class UnsupportedFormatterException(Exception):
    pass


class BrokerageFormatterFactory:
    formatters = {
        'csv': CsvFormatter
    }

    def get_supported_formatters(self):
        return self.formatters.keys()

    def get_formatter(self, formatter_name):
        formatter_class = self.formatters.get(formatter_name)
        if formatter_class is None:
            supported_formatters = ', '.join(self.get_supported_formatters())
            raise UnsupportedFormatterException(f"Formatter must be one of {supported_formatters}")
        return formatter_class()
