import socket
import pickle
import numpy as np
import time  # Fix: Added missing import for retry logic

class RingCommunicator:
    def __init__(self, node_id, port, neighbor_ip, neighbor_port):
        self.node_id = node_id
        self.port = port
        self.neighbor_ip = neighbor_ip
        self.neighbor_port = neighbor_port
        
    def send_gradient(self, gradient):
        compressed_grad = gradient.astype(np.float16)
        data = pickle.dumps(compressed_grad)
        
        connected = False
        attempts = 0
        while not connected and attempts < 50:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect((self.neighbor_ip, self.neighbor_port))
                    s.sendall(data)
                    connected = True
            except (ConnectionRefusedError, socket.timeout):
                attempts += 1
                time.sleep(0.2) # Wait for neighbor to start listening

    def receive_gradient(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(10.0) # [P2] Logic: Prevents terminal from sticking
            s.bind(('', self.port))
            s.listen(1)
            try:
                conn, addr = s.accept()
                with conn:
                    data = b""
                    while True:
                        packet = conn.recv(4096)
                        if not packet: break
                        data += packet
                    return pickle.loads(data).astype(np.float32)
            except socket.timeout:
                return None # Return None if neighbor finished early