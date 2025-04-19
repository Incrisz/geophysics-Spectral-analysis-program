import pandas as pd
import matplotlib.pyplot as plt

# Load Excel file
df = pd.read_excel("kaltungo.xlsx")

# Clean and convert columns to numeric, forcing invalid entries to NaN
x = pd.to_numeric(df.iloc[:, 0], errors='coerce')  # X (CYC/K_unit)
y = pd.to_numeric(df.iloc[:, 1], errors='coerce')  # Y (Ln_P)

# Filter out rows where either x or y is NaN
valid_data = df.dropna(subset=[df.columns[0], df.columns[1]])

# Re-convert the cleaned columns
x = pd.to_numeric(valid_data.iloc[:, 0], errors='coerce')
y = pd.to_numeric(valid_data.iloc[:, 1], errors='coerce')

# Further filter out any remaining non-numeric values from x and y
valid_data = valid_data[(x.notna()) & (y.notna())]

# Plot the cleaned data
plt.figure(figsize=(8, 5))
plt.plot(valid_data.iloc[:, 0], valid_data.iloc[:, 1], marker='o', linestyle='-', color='blue')
plt.title('kaltungo 2D Radial Spectrum')
plt.xlabel('X (CYC/K_unit) - 2D RADIALLY')
plt.ylabel('Y (Ln_P) - SPECTRUM')
plt.grid(True)
plt.tight_layout()
plt.show()
