import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definisikan variabel input dan output
nilai_ndvi = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'nilai_ndvi')
nilai_reflektansi = ctrl.Antecedent(np.arange(0, 101, 1), 'nilai_reflektansi')
kualitas_tanaman = ctrl.Consequent(np.arange(0, 51, 1), 'kualitas_tanaman')

# Membership functions for NDVI
nilai_ndvi['rendah'] = fuzz.trimf(nilai_ndvi.universe, [0, 0, 0.26])
nilai_ndvi['tinggi'] = fuzz.trapmf(nilai_ndvi.universe, [0.2, 0.3, 1, 1])

# Membership functions for Reflektansi
nilai_reflektansi['rendah'] = fuzz.trapmf(nilai_reflektansi.universe, [0, 0, 35, 55])
nilai_reflektansi['tinggi'] = fuzz.trapmf(nilai_reflektansi.universe, [40, 50, 100, 100])

# Membership functions for Kualitas Tanaman
kualitas_tanaman['sakit'] = fuzz.trimf(kualitas_tanaman.universe, [0, 25, 50])
kualitas_tanaman['sehat'] = fuzz.trimf(kualitas_tanaman.universe, [0, 25, 50])

# Define the fuzzy rules
rule1 = ctrl.Rule(nilai_ndvi['rendah'] | nilai_reflektansi['tinggi'], kualitas_tanaman['sakit'])
rule2 = ctrl.Rule(nilai_ndvi['rendah'] | nilai_reflektansi['rendah'], kualitas_tanaman['sakit'])
rule3 = ctrl.Rule(nilai_ndvi['tinggi'] | nilai_reflektansi['tinggi'], kualitas_tanaman['sakit'])
rule4 = ctrl.Rule(nilai_ndvi['tinggi'] | nilai_reflektansi['rendah'], kualitas_tanaman['sehat'])
rule5 = ctrl.Rule(nilai_ndvi['tinggi'] | nilai_reflektansi['rendah'], kualitas_tanaman['sehat'])

# Control system
kualitas_tanaman_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
kualitas_tanaman_simulasi = ctrl.ControlSystemSimulation(kualitas_tanaman_ctrl)

# Input values
nilai_ndvi_input = 0.2
nilai_reflektansi_input = 50

# Set inputs
kualitas_tanaman_simulasi.input['nilai_ndvi'] = nilai_ndvi_input
kualitas_tanaman_simulasi.input['nilai_reflektansi'] = nilai_reflektansi_input

# Compute
kualitas_tanaman_simulasi.compute()

# Output
print(f'Input NDVI: {nilai_ndvi_input}')
print(f'Input Reflektansi: {nilai_reflektansi_input}')
print(f'Output Kualitas Tanaman: {kualitas_tanaman_simulasi.output["kualitas_tanaman"]}')
