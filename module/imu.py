# ------- IMPORTS ---------
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D



# ------- LECTURE DES FICHIERS ---------
def read_imu_file (filename):

    data = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if line == "":
                continue

            obj = json.loads (line)

            time = obj["time"]
            index = obj["index"]
            frame = obj["frame"][0]

            data.append ({

                "time": time,
                "index": index,

                "timestamp_ms": frame ["timestamp"],

                "accelerometre_x": frame ["accelerometer"]["x"],
                "accelerometre_y": frame ["accelerometer"]["y"],
                "accelerometre_z": frame ["accelerometer"]["z"],

                "gyroscope_x": frame ["gyroscope"]["x"],
                "gyroscope_y": frame ["gyroscope"]["y"],
                "gyroscope_z": frame ["gyroscope"]["z"],

                "magnetometre_x": frame ["magnetometer"]["x"],
                "magnetometre_y": frame ["magnetometer"]["y"],
                "magnetometre_z": frame ["magnetometer"]["z"],

                "accelerometre_freq": frame ["accelerometer"]["frequency"],
                "gyroscope_freq": frame ["gyroscope"]["frequency"],
                "magnetometre_freq": frame ["magnetometer"]["frequency"],


            })

    df = pd.DataFrame(data)
    df = df.sort_values("time")
    df = df.drop_duplicates(subset="time")

    return df



#--------------- AFFICHAGE IMU -------------------
def plot_imu (data_frame, source_name, capteur_type):

    plt.figure(figsize=(9, 4))

    plt.plot(
        data_frame["time"],
        data_frame[f"{capteur_type}_x"],
        label=f"{capteur_type}_x",
        color="darkorange",
        alpha=1
    )


    plt.plot(
        data_frame["time"],
        data_frame[f"{capteur_type}_y"],
        label=f"{capteur_type}_y",
        color="limegreen",
        alpha=1
    )


    plt.plot(
        data_frame["time"],
        data_frame[f"{capteur_type}_z"],
        label=f"{capteur_type}_z",
        color="deepskyblue",
        alpha=1
    )


    plt.xlabel("Temps (s)")

    if capteur_type == "acc":

        plt.ylim(-30, 30)
        plt.ylabel("Accélération (m/s^2)")
        plt.title(f"Accéléromètre {source_name}")

    elif capteur_type == "gyro":
        plt.ylim(-20, 20)
        plt.ylabel("Vitesse de rotation (rad/s)")
        plt.title(f"Gyroscope {source_name}")

    elif capteur_type == "mag":
        plt.ylabel("Champs magnétiques (µT)")
        plt.title(f" Magnétometre {source_name}")


    plt.legend()
    plt.grid(True)
    plt.show()




# --- Sélectionne une portion temporelle d'un DataFrame ---
def select_time_window(
        t_debut, # Début de la fenêtre en secondes
        duree,    #Durée de la fenêtre en secondes
        data_frame_lsm9ds1= None, # DataFrame contenant la colonne "time"
        data_frame_comote = None,
        data_frame_riot = None
):

    # Calcul du temps de fin
    t_fin = t_debut + duree


    # ----- Fenetrage -------------
    data_frames = {
        "lsm9ds1": data_frame_lsm9ds1,
        "comote": data_frame_comote,
        "riot": data_frame_riot
    }


    # Suppression des sources non fournies
    data_frames = {
        source_name: data_frame
        for source_name, data_frame in data_frames.items()
        if data_frame is not None
    }

    if not data_frames:
        raise ValueError("Aucun DataFrame n'a été fourni.")


    data_frames_window = {}

    for source_name, data_frame in data_frames.items():


        data_frame_window = data_frame[
            (data_frame["time"] >= t_debut) &
            (data_frame["time"] < t_fin)
        ].copy()

        data_frame_window = (data_frame_window.reset_index(drop=True))

        if len(data_frame_window) < 2:
            raise ValueError(
                f"La fenêtre temporelle du fichier "
                f"{source_name} sélectionnée ne contient "
                f"pas assez de données."
            )

        data_frames_window[source_name] = data_frame_window



    # ---------------- Infos Fenetrage ---------------
    print("--------- Fenêtre temporelle ---------")
    print(f"Temps demandé : {t_debut:.3f} s à {t_fin:.3f} s")
    print(f"Durée demandée : {duree:.3f} s")

    for source_name, data_frame_window in data_frames_window.items():
        print(f"\n--------- {source_name.upper()} ---------")
        print(
            f"Premier point réel : "
            f"{data_frame_window['time'].iloc[0]:.3f} s"
        )

        print(
            f"Dernier point réel : "
            f"{data_frame_window['time'].iloc[-1]:.3f} s"
        )

        print(
            f"Nombre d'échantillons : "
            f"{len(data_frame_window)}"

        )

    print("--------------------------------------\n")

    return data_frames_window




#-------------- PLOT ZOOM POINTS TEMPOREL --------------
def plot_pas_temporel_same_sensor(
        dataframe,
        capteur_type,
        t_debut,
        duree_fenetre=0.1
):


    t_fin = t_debut + duree_fenetre

    data_frame_zoom = dataframe[
        (dataframe["time"] >= t_debut) &
        (dataframe["time"] <= t_fin)
    ]


    plt.plot(
        data_frame_zoom["time"],
        data_frame_zoom[f"{capteur_type}_x"],
        "o",
        markersize=8,
        label=f"{capteur_type}_x",
    )

    plt.plot(
        data_frame_zoom["time"],
        data_frame_zoom[f"{capteur_type}_y"],
        "x",
        markersize=9,
        label=f"{capteur_type}_y"
    )


    plt.plot(
        data_frame_zoom["time"],
        data_frame_zoom[f"{capteur_type}_z"],
        "D",
        markersize=8,
        label=f"{capteur_type}_z"
    )



    # Ligne verticale pour chaque échantillon LSM9DS1
    for t in data_frame_zoom["time"]:
        plt.axvline(
            t,
            linestyle=":",
            alpha=0.25
        )



    plt.xlabel("Temps (s)")
    plt.ylabel(capteur_type)
    plt.title(f"Instants d'échantillonnage bruts — {capteur_type}")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()




