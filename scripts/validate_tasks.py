from validators.specification import SpecificationValidator
from colorama import Fore
import sys

def main():
    validator = SpecificationValidator()
    if validator.validate_all_tasks():
        print(Fore.GREEN + "All tasks are valid!" + Fore.RESET)
        sys.exit(0)
    else:
        print(Fore.RED + "Structure validation failed:" + Fore.RESET)
        sys.exit(1)

if __name__ == '__main__':
    main()