import unittest
import unittest.mock
import io
from process_manager import ProcessManager

# Define a test class for the ProcessManager
class TestProcessManager(unittest.TestCase):
    # Setup method: Initialize the ProcessManager instance before each test
    def setUp(self):
        self.manager = ProcessManager()

    # Define a custom assertion method for checking error messages in stderr
    @unittest.mock.patch('sys.stderr', new_callable=io.StringIO)
    def assert_stderr(self, process_pid, expected_error, mock_stderr):
        # Terminate a process and capture the error message from stderr
        self.manager.terminate_process(process_pid)
        error_msg = mock_stderr.getvalue().strip()
        # Check if the expected error message is present in the captured error message

        self.assertTrue(expected_error in error_msg)

    # Test case for creating a new process
    def test_create_process(self):
        # Create a new process with a test command
        self.manager.create_process("echo 'Test process'")
        # Get the list of active processes
        processes = self.manager.list_processes()
        # Check if the string "Process PID" is present in the first process description
        self.assertTrue("Process PID" in processes[0])

    # Test case for creating new threads
    def test_create_thread(self):
        # Define a dummy thread function
        def thread_function():
            pass

        # Create two new threads with the dummy function
        self.manager.create_thread(thread_function)
        self.manager.create_thread(thread_function)
        # Synchronize (join) all active threads

        self.manager.synchronize_threads()

    # Test case for terminating a process
    def test_terminate_process(self):
        # Create a new process with a test command
        self.manager.create_process("echo 'Test process'")
        # Get the list of active processes
        processes = self.manager.list_processes()
        # Extract the PID of the first process
        process_pid = str(processes[0].split()[-1])
        # Terminate the process by its PID
        self.manager.terminate_process(process_pid)
        # Check if the process with the specified PID is no longer in the list
        self.assertNotIn(process_pid, self.manager.list_processes())

# Run the unittest framework if this script is the main program
if __name__ == '__main__':
    unittest.main()
