# AeroStream: Real-Time Satellite Telemetry Pipeline

AeroStream is a full-stack telemetry simulation and processing engine. It demonstrates a high-performance data pipeline connecting low-level C++ simulation with Python-based data persistence and analysis.

## 🚀 System Architecture
- **Producer (C++):** A high-performance simulation engine utilizing the **Factory Design Pattern** to generate varied satellite telemetry packets (GPS, Power, Thermal).
- **Communication:** Utilizing Linux **Standard Streams and Pipes** for inter-process communication (IPC).
- **Consumer (Python):** A data ingestion script that parses real-time streams and manages database transactions.
- **Storage (SQLite):** A relational database for persistent storage of satellite health history.

## 🛠️ Tech Stack
- **Languages:** C++ (Modern 17/20), Python 3.x
- **Environment:** Linux (WSL2 / Ubuntu)
- **Database:** SQLite3
- **DevOps:** Git, GitHub Actions (CI/CD - *Coming Soon*)

## 🚦 Getting Started
1. **Compile the Producer:**
   ```bash
   g++ main.cpp -o telemetry_sim -pthread
   ```

2. **Run the Pipeline:**
   ```bash
   ./telemetry_sim | python3 processor.py
   ```

3. **Query the Data:**
   ```bash
   sqlite3 satellite_data.db "SELECT * FROM telemetry LIMIT 10;"
   ```
## 🧠 Design Patterns Used
- **Factory Method:** Used in the C++ core to decouple object creation from the main simulation loop, allowing for easy expansion of new sensor types.
- **Smart Pointers:** Utilizing `std::unique_ptr` for safe, automated memory management.