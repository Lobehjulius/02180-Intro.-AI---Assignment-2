import sys

from Mastermind_demo import main as run_mastermind_demo
from demo import main as run_demo


def print_usage() -> None:
    print("Usage:")
    print("  python src/main.py demo")
    print("  python src/main.py mastermind")


def main() -> None:
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "demo"

    if mode == "demo":
        run_demo()
        return

    if mode == "mastermind":
        run_mastermind_demo()
        return

    print(f"Unknown mode: {mode}")
    print_usage()


if __name__ == "__main__":
    main()
