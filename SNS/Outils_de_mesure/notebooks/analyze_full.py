import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats, signal

# ==========================================
# CONFIGURATION
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "rapport", "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)

# ==========================================
# FONCTIONS D'ANALYSE
# ==========================================

def load_all_processed_data():
    """Charge tous les fichiers CSV traités."""
    files = glob.glob(os.path.join(PROCESSED_DIR, "*_processed.csv"))
    data_dict = {}
    for f in files:
        name = os.path.basename(f).replace("_processed.csv", "")
        df = pd.read_csv(f)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
        data_dict[name] = df
    return data_dict

def detect_sprints(df, threshold=400, min_dist_sec=30):
    """Détecte les pics de puissance > threshold."""
    if df is None or len(df) == 0:
        return []
    
    # On utilise la puissance Assioma comme référence si dispo, sinon Wahoo
    # Mais ici on compare les deux, donc on prend la puissance Assioma pour la détection "référence"
    power_values = df['power_assioma'].fillna(0).values
    
    # Trouver les pics
    peaks, properties = signal.find_peaks(power_values, height=threshold, distance=min_dist_sec)
    
    sprint_data = []
    for p in peaks:
        # Fenêtre autour du pic (ex: -5s à +5s)
        start = max(0, p - 5)
        end = min(len(df), p + 5)
        
        subset = df.iloc[start:end]
        max_wahoo = subset['power_wahoo'].max()
        max_assioma = subset['power_assioma'].max()
        
        sprint_data.append({
            'timestamp': df.index[p],
            'max_wahoo': max_wahoo,
            'max_assioma': max_assioma
        })
        
    return pd.DataFrame(sprint_data)

def analyze_sprints(data_dict):
    """P3: Reproducibilité intra-individuelle des sprints."""
    print("--- Analyse des Sprints ---")
    
    all_sprints = []
    
    # On sait que SprintGrA et SprintGrB contiennent les sprints de plusieurs personnes
    # Mais on n'a pas l'ID sujet. 
    # HYPOTHÈSE: Les sprints sont groupés par 3.
    
    full_sprint_df = pd.DataFrame()
    
    # On regarde dans tous les fichiers, car certains individuels ont aussi des sprints
    for name, df in data_dict.items():
        sprints = detect_sprints(df, threshold=400) # Seuil 400W pour être large
        if len(sprints) > 0:
            sprints['source_file'] = name
            full_sprint_df = pd.concat([full_sprint_df, sprints])

    if len(full_sprint_df) == 0:
        print("Aucun sprint détecté.")
        return
    
    # Tri temporel pour essayer de grouper
    full_sprint_df.sort_values('timestamp', inplace=True)
    
    # On va essayer de calculer le CV par cluster de 3 sprints consécutifs
    # C'est une approximation faute de mieux (ID sujet manquant dans les fichiers groupés)
    
    # Pour les fichiers "SprintGr*", on suppose des blocs de 3
    # Pour les fichiers individuels (ex: Anton), on prend ses sprints à lui.
    
    cv_results = []
    
    for name in full_sprint_df['source_file'].unique():
        subset = full_sprint_df[full_sprint_df['source_file'] == name]
        
        # Si fichier de groupe, on découpe par 3
        if "SprintGr" in name:
            n_sprints = len(subset)
            n_subjects = n_sprints // 3
            
            for i in range(n_subjects):
                # Bloc de 3 sprints
                bloc = subset.iloc[i*3 : (i+1)*3]
                if len(bloc) < 3: continue
                
                mean_w = bloc['max_wahoo'].mean()
                std_w = bloc['max_wahoo'].std()
                cv_w = (std_w / mean_w) * 100 if mean_w > 0 else 0
                
                mean_a = bloc['max_assioma'].mean()
                std_a = bloc['max_assioma'].std()
                cv_a = (std_a / mean_a) * 100 if mean_a > 0 else 0
                
                cv_results.append({'Source': name, 'Subject_Idx': i, 'CV_Wahoo': cv_w, 'CV_Assioma': cv_a})
        else:
            # Fichier individuel
            if len(subset) >= 2:
                mean_w = subset['max_wahoo'].mean()
                std_w = subset['max_wahoo'].std()
                cv_w = (std_w / mean_w) * 100 if mean_w > 0 else 0
                
                mean_a = subset['max_assioma'].mean()
                std_a = subset['max_assioma'].std()
                cv_a = (std_a / mean_a) * 100 if mean_a > 0 else 0
                
                cv_results.append({'Source': name, 'Subject_Idx': 0, 'CV_Wahoo': cv_w, 'CV_Assioma': cv_a})

    cv_df = pd.DataFrame(cv_results)
    print(f"CV Moyen Wahoo (Sprints): {cv_df['CV_Wahoo'].mean():.2f}%")
    print(f"CV Moyen Assioma (Sprints): {cv_df['CV_Assioma'].mean():.2f}%")
    
    # Graphique CV (Boxplot) qui sera intégré au rapport
    plt.figure(figsize=(6, 5))
    sns.boxplot(data=cv_df[['CV_Wahoo', 'CV_Assioma']])
    plt.title('Comparaison de la Reproductibilité (CV %)')
    plt.ylabel('Coefficient de Variation (%)')
    plt.savefig(os.path.join(FIGURES_DIR, "sprint_cv_boxplot.png"))
    plt.close()
    
    return cv_df

