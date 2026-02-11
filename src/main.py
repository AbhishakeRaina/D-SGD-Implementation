import multiprocessing as mp
import numpy as np
import time
from worker import run_worker

def main():
    num_nodes = 4
    model_dim = 1000
    configs = []
    for i in range(num_nodes):
        configs.append({
            'port': 8000 + i, 
            'n_ip': '127.0.0.1',
            'n_port': 8000 + ((i + 1) % num_nodes),
            'model_dim': model_dim,
            'epochs': 5,
            'lr': 0.01
        })

    print(f"Starting D-SGD with {num_nodes} nodes in Ring Topology...")
    processes = [mp.Process(target=run_worker, args=(i, None, configs[i])) for i in range(num_nodes)]
    for p in processes:
        p.start()
        time.sleep(0.2)
    for p in processes:
        p.join()
    print("Training Complete.")

if __name__ == "__main__":
    main()