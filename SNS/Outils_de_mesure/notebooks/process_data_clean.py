import os
import glob
import zipfile
import fitdecode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy import signal

# ==========================================
# CONFIGURATION
# ==========================================
# Définir le répertoire de base par rapport à l'emplacement du script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

ASSIOMA_ZIP_DIR = os.path.join(DATA_DIR, "datas_Assioma")
ASSIOMA_UNZIPPED_DIR = os.path.join(DATA_DIR, "unzipped_Assioma")
WAHOO_DIR = os.path.join(DATA_DIR, "datas_Wahoo")
OUTPUT_DIR = os.path.join(DATA_DIR, "processed")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "rapport", "figures")

# Assurez-vous que les dossiers de sortie existent
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# ==========================================
# FONCTIONS UTILITAIRES
# ==========================================

def map_assioma_files():
    """
    Parcourt les fichiers ZIP Assioma pour associer les noms de fichiers .fit (ID)
    aux noms lisibles des athlètes (nom du zip).
    Retourne un dictionnaire {nom_fit: nom_athlete}.
    """
    mapping = {}
    zip_files = glob.glob(os.path.join(ASSIOMA_ZIP_DIR, "*.zip"))
    
    print(f"Analyse de {len(zip_files)} fichiers ZIP Assioma...")
    
    for zf_path in zip_files:
        # Le nom du zip est le nom de l'athlète (ex: Matys_70rpm.zip -> Matys_70rpm)
        athlete_name = os.path.basename(zf_path).replace(".zip", "")
        
        try:
            with zipfile.ZipFile(zf_path, 'r') as z:
                for filename in z.namelist():
                    if filename.endswith(".fit") and "ACTIVITY" in filename:
                        mapping[filename] = athlete_name
        except zipfile.BadZipFile:
            print(f"ATTENTION: Impossible de lire {zf_path}")

    # Ajouts manuels pour les cas connus (Sprints) si nécessaire
    # Ces IDs ont été identifiés précédemment pour les sprints
    # mapping["21556116585_ACTIVITY.fit"] = "SprintGrA" # Correspond à Sprints_Gr2
    # mapping["21553999314_ACTIVITY.fit"] = "SprintGrB" # Correspond à Sprints_Gr1
    
    return mapping

def parse_fit_file(path):
    """
    Lit un fichier .fit et retourne un DataFrame avec index temporel.
    Extrait uniquement la puissance et la cadence.
    Rééchantillonne à 1Hz pour uniformiser.
    """
    data = []
    
    if not os.path.exists(path):
        print(f"ERREUR: Fichier introuvable: {path}")
        return None

    try:
        with fitdecode.FitReader(path) as fit:
            for frame in fit:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA and frame.name == 'record':
                    fields = {f.name: f.value for f in frame.fields}
                    if 'timestamp' in fields and 'power' in fields:
                        data.append(fields)

    except Exception as e:
        print(f"ERREUR lors de la lecture de {path}: {e}")
        return None
    
    if not data:
        return None
        
    df = pd.DataFrame(data)
    
    # Conversion du timestamp
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        df.set_index('timestamp', inplace=True)
    
    # Sélection des colonnes utiles
    cols_to_keep = ['power', 'cadence']
    existing_cols = [c for c in cols_to_keep if c in df.columns]
    df = df[existing_cols]
    
    # Rééchantillonnage à 1 seconde (moyenne)
    df = df.resample('1s').mean()
    
    # Nettoyage des NaN sur la puissance (remplacer par 0 ou interpolation selon contexte, ici 0 est sûr pour les pauses)
    df['power'] = df['power'].fillna(0)
    
    return df

