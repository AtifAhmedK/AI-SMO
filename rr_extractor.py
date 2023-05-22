#required for gui_master, extracts standard deviation of RR intervals from ecg text file
import numpy as np
import biosppy.signals.ecg as ecg

def rr_stddev(ecg_file):

	# Read ECG values from text file
	ecg_values = np.loadtxt(ecg_file.strip('"'))
	# Apply biosppy ECG processing
	out = ecg.ecg(signal=ecg_values, sampling_rate=860, show=False)
	
	# Extract R-R intervals
	rr_intervals = np.diff(out['rpeaks'] / 860)

	# Print R-R intervals
	#print(rr_intervals)
	deviation = np.std(rr_intervals)
	return(deviation)
