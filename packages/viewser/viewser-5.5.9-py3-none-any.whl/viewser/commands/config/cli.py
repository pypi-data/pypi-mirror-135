import sys
import click
import json
import tabulate
from viewser import settings

@click.group(name="config", short_help="configure viewser")
def cli():
    """
    Configure viewser
    """

@cli.command(name="interactive", short_help="interactively configure viewser")
def config_interactive():
    """
    Interactively configure viewser (useful for first-time config)
    """
    settings.configure_interactively()
    click.echo("All done!")

@cli.command(name="set", short_help="set a configuration value")
@click.argument("name", type=str)
@click.argument("value", type=str, default=1)
@click.option("--override/--no-override",default=True)
def config_set(name: str, value: str, override: bool): # pylint: disable=redefined-builtin
    """
    Set a configuration value.
    """
    overrides = True
    try:
        settings.config.get(name)
    except KeyError:
        overrides = False

    if not override and overrides:
        click.echo(f"Setting {name} already set, override not specified (see --help)")
        return

    settings.config.set(name,value)
    click.echo(f"{name}: {value}")

@cli.command(name="get", short_help="get a configuration value")
@click.argument("name", type=str)
def config_get(name: str):
    """
    Get a configuration value.
    """
    value = settings.config.get(name)
    if value:
        click.echo(f"{name}: {value}")
    else:
        click.echo(f"{name} not set")
        sys.exit(1)

@cli.command(name="reset", short_help="reset default config values")
@click.confirmation_option(prompt="Reset config?")
def config_reset():
    """
    Reset config, writing default values over current values.
    """
    settings.config.load(settings.static.DEFAULT_SETTINGS, overwrite = True)
    click.echo("Config file reset")

@cli.command(name="list", short_help="show all configuration settings")
def config_list():
    """
    Show all current configuration values
    """
    click.echo(tabulate.tabulate(settings.config.list().items()))

@cli.command(name="unset", short_help="unset a configuration value")
@click.confirmation_option(prompt="Unset config key?")
@click.argument("name", type=str)
def config_unset(name: str):
    """
    Unset a configuration value, removing its entry from the config file.
    """
    current_value = settings.config.get(name)
    settings.config.unset(name)
    click.echo(f"Unset {name} (was {current_value})")

@cli.command(name = "dump", short_help = "dump current config as JSON")
def config_dump():
    click.echo(json.dumps(settings.config.list()))
