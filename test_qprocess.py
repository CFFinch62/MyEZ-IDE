#!/usr/bin/env python3
"""
Test QProcess argument handling for debugserver command
"""
import sys
import os
import shutil
from PyQt6.QtCore import QProcess, QCoreApplication

def test_debugserver():
    app = QCoreApplication(sys.argv)
    
    # Find ez interpreter
    ez_path = shutil.which('ez')
    if not ez_path:
        # Try relative path from IDE directory to EZ directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ez_path = os.path.join(script_dir, '..', 'EZ', 'ez')
        ez_path = os.path.abspath(ez_path)
    
    print(f"EZ path: {ez_path}")
    print(f"EZ exists: {os.path.exists(ez_path)}")
    print(f"EZ executable: {os.access(ez_path, os.X_OK)}")
    
    # Test file
    test_file = os.path.abspath('examples/hello.ez')
    print(f"Test file: {test_file}")
    print(f"Test file exists: {os.path.exists(test_file)}")
    
    # Create process
    process = QProcess()
    process.setWorkingDirectory(os.path.dirname(test_file))
    
    # Connect to output
    def on_output():
        data = process.readAllStandardOutput().data().decode('utf-8')
        print(f"STDOUT: {data}")
    
    def on_error():
        data = process.readAllStandardError().data().decode('utf-8')
        print(f"STDERR: {data}")
    
    def on_finished(exit_code, exit_status):
        print(f"Process finished: exit_code={exit_code}, status={exit_status}")
        app.quit()
    
    process.readyReadStandardOutput.connect(on_output)
    process.readyReadStandardError.connect(on_error)
    process.finished.connect(on_finished)
    
    # Start process
    print(f"\nStarting: {ez_path} debugserver {test_file}")
    print(f"Arguments: {['debugserver', test_file]}")
    process.start(ez_path, ['debugserver', test_file])
    
    if not process.waitForStarted(3000):
        print("ERROR: Failed to start process")
        print(f"Error: {process.errorString()}")
        return 1
    
    print("Process started successfully")
    return app.exec()

if __name__ == '__main__':
    sys.exit(test_debugserver())
