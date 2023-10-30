import os
import threading
import logging
import subprocess
import tkinter as tk
from tkinter import messagebox

class ProcessManager:
    def __init__(self):
        self.processes = []
        self.threads = []

    def create_process(self, command):
        try:
            process = subprocess.Popen(command, shell=True)
            self.processes.append(process)
            logging.info(f"Created process with PID {process.pid}")
        except Exception as e:
            logging.error(f"Error creating process: {str(e)}")
            messagebox.showerror("Error", f"Error creating process: {str(e)}")

    def create_thread(self, thread_function):
        try:
            thread = threading.Thread(target=thread_function)
            self.threads.append(thread)
            thread.start()
            logging.info(f"Created thread with ID {thread.ident}")
        except Exception as e:
            logging.error(f"Error creating thread: {str(e)}")
            messagebox.showerror("Error", f"Error creating thread: {str(e)}")

    def list_processes(self):
        return [f"Process PID: {p.pid}" for p in self.processes]

    def terminate_process(self, pid):
        try:
            for process in self.processes:
                if str(process.pid) == pid:
                    process.terminate()
                    self.processes.remove(process)
                    logging.info(f"Terminated process with PID {pid}")
                    return
            logging.error(f"Process with PID {pid} not found")
        except Exception as e:
            logging.error(f"Error terminating process: {str(e)}")
            messagebox.showerror("Error", f"Error terminating process: {str(e)}")

    def synchronize_threads(self):
        for thread in self.threads:
            thread.join()

def create_thread_gui():
    command = command_entry.get()
    if command:
        manager.create_process(command)
        messagebox.showinfo("Process Created", f"Created process with command: {command}")
    else:
        messagebox.showerror("Error", "Please enter a valid command.")

def list_processes_gui():
    processes = manager.list_processes()
    if processes:
        processes_info = '\n'.join(processes)
        messagebox.showinfo("Running Processes", processes_info)
    else:
        messagebox.showinfo("Running Processes", "No processes are running.")

def terminate_process_gui():
    pid = pid_entry.get()
    if pid:
        try:
            manager.terminate_process(pid)
        except Exception as e:
            messagebox.showerror("Error", f"Error terminating process: {str(e)}")
    else:
        messagebox.showerror("Error", "Please enter a PID to terminate.")

if __name__ == '__main__':
    logging.basicConfig(filename='process_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    manager = ProcessManager()

    app = tk.Tk()
    app.title("Process Manager GUI")

    tk.Label(app, text="Enter a command:").pack()
    command_entry = tk.Entry(app)
    command_entry.pack()
    create_process_button = tk.Button(app, text="Create Process", command=create_thread_gui)
    create_process_button.pack()

    list_processes_button = tk.Button(app, text="List Processes", command=list_processes_gui)
    list_processes_button.pack()

    tk.Label(app, text="Enter PID to terminate:").pack()
    pid_entry = tk.Entry(app)
    pid_entry.pack()
    terminate_process_button = tk.Button(app, text="Terminate Process", command=terminate_process_gui)
    terminate_process_button.pack()

    app.mainloop()
import os
import threading
import logging
import subprocess
import tkinter as tk
from tkinter import messagebox

class ProcessManager:
    def __init__(self):
        self.processes = []
        self.threads = []

    def create_process(self, command):
        try:
            # Create a new process using the provided command
            process = subprocess.Popen(command, shell=True)
            self.processes.append(process)
            logging.info(f"Created process with PID {process.pid}")
        except Exception as e:
            # Log an error and show an error message if process creation fails
            logging.error(f"Error creating process: {str(e)}")
            messagebox.showerror("Error", f"Error creating process: {str(e)}")

    def create_thread(self, thread_function):
        try:
            # Create a new thread with the specified function
            thread = threading.Thread(target=thread_function)
            self.threads.append(thread)
            thread.start()
            logging.info(f"Created thread with ID {thread.ident}")
        except Exception as e:
            # Log an error and show an error message if thread creation fails
            logging.error(f"Error creating thread: {str(e)}")
            messagebox.showerror("Error", f"Error creating thread: {str(e)}")

    def list_processes(self):
        return [f"Process PID: {p.pid}" for p in self.processes]

    def terminate_process(self, pid):
        try:
            for process in self.processes:
                if str(process.pid) == pid:
                    # Terminate the process with the specified PID
                    process.terminate()
                    self.processes.remove(process)
                    logging.info(f"Terminated process with PID {pid}")
                    return
            logging.error(f"Process with PID {pid} not found")
        except Exception as e:
            # Log an error and show an error message if process termination fails
            logging.error(f"Error terminating process: {str(e)}")
            messagebox.showerror("Error", f"Error terminating process: {str(e)}")

    def synchronize_threads(self):
        # Synchronize (join) all active threads
        for thread in self.threads:
            thread.join()

def create_thread_gui():
    command = command_entry.get()
    if command:
        manager.create_process(command)
        messagebox.showinfo("Process Created", f"Created process with command: {command}")
    else:
        messagebox.showerror("Error", "Please enter a valid command.")

def list_processes_gui():
    processes = manager.list_processes()
    if processes:
        processes_info = '\n'.join(processes)
        messagebox.showinfo("Running Processes", processes_info)
    else:
        messagebox.showinfo("Running Processes", "No processes are running.")

def terminate_process_gui():
    pid = pid_entry.get()
    if pid:
        try:
            manager.terminate_process(pid)
        except Exception as e:
            messagebox.showerror("Error", f"Error terminating process: {str(e)}")
    else:
        messagebox.showerror("Error", "Please enter a PID to terminate.")

if __name__ == '__main__':
    # Configure logging to write to a log file
    logging.basicConfig(filename='process_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Create an instance of the ProcessManager class
    manager = ProcessManager()

    # Create the GUI application
    app = tk.Tk()
    app.title("Process Manager GUI")

    # Create a label and entry for entering a command
    tk.Label(app, text="Enter a command:").pack()
    command_entry = tk.Entry(app)
    command_entry.pack()

    # Create a button to create a process
    create_process_button = tk.Button(app, text="Create Process", command=create_thread_gui)
    create_process_button.pack()

    # Create a button to list running processes
    list_processes_button = tk.Button(app, text="List Processes", command=list_processes_gui)
    list_processes_button.pack()

    # Create a label and entry for entering a PID to terminate
    tk.Label(app, text="Enter PID to terminate:").pack()
    pid_entry = tk.Entry(app)
    pid_entry.pack()

    # Create a button to terminate a process
    terminate_process_button = tk.Button(app, text="Terminate Process", command=terminate_process_gui)
    terminate_process_button.pack()

    # Start the GUI application
    app.mainloop()
