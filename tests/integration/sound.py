import time

from pyos_utils import sound


def run_tests() -> None:
    print("Running tests for sound module...")

    time.sleep(1.0)
    print("Muting sound...")
    time.sleep(1.0)
    sound.mute()
    print("Playing beep while muted...")
    time.sleep(1.0)
    sound.play_beep()
    time.sleep(1.0)
    print("Unmuting sound...")
    time.sleep(1.0)
    sound.unmute()
    time.sleep(1.0)
    print("Playing beep...")
    time.sleep(1.0)
    sound.play_beep()
    time.sleep(1.0)

    print("Setting volume to 50% [0.5]...")
    time.sleep(1.0)
    sound.set_volume(0.5)
    time.sleep(1.0)
    print("Playing beep...")
    time.sleep(1.0)
    sound.play_beep()

    print("Setting volume to 20% [0.2]...")
    time.sleep(1.0)
    sound.set_volume(0.2)
    time.sleep(1.0)
    print("Playing beep...")
    time.sleep(1.0)
    sound.play_beep()

    print("Getting volume...")
    time.sleep(1.0)
    volume = sound.get_volume()
    print(f"Volume: {volume}")

    print("Tests for sound module completed.")


if __name__ == "__main__":
    run_tests()
