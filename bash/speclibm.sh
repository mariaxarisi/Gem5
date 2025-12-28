#!/usr/bin/env bash

# Base paths (adjust if needed)
REPO_ROOT="/home/arch/Desktop/Repo"
GEM5_DIR="/home/arch/Desktop/gem5"
GEM5_BIN="/home/arch/Desktop/gem5/build/ARM/gem5.opt"

# Output root for this exploration
OUT_ROOT="${REPO_ROOT}/spec-performance-opt/speclibm"

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
  local l1d_size="$1"
  local l1d_assoc="$2"
  local l2_size="$3"
  local l2_assoc="$4"
  local line_size="$5"

  # Code: {l1i_size}_{l1i_assoc}_{l1d_size}_{l1d_assoc}_{l2_size}_{l2_assoc}_{cache_line_size}
  local code="${BASE_L1I_SIZE}_${BASE_L1I_ASSOC}_${l1d_size}_${l1d_assoc}_${l2_size}_${l2_assoc}_${line_size}"
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
    --l1i_size="${BASE_L1I_SIZE}" \
    --l1i_assoc="${BASE_L1I_ASSOC}" \
    --l1d_size="${l1d_size}" \
    --l1d_assoc="${l1d_assoc}" \
    --l2_size="${l2_size}" \
    --l2_assoc="${l2_assoc}" \
    --cacheline_size="${line_size}" \
    -c "${GEM5_DIR}/spec_cpu2006/470.lbm/src/speclibm" \
    -o "20 ${GEM5_DIR}/spec_cpu2006/470.lbm/data/lbm.in 0 1 ${GEM5_DIR}/spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" \
    -I 100000000

  # Clean up unneeded files
  rm -rf "${out_dir}/fs/" 2>/dev/null || true
  rm -f "${out_dir}/config.dot"* 2>/dev/null || true
}

# 1) Sweep L1D size: 16, 32, 64, 128 kB 
L1D_SIZES=("16kB" "32kB" "64kB" "128kB")
for l1d_size in "${L1D_SIZES[@]}"; do
  run_config "${l1d_size}" "${BASE_L1D_ASSOC}" "${BASE_L2_SIZE}" "${BASE_L2_ASSOC}" "${BASE_LINE_SIZE}"
done

# 2) Sweep L1D associativity: 1, 2, 4 (
L1D_ASSOCS=("1" "2" "4")
for l1d_assoc in "${L1D_ASSOCS[@]}"; do
  run_config "${BASE_L1D_SIZE}" "${l1d_assoc}" "${BASE_L2_SIZE}" "${BASE_L2_ASSOC}" "${BASE_LINE_SIZE}"
done

# 3) Sweep L2 size: 1, 2, 4 MB 
L2_SIZES=("1MB" "2MB" "4MB")
for l2_size in "${L2_SIZES[@]}"; do
  run_config "${BASE_L1D_SIZE}" "${BASE_L1D_ASSOC}" "${l2_size}" "${BASE_L2_ASSOC}" "${BASE_LINE_SIZE}"
done

# 4) Sweep L2 associativity: 4, 8, 16 
L2_ASSOCS=("4" "8" "16")
for l2_assoc in "${L2_ASSOCS[@]}"; do
  run_config "${BASE_L1D_SIZE}" "${BASE_L1D_ASSOC}" "${BASE_L2_SIZE}" "${l2_assoc}" "${BASE_LINE_SIZE}"
done

# 5) Sweep line size: 16, 32, 64 B 
LINE_SIZES=("32" "64" "128")
for line_size in "${LINE_SIZES[@]}"; do
  run_config "${BASE_L1D_SIZE}" "${BASE_L1D_ASSOC}" "${BASE_L2_SIZE}" "${BASE_L2_ASSOC}" "${line_size}"
done
