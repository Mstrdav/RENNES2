
import os
import glob
import fitdecode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Directories
DATA_DIR = "../data"
ASSIOMA_DIR = os.path.join(DATA_DIR, "unzipped_Assioma")
WAHOO_DIR = os.path.join(DATA_DIR, "datas_Wahoo")
OUTPUT_DIR = "../data/processed"
FIGURES_DIR = "../rapport/figures"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# Mapping Assioma filenames (which are IDs) to readable names based on Zip files
# I need to reconstruct this mapping or assume the unzipped files are there.
# Since filenames in unzipped_Assioma are IDs like 21553997254_ACTIVITY.fit, I need to know which is which.
# I can use the zip list I saw earlier or re-list them.
# Better approach: Iterate over zip files in datas_Assioma, verify their content name, and map.

zip_files = glob.glob(os.path.join(DATA_DIR, "datas_Assioma", "*.zip"))
assioma_map = {}

import zipfile

print("Mapping Assioma files...")
for zf in zip_files:
    basename = os.path.basename(zf).replace(".zip", "")
    with zipfile.ZipFile(zf, 'r') as z:
        for name in z.namelist():
            if name.endswith(".fit"):
                assioma_map[name] = basename
                # Also copy/rename for clarity if needed, or just load from unzipped path
                # We already unzipped them to unzipped_Assioma
                
print(f"Found {len(assioma_map)} Assioma mappings.")

# Wahoo files are named clearly: YYYY-MM-DD-HHMMSS-Name_RPM.fit
wahoo_files = glob.glob(os.path.join(WAHOO_DIR, "*.fit"))

def parse_fit(path):
    data = []
    with fitdecode.FitReader(path) as fit:
        for frame in fit:
            if frame.frame_type == fitdecode.FIT_FRAME_DATA and frame.name == 'record':
                fields = {f.name: f.value for f in frame.fields}
                if 'timestamp' in fields and 'power' in fields:
                    data.append(fields)
    
    if not data:
        return None
        
    df = pd.DataFrame(data)
    # Ensure timestamp is datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        df.set_index('timestamp', inplace=True)
    
    # Keep only relevant columns
    cols = ['power', 'cadence']
    df = df[[c for c in cols if c in df.columns]]
    
    # Resample to 1s to regularize
    df = df.resample('1s').mean()
    return df

# Process pairs
pairs = []

for w_path in wahoo_files:
    w_name = os.path.basename(w_path)
    # Extract "Name_RPM" from "2026-01-15-093049-Matys_70rpm.fit"
    # Split by '-' and take the part after HHMMSS? 
    # Or simply search for the matching name in Assioma map values.
    
    # Standardize name: Matys_70rpm
    # Wahoo name format: Date-Time-Name_RPM.fit. 
    # Careful, some might differ.
    
    parts = w_name.split('-')
    if len(parts) >= 4:
        # Reconstruct potential key name
        # parts[3] might be "Matys_70rpm.fit"
        candidate_name = parts[-1].replace(".fit", "")
        
        # Check if we have an Assioma match
        match_id = None
        
        # Explicit mapping for Sprints
        # Based on timestamp analysis:
        # Wahoo SprintGrA (13:00) matches Assioma Sprints_Gr2 (13:00) -> 21556116585
        # Wahoo SprintGrB (11:07) matches Assioma Sprints_Gr1 (11:02) -> 21553999314
        if candidate_name == "SprintGrA":
            match_id = "21556116585_ACTIVITY.fit" 
        elif candidate_name == "SprintGrB":
            match_id = "21553999314_ACTIVITY.fit"
        
        if not match_id:
            # Try exact match first
            for fit_name, friendly_name in assioma_map.items():
                if friendly_name == candidate_name:
                    match_id = fit_name
                    break
        
        # If not found, try partial match
        if not match_id:
            for fit_name, friendly_name in assioma_map.items():
                if candidate_name in friendly_name or friendly_name in candidate_name:
                    match_id = fit_name
                    break
        
        if match_id:
            pairs.append({
                "name": candidate_name,
                "wahoo_path": w_path,
                "assioma_path": os.path.join(ASSIOMA_DIR, match_id)
            })
        else:
            print(f"No Assioma match for Wahoo file: {candidate_name}")

print(f"Found {len(pairs)} pairs to process.")

summary_stats = []

