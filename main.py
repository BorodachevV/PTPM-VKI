import logging
import sys

from calculator import TriangleCalculator
from database import TriangleDatabase
from user_interface import ConsoleUserInterface
from external_service import MockEmailService
from controller import Controller


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | [%(levelname)-7s] | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    controller = Controller(
        calc=TriangleCalculator(),
        db=TriangleDatabase("triangles.db"),
        ui=ConsoleUserInterface(),
        external=MockEmailService(),
    )
    try:
        while True:
            print(controller.process())
    except (EOFError, KeyboardInterrupt):
        print("\nВыход.")


if __name__ == "__main__":
    main()