#this code integrates all the modules - data from emotion detection, ecg, gsr, and code quality scores

#create a window, display a problem statement, ask for input file name and test for code quality and display code quality
import tkinter as tk
import random
import subprocess
from subprocess import PIPE
import re
import numpy 
import rr_extractor

productivity_metric = 0

def get_random_statement():
	with open("problem_statements.txt", "r") as f: # a text file with random problem statements, make sure you have it in the same root as this code
		statements = f.readlines()
		return random.choice(statements)
		
		

# find major count of emotion, find avg of ecg and gsr  = final stress metric
def calc_metrics():
	file_path = entry.get()
	#code quality checker
	if file_path != None:
		argum = ['python -m code_quality -d ']
		argum[0] = argum[0]+file_path
		process = subprocess.Popen(argum[0], shell=True, stdout=PIPE)
		output = process.communicate()
		output = output[0].decode()
		print(output)
		metrics = list(re.findall(r"[-+]?(?:\d*\.*\d+)", output))
		productivity_metric = numpy.mean([float(metrics[0]),float(metrics[2]),float(metrics[4]),float(metrics[6])])		
		productivity_metric = productivity_metric/10
	#get all file paths
	emotion_file = entry2.get()
	ecg_file = entry3.get()
	gsr_file = entry4.get()
	#read emotion file path and get major emotion
	fs_ef = open(emotion_file.strip('"'), "r")
	lines = fs_ef.readlines()
	emotions_dict = {i:lines.count(i) for i in lines}
	print (emotions_dict)
	major_emotion = max(emotions_dict, key=emotions_dict.get)
	print("Most repeated emotion = ",major_emotion)
	fs_ef.close()
	#read ecg file path and find avg of pulse readings
	ecg_dev = rr_extractor.rr_stddev(ecg_file)
	print("R-R deviation = ", ecg_dev)
	#reading gsr file path and finding std dev
	with open(gsr_file.strip('"'), 'r') as f:
		data = [float(line.strip("\n")) for line in f.readlines()]
	gsr_dev = numpy.std(data)
	print("gsr deviation = ", gsr_dev)
	
	emotion_labels = {'Happy':1,'Neutral':2,'Fear':3,'Sad':4}
	emotion_metric = emotion_labels[major_emotion.strip("\n")]
	print("emotion metric = ", emotion_metric)

	stress_metric = emotion_metric-ecg_dev+gsr_dev
	print("ultimate stress metric = ", stress_metric)
	print("ultimate productivity metric = ", productivity_metric)
	
	



def open_window(): # Problem statement window
	# Create a new window
	new_window = tk.Toplevel(window)
	new_window.title("New Window")
	new_window.geometry("500x500")
	st = get_random_statement()
	# Add widgets to the new window
	text_widget = tk.Text(new_window, height=10, width=50)
	text_widget.insert(tk.END, st)
	text_widget.pack()
	#label = tk.Label(new_window, text=st)
	button = tk.Button(new_window, text="Completed The Task!", command=new_window.destroy)
	button.pack()
	#label.pack()



	
# Create Tkinter window
window = tk.Tk()
window.geometry("500x500")
window.title("Stress and Productivity analyser")

# Create label to display statement
#statement_label = tk.Label(window, text=get_random_statement())
#statement_label.pack()

# Create button to generate new random statement
generate_button = tk.Button(window, text="Generate Problem Statement", command=open_window)
generate_button.pack()

label = tk.Label(window, text="Enter solution file path: ")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Submit file path")
button.pack()


label2 = tk.Label(window, text="Enter emotion list file path: ")
label2.pack()
entry2 = tk.Entry(window)
entry2.pack()
button2 = tk.Button(window, text="Submit file path")
button2.pack()

label3 = tk.Label(window, text="Enter ECG list file path: ")
label3.pack()
entry3 = tk.Entry(window)
entry3.pack()
button3 = tk.Button(window, text="Submit file path")
button3.pack()

label4 = tk.Label(window, text="Enter GSR list file path: ")
label4.pack()
entry4 = tk.Entry(window)
entry4.pack()
button4 = tk.Button(window, text="Submit file path", command=calc_metrics)
button4.pack()


window.mainloop()

