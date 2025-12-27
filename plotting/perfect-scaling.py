import os
import matplotlib.pyplot as plt


benchmarks = ['specbzip', 'spechmmer', 'speclibm', 'specmcf', 'specsjeng']

cur_dir = os.path.dirname(os.path.abspath(__file__))
clock_dirs = {
    1: os.path.join(cur_dir, '..', 'spec', 'cpu-clock-1GHz'),
    2: os.path.join(cur_dir, '..', 'spec', 'cpu-clock-2GHz'),
    4: os.path.join(cur_dir, '..', 'spec', 'cpu-clock-4GHz'),
}
assets_dir = os.path.join(cur_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)


def parse_sim_seconds(stats_path: str) -> float | None:
    """Parse sim_seconds from a gem5 stats.txt file. Returns None if not found."""

    if not os.path.exists(stats_path):
        return None

    with open(stats_path, 'r') as f:
        for line in f:
            if line.startswith('sim_seconds'):
                # Format: sim_seconds <value> # comment
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        return float(parts[1])
                    except ValueError:
                        return None
    return None


def main() -> None:
    # Collect sim_seconds[benchmark][freq] = value
    sim_seconds = {b: {} for b in benchmarks}

    for freq_ghz, base_dir in clock_dirs.items():
        for bench in benchmarks:
            stats_path = os.path.join(base_dir, bench, 'stats.txt')
            value = parse_sim_seconds(stats_path)
            if value is None:
                print(f"Warning: sim_seconds not found for {bench} at {freq_ghz}GHz ({stats_path})")
            else:
                sim_seconds[bench][freq_ghz] = value

    # Prepare plot
    fig, ax = plt.subplots(figsize=(8, 5))

    freqs = sorted(clock_dirs.keys())  # [1, 2, 4]

    # Plot one line per benchmark
    for bench in benchmarks:
        y = [sim_seconds[bench].get(f, float('nan')) for f in freqs]
        ax.plot(freqs, y, marker='o', label=bench)

    ax.set_xlabel('CPU clock (GHz)')
    ax.set_ylabel('Simulated time (sim_seconds)')
    ax.set_title('Scaling of sim_seconds with CPU clock')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend()

    out_path = os.path.join(assets_dir, 'perfect-scaling.png')
    plt.tight_layout()
    plt.savefig(out_path)
    print(f'Saved plot to {out_path}')


if __name__ == '__main__':
    main()
