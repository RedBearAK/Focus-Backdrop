import argparse

from focus_backdrop.main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Focus Backdrop")
    parser.add_argument("--preferences", action="store_true", help="Open the preferences dialog")
    args = parser.parse_args()
    main(args)
