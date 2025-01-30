import typer

from .runner import PanchamRunner
from .pancham_configuration import OrderedPanchamConfiguration

app = typer.Typer()

@app.command()
def run(data_configuration: str, configuration: str):
    pancham_configuration = OrderedPanchamConfiguration(configuration)

    runner = PanchamRunner(pancham_configuration)
    runner.load_and_run(data_configuration)
