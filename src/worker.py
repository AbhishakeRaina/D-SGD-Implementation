import time
import numpy as np
from communicator import RingCommunicator
from monitoring import SystemMonitor

def run_worker(node_id, data_shard, config):
    comm = RingCommunicator(node_id, config['port'], config['n_ip'], config['n_port'])
    monitor = SystemMonitor()
    weights = np.random.randn(config['model_dim'])
    
    for epoch in range(config['epochs']):
        start_comp = time.time()
        grads = np.random.randn(config['model_dim']) * 0.01
        time.sleep(0.1) 
        t_compute = time.time() - start_comp
        
        start_comm = time.time()
        comm.send_gradient(grads)
        global_grads = comm.receive_gradient()
        t_comm = time.time() - start_comm
        
        # P2: Robustness Check to prevent NoneType Error
        if global_grads is not None:
            weights -= config['lr'] * global_grads
        
        monitor.report(node_id, t_compute, t_comm)