#-------------- PLOT ZOOM POINTS TEMPOREL --------------
def plot_pas_temporel(
        df_lsm9ds1,
        df_comote,
        df_riot,
        capteur_type,
        axe,
        t_debut,
        duree_fenetre=0.1
):


    col = f"{capteur_type}_{axe}"
    t_fin = t_debut + duree_fenetre

    lsm_zoom = df_lsm9ds1[
        (df_lsm9ds1["time"] >= t_debut) &
        (df_lsm9ds1["time"] <= t_fin)
    ]

    comote_zoom = df_comote[
        (df_comote["time"] >= t_debut) &
        (df_comote["time"] <= t_fin)
    ]

    riot_zoom = df_riot[
        (df_riot["time"] >= t_debut) &
        (df_riot["time"] <= t_fin)
        ]


    fig, ax = plt.subplots(figsize=(11, 4.5))

    # Points du LSM9DS1
    ax.plot(
        lsm_zoom["time"],
        lsm_zoom[col],
        linestyle="none",
        marker="o",
        markersize=8,
        color="cornflowerblue",
        alpha=1
    )

    # Points de CoMote
    ax.plot(
        comote_zoom["time"],
        comote_zoom[col],
        linestyle="none",
        marker="x",
        markersize=9,
        color="orange",
        alpha=1
    )

    # Points du R-IoT
    ax.plot(
        riot_zoom["time"],
        riot_zoom[col],
        linestyle="none",
        marker="D",
        markersize=8,
        color="mediumseagreen",
        alpha=1
    )

    # Lignes verticales du LSM9DS1
    for t in lsm_zoom["time"]:
        ax.axvline(
            t,
            linestyle=":",
            color="cornflowerblue",
            alpha=0.6
        )

    # Lignes verticales de CoMote
    for t in comote_zoom["time"]:
        ax.axvline(
            t,
            linestyle="--",
            color="orange",
            alpha=0.6
        )

    # Lignes verticales du R-IoT
    for t in riot_zoom["time"]:
        ax.axvline(
            t,
            linestyle="--",
            color="mediumseagreen",
            alpha=0.6
        )

    # Éléments personnalisés de la légende
    elements_legende = [
        Line2D(
            [0], [0],
            color="cornflowerblue",
            linestyle=":",
            linewidth=1.5,
            marker="o",
            markersize=8,
            label="LSM9DS1"
        ),
        Line2D(
            [0], [0],
            color="orange",
            linestyle="--",
            linewidth=1.5,
            marker="x",
            markersize=9,
            label="CoMote"
        ),
        Line2D(
            [0], [0],
            color="mediumseagreen",
            linestyle="--",
            linewidth=1.5,
            marker="D",
            markersize=8,
            label="R-IoT"
        )
    ]

    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Gyrosocpe - Axe X (rad/s)")
    ax.set_title(
        f"Échantillons bruts acquis par les trois sources de mouvement \n sur une fenêtre temporelle de 15ms",
        pad=20
    )
    ax.grid(True, alpha=0.3)




    # Légende placée à droite du graphique
    ax.legend(
        handles=elements_legende,
        title="Sources",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0
    )

    # Réserve de l’espace à droite pour la légende
    fig.tight_layout()
    fig.subplots_adjust(right=0.78)

    plt.show()





#-------------- CALCUL DE DONNÉES --------------
def calcul_frequence_brute (df_lsm9ds1, df_comote, df_riot):

    # ----------- LSM9DS1 -----------
    period_lsm = df_lsm9ds1["time"].diff()
    period_lsm = period_lsm.dropna()
    period_lsm = period_lsm[period_lsm > 0]

    freq_moy_lsm = 1 / np.mean(period_lsm)
    freq_median_lsm = 1 / np.median(period_lsm)

    print(" ------- LSM9DS1  ----------")
    print(f"Période moyenne : {np.mean(period_lsm * 1000):.3f} ms")
    print(f"Fréquence moyenne : {freq_moy_lsm:.3f} Hz")
    print(f"Période min : {np.min(period_lsm * 1000):.3f} ms")
    print(f"Période max : {np.max(period_lsm * 1000):.3f} ms")
    print("\n")

    #print(f"Période médiane : {np.median(period_lsm * 1000):.3f} ms")
    print(f"Fréquence médiane : {freq_median_lsm:.3f} Hz")
    print("\n")


    # --------------- CoMote ------------
    period_comote = df_comote["time"].diff()
    period_comote = period_comote.dropna()
    period_comote = period_comote[period_comote > 0]

    freq_moy_comote = 1 / np.mean(period_comote)
    freq_median_comote = 1 / np.median(period_comote)


    print(" --------- CoMote ----------")
    print(f"Période moyenne : {np.mean(period_comote * 1000):.3f} ms")
    print(f"Fréquence moyenne : {freq_moy_comote:.3f} Hz")
    print(f"Période min : {np.min(period_comote * 1000):.3f} ms")
    print(f"Période max : {np.max(period_comote * 1000):.3f} ms")
    print("\n")

    #print(f"Période médiane : {np.median(period_comote * 1000):.3f} ms")
    print(f"Fréquence médiane : {freq_median_comote:.3f} Hz")
    print("\n")


    # ------------- R-IoT -----------
    period_riot = df_riot["time"].diff()
    period_riot = period_riot.dropna()
    period_riot = period_riot[period_riot > 0]


    freq_moy_riot = 1 / np.mean(period_riot)
    freq_median_riot = 1 / np.median(period_riot)

    print(" --------- R-IoT ----------")
    print(f"Période moyenne : {np.mean(period_riot * 1000):.3f} ms")
    print(f"Fréquence moyenne : {freq_moy_riot:.3f} Hz")
    print(f"Période min : {np.min(period_riot * 1000):.3f} ms")
    print(f"Période max : {np.max(period_riot * 1000):.3f} ms")
    print("\n")

    #print(f"Période médiane : {np.median(period_riot * 1000):.3f} ms")
    print(f"Fréquence médiane : {freq_median_riot:.3f} Hz")
    print("\n")



