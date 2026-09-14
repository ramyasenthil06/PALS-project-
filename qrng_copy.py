import vl53l5cx_ctypes
import numpy as np
import csv
import time
from datetime import datetime
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
print("Initializing VL53LCX.....")
tof=vl53l5cx_ctypes.VL53L5CX()
print("Starting")
tof.set_resolution(8*8)
tof.enable_motion_indicator(8*8)
tof.start_ranging()
highs = 0
lows = 0
c = 0
file_name = "QRNG.csv"
with open(file_name, 'a+', newline="") as file:
	file.seek(0)
	reader = csv.reader(file)
	if not file.readline():
		writer = csv.writer(file)
		writer.writerow(["time"]+[f"reading_{i}" for i in range(64)]+["binary", "rand_num", "highs", "lows", "digits"])
	file.flush()
try:
	t = int(input("Enter No. of Random Numbers required: "))
	k=0
	run = True
	while run:
		if tof.data_ready():
			k += 1
			if(k>=t):
				run = False
			data=tof.get_data()
			distances = np.asarray(data.distance_mm).reshape(-1)
			minimum = np.min(distances)
			maximum = np.max(distances)
			normalized = distances / maximum
			qc = QuantumCircuit(64,64)
			for i in range(64):
				theta = normalized[i] * np.pi
				qc.h(i)
				qc.rz(theta, i)
			for i in range(63):
				qc.cz(i,i+1)
			qc.measure(range(64),range(64))
			aer = AerSimulator(method = 'matrix_product_state')
			job = aer.run(qc,shots = 1)
			result = job.result()
			counts = result.get_counts()
			binary = list(counts.keys())[0]
			ran_num = int(binary,2)
			low = str(binary).count('0')
			high = str(binary).count('1')
			digits = len(str(abs(ran_num)))
			print("Binary = ",binary,"\nNumber = ",ran_num,"\nCount = ",k)
			with open(file_name,'a',newline = '') as file:
				writer = csv.writer(file)
				writer.writerow([datetime.now().isoformat()]+distances.tolist()+[binary, ran_num, high, low, digits])
				file.flush()
except KeyboardInterrupt:
	print("Stopping")
tof.stop_ranging
