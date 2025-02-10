import typer

from .reporter_lib.halo_reporter import HaloReporter
from .reporter import get_reporter
from .runner import PanchamRunner
from .pancham_configuration import OrderedPanchamConfiguration

app = typer.Typer()

@app.command()
def run(data_configuration: str, configuration: str):
    pancham_configuration = OrderedPanchamConfiguration(configuration)

    if pancham_configuration.reporter_name == 'spinner':
        reporter = get_reporter(pancham_configuration.debug_status, HaloReporter())
    else:
        reporter = get_reporter(pancham_configuration.debug_status)

    runner = PanchamRunner(pancham_configuration, reporter = reporter)
    runner.load_and_run(data_configuration)
