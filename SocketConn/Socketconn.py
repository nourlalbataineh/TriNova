import socket
# Configuration
HOST = '127.0.0.1'
PORT = 5005

# Create socket
def create_socket():
    """Create and return a UDP socket"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Attempting to connect to Unity at {HOST}:{PORT}")
    return sock

sock = create_socket()

def send_command(sock,command):
    """Send a command to Unity"""
    sock.sendto(command.encode('utf-8'), (HOST, PORT))


def rotate_up(sock):
    """Tilt camera upward"""
    send_command(sock,f"ROTATE_UP")
    
def rotate_down(sock):
    """Tilt camera downward"""
    send_command(sock,f"ROTATE_DOWN")
    
def rotate_left(sock):
    """Pan camera left"""
    send_command(sock,f"ROTATE_LEFT")
    
def rotate_right(sock):
    """Pan camera right"""
    send_command(sock,f"ROTATE_RIGHT")
    
def zoom(sock,amount):
    """Send zoom command (positive zooms in, negative zooms out)"""
    send_command(sock,f"ZOOM {amount}")
    
def lock_object(sock, object_name):
    """Send lock to object command"""
    send_command(sock,f"LOCK {object_name}")
    
def unlock(sock):
    """Send unlock command"""
    send_command(sock,"UNLOCK")

def next_lock(sock):
    """Send command to lock to the next object"""
    send_command(sock,"NEXT_LOCK")