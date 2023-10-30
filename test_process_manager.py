import logging
import tkinter as tk
from tkinter import messagebox
import os

# Import the ProcessManager class from process_manager.py
from process_manager import ProcessManager

class ProcessManagerGUI:
    def __init__(self, root):
        # Initialize the GUI
        self.root = root
        self.root.title("Process Manager GUI")
        self.manager = ProcessManager()

        # Create Process
        tk.Label(root, text="Enter a command:").pack()
        self.command_entry = tk.Entry(root)
        self.command_entry.pack()
        create_process_button = tk.Button(root, text="Create Process", command=self.create_process)
        create_process_button.pack()

        # List Processes
        list_processes_button = tk.Button(root, text="List Processes", command=self.list_processes)
        list_processes_button.pack()

        # Terminate Process
        tk.Label(root, text="Enter PID to terminate:").pack()
        self.pid_entry = tk.Entry(root)
        self.pid_entry.pack()
        terminate_process_button = tk.Button(root, text="Terminate Process", command=self.terminate_process)
        terminate_process_button.pack()

    def create_process(self):
        # Handle the "Create Process" button click
        command = self.command_entry.get()
        if command:
            try:
                # Attempt to create a new process
                self.manager.create_process(command)
                messagebox.showinfo("Process Created", f"Created process with command: {command}")
            except Exception as e:
                # Log and display an error message if process creation fails
                error_msg = f"Error creating process: {str(e)}"
                logging.error(error_msg)
                messagebox.showerror("Error", error_msg)
        else:
            messagebox.showerror("Error", "Please enter a valid command.")

    def list_processes(self):
        # Handle the "List Processes" button click
        process_info = self.manager.list_processes()
        if process_info:
            # Display the list of running processes
            messagebox.showinfo("Running Processes", "\n".join(process_info))
        else:
            messagebox.showinfo("Running Processes", "No processes are running.")

    def terminate_process(self):
        # Handle the "Terminate Process" button click
        pid_str = self.pid_entry.get()
        if pid_str:
            try:
                # Attempt to terminate a process by PID
                pid = int(pid_str)
                self.manager.terminate_process(pid)
            except ValueError:
                # Display an error message for an invalid PID
                messagebox.showerror("Error", "Invalid PID. Please enter a valid numeric PID.")
        else:
            messagebox.showerror("Error", "Please enter a PID to terminate.")

if __name__ == '__main__':
    # Configure logging to write to a log file
    logging.basicConfig(filename='process_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    root = tk.Tk()
    app = ProcessManagerGUI(root)
    root.mainloop()
