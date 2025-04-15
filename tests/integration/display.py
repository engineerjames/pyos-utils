import time

from pyos_utils import display

if __name__ == "__main__":
    display_interface = display.DisplayInterfaceFactory.create_interface()
    display_info = display_interface.get_info()
    print(f"Found {len(display_info)} display(s).")
    print(display_info[0])
    time.sleep(1)
