import socket
import time

class UnityCameraController:
    def __init__(self, host='127.0.0.1', port=5005):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Attempting to connect to Unity at {host}:{port}")
        
        self.send_command("PING")
        time.sleep(0.5)  # Brief delay for Unity to respond

    def send_command(self, command):
        self.sock.sendto(command.encode('utf-8'), (self.host, self.port))
    
    def lock_object(self, object_name):
        """Send lock to object command"""
        self.send_command(f"LOCK {object_name}")
    
    def unlock(self):
        """Send unlock command"""
        self.send_command("UNLOCK")

# Example usage
if __name__ == "__main__":
    controller = UnityCameraController()
    
    # Rotate camera
    controller.send_command("LOCK Mars")  