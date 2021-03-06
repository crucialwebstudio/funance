import click

from selenium.common.exceptions import WebDriverException

from funance.scrape.provider import ProviderFactory


@click.command(
    short_help='Scrape data from supported providers'
)
@click.argument('provider', type=click.Choice(ProviderFactory().get_supported_providers(), case_sensitive=True))
@click.option('--session', is_flag=True, help='Re-use existing session. See `funance chromedriver service`')
def scrape(provider, session):
    """Scrape data from supported providers"""

    try:
        p = ProviderFactory().get_provider(provider, session)
        p.scrape()
    except (WebDriverException, KeyboardInterrupt) as e:
        # driver.close()
        # driver.quit()
        raise e
    finally:
        pass
        # driver.quit()