for pair in pairs:
    name = pair['name']
    print(f"Processing {name}...")
    
    w_df = parse_fit(pair['wahoo_path'])
    a_df = parse_fit(pair['assioma_path'])
    
    if w_df is None or a_df is None:
        print(f"Error reading data for {name}")
        continue
        
    print(f"  Wahoo: {w_df.index[0]} to {w_df.index[-1]} ({len(w_df)} pts)")
    print(f"  Assioma: {a_df.index[0]} to {a_df.index[-1]} ({len(a_df)} pts)")
    
    # Rename columns
    w_df.columns = [f"{c}_wahoo" for c in w_df.columns]
    a_df.columns = [f"{c}_assioma" for c in a_df.columns]
    
    # Synchronize using Cross-Correlation on Power
    # Resample to common 1s grid
    # Get common time range? No, they might be offset.
    # Convert index to seconds from start for correlation
    
    # We work with numpy arrays for correlation
    # We assume sampling rate is 1Hz (as resampled above)
    
    p1 = w_df['power_wahoo'].fillna(0).values
    p2 = a_df['power_assioma'].fillna(0).values
    
    # Normalize
    p1 = (p1 - np.mean(p1)) / (np.std(p1) + 1e-6)
    p2 = (p2 - np.mean(p2)) / (np.std(p2) + 1e-6)
    
    # Cross correlate
    from scipy import signal
    correlation = signal.correlate(p1, p2, mode='full')
    lags = signal.correlation_lags(len(p1), len(p2), mode='full')
    lag = lags[np.argmax(correlation)]
    
    print(f"  Detected lag: {lag} seconds")
    
    # Apply lag to Assioma timestamp
    # If lag is positive, p1 starts after p2? 
    # correlation[k] = sum(p1[n] * p2[n+k])
    # Peak at lag k means p1 matches p2 shifted by k.
    # So we shift p2 (Assioma) by k seconds to match p1.
    
    a_df_shifted = a_df.copy()
    a_df_shifted.index = a_df.index + pd.Timedelta(seconds=int(lag))
    
    # Merge with shift
    combined = pd.merge_asof(w_df.sort_index(), a_df_shifted.sort_index(), left_index=True, right_index=True, direction='nearest', tolerance=pd.Timedelta('1s'))
    combined = combined.dropna()
    
    if len(combined) < 10:
        print(f"  Warning: Only {len(combined)} points matched after sync.")
    
    # Calculate difference
    if 'power_wahoo' in combined.columns and 'power_assioma' in combined.columns:
        combined['power_diff'] = combined['power_wahoo'] - combined['power_assioma']
        
        mean_w = combined['power_wahoo'].mean()
        mean_a = combined['power_assioma'].mean()
        corr = combined['power_wahoo'].corr(combined['power_assioma'])
        
        summary_stats.append({
            "Name": name,
            "Mean_Wahoo": mean_w,
            "Mean_Assioma": mean_a,
            "Diff_Mean": combined['power_diff'].mean(),
            "Diff_Std": combined['power_diff'].std(),
            "Correlation": corr,
            "N_Points": len(combined)
        })
        
        # Save processed csv
        combined.to_csv(os.path.join(OUTPUT_DIR, f"{name}_processed.csv"))
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(combined.index, combined['power_wahoo'], label='Wahoo')
        plt.plot(combined.index, combined['power_assioma'], label='Assioma', alpha=0.7)
        plt.title(f"Power Comparison - {name}")
        plt.ylabel("Power (W)")
        plt.legend()
        plt.savefig(os.path.join(FIGURES_DIR, f"{name}_power.png"))
        plt.close()
        
        # Bland-Altman
        plt.figure(figsize=(6, 6))
        means = (combined['power_wahoo'] + combined['power_assioma']) / 2
        diffs = combined['power_wahoo'] - combined['power_assioma']
        mean_diff = diffs.mean()
        std_diff = diffs.std()
        
        plt.scatter(means, diffs, alpha=0.5)
        plt.axhline(mean_diff, color='red', linestyle='--', label='Mean Diff')
        plt.axhline(mean_diff + 1.96*std_diff, color='gray', linestyle=':', label='+1.96 SD')
        plt.axhline(mean_diff - 1.96*std_diff, color='gray', linestyle=':', label='-1.96 SD')
        plt.title(f"Bland-Altman - {name}")
        plt.xlabel("Mean Power (W)")
        plt.ylabel("Difference (Wahoo - Assioma)")
        plt.legend()
        plt.savefig(os.path.join(FIGURES_DIR, f"{name}_bland_altman.png"))
        plt.close()

# Save summary stats
if summary_stats:
    res_df = pd.DataFrame(summary_stats)
    res_df.to_csv(os.path.join(OUTPUT_DIR, "summary_stats.csv"), index=False)
    print("\nSummary Stats:")
    print(res_df)
else:
    print("No summary stats generated.")
