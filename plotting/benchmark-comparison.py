import os
import matplotlib.pyplot as plt

benchmarks = ['specbzip', 'spechmmer', 'speclibm', 'specmcf', 'specsjeng']

cur_dir = os.path.dirname(os.path.abspath(__file__))
benchmarks_dir = os.path.join(cur_dir, '..', 'spec', 'cpu-clock-2GHz')
assets_dir = os.path.join(cur_dir, '..', 'assets', 'benchmark-comparison')

# Ensure output directory exists
os.makedirs(assets_dir, exist_ok=True)

# Metrics to collect per benchmark
sim_seconds = {}
cpi = {}
insts = {}

l1i_miss = {}
l1d_miss = {}
l2_miss = {}

for benchmark in benchmarks:
    stats_file = os.path.join(benchmarks_dir, benchmark, 'stats.txt')
    if not os.path.isfile(stats_file):
        continue

    with open(stats_file, 'r') as f:
        for line in f:
            # Skip comments/empty lines
            if line.strip() == '' or line.strip().startswith('#'):
                continue

            # Execution time (simulated seconds)
            if line.startswith('sim_seconds'):
                parts = line.split()
                sim_seconds[benchmark] = float(parts[1])

            # CPI
            elif line.startswith('system.cpu.cpi'):
                parts = line.split()
                cpi[benchmark] = float(parts[1])

            # Committed instructions
            elif line.startswith('system.cpu.committedInsts'):
                parts = line.split()
                insts[benchmark] = int(parts[1])

            # L1 Instruction cache miss rate
            elif 'icache.overall_miss_rate::total' in line:
                parts = line.split()
                l1i_miss[benchmark] = float(parts[1])

            # L1 Data cache miss rate
            elif 'dcache.overall_miss_rate::total' in line:
                parts = line.split()
                l1d_miss[benchmark] = float(parts[1])

            # L2 miss rate
            elif '.l2.overall_miss_rate::total' in line or 'l2.overall_miss_rate::total' in line:
                parts = line.split()
                l2_miss[benchmark] = float(parts[1])

# Helper to generate bar plots
labels = benchmarks
x = range(len(labels))

# 1) Execution time (sim_seconds)
values = [sim_seconds.get(b, 0) for b in labels]
plt.figure(figsize=(8, 5))
plt.bar(x, values, color='skyblue')
plt.xticks(x, labels, rotation=45)
plt.ylabel('Simulated Time (s)')
plt.title('Execution Time (sim_seconds) per Benchmark')
plt.tight_layout()
plt.savefig(os.path.join(assets_dir, 'sim_seconds.png'))
plt.close()

# 2) CPI
values = [cpi.get(b, 0) for b in labels]
plt.figure(figsize=(8, 5))
plt.bar(x, values, color='orange')
plt.xticks(x, labels, rotation=45)
plt.ylabel('CPI')
plt.title('CPI per Benchmark')
plt.tight_layout()
plt.savefig(os.path.join(assets_dir, 'cpi.png'))
plt.close()

# 3) Committed instructions
values = [insts.get(b, 0) for b in labels]
plt.figure(figsize=(8, 5))
plt.bar(x, values, color='green')
plt.xticks(x, labels, rotation=45)
plt.ylabel('Committed Instructions')
plt.title('Committed Instructions per Benchmark')
plt.tight_layout()
plt.savefig(os.path.join(assets_dir, 'committed_insts.png'))
plt.close()

# 4) L1 I-cache miss rate
values = [l1i_miss.get(b, 0) for b in labels]
plt.figure(figsize=(8, 5))
plt.bar(x, values, color='red')
plt.xticks(x, labels, rotation=45)
plt.ylabel('L1 I-cache Miss Rate')
plt.title('L1 Instruction Cache Overall Miss Rate per Benchmark')
plt.tight_layout()
plt.savefig(os.path.join(assets_dir, 'l1i_miss_rate.png'))
plt.close()

# 5) L1 D-cache miss rate
values = [l1d_miss.get(b, 0) for b in labels]
plt.figure(figsize=(8, 5))
plt.bar(x, values, color='purple')
plt.xticks(x, labels, rotation=45)
plt.ylabel('L1 D-cache Miss Rate')
plt.title('L1 Data Cache Overall Miss Rate per Benchmark')
plt.tight_layout()
plt.savefig(os.path.join(assets_dir, 'l1d_miss_rate.png'))
plt.close()

# 6) L2 cache miss rate
values = [l2_miss.get(b, 0) for b in labels]
plt.figure(figsize=(8, 5))
plt.bar(x, values, color='brown')
plt.xticks(x, labels, rotation=45)
plt.ylabel('L2 Cache Miss Rate')
plt.title('L2 Cache Overall Miss Rate per Benchmark')
plt.tight_layout()
plt.savefig(os.path.join(assets_dir, 'l2_miss_rate.png'))
plt.close()
