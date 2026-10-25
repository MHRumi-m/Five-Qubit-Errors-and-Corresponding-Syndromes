# Five-Qubit-Errors-and-Corresponding-Syndromes
Quantum Error Correction with Five Qubit Code and Syndrome Mapping with Qiskit

This repository contains a Qiskit implementation designed to evaluate and map all possible $4^5 = 1024$ Pauli error configurations ($X, Y, Z, I$) acting on an encoded 5-qubit quantum state. It works like active error tracking where you only read the ancilla measurements and no logical bit measurement is required. 

## Methodology
1. **Encoding:** Initializes a 14-qubit register. 5 physical qubits are taken to encode a logical state.
2. **Error Injection:** Systematically steps through every mathematical permutation of single and multi-qubit Pauli errors across all 5 code qubits.
3. **Syndrome Extraction:** Measures the 4 traditional stabilizer generators ($g_1, g_2, g_3, g_4$) using ancilla tracking lines.
4. **Data Aggregation:** Groups error strings under their respective resulting 4-bit binary syndrome key and compiles them into a structured spreadsheet.

## Environment Requirements
To execute this code locally without errors, ensure your environment uses the following specific framework versions:
* **Qiskit:** `2.6.1`
* **Qiskit Aer:** `0.18.0`
* **Dependencies:** `pandas`, `openpyxl`, `numpy`

## Project Files
* `MainCode.py`: Main Python script executing the error injection loop and stabilizer measurements.

## Execution Instructions
You can install the required frameworks and execute the script directly through your terminal using the following commands:

```bash
# Install the framework versions used in this project
pip install qiskit==2.6.1 qiskit-aer==0.18.0 pandas openpyxl numpy

# Run the syndrome extraction simulation
python MainCode.py
```
Upon successful execution, the script yields a `qkd_syndrome.xlsx` map in the root directory.