#--------------- INTERPOLATION LINEAIRE ----------------
def interpolation_lineaire(df_lsm9ds1, df_comote, df_riot):

    # Fenêtre temporelle commune
    t_start = max(
            df_lsm9ds1["time"].min(),
            df_comote["time"].min(),
            df_riot["time"].min()

    ) # En seconde

    t_end = min(
        df_lsm9ds1["time"].max(),
        df_comote["time"].max(),
        df_riot["time"].max()
)

    # Vérification qu'une fenêtre commune existe
    if t_start >= t_end:
        raise ValueError(
            "Les trois enregistrements n'ont pas de fenêtre temporelle commune."
        )



    # Filtrage sur la fenêtre commune
    df_lsm9ds1_overlap = df_lsm9ds1[
        (df_lsm9ds1["time"] >= t_start) &
        (df_lsm9ds1["time"] <= t_end)
    ].copy()

    df_comote_overlap = df_comote[
        (df_comote["time"] >= t_start) &
        (df_comote["time"] <= t_end)
    ].copy()


    df_riot_overlap = df_riot[
        (df_riot["time"] >= t_start) &
        (df_riot["time"] <= t_end)
        ].copy()


    # Caclul des fréquences moyennes
    dt_lsm9ds1 = df_lsm9ds1_overlap["time"].diff().dropna()
    dt_comote = df_comote_overlap["time"].diff().dropna()
    dt_riot = df_riot_overlap["time"].diff().dropna()

    # On conserve seulement les pas strictement positifs
    dt_lsm9ds1 = dt_lsm9ds1[dt_lsm9ds1 > 0]
    dt_comote = dt_comote[dt_comote > 0]
    dt_riot = dt_riot[dt_riot > 0]

    if dt_lsm9ds1.empty or dt_comote.empty or dt_riot.empty:
        raise ValueError("Au moins un DataFrame ne contient pas assez de points temporels valides.")


    freq_moy_lsm9ds1 = 1 / dt_lsm9ds1.mean()
    freq_moy_comote = 1 / dt_comote.mean()
    freq_moy_riot = 1 / dt_riot.mean()


    print("---------------- Données Interpolation ---------------------- \n")

    print(f"Time Start : {t_start:.6f} s")
    print(f"Time End   : {t_end:.6f} s")
    print()

    print(f"Fréquence moyenne LSM9DS1 : {freq_moy_lsm9ds1:.3f} Hz")
    print(f"Fréquence moyenne CoMote  : {freq_moy_comote:.3f} Hz")
    print(f"Fréquence moyenne R-IoT   : {freq_moy_riot:.3f} Hz")


    # -------- Construction de la grille temporelle commune -------

    # Fréquence la plus faible des trois capteurs
    freq_cible = min(
        freq_moy_lsm9ds1,
        freq_moy_comote,
        freq_moy_riot
    )

    dt_cible = 1 / freq_cible

    t_common = np.arange(
        t_start,
        t_end,
        dt_cible
    )

    print(f"\nFréquence cible : {freq_cible:.3f} Hz")
    print(f"Pas temporel cible : {dt_cible * 1000:.3f} ms")



    # Colonnes à interpoler
    cols = ["accelerometre_x", "accelerometre_y", "accelerometre_z",
            "gyroscope_x", "gyroscope_y", "gyroscope_z",
            "magnetometre_x", "magnetometre_y", "magnetometre_z"]


    # Interpolation linéaire
    df_lsm9ds1_interp = pd.DataFrame({"time": t_common})
    df_comote_interp  = pd.DataFrame({"time": t_common})
    df_riot_interp = pd.DataFrame({"time": t_common})

    for col in cols:
        df_lsm9ds1_interp[col] = np.interp(
            t_common,
            df_lsm9ds1_overlap["time"].to_numpy(),
            df_lsm9ds1_overlap[col].to_numpy()
        )


        df_comote_interp[col] = np.interp(
            t_common,
            df_comote_overlap["time"].to_numpy(),
            df_comote_overlap[col].to_numpy()
        )

        df_riot_interp[col] = np.interp(
            t_common,
            df_riot_overlap["time"].to_numpy(),
            df_riot_overlap[col].to_numpy()
        )

    print("\n")
    print(f"Nombre de points après interpolation : {len(t_common)}")

    return (
        df_lsm9ds1_interp,
        df_comote_interp,
        df_riot_interp
    )



#------------- CALCUL ERREUR -------------



