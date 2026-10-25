from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np
from google.colab import files
import pandas as pd
import io, random
from itertools import combinations, product

def make_circuit():
  qr = QuantumRegister(14)
  cr = ClassicalRegister(10)
  qc = QuantumCircuit(qr, cr)
  return qc, qr, cr

def QKD_encoder(qc, qr, cr):
  # apply 5 qubit encoder
  qc.x(qr[1])
  qc.x(qr[4])
  qc.cx(qr[0], qr[1])
  qc.h(qr[1])
  qc.h(qr[2])
  qc.cx(qr[2], qr[0])
  qc.cx(qr[2], qr[3])
  qc.cx(qr[1], qr[3])
  qc.cx(qr[0], qr[4])
  qc.cx(qr[1], qr[0])
  qc.h(qr[3])
  qc.h(qr[4])
  qc.cx(qr[3], qr[0])
  qc.cx(qr[4], qr[0])
  return qc, qr, cr

def bit_and_phase_flip(qc, qr, cr, flip_qubit, rand_axis):
  # choose x,y,z error
  if rand_axis == 0:
    qc.x(qr[flip_qubit])
  elif rand_axis == 1:
    qc.z(qr[flip_qubit])
  elif rand_axis == 2:
    qc.x(qr[flip_qubit])
    qc.z(qr[flip_qubit])
  return qc, qr, cr

def decoding(qc, qr, cr):
  # g1 syndrome: XZZXI
  qc.reset(qr[5])
  qc.h(qr[0]); qc.cx(qr[0], qr[5]); qc.h(qr[0])
  qc.cx(qr[1], qr[5])
  qc.cx(qr[2], qr[5])
  qc.h(qr[3]); qc.cx(qr[3], qr[5]); qc.h(qr[3])
  qc.barrier()

  # g2 syndrome: IXZZX
  qc.reset(qr[6])
  qc.h(qr[1]); qc.cx(qr[1], qr[6]); qc.h(qr[1])
  qc.cx(qr[2], qr[6])
  qc.cx(qr[3], qr[6])
  qc.h(qr[4]); qc.cx(qr[4], qr[6]); qc.h(qr[4])
  qc.barrier()

  # g3 syndrome: XIXZZ
  qc.reset(qr[7])
  qc.h(qr[0]); qc.cx(qr[0], qr[7]); qc.h(qr[0])
  qc.h(qr[2]); qc.cx(qr[2], qr[7]); qc.h(qr[2])
  qc.cx(qr[3], qr[7])
  qc.cx(qr[4], qr[7])
  qc.barrier()

  # g4 syndrome: ZXIXZ
  qc.reset(qr[8])
  qc.cx(qr[0], qr[8])
  qc.h(qr[1]); qc.cx(qr[1], qr[8]); qc.h(qr[1])
  qc.h(qr[3]); qc.cx(qr[3], qr[8]); qc.h(qr[3])
  qc.cx(qr[4], qr[8])
  qc.barrier()

  # measure ancillas to get syndrome measurements
  qc.measure([qr[5], qr[6], qr[7], qr[8]], [cr[3], cr[2], cr[1], cr[0]])
  return qc, qr, cr

# Initialize dictionary
gate_map = {0: 'X', 1: 'Z', 2: 'Y', 3: 'I'}
syndrome_columns = {}
output_filename = "qkd_syndrome.xlsx"

#all possible Pauli errors
for q4_axis in range(4):
  for q3_axis in range(4):
    for q2_axis in range(4):
      for q1_axis in range(4):
        for q0_axis in range(4):


          qc, qr, cr = make_circuit()
          qc, qr, cr = QKD_encoder(qc, qr, cr)

          qubit_axes = [q0_axis, q1_axis, q2_axis, q3_axis, q4_axis]

          qc_copy = qc.copy()
          for flip_qubit, rand_axis in enumerate(qubit_axes):
              if rand_axis < 3:  #ignore 'I'
                 qc_copy, qr, cr = bit_and_phase_flip(qc_copy, qr, cr, flip_qubit, rand_axis)

          qc_copy, qr, cr = decoding(qc_copy, qr, cr)

          simulation = AerSimulator()
          qc_transpiled = transpile(qc_copy, simulation)
          result = simulation.run(qc_transpiled, shots=1, memory=True).result()
          memory = result.get_memory()

          outcome = memory[0]


          syndrome_key = outcome[-4:]

          axes_string = ''.join(gate_map[axis] for axis in qubit_axes)
          if syndrome_key not in syndrome_columns:
              syndrome_columns[syndrome_key] = []
          syndrome_columns[syndrome_key].append(axes_string)

# Balancing step
max_length = max(len(lst) for lst in syndrome_columns.values())
for syndrome in syndrome_columns:
    current_length = len(syndrome_columns[syndrome])
    if current_length < max_length:
        syndrome_columns[syndrome].extend([""] * (max_length - current_length))

# Build and export DataFrame
df = pd.DataFrame(syndrome_columns)
df = df.reindex(sorted(df.columns), axis=1)

df.to_excel(output_filename, index=False)
files.download(output_filename)
