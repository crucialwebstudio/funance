from datetime import date

from dateutil.relativedelta import relativedelta

from .datespec import DATE_FORMAT
from .projector import Projector
from funance.dashboard.components import ForecastLineAIO


def get_charts(spec):
    start_date = date.today() + relativedelta(days=1)
    end_date = start_date + relativedelta(years=1)
    projector = Projector.from_spec(spec,
                                    start_date.strftime(DATE_FORMAT),
                                    end_date.strftime(DATE_FORMAT))
    charts = []
    for chart in spec['chart_spec']:
        accounts = list(
            map(
                lambda a: dict(
                    name=projector.get_account(a).name,
                    df=projector.get_account(a).get_running_balance_grouped()
                ),
                chart['account_ids']
            )
        )
        charts.append(ForecastLineAIO(title=chart['name'], accounts=accounts))
    return charts