def calcul_erreurs_inertielles(
    df_lsm9ds1,
    df_riot,
    df_comote,
    capteurs_types=("accelerometre", "gyroscope"),
    axes=("x", "y", "z"),
    unites=None
):
    """
    Calcule les erreurs entre trois sources de mouvement.

    Comparaisons réalisées :
        1. LSM9DS1 - CoMote
        2. LSM9DS1 - R-IoT
        3. R-IoT - CoMote

    Pour chaque comparaison, les erreurs sont calculées :
        - pour chaque type de capteur ;
        - pour les axes x, y et z.

    Les colonnes des DataFrames doivent être nommées selon
    le format suivant :

        <capteur_type>_<axe>

    Par exemple :
        accelerometre_x
        accelerometre_y
        accelerometre_z
        gyroscope_x
        gyroscope_y
        gyroscope_z

    Les trois DataFrames doivent avoir été interpolés sur la
    même grille temporelle et posséder des index compatibles.

    Paramètres
    ----------
    df_lsm9ds1, df_riot, df_comote : pandas.DataFrame
        Données interpolées des trois sources.

    capteurs_types : tuple ou liste de str
        Préfixes utilisés pour identifier les colonnes des
        capteurs.

    axes : tuple ou liste de str
        Axes à comparer.

    unites : dict, optionnel
        Unité associée à chaque type de capteur.

        Exemple :
            {
                "accelerometre": "m/s²",
                "gyroscope": "rad/s"
            }

    Retour
    ------
    tableau_resultats : pandas.DataFrame
        Tableau contenant une ligne par combinaison :
        comparaison, capteur et axe.
    """

    if unites is None:
        unites = {
            "accelerometre": "m/s²",
            "gyroscope": "rad/s"
        }

    sources = {
        "LSM9DS1": df_lsm9ds1,
        "R-IoT": df_riot,
        "CoMote": df_comote
    }

    # L’ordre de la soustraction est important.
    comparaisons = [
        ("LSM9DS1", "CoMote"),
        ("LSM9DS1", "R-IoT"),
        ("R-IoT", "CoMote")
    ]

    # --------------------------------------------------
    # Vérification des colonnes
    # --------------------------------------------------

    colonnes_manquantes = []

    for source_name, data_frame in sources.items():

        for capteur_type in capteurs_types:

            for axe in axes:

                colonne = f"{capteur_type}_{axe}"

                if colonne not in data_frame.columns:
                    colonnes_manquantes.append(
                        f"{source_name} : {colonne}"
                    )

    if colonnes_manquantes:
        message = "\n".join(colonnes_manquantes)

        raise ValueError(
            "Certaines colonnes sont manquantes :\n"
            f"{message}"
        )

    # --------------------------------------------------
    # Calcul des erreurs
    # --------------------------------------------------

    resultats = []

    for source_1, source_2 in comparaisons:

        df_1 = sources[source_1]
        df_2 = sources[source_2]

        nom_comparaison = (
            f"{source_1} - {source_2}"
        )

        for capteur_type in capteurs_types:

            for axe in axes:

                colonne = f"{capteur_type}_{axe}"

                # Conversion en données numériques
                valeurs_1 = pd.to_numeric(
                    df_1[colonne],
                    errors="coerce"
                )

                valeurs_2 = pd.to_numeric(
                    df_2[colonne],
                    errors="coerce"
                )

                # Alignement sur les index communs
                valeurs_1, valeurs_2 = valeurs_1.align(
                    valeurs_2,
                    join="inner"
                )

                # Suppression des lignes contenant un NaN
                valeurs_valides = pd.DataFrame({
                    "source_1": valeurs_1,
                    "source_2": valeurs_2
                }).dropna()

                if valeurs_valides.empty:
                    print(
                        "Aucune donnée commune pour "
                        f"{nom_comparaison}, "
                        f"{capteur_type}, axe {axe}."
                    )
                    continue

                # Erreur signée :
                # première source moins deuxième source
                erreur = (
                    valeurs_valides["source_1"]
                    - valeurs_valides["source_2"]
                )

                # Indicateurs
                erreur_moyenne = erreur.mean()

                mae = erreur.abs().mean()

                rmse = np.sqrt(np.mean(np.square(erreur)))

                erreur_minimale = erreur.min()
                erreur_maximale = erreur.max()

                erreur_absolue_maximale = (
                    erreur.abs().max()
                )

                ecart_type = erreur.std()

                resultats.append({
                    "Comparaison": nom_comparaison,
                    "Source 1": source_1,
                    "Source 2": source_2,
                    "Capteur": capteur_type,
                    "Axe": axe.upper(),

                    "Unité": unites.get(
                        capteur_type,
                        ""
                    ),

                    #"Nombre de valeurs": len(erreur),

                    # Biais signé
                    "Erreur moyenne": erreur_moyenne,

                    # Erreur absolue moyenne
                    "MAE": mae,

                    # Racine de l'erreur quadratique moyenne
                    "RMSE": rmse,

                    # Dispersion de l'erreur
                    #"Écart-type": ecart_type,

                    # Valeurs extrêmes signées
                    #"Erreur minimale": erreur_minimale,
                    #"Erreur maximale": erreur_maximale,

                    # Plus grand écart sans considérer le signe
                    "Erreur absolue maximale": erreur_absolue_maximale
                })

    # --------------------------------------------------
    # Construction et classement du tableau
    # --------------------------------------------------

    tableau_resultats = pd.DataFrame(resultats)

    ordre_comparaisons = [
        "LSM9DS1 - CoMote",
        "LSM9DS1 - R-IoT",
        "R-IoT - CoMote"
    ]

    tableau_resultats["Comparaison"] = pd.Categorical(
        tableau_resultats["Comparaison"],
        categories=ordre_comparaisons,
        ordered=True
    )

    tableau_resultats["Capteur"] = pd.Categorical(
        tableau_resultats["Capteur"],
        categories=list(capteurs_types),
        ordered=True
    )

    tableau_resultats["Axe"] = pd.Categorical(
        tableau_resultats["Axe"],
        categories=[
            axe.upper()
            for axe in axes
        ],
        ordered=True
    )

    tableau_resultats = tableau_resultats.sort_values(
        by=[
            "Comparaison",
            "Capteur",
            "Axe"
        ]
    ).reset_index(drop=True)

    return tableau_resultats



