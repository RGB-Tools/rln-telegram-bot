"""Utilities module."""
import os
import sys
from configparser import ConfigParser, MissingSectionHeaderError

from rgb_lib import BitcoinNetwork


def die(message=None, exit_code=1):
    """Print message to stderr and exit with the requested error code."""
    if message:
        print(message, file=sys.stderr)
    sys.exit(exit_code)


def parse_config():
    """Parse the configuration file."""
    if not os.path.exists("config.ini"):
        die("config.ini not found, copy and eventually edit the config.ini.sample file")
    raw_config = ConfigParser()
    config_section = "config"
    try:
        raw_config.read("config.ini", encoding="utf-8")
        if not raw_config.has_section(config_section):
            raise RuntimeError
    except (MissingSectionHeaderError, RuntimeError):
        die(f"config.ini should contain a [{config_section}] section")
    return raw_config["config"]


def get_or_exit(conf, var_name, integer=False):
    """Get the requested config option, exit when missing."""
    config_val = conf.get(var_name)
    if config_val is None:
        die(f"No {var_name} in config")
    if integer:
        if not config_val.isdigit():
            die("the config variable {var_name} must be an integer")
        return int(config_val)
    return config_val


def get_or_default(conf, var_name, default_val):
    """Get the requested config option, use default when missing."""
    config_val = conf.get(var_name)
    return default_val if config_val is None else config_val


def parse_network(network):
    """Parse the given network string and return the corresponding enum."""
    match network:
        case "Mainnet":
            return BitcoinNetwork.MAINNET
        case "Regtest":
            return BitcoinNetwork.REGTEST
        case "Signet":
            return BitcoinNetwork.SIGNET
        case "Testnet":
            return BitcoinNetwork.TESTNET
        case _:
            die(f"Node is running on an unsupported network: {network}")
