import typer
import sys
from loguru import logger
from datetime import datetime
from colorama import init, Fore, Style

from .utils.fetch_data import FetchData

init(autoreset=True)  # colorama init
timestamp = datetime.now().strftime("%Y-%m-%d T%H%M%S")

app = typer.Typer(add_completion=False)


# @logger.catch  # for internal debugging
@app.callback(no_args_is_help=True,
              invoke_without_command=True,
              help='A metadata plugin for fetching Metadata from the Fichub API for the fichub-cli')
def metadata(
    input: str = typer.Option(
        "", "-i", "--input", help="Input: Either an URL or path to a file"),

    out_dir: str = typer.Option(
        "", "-o", " --out-dir", help="Path to the Output directory for files (default: Current Directory)"),

    debug: bool = typer.Option(
        False, "-d", " --debug", help="Show the log in the console for debugging", is_flag=True),

    log: bool = typer.Option(
        False, help="Save the logfile for debugging", is_flag=True),

    automated: bool = typer.Option(
        False, "-a", "--automated", help="For internal testing only", is_flag=True, hidden=True),

    version: bool = typer.Option(
        False, help="Display version & quit", is_flag=True)


):
    if log:
        debug = True
        typer.echo(
            Fore.GREEN + f"Creating fichub_cli - {timestamp}.log in the current directory" + Style.RESET_ALL)
        logger.add(f"fichub_cli - {timestamp}.log")

    if input:
        fic = FetchData(debug=debug, automated=automated,
                        out_dir=out_dir)
        fic.get_metadata(input)

    if version:
        typer.echo("fichub-cli-metadata: v0.1")

    try:
        if fic.exit_status == 1:
            typer.echo(Fore.RED + """
Unsupported URLs found! Check err.log in the current directory!""" + Style.RESET_ALL)
        sys.exit(fic.exit_status)
    except UnboundLocalError:
        sys.exit(0)
