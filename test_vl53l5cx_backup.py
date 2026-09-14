import vl53l5cx_ctypes
import time
print("Initializing VL53LCX.....")
tof=vl53l5cx_ctypes.VL53L5CX()
print("Starting")
try:
	tof.start_ranging()
	while True:
		if tof.data_ready():
			data=tof.get_data()
			print(data.distance_mm)
		time.sleep(0.01)
except KeyboardInterrupt:
	print("Stopping")
	tof.stop_ranging
