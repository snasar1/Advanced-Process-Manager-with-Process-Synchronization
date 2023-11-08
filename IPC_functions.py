#Inter-Process Communication (IPC)

import logging
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import multiprocessing

# Configure logging
logging.basicConfig(filename='process_manager.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ProcessManager:
    def __init__(self):
        self.processes = []

    def create_process(self, command):
        try:
            # Create a new process using the provided command
            process = subprocess.Popen(command, shell=True)
            self.processes.append(process)
            logging.info(f"Created process with PID {process.pid}")
        except Exception as e:
            # Log an error and show an error message if process creation fails
            error_msg = f"Error creating process: {str(e)}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)

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

                    # Display a message box for process termination
                    messagebox.showinfo("Process Terminated", f"Process with PID {pid} terminated.")

                    return
            logging.error(f"Process with PID {pid} not found")
        except Exception as e:
            # Log an error and show an error message if process termination fails
            error_msg = f"Error terminating process: {str(e)}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)


def create_thread_gui():
    try:
        command = command_entry.get()
        if command:
            if validate_command(command):
                manager.create_process(command)
                messagebox.showinfo("Process Created", f"Created process with command: {command}")
            else:
                messagebox.showerror("Error", "Invalid command. Please enter a valid command.")
        else:
            messagebox.showerror("Error", "Please enter a valid command.")
    except Exception as e:
        # Log an error and show an error message for GUI errors
        error_msg = f"Error creating process: {str(e)}"
        logging.error(error_msg)
        messagebox.showerror("Error", error_msg)


def validate_command(command):
    # Custom command validation logic
    # For example, check if it's a non-empty string
    return bool(command.strip())


def list_processes_gui():
    try:
        processes = manager.list_processes()
        if processes:
            processes_info = '\n'.join(processes)
            messagebox.showinfo("Running Processes", processes_info)
        else:
            messagebox.showinfo("Running Processes", "No processes are running.")
    except Exception as e:
        # Log an error and show an error message for GUI errors
        error_msg = f"Error listing processes: {str(e)}"
        logging.error(error_msg)
        messagebox.showerror("Error", error_msg)


def terminate_process_gui():
    try:
        pid = pid_entry.get()
        if pid:
            manager.terminate_process(pid)
        else:
            messagebox.showerror("Error", "Please enter a PID to terminate.")
    except Exception as e:
        # Log an error and show an error message for GUI errors
        error_msg = f"Error terminating process: {str(e)}"
        logging.error(error_msg)
        messagebox.showerror("Error", error_msg)


def simulate_producer_consumer(pid, data_queue):
    try:
        for i in range(5):
            data = f"Data {i} produced by {pid}"
            logging.info(f"Process {pid} produced {data}")
            data_queue.put(data)
    except Exception as e:
        # Log an error for IPC errors
        logging.error(f"IPC error: {str(e)}")


def start_producer_consumer(pid, data_queue):
    try:
        # Create a new process for producer-consumer simulation
        process = multiprocessing.Process(target=simulate_producer_consumer, args=(pid, data_queue))
        process.start()
        return process
    except Exception as e:
        # Log an error for process creation errors
        logging.error(f"Error creating producer-consumer process: {str(e)}")


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(filename='process_manager.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Create a ProcessManager instance
    manager = ProcessManager()

    # Create a tkinter GUI
    app = tk.Tk()
    app.title("Process Manager GUI")

    # Label and entry for entering a command
    tk.Label(app, text="Enter a command:").pack()
    command_entry = tk.Entry(app)
    command_entry.pack()

    # Button to create a process
    create_process_button = tk.Button(app, text="Create Process", command=create_thread_gui)
    create_process_button.pack()

    # Button to list running processes
    list_processes_button = tk.Button(app, text="List Processes", command=list_processes_gui)
    list_processes_button.pack()

    # Label and entry for entering a PID to terminate
    tk.Label(app, text="Enter PID to terminate:").pack()
    pid_entry = tk.Entry(app)
    pid_entry.pack()

    # Button to terminate a process
    terminate_process_button = tk.Button(app, text="Terminate Process", command=terminate_process_gui)
    terminate_process_button.pack()

    # Start the GUI application
    app.mainloop()