def synchronize_signals(wahoo_df, assioma_df):
    """
    Synchronise deux DataFrames de puissance en utilisant les timestamps
    pour un alignement grossier, puis la corrélation croisée pour l'ajustement fin.
    """
    # 1. Création d'une grille temporelle commune
    t_min = min(wahoo_df.index[0], assioma_df.index[0])
    t_max = max(wahoo_df.index[-1], assioma_df.index[-1])
    
    # Création de l'index complet (1s)
    full_idx = pd.date_range(start=t_min, end=t_max, freq='1s')
    
    # Réindexation pour aligner temporellement (remplissage des trous par 0)
    w_aligned = wahoo_df.reindex(full_idx, fill_value=0)
    a_aligned = assioma_df.reindex(full_idx, fill_value=0)
    
    # Extraction des numpy arrays pour corrélation
    p1 = w_aligned['power'].fillna(0).values
    p2 = a_aligned['power'].fillna(0).values
    
    # Normalisation
    p1_norm = (p1 - np.mean(p1)) / (np.std(p1) + 1e-6)
    p2_norm = (p2 - np.mean(p2)) / (np.std(p2) + 1e-6)
    
    # Corrélation croisée
    correlation = signal.correlate(p1_norm, p2_norm, mode='full')
    lags = signal.correlation_lags(len(p1_norm), len(p2_norm), mode='full')
    lag = lags[np.argmax(correlation)]
    
    print(f"  -> Décalage fin détecté : {lag} secondes")
    
    # Si le lag est trop important (> 60s), c'est suspect quand on a déjà aligné par timestamp
    # Sauf si les horloges sont déréglées. 
    # Pour les fichiers 70rpm, le timestamp semble OK (juste décalé en contenu), donc le lag devrait être proche de 0
    # car on a aligné les 0 avec les 0.
    
    # Application du décalage à Assioma (sur les données d'origine)
    assioma_shifted = assioma_df.copy()
    assioma_shifted.index = assioma_df.index + pd.Timedelta(seconds=int(lag))
    
    # Renommage
    wahoo_final = wahoo_df.rename(columns={'power': 'power_wahoo', 'cadence': 'cadence_wahoo'})
    assioma_final = assioma_shifted.rename(columns={'power': 'power_assioma', 'cadence': 'cadence_assioma'})
    
    # Fusion finale
    combined = pd.merge_asof(
        wahoo_final.sort_index(), 
        assioma_final.sort_index(), 
        left_index=True, 
        right_index=True, 
        direction='nearest', 
        tolerance=pd.Timedelta('1s')
    )
    
    combined = combined.dropna(subset=['power_wahoo', 'power_assioma'])
    
    return combined

def find_pairs(assioma_mapping):
    """
    Identifie les paires de fichiers Wahoo et Assioma correspondantes.
    Retourne une liste de dictionnaires.
    """
    pairs = []
    wahoo_files = glob.glob(os.path.join(WAHOO_DIR, "*.fit"))
    
    print(f"Recherche de correspondances parmi {len(wahoo_files)} fichiers Wahoo...")
    
    for w_path in wahoo_files:
        w_filename = os.path.basename(w_path)
        
        # Format Wahoo attendu: YYYY-MM-DD-HHMMSS-Nom_RPM.fit
        # On extrait la partie après le dernier tiret qui contient le nom
        parts = w_filename.split('-')
        
        candidate_name = ""
        if len(parts) >= 4:
            # Prend tout après le timestamp (partie date + heure = 3 parties si séparées par -)
            # Ex: 2026-01-15-093049-Matys_70rpm.fit -> Matys_70rpm
            # Attention, parfois le nom contient des tirets ? 
            # Le format semble être DATE-HEURE-NOM.fit
            candidate_name = parts[-1].replace(".fit", "")
        else:
            candidate_name = w_filename.replace(".fit", "")
            
        # Logique de correspondance
        match_id = None
        
        # 1. Cas Spéciaux (Sprints)
        if "SprintGrA" in candidate_name:
            # SprintGrA correspond à Sprints_Gr2 -> 21556116585
            match_id = "21556116585_ACTIVITY.fit"
        elif "SprintGrB" in candidate_name:
            # SprintGrB correspond à Sprints_Gr1 -> 21553999314
            match_id = "21553999314_ACTIVITY.fit"
        
        # 2. Recherche par nom dans le mapping Assioma
        if not match_id:
            # Essai correspondance exacte du nom mapped
            for fit_id, mapped_name in assioma_mapping.items():
                if mapped_name == candidate_name:
                    match_id = fit_id
                    break
        
        # 3. Recherche par inclusion (ex: Matys dans Matys_70rpm)
        if not match_id:
            for fit_id, mapped_name in assioma_mapping.items():
                if mapped_name in candidate_name or candidate_name in mapped_name:
                    match_id = fit_id
                    break

        if match_id:
            # Vérifier si le fichier Assioma existe
            a_path = os.path.join(ASSIOMA_UNZIPPED_DIR, match_id)
            if os.path.exists(a_path):
                pairs.append({
                    "name": candidate_name,
                    "wahoo_path": w_path,
                    "assioma_path": a_path
                })
            else:
                print(f"  ATTENTION: Correspondance trouvée pour {candidate_name} ({match_id}) mais fichier Assioma manquant (Chemin: {a_path}).")
        else:
            print(f"  PERDU: Pas de correspondance Assioma trouvée pour {candidate_name}")
            
    return pairs

