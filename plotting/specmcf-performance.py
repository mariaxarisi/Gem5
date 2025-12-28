import os
import matplotlib.pyplot as plt

# Paths
cur_dir = os.path.dirname(os.path.abspath(__file__))
perf_dir = os.path.join(cur_dir, '..', 'spec-performance-opt', 'specmcf')
assets_dir = os.path.join(cur_dir, '..', 'assets', 'specmcf')
os.makedirs(assets_dir, exist_ok=True)

# Baseline values
base_l1i_size = "32kB"
base_l1i_assoc = "2"
base_l1d_size = "64kB"
base_l1d_assoc = "2"
base_l2_size = "2MB"
base_l2_assoc = "8"
base_line_size = "64"

l1i_sizes = ["16kB", "32kB", "64kB", "128kB"]
l1i_assocs = ["1", "2", "4"]

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

# 1. CPI vs L1I size
cpi_l1i_size = []
for l1i in l1i_sizes:
    code = f"{l1i}_{base_l1i_assoc}_{base_l1d_size}_{base_l1d_assoc}_{base_l2_size}_{base_l2_assoc}_{base_line_size}"
    stats_path = os.path.join(perf_dir, code, "stats.txt")
    cpi = get_cpi_from_stats(stats_path)
    cpi_l1i_size.append(cpi)

plt.figure()
plt.plot(l1i_sizes, cpi_l1i_size, marker='o')
plt.xlabel("L1I Size")
plt.ylabel("CPI")
plt.title("specmcf: CPI vs L1I Size")
plt.grid(True)
plt.savefig(os.path.join(assets_dir, "cpi_vs_l1i_size.png"))

# 2. CPI vs L1I associativity
cpi_l1i_assoc = []
for l1i_assoc in l1i_assocs:
    code = f"{base_l1i_size}_{l1i_assoc}_{base_l1d_size}_{base_l1d_assoc}_{base_l2_size}_{base_l2_assoc}_{base_line_size}"
    stats_path = os.path.join(perf_dir, code, "stats.txt")
    cpi = get_cpi_from_stats(stats_path)
    cpi_l1i_assoc.append(cpi)

plt.figure()
plt.plot(l1i_assocs, cpi_l1i_assoc, marker='o')
plt.xlabel("L1I Associativity")
plt.ylabel("CPI")
plt.title("specmcf: CPI vs L1I Associativity")
plt.grid(True)
plt.savefig(os.path.join(assets_dir, "cpi_vs_l1i_assoc.png"))

print("Plots saved in", assets_dir)