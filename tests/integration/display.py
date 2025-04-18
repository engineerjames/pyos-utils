from pyos_utils import display
from pyos_utils.display._info import DisplayInfo
from pyos_utils.display._interface import DisplayInterface

if __name__ == "__main__":
    display_interface: DisplayInterface = display.DisplayInterfaceFactory.create_interface()
    display_info: list[DisplayInfo] = display_interface.get_info()
    print(f"Found {len(display_info)} display(s).")

    for i, info in enumerate(display_info):
        print(f"Display {i}:")
        print(info)
