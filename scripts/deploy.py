from pathlib import Path

from brownie import AffiliateToken, Contract, accounts, config, network, project, web3
from eth_utils import is_checksum_address

import click

# User Input 
affiliateTokenName = "abcdef"
affiliateTokenSymbol = "ABC"

API_VERSION = config["dependencies"][0].split("@")[-1]
Vault = project.load(
    Path.home() / ".brownie" / "packages" / config["dependencies"][0]
).Vault

def get_address(msg: str, default: str = None) -> str:
  
    val = click.prompt(msg, default=default)

    # Keep asking user for click.prompt until it passes
    while True:

        if is_checksum_address(val):
            return val
        elif addr := web3.ens.address(val):
            click.echo(f"Found ENS '{val}' [{addr}]")
            return addr

        click.echo(
            f"I'm sorry, but '{val}' is not a checksummed address or valid ENS record"
        )
        # NOTE: Only display default once
        val = click.prompt(msg)

def main():
    print(f"You are using the '{network.show_active()}' network")
    dev = accounts.load(click.prompt("Account", type=click.Choice(accounts.load())))
    print(f"You are using: 'dev' [{dev.address}]")
    token = Contract.from_explorer(get_address("Underlying token"))
    registry = get_address("Registry address,", "v2.registry.ychad.eth")
    
    print(
        f"""
    Affiliate Token Parameters
      api: {API_VERSION}
      affiliate token name: {affiliateTokenName}
      affiliate token symbol: {affiliateTokenSymbol}
      vault: {token.name()}
      symbol: '{token.symbol()}'
    """
    )
    
    publish_source = click.confirm("Verify source on etherscan?")
    
    affiliatetoken = AffiliateToken.deploy(token, registry, affiliateTokenName, affiliateTokenSymbol, {"from": dev}, publish_source=publish_source)
    
    print(f"Deployed {affiliatetoken}")
