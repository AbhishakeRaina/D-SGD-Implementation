# Distributed Stochastic Gradient Descent (D-SGD) via Ring All-Reduce

## 🚀 Project Overview
This repository contains a high-performance, decentralized implementation of Distributed Stochastic Gradient Descent (D-SGD). By moving away from centralized Parameter Server architectures, this project utilizes a **Ring All-Reduce** topology to share the communication load equally across all nodes. This ensures that the "Synchronization Tax" remains manageable as the system scales, making it ideal for large-scale Machine Learning optimization.

## 📂 Repository Structure & Components
The implementation is modularized into four core Python scripts:

- **`src/main.py`**: The **Master Coordinator**. It handles global data sharding (partitioning the dataset into local shards $D_i$) and orchestrates the spawning of distributed worker processes.
- **`src/worker.py`**: The **Local Optimizer**. It manages the training loop, executes the forward/backward passes ($T_{compute}$), and coordinates with the communicator for weight updates.
- **`src/communicator.py`**: The **Decentralized Network Layer**. It implements peer-to-peer TCP/IP socket logic for gradient exchange, featuring FP16 quantization to reduce bandwidth footprint.
- **`src/monitoring.py`**: The **Health Monitor**. It tracks real-time CPU and RAM usage to detect `kswapd` activity and identify "straggler" nodes before they impact global training FPS.

## [P0] Problem Formulation
We solve the global optimization problem:
$$\min_{w \in \mathbb{R}^d} F(w) = \frac{1}{N} \sum_{i=1}^{N} \mathbb{E}_{x \sim \mathcal{D}_i} [f(w; x)]$$
The design focuses on achieving **Linear Speedup** ($S \approx N$) and minimizing the **Response Time** ($T_{resp} = T_{compute} + T_{comm} + T_{sync}$).

## [P1] Implementation Design
- **Topology:** Peer-to-Peer Ring All-Reduce.
- **Isolation:** OS-level process isolation using Python `multiprocessing`.
- **Latency Hiding:** Staggered starts and non-blocking socket strategies.
- **Deadlock Mitigation:** 10-second socket timeouts and `NoneType` guards to ensure graceful shutdown during asynchronous process exits.

[Image of the Ring All-Reduce collective communication algorithm steps]

## [P3] Performance Benchmark
Our empirical tests on a 4-node simulated cluster yielded the following results:

| Phase | Avg $T_{comm}$ | System Status | Efficiency |
| :--- | :--- | :--- | :--- |
| **Handshake** | ~10.28s | Socket Initialization | Low (Startup Cost) |
| **Steady State**| **~0.013s - 0.20s** | Active Sync | **High (Optimal)** |

*Observation: Once the TCP ring is warm, the communication cost drops by over 500x, allowing the system to remain computation-bound.*

### **Execution Output**
![Execution Output](docs/output_screenshot.png)

## 👥 Assignment Team & Contribution
- **Abhishake Raina (2024ac05025)**: **Lead Architect**. Designed the Ring All-Reduce logic, Socket API, Deadlock Mitigation, and Telemetry systems.
- **Amisha Tripathi (2024ac05303)**: Literature Survey & Mathematical Formulation.
- **Nitin Kant (2024AC05776)**: Speedup Analysis & Performance Benchmarking.
- **Aditya Shukla (2024ac05481)**: Fault Tolerance & Logic Verification.
- **Mansi Kathuria (2024AC05432)**: Hardware Telemetry & Resource Analysis.