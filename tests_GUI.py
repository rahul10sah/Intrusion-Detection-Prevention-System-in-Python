import unittest
import tkinter as tk
from idps_GUI import IDPSGUI
import os

class TestIDPSGUI(unittest.TestCase):
    def setUp(self):
        """Initialize the GUI without requiring user input."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window during tests
        
        # Mock authentication to bypass password input
        IDPSGUI.authenticate = lambda self: True
        self.gui = IDPSGUI(self.root)
    
    def test_start_idps(self):
        """Test if IDPS starts correctly."""
        self.gui.start_idps()
        self.assertTrue(self.gui.monitoring, "IDPS did not start correctly.")
        
    def test_clear_logs(self):
        """Test if logs are cleared successfully."""
        log_files = ["./logs/file_log.txt", "./logs/network_connections_log.txt", "./logs/processes_log.txt"]
        
        # Create dummy logs
        for file in log_files:
            with open(file, "w") as f:
                f.write("Dummy log data")
        
        self.gui.clear_logs()
        
        # Check if logs are empty
        for file in log_files:
            with open(file, "r") as f:
                content = f.read()
            self.assertEqual(content, "", f"Log file {file} was not cleared.")
    
    def tearDown(self):
        """Close the GUI after tests."""
        self.root.destroy()

if __name__ == "__main__":
    unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(TestIDPSGUI))