#-------------- AFFICHAGE ERREUR ET DONNEES ----------------
def plot_imu_err (df_lsm9ds1_final, df_comote_sync, capteur_type, axe):


    # ---------------- Affichage des données -------------------
    plt.close("all")
    col = f"{capteur_type}_{axe}"

    print("\n")

    print ("---------------- Valeurs Interpolés ----------------------\n")

    print("------ LSM9DS1 ------\n")
    print(df_lsm9ds1_final[["time", col]].head(10))

    print("\n")

    print("------ CoMote ------\n")
    print(df_comote_sync[["time", col]].head(10))

    print("\n")

    diff = df_lsm9ds1_final[col].values - df_comote_sync[col].values
    print("Différence Max : ", diff.max())
    print("Différence Min:", diff.min())

    print("\n")

    print("df_lsm9ds1_final : ", df_lsm9ds1_final.columns.tolist())
    print("\n")
    print("df_com_sync : ", df_comote_sync.columns.tolist())


    #--------------------- Plots --------------------
    fig, axes = plt.subplots(2, 1, figsize=(11, 11))


    # -------- Signaux Synchronisés -------
    axes[0].plot(
        df_lsm9ds1_final["time"],
        df_lsm9ds1_final[col],
        label=f"lsm9ds1_{col}",
        color="blue",
        linewidth=1,
        alpha=1
    )


    axes[0].plot(
        df_comote_sync["time"],
        df_comote_sync[col],
        label=f"comote_{col}",
        color="red",
        linewidth=1,
        alpha=1
    )


    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel(col)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].set_title("Signaux LSM9DS1 et CoMote ", fontsize=13, fontweight="bold")


    # -------- Erreur --------
    axes[1].plot(
        df_lsm9ds1_final["time"],
        df_lsm9ds1_final[f"err_{col}"],
        label=f"err_{col}",
        color="orange",
        linewidth=1,
        alpha=1
    )


    axes[1].set_ylabel("Erreur (rad/s)", color="orange")
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlabel("Time (s)")
    axes[1].legend()
    axes[1].set_title("Erreur", fontsize=13, fontweight="bold")


    # --- Boxplot ---
    # axes[2].boxplot(df_lsm9ds1_final[f"err_{col}"].values,
    #                 vert=True,
    #                 patch_artist=True,
    #                 boxprops=dict(facecolor="orange", alpha=1),
    #                 medianprops=dict(color="red", alpha=0.8, linewidth=1),
    #                 whiskerprops=dict(color="gray", linewidth=1),
    #                 flierprops=dict(marker="o", color="green", markersize=3, alpha=0.5))
    #
    # #axes[2].axhline(0, color="cyan", linestyle="--", linewidth=1, label="Période nominale")
    # axes[2].set_ylabel("Erreur (rad/s)")
    # axes[2].set_xlabel("LSM9DS1 - CoMote")
    # axes[2].set_title(f"Erreur Gyroscope_{axe} ", fontsize=13, fontweight="bold")
    # axes[2].set_xticks([])
    # #axes[2].legend()
    # axes[2].grid(True, alpha=0.3)


    plt.suptitle(
            f"Comparaison Gyroscope_{axe} : LSM9DS1 vs CoMote",
            fontsize=13,
            fontweight="bold",
    )
    plt.show()

        # if i > 0:
        #     ax.sharex(axes[0])
        #
        # lines1, labels1 = ax.get_legend_handles_labels()
        # lines2, labels2 = ax2.get_legend_handles_labels()
        # ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)





