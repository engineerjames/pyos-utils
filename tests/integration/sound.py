import time

from pyos_utils import sound


def run_tests() -> None:
    print("Running tests for sound module...")

    sound_interface: sound.SoundInterface = sound.SoundInterfaceFactory.create_interface()

    time.sleep(1.0)
    print("Muting sound...")
    time.sleep(1.0)
    sound_interface.mute()
    print("Playing beep while muted...")
    time.sleep(1.0)
    sound_interface.play_beep()
    time.sleep(1.0)
    print("Unmuting sound...")
    time.sleep(1.0)
    sound_interface.unmute()
    time.sleep(1.0)
    print("Playing beep...")
    time.sleep(1.0)
    sound_interface.play_beep()
    time.sleep(1.0)

    print("Setting volume to 50% [0.5]...")
    time.sleep(1.0)
    sound_interface.set_volume(0.5)
    time.sleep(1.0)
    print("Playing beep...")
    time.sleep(1.0)
    sound_interface.play_beep()

    print("Setting volume to 20% [0.2]...")
    time.sleep(1.0)
    sound_interface.set_volume(0.2)
    time.sleep(1.0)
    print("Playing beep...")
    time.sleep(1.0)
    sound_interface.play_beep()

    print("Getting volume...")
    time.sleep(1.0)
    volume = sound_interface.get_volume()
    print(f"Volume: {volume}")

    print("Tests for sound module completed.")


if __name__ == "__main__":
    run_tests()
