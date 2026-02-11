import psutil
import time

class SystemMonitor:
    def report(self, node_id, t_compute, t_comm):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        
        # Straggler detection logic
        is_straggler = ram_usage > 90
            
        print(f"[Node {node_id}] | T_comp: {t_compute:.4f}s | T_comm: {t_comm:.4f}s "
              f"| CPU: {cpu_usage}% | RAM: {ram_usage}% | Straggler: {is_straggler}")