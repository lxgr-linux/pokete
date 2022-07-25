import time
import multiprocessing
import playsound

th = multiprocessing.Process(
    target=playsound.playsound,
    args=("./assets/music/01 A Night Of Dizzy Spells.mp3",)
)

th.start()

time.sleep(5)

th.terminate()