# ---- Graphique de corrélation ---
def calcul_plot_correlations(
    df_lsm9ds1,
    df_riot,
    df_comote,
    capteurs_types=("accelerometre", "gyroscope"),
    axes=("x", "y", "z"),
    unites=None,
    noms_capteurs=None,
    max_points_affiches=5000
):
    """
    Calcule et affiche les corrélations entre trois sources.

    Comparaisons :
        1. LSM9DS1 - CoMote
        2. LSM9DS1 - R-IoT
        3. R-IoT - CoMote

    Pour chaque comparaison, l'analyse est réalisée pour :
        - l'accéléromètre et le gyroscope ;
        - les axes X, Y et Z.

    Les colonnes doivent respecter le format :

        <capteur_type>_<axe>

    Exemples :
        accelerometre_x
        accelerometre_y
        accelerometre_z
        gyroscope_x
        gyroscope_y
        gyroscope_z

    Les trois DataFrames doivent avoir été interpolés sur la
    même grille temporelle et posséder des index compatibles.

    Retour
    ------
    tableau_resultats : pandas.DataFrame
        Tableau regroupant les 18 configurations.
    """

    if unites is None:
        unites = {
            "accelerometre": "m/s²",
            "gyroscope": "rad/s"
        }

    if noms_capteurs is None:
        noms_capteurs = {
            "accelerometre": "Accéléromètre",
            "gyroscope": "Gyroscope"
        }

    sources = {
        "LSM9DS1": df_lsm9ds1,
        "R-IoT": df_riot,
        "CoMote": df_comote
    }

    # L’ordre définit également le sens de la régression :
    # la première source est placée sur l’axe X ;
    # la deuxième source est placée sur l’axe Y.
    comparaisons = [
        ("LSM9DS1", "CoMote"),
        ("LSM9DS1", "R-IoT"),
        ("R-IoT", "CoMote")
    ]

    couleurs_comparaisons = {
        "LSM9DS1 - CoMote": "#E69F00",  # Orange
        "LSM9DS1 - R-IoT": "#56B4E9",  # Bleu ciel
        "R-IoT - CoMote": "#009E73"  # Vert bleuté
    }

    generateur = np.random.default_rng(42)

    resultats = []

    # --------------------------------------------------
    # Vérification des colonnes
    # --------------------------------------------------

    colonnes_manquantes = []

    for source_name, data_frame in sources.items():

        for capteur_type in capteurs_types:

            for axe in axes:

                colonne = f"{capteur_type}_{axe}"

                if colonne not in data_frame.columns:
                    colonnes_manquantes.append(
                        f"{source_name} : {colonne}"
                    )

    if colonnes_manquantes:
        raise ValueError(
            "Certaines colonnes sont manquantes :\n"
            + "\n".join(colonnes_manquantes)
        )

    # --------------------------------------------------
    # Comparaisons
    # --------------------------------------------------

    for source_x, source_y in comparaisons:

        df_x = sources[source_x]
        df_y = sources[source_y]

        nom_comparaison = (
            f"{source_x} - {source_y}"
        )

        couleur = couleurs_comparaisons[
            nom_comparaison
        ]

        # Deux lignes : accéléromètre et gyroscope
        # Trois colonnes : X, Y et Z
        nombre_capteurs = len(capteurs_types)

        if nombre_capteurs == 1:
            hauteur_figure = 4.5
        else:
            hauteur_figure = 8

        fig, axes_figure = plt.subplots(
            nrows=nombre_capteurs,
            ncols=len(axes),
            figsize=(15, hauteur_figure),
            squeeze=False
        )

        for indice_capteur, capteur_type in enumerate(
            capteurs_types
        ):

            unite = unites.get(
                capteur_type,
                ""
            )

            nom_capteur = noms_capteurs.get(
                capteur_type,
                capteur_type.capitalize()
            )

            for indice_axe, axe in enumerate(axes):

                ax = axes_figure[
                    indice_capteur,
                    indice_axe
                ]

                colonne = f"{capteur_type}_{axe}"

                # ------------------------------------------
                # Préparation des données
                # ------------------------------------------

                serie_x = pd.to_numeric(
                    df_x[colonne],
                    errors="coerce"
                )

                serie_y = pd.to_numeric(
                    df_y[colonne],
                    errors="coerce"
                )

                # Alignement sur les index communs
                serie_x, serie_y = serie_x.align(
                    serie_y,
                    join="inner"
                )

                donnees_valides = pd.DataFrame({
                    "x": serie_x,
                    "y": serie_y
                })

                # Suppression des NaN et valeurs infinies
                donnees_valides = donnees_valides[
                    np.isfinite(donnees_valides["x"])
                    & np.isfinite(donnees_valides["y"])
                ]

                if len(donnees_valides) < 2:

                    ax.text(
                        0.5,
                        0.5,
                        "Données insuffisantes",
                        ha="center",
                        va="center",
                        transform=ax.transAxes
                    )

                    ax.set_axis_off()

                    continue

                x = donnees_valides["x"].to_numpy()
                y = donnees_valides["y"].to_numpy()

                # Une corrélation ne peut pas être calculée
                # si l'une des deux séries est constante.
                if np.std(x) == 0 or np.std(y) == 0:

                    ax.text(
                        0.5,
                        0.5,
                        "Corrélation impossible :\n"
                        "une série est constante",
                        ha="center",
                        va="center",
                        transform=ax.transAxes
                    )

                    ax.set_axis_off()

                    continue

                # ------------------------------------------
                # Corrélation et régression
                # ------------------------------------------

                correlation = np.corrcoef(
                    x,
                    y
                )[0, 1]

                # Régression y = pente * x + origine
                pente, origine = np.polyfit(
                    x,
                    y,
                    1
                )

                # Pour une régression linéaire simple avec
                # constante, R² est égal à r².
                #r_carre = correlation ** 2

                resultats.append({
                    "Comparaison": nom_comparaison,
                    "Source X": source_x,
                    "Source Y": source_y,
                    "Capteur": capteur_type,
                    "Axe": axe.upper(),
                    "Unité": unite,
                    "Nombre de valeurs": len(x),
                    "Corrélation de Pearson r": correlation,
                    #"Coefficient R²":r_carre,
                    "Pente": pente,
                    "Ordonnée à l'origine": origine
                })

                # ------------------------------------------
                # Limites communes des deux axes
                # ------------------------------------------

                valeur_minimale = min(
                    x.min(),
                    y.min()
                )

                valeur_maximale = max(
                    x.max(),
                    y.max()
                )

                amplitude = (
                    valeur_maximale - valeur_minimale
                )

                marge = 0.05 * amplitude

                if marge == 0:
                    marge = 1

                limite_minimale = (
                    valeur_minimale - marge
                )

                limite_maximale = (
                    valeur_maximale + marge
                )

                x_regression = np.array([
                    limite_minimale,
                    limite_maximale
                ])

                y_regression = (
                    pente * x_regression
                    + origine
                )

                # ------------------------------------------
                # Sélection des points affichés
                # ------------------------------------------

                indices_affiches = np.arange(
                    len(x)
                )

                if (
                    max_points_affiches is not None
                    and len(indices_affiches)
                    > max_points_affiches
                ):
                    indices_affiches = generateur.choice(
                        indices_affiches,
                        size=max_points_affiches,
                        replace=False
                    )

                x_affiche = x[indices_affiches]
                y_affiche = y[indices_affiches]

                # ------------------------------------------
                # Graphique
                # ------------------------------------------

                ax.scatter(
                    x_affiche,
                    y_affiche,
                    s=10,
                    alpha=1.0,
                    color=couleur,
                    edgecolors="none",
                    rasterized=True
                )

                # Accord parfait
                ax.plot(
                    [
                        limite_minimale,
                        limite_maximale
                    ],
                    [
                        limite_minimale,
                        limite_maximale
                    ],
                    linestyle="--",
                    color="black",
                    linewidth=1.2
                )

                # Régression linéaire
                ax.plot(
                    x_regression,
                    y_regression,
                    color="red",
                    linewidth=2,
                    alpha=0.8
                )

                ax.set_xlim(
                    limite_minimale,
                    limite_maximale
                )

                ax.set_ylim(
                    limite_minimale,
                    limite_maximale
                )

                # Même échelle sur X et Y
                ax.set_aspect(
                    "equal",
                    adjustable="box"
                )

                ax.set_title(
                    f"{nom_capteur} — axe {axe.upper()}",
                    fontweight="bold",
                    pad=10
                )

                ax.set_xlabel(
                    f"{source_x} ({unite})"
                )

                ax.set_ylabel(
                    f"{source_y} ({unite})"
                )

                ax.grid(
                    True,
                    alpha=0.25
                )


        # --------------------------------------------------
        # Légende commune
        # --------------------------------------------------

        elements_legende = [
            Line2D(
                [0],
                [0],
                marker="o",
                linestyle="none",
                markerfacecolor=couleur,
                markeredgecolor="none",
                markersize=6,
                label="Paires de mesures"
            ),
            Line2D(
                [0],
                [0],
                color="black",
                linestyle="--",
                linewidth=1.2,
                label="Accord parfait : y = x"
            ),
            Line2D(
                [0],
                [0],
                color="red",
                linestyle="-",
                linewidth=2,
                label="Régression linéaire"
            )
        ]

        fig.legend(
            handles=elements_legende,
            loc="center left",
            bbox_to_anchor=(0.88, 0.5),
            title="Légende"
        )


        if nombre_capteurs == 1:

            fig.suptitle(
                f"Corrélation entre {source_x} et {source_y}",
                fontsize=15,
                fontweight="bold",
                y=1.10
            )

            fig.subplots_adjust(
                left=0.07,
                right=0.86,
                top=0.86,
                bottom=0.14,
                wspace=0.35,
                hspace=0
            )

        else:

            fig.suptitle(
                f"Corrélation entre {source_x} et {source_y}",
                fontsize=15,
                fontweight="bold",
                y=0.98
            )

            fig.subplots_adjust(
                left=0.07,
                right=0.86,
                top=0.88,
                bottom=0.08,
                wspace=0.35,
                hspace=0.40
            )

        plt.show()

    # --------------------------------------------------
    # Tableau final
    # --------------------------------------------------

    tableau_resultats = pd.DataFrame(
        resultats
    )

    ordre_comparaisons = [
        "LSM9DS1 - CoMote",
        "LSM9DS1 - R-IoT",
        "R-IoT - CoMote"
    ]

    tableau_resultats["Comparaison"] = pd.Categorical(
        tableau_resultats["Comparaison"],
        categories=ordre_comparaisons,
        ordered=True
    )

    tableau_resultats["Capteur"] = pd.Categorical(
        tableau_resultats["Capteur"],
        categories=list(capteurs_types),
        ordered=True
    )

    tableau_resultats["Axe"] = pd.Categorical(
        tableau_resultats["Axe"],
        categories=[
            axe.upper()
            for axe in axes
        ],
        ordered=True
    )

    tableau_resultats = tableau_resultats.sort_values(
        by=[
            "Comparaison",
            "Capteur",
            "Axe"
        ]
    ).reset_index(drop=True)

    return tableau_resultats





