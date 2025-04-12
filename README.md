Neural Encryption & Network Infiltration - Tkinter GUI Simulations: 

This repository contains two Python graphical user interface (GUI) applications built using Tkinter library. These applications simulate futuristic/cyberpunk-themed interfaces: one for accessing a secure system via a neural implant and another for simulating a network infiltration process.

**Note:** These are purely **simulations** for visual demonstration and educational purposes. They do not perform any real encryption, network scanning, or hacking activities.

They were created for a graphical comic story: FUGITIVE DAWN
Hong Kong Slum Patrol which you can read for free and test out here: https://new.express.adobe.com/webpage/YaTMGDsZ6EWiS

## Applications

1.  [Neural Encryption Interface (`neural_encryption_dark.py`)](#neural-encryption-interface)
2.  [MIMIC - Network Infiltration System (`mimic.py`)](#mimic---network-infiltration-system)



## 1. Neural Encryption Interface (`neural_encryption_dark.py`)

Simulates accessing a high-security system ("Axiom Secure") through a neural interface. The process involves establishing a connection, visualizing a generated encryption key, and simulating the transfer and display of sensitive data.


![Neural Encrypter](https://github.com/user-attachments/assets/248700c3-206d-48db-87a6-319c75a4e935)



### Features

*   **Dark Theme Interface:** Uses `customtkinter` for a modern, dark look.
*   **Simulated Connection:** Mimics connecting to a secure neural implant with visual feedback.
*   **Encryption Key Visualization:** Generates a random key and "visualizes" it on a canvas using simple graphical elements.
*   **Simulated Data Transfer:** Shows a progress bar indicating the transfer of "encrypted evidence".
*   **Data Display:** Presents simulated "decrypted" source code/evidence in a scrolled text area after successful transfer.
*   **Threading:** Uses threading for non-blocking simulation of connection, visualization, and transfer processes.

---

## 2. MIMIC - Network Infiltration System (`mimic.py`)

Simulates an advanced tool ("MIMIC") used for infiltrating secure computer networks. It features a dynamic network graph, a terminal-like log output, and progresses through stages of scanning, infiltration, analysis, and data gathering.


![Mimic](https://github.com/user-attachments/assets/c2f724e5-2af0-4db8-9187-c76df7507dc1)

### Features

*   **Hacker-Themed UI:** Dark interface with green accents (`customtkinter`).
*   **Network Topology Visualization:** A dynamic canvas displaying network nodes (servers, routers, firewalls, etc.) and connections. Nodes change appearance based on status (inactive, active, infected).
*   **Simulated Operations:** Guides the user through simulated steps:
    *   **Scan Network:** Maps the topology and identifies potential targets.
    *   **Deploy Mimic:** Simulates infiltrating the network and spreading through nodes.
    *   **Analyze Environment:** Simulates searching for valuable information on infected nodes.
    *   **Gather Intelligence:** Simulates exfiltrating the "discovered" data.
*   **Terminal Output:** A log area displaying timestamped messages about the ongoing simulation status, successes, warnings, and errors.
*   **Progress Modules:** Separate progress bars and status text for different phases of the operation (Infiltration, Mimicry, Data Collection).
*   **Status Bar:** Displays overall system status indicators (Connection, Encryption, Detection Risk, Progress).
*   **Threading:** Uses threading to run simulations without freezing the UI.

---

## Prerequisites

*   **Python:** Version 3.7 or higher recommended.
*   **Tkinter:** Usually included with standard Python distributions.
*   **CustomTkinter:** A Python UI library based on Tkinter.

---

## Setup and Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    # Create a virtual environment (optional but recommended)
    python -m venv venv
    # Activate it (Windows)
    .\venv\Scripts\activate
    # Activate it (macOS/Linux)
    source venv/bin/activate

    # Install required library
    pip install customtkinter
 


3.  **Run the applications:**
    Navigate to the directory containing the scripts in your terminal and run them individually:

    *   To run the Neural Encryption Interface:
        ```bash
        python neural_encryption_dark.py
        ```
    *   To run the MIMIC Network Infiltration System:
        ```bash
        python mimic.py
        ```

---

## Disclaimer ⚠️

These applications are **simulations only** created for educational and demonstration purposes.

*   `neural_encryption_dark.py` **does not** perform any real encryption or connect to any real devices.
*   `mimic.py` **does not** perform any real network scanning, infiltration, hacking, or data exfiltration. It does not interact with your network or any external systems in a harmful way.

Do not attempt to use concepts depicted here for illegal or unethical activities. The author is not responsible for any misuse of this code.

---

## License

(GNU)

