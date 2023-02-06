import click
import os
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from subprocess import call

class CLONE_TYPES(Enum):
    HTTP = "http"
    HTTPS = "https"
    SSH = "ssh"

CLONE_TYPE_CHOICES = [TYPE.value for TYPE in CLONE_TYPES]

DEFAULT_CODE_DIR = os.path.join(Path.home(), "Code")

CODE_DIR = os.getenv('CODE_DIR', DEFAULT_CODE_DIR)

@dataclass
class Repo:
    repo_address: str
    repo_clone_type: CLONE_TYPES
    repo_vendor: str
    repo_owner: str
    repo_name: str

def _parse_repo_address(repo_address: str) -> Repo:
    if repo_address.startswith('https') or repo_address.startswith('http'):
        protocol, uri = tuple(repo_address.split('://'))
        repo_attributes = tuple(uri.split('/'))
        repo_clone_type = CLONE_TYPES[protocol.upper()]
        return Repo(repo_address, repo_clone_type, *repo_attributes)
    elif repo_address.startswith('git@'):
        repo_clone_type = CLONE_TYPES.SSH
        _, uri = tuple(repo_address.split('@'))
        repo_vendor, repo_address = tuple(uri.split(':'))
        repo_attributes = tuple(repo_address.split('/'))
        return Repo(repo_address, repo_clone_type, repo_vendor, *repo_attributes)
    else:
        raise ValueError(f"Unsupported repo address: {repo_address}")

def _invoke_clone_git(repo: Repo, default_clone_type=None):
    target_dir = os.path.join(CODE_DIR, repo.repo_vendor, repo.repo_owner, repo.repo_name)
    cmdline = ['git', 'clone', repo.repo_address, target_dir]
    if default_clone_type:
        if default_clone_type == CLONE_TYPES.HTTP or default_clone_type == CLONE_TYPES.HTTPS:
            repo_address = f"{default_clone_type}://{repo.repo_vendor}/{repo.repo_owner}/{repo.repo_name}.git"
            cmdline = ['git', 'clone', repo_address, target_dir]
        if default_clone_type == CLONE_TYPES.SSH:
            repo_address = f"git@{repo.repo_vendor}:{repo.repo_owner}/{repo.repo_name}.git"
            cmdline = ['git', 'clone', repo_address, target_dir]
    call(cmdline)

@click.command()
@click.argument('repo_addresses', nargs=-1)
@click.option('-t', '--type', help="Type of clone connections.", type=click.Choice(CLONE_TYPE_CHOICES))
def main(repo_addresses, type):
    """CLI for automatically clone git repo in the custom dir structures."""
    default_clone_type = type
    if len(repo_addresses) == 0:
        raise ValueError("Please provice repo address.")

    for repo_address in repo_addresses:
        repo = _parse_repo_address(repo_address)
        _invoke_clone_git(repo, default_clone_type)


if __name__ == "__main__":
    main()