def calcul_et_plot_distance_cosinus_3d(
        df_lsm9ds1,
        df_comote,
        capteur_type,
        seuil_norme=0.1
):
    """
    Calcule et affiche la distance cosinus entre les vecteurs 3D
    du LSM9DS1 et du CoMote au cours du temps.

    Paramètres
    ----------
    df_lsm9ds1 : pandas.DataFrame
        Données interpolées du LSM9DS1.

    df_comote : pandas.DataFrame
        Données interpolées du CoMote.

    capteur_type : str
        Type de capteur : "gyro", "acc" ou "mag".

    seuil_norme : float
        Norme minimale pour considérer que la direction du vecteur
        est suffisamment fiable. Les points sous ce seuil sont ignorés.

    Retour
    ------
    resultat : pandas.DataFrame
        DataFrame contenant le temps, les normes, la similarité cosinus,
        la distance cosinus et l'angle entre les vecteurs.
    """

    # Colonnes correspondant aux trois axes
    cols = [
        f"{capteur_type}_x",
        f"{capteur_type}_y",
        f"{capteur_type}_z"
    ]

    # Vérification de la présence des colonnes
    colonnes_manquantes_lsm = [
        col for col in cols
        if col not in df_lsm9ds1.columns
    ]

    colonnes_manquantes_comote = [
        col for col in cols
        if col not in df_comote.columns
    ]

    if colonnes_manquantes_lsm:
        raise ValueError(
            f"Colonnes absentes dans le DataFrame LSM9DS1 : "
            f"{colonnes_manquantes_lsm}"
        )

    if colonnes_manquantes_comote:
        raise ValueError(
            f"Colonnes absentes dans le DataFrame CoMote : "
            f"{colonnes_manquantes_comote}"
        )

    # Vérification des tailles
    if len(df_lsm9ds1) != len(df_comote):
        raise ValueError(
            "Les deux DataFrames doivent avoir le même nombre de lignes. "
            "Utilise les données après interpolation."
        )

    # Vérification que les temps sont identiques
    if not np.allclose(
        df_lsm9ds1["time"].to_numpy(),
        df_comote["time"].to_numpy()
    ):
        raise ValueError(
            "Les deux DataFrames ne possèdent pas la même grille temporelle."
        )

    # Temps commun
    temps = df_lsm9ds1["time"].to_numpy(dtype=float)

    # Vecteurs 3D : une ligne correspond à un instant
    vecteurs_lsm = df_lsm9ds1[cols].to_numpy(dtype=float)
    vecteurs_comote = df_comote[cols].to_numpy(dtype=float)

    # Produit scalaire à chaque instant
    produits_scalaires = np.sum(
        vecteurs_lsm * vecteurs_comote,
        axis=1
    )

    # Normes des vecteurs à chaque instant
    normes_lsm = np.linalg.norm(
        vecteurs_lsm,
        axis=1
    )

    normes_comote = np.linalg.norm(
        vecteurs_comote,
        axis=1
    )

    # Dénominateur de la formule du cosinus
    denominateurs = normes_lsm * normes_comote

    # Initialisation avec NaN
    similarites = np.full(
        len(temps),
        np.nan
    )

    # Points valides :
    # - valeurs finies
    # - normes supérieures au seuil
    masque_valide = (
        np.isfinite(produits_scalaires) &
        np.isfinite(normes_lsm) &
        np.isfinite(normes_comote) &
        (normes_lsm > seuil_norme) &
        (normes_comote > seuil_norme) &
        (denominateurs > 0)
    )

    # Similarité cosinus
    similarites[masque_valide] = (
        produits_scalaires[masque_valide]
        / denominateurs[masque_valide]
    )

    # Protection contre les erreurs numériques
    similarites = np.clip(
        similarites,
        -1.0,
        1.0
    )

    # Distance cosinus
    distances = 1 - similarites

    # Angle entre les deux vecteurs
    angles_deg = np.degrees(
        np.arccos(similarites)
    )

    # Création du DataFrame résultat
    resultat = pd.DataFrame({
        "time": temps,
        "norme_lsm9ds1": normes_lsm,
        "norme_comote": normes_comote,
        "similarite_cosinus": similarites,
        "distance_cosinus": distances,
        "angle_deg": angles_deg,
        "point_valide": masque_valide
    })

    # ==========================================================
    # AFFICHAGE DES RÉSULTATS NUMÉRIQUES
    # ==========================================================

    distances_valides = resultat[
        "distance_cosinus"
    ].dropna()

    angles_valides = resultat[
        "angle_deg"
    ].dropna()

    print(
        f"\n----- Distance cosinus 3D : {capteur_type} -----\n"
    )

    print(
        f"Nombre total de points : {len(resultat)}"
    )

    print(
        f"Nombre de points valides : {len(distances_valides)}"
    )

    print(
        f"Points ignorés car mouvement trop faible ou invalide : "
        f"{len(resultat) - len(distances_valides)}"
    )

    if not distances_valides.empty:

        print(
            f"\nDistance cosinus moyenne : "
            f"{distances_valides.mean():.4f}"
        )

        print(
            f"Distance cosinus médiane : "
            f"{distances_valides.median():.4f}"
        )

        print(
            f"Distance cosinus maximale : "
            f"{distances_valides.max():.4f}"
        )

        print(
            f"\nAngle moyen : "
            f"{angles_valides.mean():.2f}°"
        )

        print(
            f"Angle médian : "
            f"{angles_valides.median():.2f}°"
        )

    # ==========================================================
    # AFFICHAGE AU COURS DU TEMPS
    # ==========================================================

    plt.figure(figsize=(11, 5))

    plt.plot(
        resultat["time"],
        resultat["distance_cosinus"],
        linewidth=1,
        label="Distance cosinus"
    )

    # Référence : mêmes directions
    plt.axhline(
        y=0,
        linestyle="--",
        linewidth=1.2,
        label="Directions identiques"
    )

    # Référence : directions orthogonales
    plt.axhline(
        y=1,
        linestyle=":",
        linewidth=1,
        label="Directions orthogonales"
    )

    plt.xlabel("Temps (s)")
    plt.ylabel("Distance cosinus")

    plt.title(
        f"Distance cosinus entre les vecteurs 3D "
        f"{capteur_type}\n"
        "LSM9DS1 et CoMote",
        fontsize=12,
        fontweight="bold"
    )

    plt.ylim(-0.05, 2.05)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return resultat




