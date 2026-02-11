# Distributed Stochastic Gradient Descent (D-SGD) via Ring All-Reduce

## 🚀 Project Overview
This repository contains a high-performance, decentralized implementation of Distributed Stochastic Gradient Descent (D-SGD). [cite_start]Traditional distributed systems often rely on a centralized "Parameter Server" which becomes a massive bottleneck as the model density increases[cite: 24, 28]. [cite_start]This project utilizes a **Ring All-Reduce** topology to distribute the communication load equally across all nodes, ensuring near-linear scalability[cite: 43, 44].

## 📂 Repository Structure & Components
The implementation is modularized into four core Python scripts to ensure a clean separation between computation and communication:

- **`src/main.py` (The Master Coordinator)**: Acts as the system orchestrator. [cite_start]It performs "Data Sharding," which involves partitioning the global dataset into local shards $\mathcal{D}_i$ so each node works on a unique subset[cite: 50].
- **`src/worker.py` (The Local Optimizer)**: The mathematical engine of the node. [cite_start]It manages the training loop and executes forward/backward passes to compute gradients locally[cite: 65].
- **`src/communicator.py` (The Network Layer)**: Handles peer-to-peer TCP/IP socket logic. [cite_start]It uses **FP16 Quantization** to halve the data size, directly improving the "Response Time" of each iteration[cite: 84, 85].
- **`src/monitoring.py` (The Health Monitor)**: Tracks real-time CPU and RAM usage. [cite_start]It specifically watches for `kswapd` (kernel swap daemon) activity, which occurs when RAM usage exceeds physical limits and triggers disk swapping[cite: 69, 70].

---

## [P0] Problem Formulation
[cite_start]We aim to solve the global optimization problem where the goal is to find the best model weights ($w$) that minimize the average loss across all distributed data shards[cite: 46]:

$$\min_{w \in \mathbb{R}^d} F(w) = \frac{1}{N} \sum_{i=1}^{N} \mathbb{E}_{x \sim \mathcal{D}_i} [f(w; x)]$$

### Performance Objectives
- [cite_start]**Speedup ($S$):** We aim for **Linear Speedup** ($S \approx N$), representing the factor by which training time is reduced compared to a single node[cite: 54, 58].
- [cite_start]**Response Time ($T_{resp}$):** The total wall-clock time for a complete iteration is minimized[cite: 62]:
$$T_{resp} = T_{compute} + T_{comm} + T_{sync}$$
  - [cite_start]**$T_{compute}$**: Time taken for forward and backward passes on a local shard[cite: 65].
  - [cite_start]**$T_{comm}$**: Time used by the communication primitive to exchange gradient buffers[cite: 66].
  - [cite_start]**$T_{sync}$**: Synchronization delay or "idle time" spent at the global barrier[cite: 67].

---

## [P1] Implementation Design & Topology
[cite_start]Our design utilizes a decentralized architecture to bypass the limitations of central servers[cite: 9, 72].

- **Topology:** **Peer-to-Peer Ring All-Reduce**. [cite_start]In this setup, each node communicates only with its immediate neighbors in a logical ring[cite: 43, 82].
- [cite_start]**Latency Hiding:** Double buffering allows the communication thread to work in parallel with the computation thread[cite: 75].
- [cite_start]**Quantization:** Reducing precision from 32-bit to 16-bit (FP16) halves the communication payload ($C$)[cite: 84, 85].



---

## [P2] Solving the "Distributed Deadlock"
A critical challenge in synchronous rings is the **Circular Deadlock**. If one node finishes its epoch and exits while its neighbor is still attempting to send data, the entire system hangs indefinitely.

### Our Technical Solutions:
- **Socket Timeouts**: We implemented a 10-second timeout on all network `recv` calls to prevent zombie processes.
- **Graceful Shutdown**: If a node detects a timeout, it assumes the neighbor has finished and safely shuts down its own process instead of freezing.
- [cite_start]**Health-Based Scheduling**: Real-time hardware telemetry identifies "Stragglers" (slow nodes) to ensure the global training FPS is maintained[cite: 89, 90].

---

## [P3] Performance Benchmark
[cite_start]Our empirical tests on a 4-node simulated cluster demonstrated the transition from a high-cost initialization to an efficient steady state[cite: 58]:

| Phase | Avg $T_{comm}$ | System Status | Efficiency |
| :--- | :--- | :--- | :--- |
| **Handshake** | ~10.28s | Initializing TCP connections | Low (Startup Cost) |
| **Steady State** | **~0.013s - 0.20s** | Active Gradient Sync | **High (Optimal)** |

[cite_start]**Observation**: Once the TCP ring is warm, the communication cost drops by over 500x, ensuring the system remains "Computation-Bound" rather than waiting for the network[cite: 61].

### **Execution Output**
![Execution Output](docs/output_screenshot.png)

---

## 👥 Assignment Team & Contribution
- **Abhishake Raina (2024ac05025)**: **Lead Architect**. Designed the Ring All-Reduce logic, Socket API, Deadlock Mitigation, and Telemetry systems.
- **Amisha Tripathi (2024ac05303)**: Literature Survey & Mathematical Formulation.
- **Nitin Kant (2024AC05776)**: Speedup Analysis & Performance Benchmarking.
- **Aditya Shukla (2024ac05481)**: Fault Tolerance & Logic Verification.
- **Mansi Kathuria (2024AC05432)**: Hardware Telemetry & Resource Analysis.