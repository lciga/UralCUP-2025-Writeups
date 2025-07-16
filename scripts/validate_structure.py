from validators.structure import StructureValidator
import sys
from colorama import Fore


def main():
    validator = StructureValidator()
    if validator.validate_all_tasks():
        print(Fore.GREEN + "All tasks are valid!" + Fore.RESET)
    else:
        print(Fore.RED + "Structure validation failed:" + Fore.RESET)
        for error in validator.get_errors():
            print(Fore.RED + f'- {error}' + Fore.RESET)
        sys.exit(1)


if __name__ == '__main__':
    main()