def unzip_assioma_files():
    """
    Extrait les fichiers .fit des archives ZIP Assioma vers le dossier dézippé
    si les fichiers n'existent pas déjà.
    """
    print(f"Vérification des fichiers dézippés dans {ASSIOMA_UNZIPPED_DIR}...")
    
    if not os.path.exists(ASSIOMA_UNZIPPED_DIR):
        os.makedirs(ASSIOMA_UNZIPPED_DIR)
        
    zip_files = glob.glob(os.path.join(ASSIOMA_ZIP_DIR, "*.zip"))
    count_extracted = 0
    
    for zf_path in zip_files:
        try:
            with zipfile.ZipFile(zf_path, 'r') as z:
                for file_info in z.infolist():
                    if file_info.filename.endswith(".fit") and "ACTIVITY" in file_info.filename:
                        # Chemin cible
                        target_path = os.path.join(ASSIOMA_UNZIPPED_DIR, file_info.filename)
                        
                        # On extrait seulement si le fichier n'existe pas ou taille différente
                        if not os.path.exists(target_path) or os.path.getsize(target_path) != file_info.file_size:
                            z.extract(file_info, ASSIOMA_UNZIPPED_DIR)
                            count_extracted += 1
        except zipfile.BadZipFile:
            print(f"ATTENTION: Impossible de lire l'archive {zf_path}")
            
    if count_extracted > 0:
        print(f"-> {count_extracted} fichiers Assioma extraits.")
    else:
        print("-> Tous les fichiers Assioma sont déjà extraits.")


# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    print("=== DÉBUT DU TRAITEMENT DES DONNÉES CYCLISME ===")
    
    try:
        # 0. Dézipper les fichiers Assioma si nécessaire
        unzip_assioma_files()

        # 1. Créer le mapping Assioma
        assioma_map = map_assioma_files()
        print(f"Mapping Assioma: {len(assioma_map)} fichiers trouvés.")
        
        # 2. Trouver les paires
        pairs = find_pairs(assioma_map)
        print(f"--> {len(pairs)} paires valides identifiées.\n")
        
        summary_stats = []
        
        # 3. Traiter chaque paire
        for pair in pairs:
            name = pair['name']
            print(f"Traitement de : {name}")
            
            # Chargement
            df_w = parse_fit_file(pair['wahoo_path'])
            df_a = parse_fit_file(pair['assioma_path'])
            
            if df_w is None or df_a is None:
                print("  -> Échec du chargement des fichiers.")
                continue
                
            # Vérification des dates de début
            t_w = df_w.index[0]
            t_a = df_a.index[0]
            delta_start = abs((t_w - t_a).total_seconds())
            
            print(f"  Start Wahoo: {t_w}")
            print(f"  Start Assioma: {t_a}")
            print(f"  Écart temporel initial: {delta_start:.2f} secondes")
            
            if delta_start > 3600: # Plus d'une heure d'écart
                print(f"  -> ALERTE: Écart de temps important détecté ({delta_start/3600:.1f} heures). Vérifiez l'appariement !")
            
            print(f"  Points Wahoo: {len(df_w)}, Points Assioma: {len(df_a)}")
            
            # Synchronisation
            combined = synchronize_signals(df_w, df_a)
            
            if len(combined) < 10:
                print("  -> ATTENTION: Trop peu de points communs après synchro.")
                continue
                
            # Calcul des différences
            combined['power_diff'] = combined['power_wahoo'] - combined['power_assioma']
            mean_diff = combined['power_diff'].mean()
            std_diff = combined['power_diff'].std()
            correlation = combined['power_wahoo'].corr(combined['power_assioma'])
            
            print(f"  -> Diff Moy: {mean_diff:.2f} W, Corr: {correlation:.4f}")
            
            # Sauvegarde CSV
            output_file = os.path.join(OUTPUT_DIR, f"{name}_processed.csv")
            combined.to_csv(output_file)
            print(f"  -> Sauvegardé: {output_file}")
            
            # Ajout aux stats
            summary_stats.append({
                "Athlete": name,
                "Mean_Wahoo": combined['power_wahoo'].mean(),
                "Mean_Assioma": combined['power_assioma'].mean(),
                "Diff_Mean": mean_diff,
                "Diff_Std": std_diff,
                "Correlation": correlation,
                "N_Points": len(combined)
            })
            
            # Graphique Rapide (Vérification)
            plt.figure(figsize=(10, 6)) # Un peu plus petit pour le rapport
            plt.plot(combined.index, combined['power_wahoo'], label='Wahoo', alpha=0.8, linewidth=1)
            plt.plot(combined.index, combined['power_assioma'], label='Assioma', alpha=0.6, linewidth=1)
            plt.title(f"Comparaison Puissance - {name} (Corr: {correlation:.2f})")
            plt.ylabel("Puissance (W)")
            plt.xlabel("Temps")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Sauvegarde en .png
            graph_filename = f"{name}_graph.png"
            dest_fig = os.path.join(FIGURES_DIR, graph_filename)
            plt.savefig(dest_fig, dpi=100)
            plt.close()
            print(f"  -> Figure sauvegardée: {dest_fig}")

        # 4. Sauvegarder le résumé global et générer le rapport MD
        if summary_stats:
            summary_df = pd.DataFrame(summary_stats)
            summary_path = os.path.join(OUTPUT_DIR, "summary_stats_clean.csv")
            summary_df.to_csv(summary_path, index=False)
            
            print("\n=== RÉSUMÉ DES STATISTIQUES ===")
            print(summary_df.to_string(columns=['Athlete', 'Diff_Mean', 'Correlation']))
            
            # Génération du Rapport Markdown
            report_path = os.path.join(PROJECT_ROOT, "rapport", "rapport_analyse.md")
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"# Rapport d'Analyse - Comparaison Capteurs\n\n")
                f.write(f"**Date de génération** : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                
                f.write("## 1. Résumé Global\n\n")
                # Conversion du DataFrame en Markdown
                f.write(summary_df[['Athlete', 'Mean_Wahoo', 'Mean_Assioma', 'Diff_Mean', 'Correlation']].round(2).to_markdown(index=False))
                f.write("\n\n")
                
                f.write("## 2. Détail par Athlète\n\n")
                for stat in summary_stats:
                    athlete = stat['Athlete']
                    corr = stat['Correlation']
                    diff = stat['Diff_Mean']
                    
                    f.write(f"### {athlete}\n\n")
                    f.write(f"- **Corrélation** : {corr:.4f}\n")
                    f.write(f"- **Différence Moyenne** : {diff:.2f} W\n\n")
                    
                    # Chemin relatif pour l'image dans le MD
                    img_rel_path = f"figures/{athlete}_graph.png"
                    f.write(f"![Graphique {athlete}]({img_rel_path})\n\n")
                    f.write("---\n\n")
            
            print(f"\n[SUCCÈS] Rapport généré : {report_path}")
        else:
            print("\nAucune donnée traitée.")
            
    except Exception as e:
        print(f"ERREUR CRITIQUE: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
