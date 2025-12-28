#!/usr/bin/env bash

# Base paths (adjust if needed)
REPO_ROOT="/home/arch/Desktop/Repo"
GEM5_DIR="/home/arch/Desktop/gem5"
GEM5_BIN="/home/arch/Desktop/gem5/build/ARM/gem5.opt"

# Output root for this exploration
OUT_ROOT="${REPO_ROOT}/spec-performance-opt/specmcf"

# Baseline configuration (MinorCPU, 1 GHz, 32KB/64KB L1, 2MB L2, 64B line)
BASE_L1I_SIZE="32kB"
BASE_L1I_ASSOC="2"
BASE_L1D_SIZE="64kB"
BASE_L1D_ASSOC="2"
BASE_L2_SIZE="2MB"
BASE_L2_ASSOC="8"
BASE_LINE_SIZE="64"

mkdir -p "${OUT_ROOT}"

run_config() {
  local l1i_size="$1"
  local l1i_assoc="$2"

  # Code: {l1i_size}_{l1i_assoc}_{l1d_size}_{l1d_assoc}_{l2_size}_{l2_assoc}_{cache_line_size}
  local code="${l1i_size}_${l1i_assoc}_${BASE_L1D_SIZE}_${BASE_L1D_ASSOC}_${BASE_L2_SIZE}_${BASE_L2_ASSOC}_${BASE_LINE_SIZE}"
  local out_dir="${OUT_ROOT}/${code}"

  if [ -f "${out_dir}/stats.txt" ]; then
    echo "Skipping existing configuration: ${code}"
    return
  fi

  echo "Running configuration: ${code}"
  mkdir -p "${out_dir}"

  "${GEM5_BIN}" \
    -d "${out_dir}" \
    "${GEM5_DIR}/configs/example/se.py" \
    --cpu-type=MinorCPU \
    --caches \
    --l2cache \
    --cpu-clock=1GHz \
    --l1i_size="${l1i_size}" \
    --l1i_assoc="${l1i_assoc}" \
    --l1d_size="${BASE_L1D_SIZE}" \
    --l1d_assoc="${BASE_L1D_ASSOC}" \
    --l2_size="${BASE_L2_SIZE}" \
    --l2_assoc="${BASE_L2_ASSOC}" \
    --cacheline_size="${BASE_LINE_SIZE}" \
    -c "${GEM5_DIR}/spec_cpu2006/429.mcf/src/specmcf" \
    -o "${GEM5_DIR}/spec_cpu2006/429.mcf/data/inp.in" \
    -I 100000000

  # Clean up unneeded files
  rm -rf "${out_dir}/fs/" 2>/dev/null || true
  rm -f "${out_dir}/config.dot"* 2>/dev/null || true
}

# 1) Sweep L1I size: 16, 32, 64, 128 kB
L1I_SIZES=("16kB" "32kB" "64kB" "128kB")
for l1i_size in "${L1I_SIZES[@]}"; do
  run_config "${l1i_size}" "${BASE_L1I_ASSOC}"
done

# 2) Sweep L1I associativity: 1, 2, 4
L1I_ASSOCS=("1" "2" "4")
for l1i_assoc in "${L1I_ASSOCS[@]}"; do
  run_config "${BASE_L1I_SIZE}" "${l1i_assoc}"
done