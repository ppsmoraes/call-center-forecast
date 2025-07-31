"""Module that executes code standardization and functionality tests."""

from subprocess import run
from sys import argv, exit


def run_checks(target: str) -> None:
    """
    Execute isort, black, pydocstyle, mypy and pytest, in this order, on the specified target.

    Parameters
    ----------
    target : str
        The target file or directory.
    """
    commands = [
        ['isort', '--only-modified', target],
        ['black', '--skip-string-normalization', target],
        ['pydocstyle', target],
        ['mypy', '--namespace-packages', '--explicit-package-bases', target],
        ['pytest', '--verbose'],
    ]

    for command in commands:
        result = run(command)
        if result.returncode != 0:
            print(
                f'Command {' '.join(command)} failed with exit code {result.returncode}'
            )
            exit(result.returncode)


if __name__ == '__main__':
    target = argv[1] if len(argv) > 1 else '.'
    run_checks(target)