def angle (df_cosinus_gyro):
    df_cosinus_gyro["angle_deg"] = np.degrees(
        np.arccos(
            df_cosinus_gyro["similarite_cosinus"]
        )

    )

    plt.figure(figsize=(11, 5))

    plt.plot(
        df_cosinus_gyro["time"],
        df_cosinus_gyro["angle_deg"],
        linewidth=1
    )

    plt.xlabel("Temps (s)")
    plt.ylabel("Écart angulaire (degrés)")
    plt.title(
        "Angle entre les vecteurs gyroscopiques\n"
        "LSM9DS1 et CoMote"
    )

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()





def plot_gyro_3d(
        df,
        source_name,
        capteur_type,
        t_debut=None,
        t_fin=None,
        afficher_ligne=True,
        colorer_par_temps=True
):
    """
    Affiche les mesures gyro_x, gyro_y et gyro_z dans un espace 3D.

    Paramètres
    ----------
    df : pandas.DataFrame
        DataFrame contenant time, gyro_x, gyro_y et gyro_z.

    source_name : str
        Nom du capteur affiché dans le titre.

    t_debut : float ou None
        Début de la fenêtre temporelle en secondes.
        Si None, utilise le début du DataFrame.

    t_fin : float ou None
        Fin de la fenêtre temporelle en secondes.
        Si None, utilise la fin du DataFrame.

    afficher_ligne : bool
        Relie les points dans leur ordre temporel.

    colorer_par_temps : bool
        Colore les points en fonction du temps.
    """

    colonnes = ["time", f"{capteur_type}_x", f"{capteur_type}_y", f"{capteur_type}_z"]

    # Vérification des colonnes
    colonnes_manquantes = [
        col for col in colonnes
        if col not in df.columns
    ]

    if colonnes_manquantes:
        raise ValueError(
            f"Colonnes absentes du DataFrame : {colonnes_manquantes}"
        )

    # Valeurs par défaut
    if t_debut is None:
        t_debut = df["time"].min()

    if t_fin is None:
        t_fin = df["time"].max()

    if t_debut >= t_fin:
        raise ValueError(
            "t_debut doit être strictement inférieur à t_fin."
        )

    # Sélection de la fenêtre temporelle
    df_zoom = df[
        (df["time"] >= t_debut) &
        (df["time"] <= t_fin)
    ].copy()

    # Suppression des valeurs invalides
    df_zoom = df_zoom.replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna(subset=colonnes)

    if df_zoom.empty:
        raise ValueError(
            "Aucune donnée disponible dans cette fenêtre temporelle."
        )

    temps = df_zoom["time"].to_numpy()
    df_x = df_zoom[f"{capteur_type}_x"].to_numpy()
    df_y = df_zoom[f"{capteur_type}_y"].to_numpy()
    df_z = df_zoom[f"{capteur_type}_z"].to_numpy()

    # Création du graphique 3D
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Ligne reliant les points dans l'ordre temporel
    if afficher_ligne:
        ax.plot(
            df_x,
            df_y,
            df_z,
            linewidth=1,
            alpha=0.6,
            label="Trajectoire temporelle"
        )

    # Nuage de points
    if colorer_par_temps:
        points = ax.scatter(
            df_x,
            df_y,
            df_z,
            c=temps,
            cmap="viridis",
            s=50,
            alpha=1.0
        )

        barre_couleur = fig.colorbar(
            points,
            ax=ax,
            pad=0.1,
            shrink=0.75
        )

        barre_couleur.set_label("Temps (s)")

    else:
        ax.scatter(
            df_x,
            df_y,
            df_z,
            s=50,
            alpha=0.8,
            label="Échantillons"
        )



    ax.set_xlabel(f"{capteur_type} X (rad/s)")
    ax.set_ylabel(f"{capteur_type} Y (rad/s)")
    ax.set_zlabel(f"{capteur_type} Z (rad/s)")

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)
    ax.view_init(elev=20, azim=32)



    ax.set_title(
        f"Vecteur gyroscopique 3D — {source_name}\n"
        f"Fenêtre : {t_debut:.3f} s à {t_fin:.3f} s",
        fontsize=12,
        fontweight="bold"
    )

    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()

    return df_zoom
