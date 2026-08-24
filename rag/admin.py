"""Explicit administrative vector-store operations; never imported by serving code."""

import argparse

from rag.vector_store_factory import get_vector_store_admin


def main() -> None:
    parser = argparse.ArgumentParser(description="Administer the configured vector collection.")
    parser.add_argument("operation", choices=("reset",))
    args = parser.parse_args()
    if args.operation == "reset":
        get_vector_store_admin().reset()
        print("Configured vector collection reset.")


if __name__ == "__main__":
    main()