def analyze_steady_state(data_dict):
    """P5: Fiabilité relative à 150W."""
    print("--- Analyse Steady State (150W) ---")
    
    cv_results = []
    
    for name, df in data_dict.items():
        if "Sprint" in name: continue # Ignorer les fichiers sprints purs
        
        # Filtre : Puissance autour de 150W (+/- 20W) pendant au moins 30s
        # On lisse pour éviter les pics
        df['power_smooth'] = df['power_wahoo'].rolling(10).mean()
        
        mask = (df['power_smooth'] > 130) & (df['power_smooth'] < 170)
        df_150 = df[mask]
        
        if len(df_150) > 30:
            # On considère ça comme un palier stable
            mean_w = df_150['power_wahoo'].mean()
            std_w = df_150['power_wahoo'].std()
            cv_w = (std_w / mean_w) * 100
            
            mean_a = df_150['power_assioma'].mean()
            std_a = df_150['power_assioma'].std()
            cv_a = (std_a / mean_a) * 100
            
            cv_results.append({'Source': name, 'CV_Wahoo_150': cv_w, 'CV_Assioma_150': cv_a})
            
    cv_df = pd.DataFrame(cv_results)
    if len(cv_df) > 0:
        print(f"CV Moyen Wahoo (150W): {cv_df['CV_Wahoo_150'].mean():.2f}%")
        print(f"CV Moyen Assioma (150W): {cv_df['CV_Assioma_150'].mean():.2f}%")
        return cv_df
    else:
        print("Aucun palier 150W détecté.")
        return pd.DataFrame()

def analyze_correlation_global(data_dict):
    """P4: Corrélation globale."""
    print("--- Analyse Corrélation Globale ---")
    
    frames = []
    for name, df in data_dict.items():
        frames.append(df[['power_wahoo', 'power_assioma', 'cadence_wahoo']])
    
    combined = pd.concat(frames)
    combined = combined[combined['power_assioma'] > 10] # Filtrer le bruit à 0
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(combined['power_assioma'], combined['power_wahoo'])
    
    print(f"Corrélation Globale (r): {r_value:.4f}")
    print(f"R²: {r_value**2:.4f}")
    print(f"Équation: y = {slope:.2f}x + {intercept:.2f}")
    
    # Plot
    plt.figure(figsize=(7, 7))
    plt.scatter(combined['power_assioma'], combined['power_wahoo'], alpha=0.1, s=2)
    
    # Ligne idéale
    max_val = max(combined['power_assioma'].max(), combined['power_wahoo'].max())
    plt.plot([0, max_val], [0, max_val], 'r--', label='Identité (y=x)')
    
    # Régression
    x_vals = np.array([0, max_val])
    plt.plot(x_vals, slope * x_vals + intercept, 'b-', label=f'Régression (r={r_value:.3f})')
    
    plt.xlabel('Puissance Assioma (W)')
    plt.ylabel('Puissance Wahoo (W)')
    plt.title('Corrélation Globale Wahoo vs Assioma')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig(os.path.join(FIGURES_DIR, "global_correlation.png"))
    plt.close()
    
    return combined

def analyze_bland_altman(combined_df):
    """P6: Bland-Altman."""
    print("--- Analyse Bland-Altman ---")
    
    combined_df['mean_p'] = (combined_df['power_wahoo'] + combined_df['power_assioma']) / 2
    combined_df['diff_p'] = combined_df['power_wahoo'] - combined_df['power_assioma'] # Bias = Wahoo - Assioma
    
    bias = combined_df['diff_p'].mean()
    sd_diff = combined_df['diff_p'].std()
    loa_upper = bias + 1.96 * sd_diff
    loa_lower = bias - 1.96 * sd_diff
    
    print(f"Biais Moyen: {bias:.2f} W")
    print(f"LoA Sup (+1.96 SD): {loa_upper:.2f} W")
    print(f"LoA Inf (-1.96 SD): {loa_lower:.2f} W")
    
    # Plot Bland-Altman
    plt.figure(figsize=(10, 6))
    
    # Colorer par cadence si possible (approximatif car variable continue)
    # On fait 2 groupes: < 80 rpm et >= 80 rpm
    mask_low = combined_df['cadence_wahoo'] < 80
    
    plt.scatter(combined_df.loc[mask_low, 'mean_p'], combined_df.loc[mask_low, 'diff_p'], 
                alpha=0.1, s=3, c='orange', label='< 80 rpm')
    plt.scatter(combined_df.loc[~mask_low, 'mean_p'], combined_df.loc[~mask_low, 'diff_p'], 
                alpha=0.1, s=3, c='blue', label='>= 80 rpm')
    
    plt.axhline(bias, color='black', linestyle='-', label=f'Biais ({bias:.1f} W)')
    plt.axhline(loa_upper, color='gray', linestyle='--', label=f'LoA ({loa_upper:.0f}/{loa_lower:.0f})')
    plt.axhline(loa_lower, color='gray', linestyle='--')
    plt.axhline(0, color='red', linewidth=1)
    
    plt.xlabel('Moyenne des 2 capteurs (W)')
    plt.ylabel('Différence (Wahoo - Assioma) [W]')
    plt.title('Graphique de Bland-Altman')
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(os.path.join(FIGURES_DIR, "bland_altman.png"))
    plt.close()

# ==========================================
# MAIN
# ==========================================
def main():
    data = load_all_processed_data()
    
    with open("results_final.txt", "w", encoding="utf-8") as f:
        # Redirection stdout
        import sys
        sys.stdout = f
        
        print(f"Chargé {len(data)} fichiers.")
        
        # 3. Sprints
        analyze_sprints(data)
        
        # 5. Steady State (Reliabilité Relative)
        analyze_steady_state(data)
        
        # 4. Correlation
        combined_df = analyze_correlation_global(data)
        
        # 6. Bland-Altman
        if combined_df is not None:
            analyze_bland_altman(combined_df)
            
        print("\nAnalyse terminée. Figures sauvegardées dans rapport/figures/")
        
    # Reset stdout
    sys.stdout = sys.__stdout__
    print("Résultats écrits dans results_final.txt")

if __name__ == "__main__":
    main()
