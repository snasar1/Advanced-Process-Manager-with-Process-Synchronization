import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
import multiprocessing
import logging

# Configure logging
logging.basicConfig(filename='process_manager.log', level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

# Store information about running processes
active_processes = []

# Mutex for process synchronization
process_lock = threading.Lock()

# Function to simulate a producer-consumer scenario
def producer_consumer(pid, data_queue):
    for i in range(5):
        data = f"Data {i} produced by {pid}"
        logging.info(f"Process {pid} produced {data}")
        data_queue.put(data)

# Function to create a new process
def create_process(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_pid = process.pid
        process_data_queue = multiprocessing.Queue()

        with process_lock:
            active_processes.append({
                "pid": process_pid,
                "command": command,
                "threads": [],
                "data_queue": process_data_queue
            })

        logging.info(f"Process created with PID {process_pid}")

        # Create a thread to simulate producer-consumer for the new process
        producer_thread = threading.Thread(target=producer_consumer, args=(process_pid, process_data_queue))
        producer_thread.start()

    except Exception as e:
        error_msg = f"Error creating process: {str(e)}"
        logging.error(error_msg)
        messagebox.showerror("Error", error_msg)

# Function to terminate a process
def terminate_process(pid):
    try:
        with process_lock:
            for process in active_processes:
                if process["pid"] == pid:
                    for thread in process["threads"]:
                        thread.join()
                    process["data_queue"].close()
                    process["data_queue"].join_thread()
                    process["data_queue"].cancel_join_thread()
                    active_processes.remove(process)  # Remove the process from the list
                    terminated_msg = f"Terminated process with PID {pid}"
                    logging.info(terminated_msg)
                    messagebox.showinfo("Process Terminated", terminated_msg)
                    return
            error_msg = f"Process with PID {pid} not found"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    except Exception as e:
        error_msg = f"Error terminating process: {str(e)}"
        logging.error(error_msg)
        messagebox.showerror("Error", error_msg)

# Function to create a new process via GUI
def create_thread_gui():
    command = command_entry.get()
    if command:
        try:
            create_process(command)
            messagebox.showinfo("Process Created", f"Created process with command: {command}")
        except Exception as e:
            error_msg = f"Error creating process: {str(e)}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    else:
        messagebox.showerror("Error", "Please enter a valid command.")

# Function to list information about running processes
def list_processes():
    process_info = ""
    with process_lock:
        for process in active_processes:
            process_info += f"PID: {process['pid']}, Command: {process['command']}\n"
            process_info += f"Threads: {', '.join([str(thread.ident) for thread in process['threads']])}\n"
            process_info += f"Queue Size: {process['data_queue'].qsize()}\n"
    return process_info

# Function to list running processes via GUI
def list_processes_gui():
    process_info = list_processes()
    if process_info:
        messagebox.showinfo("Running Processes", process_info)
    else:
        messagebox.showinfo("Running Processes", "No processes are running.")

# Function to terminate a process via GUI
def terminate_process_gui():
    pid_str = pid_entry.get()
    if pid_str:
        try:
            pid = int(pid_str)
            terminate_process(pid)
        except ValueError:
            messagebox.showerror("Error", "Invalid PID. Please enter a valid numeric PID.")
    else:
        messagebox.showerror("Error", "Please enter a PID to terminate.")

# Create a tkinter GUI application
app = tk.Tk()
app.title("Process Manager GUI")

# Create Process
tk.Label(app, text="Enter a command:").pack()
command_entry = tk.Entry(app)
command_entry.pack()
create_process_button = tk.Button(app, text="Create Process", command=create_thread_gui)
create_process_button.pack()

# List Processes
list_processes_button = tk.Button(app, text="List Processes", command=list_processes_gui)
list_processes_button.pack()

# Terminate Process
tk.Label(app, text="Enter PID to terminate:").pack()
pid_entry = tk.Entry(app)
pid_entry.pack()
terminate_process_button = tk.Button(app, text="Terminate Process", command=terminate_process_gui)
terminate_process_button.pack()

# Start the tkinter main loop
app.mainloop()
