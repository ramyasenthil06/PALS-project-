import subprocess
import time
song = "/home/rit123/vl53l5cx/low-frequency.aac"
player = subprocess.Popen(["cvlc", "--loop", song])
time.sleep(20)
player.terminate()
