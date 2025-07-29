from subprocess import run
from sys import argv, exit


def run_checks(target: str) -> None:
    """
    Executa isort, black e mypy em ordem no alvo especificado.

    Parameters
    ----------
    target : str
        O arquivo ou diretório alvo.
    """
    commands = [
        ['isort', target],
        ['black', target, '-S'],
        ['mypy', '--namespace-packages', '--explicit-package-bases', target],
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
