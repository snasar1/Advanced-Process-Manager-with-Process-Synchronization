import logging
from process_manager import ProcessManager

def main():
    # Configure logging to write detailed logs to the 'project_log.log' file
    logging.basicConfig(filename='project_log.log', level=logging.DEBUG)
    
    # Create a ProcessManager instance
    manager = ProcessManager()

    while True:
        print("Options:")
        print("1. Create Process")
        print("2. List Processes")
        print("3. Terminate Process")
        print("4. Create Thread")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            command = input("Enter the command for the new process: ")
            # Create a new process and log the command used
            manager.create_process(command)
            logging.info(f"Created process: {command}")

        elif choice == "2":
            # List all active processes and log the event
            processes = manager.list_processes()
            for process in processes:
                print(process)
            logging.debug("Listed processes")

        elif choice == "3":
            pid = input("Enter the PID of the process to terminate: ")
            try:
                pid = int(pid)
                # Terminate a process by its PID and log the termination
                manager.terminate_process(pid)
                logging.warning(f"Terminated process with PID {pid}")
            except ValueError:
                print("Invalid PID. Please enter a valid integer.")
                logging.error("Invalid PID entered")

        elif choice == "4":
            function = input("Enter the function for the new thread: ")
            # Create a new thread with the specified function and log the event
            manager.create_thread(function)
            logging.info(f"Created thread with function: {function}")

        elif choice == "5":
            break

if __name__ == '__main__':
    # Run the main function if the script is executed directly
    main()
