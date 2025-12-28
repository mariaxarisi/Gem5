import os
import matplotlib.pyplot as plt

# Paths
cur_dir = os.path.dirname(os.path.abspath(__file__))
perf_dir = os.path.join(cur_dir, '..', 'spec-performance-opt', 'specbzip')
assets_dir = os.path.join(cur_dir, '..', 'assets', 'specbzip')
os.makedirs(assets_dir, exist_ok=True)

# Baseline values
base_l1i_size = "32kB"
base_l1i_assoc = "2"
base_l1d_size = "64kB"
base_l1d_assoc = "2"
base_l2_size = "2MB"
base_l2_assoc = "8"
base_line_size = "64"

l1d_sizes = ["16kB", "32kB", "64kB", "128kB"]
l2_sizes = ["1MB", "2MB", "4MB"]
line_sizes = ["32", "64"]

def get_cpi_from_stats(stats_path):
    if not os.path.isfile(stats_path):
        return None
    with open(stats_path, "r") as f:
        for line in f:
            if line.startswith("system.cpu.cpi"):
                try:
                    return float(line.split()[1])
                except Exception:
                    return None
    return None

# 1. CPI vs L1D size
cpi_l1d = []
for l1d in l1d_sizes:
    code = f"{base_l1i_size}_{base_l1i_assoc}_{l1d}_{base_l1d_assoc}_{base_l2_size}_{base_l2_assoc}_{base_line_size}"
    stats_path = os.path.join(perf_dir, code, "stats.txt")
    cpi = get_cpi_from_stats(stats_path)
    cpi_l1d.append(cpi)

plt.figure()
plt.plot(l1d_sizes, cpi_l1d, marker='o')
plt.xlabel("L1D Size")
plt.ylabel("CPI")
plt.title("specbzip: CPI vs L1D Size")
plt.grid(True)
plt.savefig(os.path.join(assets_dir, "cpi_vs_l1d_size.png"))

# 2. CPI vs L2 size
cpi_l2 = []
for l2 in l2_sizes:
    code = f"{base_l1i_size}_{base_l1i_assoc}_{base_l1d_size}_{base_l1d_assoc}_{l2}_{base_l2_assoc}_{base_line_size}"
    stats_path = os.path.join(perf_dir, code, "stats.txt")
    cpi = get_cpi_from_stats(stats_path)
    cpi_l2.append(cpi)

plt.figure()
plt.plot(l2_sizes, cpi_l2, marker='o')
plt.xlabel("L2 Size")
plt.ylabel("CPI")
plt.title("specbzip: CPI vs L2 Size")
plt.grid(True)
plt.savefig(os.path.join(assets_dir, "cpi_vs_l2_size.png"))

# 3. CPI vs Line size
cpi_line = []
for line in line_sizes:
    code = f"{base_l1i_size}_{base_l1i_assoc}_{base_l1d_size}_{base_l1d_assoc}_{base_l2_size}_{base_l2_assoc}_{line}"
    stats_path = os.path.join(perf_dir, code, "stats.txt")
    cpi = get_cpi_from_stats(stats_path)
    cpi_line.append(cpi)

plt.figure()
plt.plot(line_sizes, cpi_line, marker='o')
plt.xlabel("Cache Line Size")
plt.ylabel("CPI")
plt.title("specbzip: CPI vs Cache Line Size")
plt.grid(True)
plt.savefig(os.path.join(assets_dir, "cpi_vs_line_size.png"))

print("Plots saved in", assets_dir)
