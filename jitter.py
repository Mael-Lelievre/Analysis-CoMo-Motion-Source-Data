
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pathlib import Path
import seaborn as sns
from matplotlib.ticker import MultipleLocator



# ---------- LECTURE DES FICHIERS ------------
def read_jitter_file (filename: str | Path):

    filename = Path(filename)
    data = []

    with filename.open("r", encoding="utf-8") as file:
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

            })

    df = pd.DataFrame(data)

    return df


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




#-------------- CALCUL DE DONNÉES --------------
def calcul_frequence_brute(
        df_lsm9ds1=None,
        df_comote=None,
        df_riot=None
):

    data_frames = {
        "LSM9DS1": df_lsm9ds1,
        "CoMote": df_comote,
        "R-IoT": df_riot
    }

    # On conserve uniquement les DataFrames fournis
    data_frames = {
        source_name: data_frame
        for source_name, data_frame in data_frames.items()
        if data_frame is not None
    }

    if not data_frames:
        raise ValueError(
            "Aucun DataFrame n'a été fourni."
        )

    for source_name, data_frame in data_frames.items():

        period = data_frame["time"].diff()
        period = period.dropna()
        period = period[period > 0]

        if period.empty:
            raise ValueError(
                f"Aucune période valide pour {source_name}."
            )

        freq_moy = 1 / np.mean(period)
        freq_median = 1 / np.median(period)

        print(f"--------- {source_name} ---------")

        print(
            f"Période moyenne : "
            f"{np.mean(period * 1000):.3f} ms"
        )



        print(
            f"Fréquence moyenne : "
            f"{freq_moy:.3f} Hz"
        )

        print(
            f"Période min : "
            f"{np.min(period * 1000):.3f} ms"
        )

        print(
            f"Période max : "
            f"{np.max(period * 1000):.3f} ms"
        )

        print()

        # print(
        #     f"Période médiane : "
        #     f"{np.median(period * 1000):.3f} ms"
        # )
        #
        # print(
        #     f"Fréquence médiane : "
        #     f"{freq_median:.3f} Hz"
        # )
        #
        # print()














#--------------- CALCUL/PLOT JITTER --------------------
def calcul_plot_jitter_intervalles(groupes_sources):

    nombre_intervalles = len(groupes_sources)

    fig, axes = plt.subplots(
        1,
        nombre_intervalles,
        figsize=(4 * nombre_intervalles, 4),
        sharey=True,
        constrained_layout=True

    )

    # Cas où un seul intervalle serait fourni
    axes = np.atleast_1d(axes)

    resultats = []

    couleurs_sources = {
        "LSM9DS1": "orange",
        "CoMote": "cornflowerblue",
        "R-IoT": "mediumseagreen"
    }

    for ax, (nom_intervalle, sources) in zip(
        axes,
        groupes_sources.items()
    ):

        distributions_jitter = []
        noms_sources = []

        for source_name, data_frame, periode_reference_ms in sources:

            # Tri chronologique
            if "time" in data_frame.columns:
                data = data_frame.sort_values("time").copy()
            else:
                data = data_frame.sort_values(
                    "timestamp_ms"
                ).copy()

            # Périodes mesurées en millisecondes
            periodes_ms = (
                data["timestamp_ms"]
                .diff()
                .dropna()
            )

            # Suppression des périodes incorrectes
            periodes_ms = periodes_ms[
                periodes_ms > 0
            ]

            if periodes_ms.empty:
                print(
                    f"Aucune donnée valide pour "
                    f"{source_name}, intervalle {nom_intervalle}"
                )
                continue

            # Calcul du jitter
            jitter_ms = (periodes_ms - periode_reference_ms)


            distributions_jitter.append(jitter_ms.to_numpy())
            noms_sources.append(source_name)

            q1 = jitter_ms.quantile(0.25)
            q3 = jitter_ms.quantile(0.75)

            periode_moyenne_ms = periodes_ms.mean()

            # Une ligne du tableau pour cette combinaison
            # source / intervalle
            resultats.append({

                #"Nombre de périodes":
                #   len(periodes_ms),

                "Intervalle de référence (ms)": periode_reference_ms,
                "Source": source_name,

                "Période moyenne (ms)": periode_moyenne_ms,

                "Fréquence moyenne (Hz)": 1000 / periode_moyenne_ms,

                "Période maximale (ms)": periodes_ms.max(),

                "Periode minimale (ms)": periodes_ms.min(),

                "Jitter absolu moyen (ms)": jitter_ms.abs().mean(),

                "Jitter minimal (ms)": jitter_ms.min(),

                "Jitter maximal (ms)": jitter_ms.max(),

                #"Jitter moyen signé (ms)":
                 #   jitter_ms.mean(),

                #"Écart-type du jitter (ms)":
                 #   jitter_ms.std(),

                #"Jitter médian (ms)":
                 #   jitter_ms.median(),

                #"Écart interquartile (ms)":
                 #   q3 - q1,

                #"P95 du jitter absolu (ms)":
                 #   jitter_ms.abs().quantile(0.95),


            })

        # ---------------- Boxplot de l’intervalle ----------------

        boxplot = ax.boxplot(
            distributions_jitter,
            patch_artist=True,
            medianprops=dict(
                color="red",
                linewidth=1.5
            ),
            whiskerprops=dict(
                color="gray",
                linewidth=1
            ),
            capprops=dict(
                color="gray",
                linewidth=1
            ),
            flierprops=dict(
                marker="o",
                markerfacecolor="gray",
                markeredgecolor="gray",
                markersize=3,
                alpha=1.0
            )
        )

        # Couleur constante pour chaque source
        for boite, source_name in zip(
            boxplot["boxes"],
            noms_sources
        ):
            boite.set_facecolor(
                couleurs_sources.get(
                    source_name,
                    "lightgray"
                )
            )
            boite.set_alpha(0.8)

        ax.set_xticks(
            range(1, len(noms_sources) + 1),
            noms_sources
        )

        ax.axhline(
            0,
            color="black",
            linestyle="--",
            linewidth=1
        )

        ax.set_title(
            f"Intervalle : {nom_intervalle}",
            fontweight="bold",
            pad = 10
        )

        ax.set_xlabel("Source")
        ax.grid(axis="y", alpha=0.3)
        ax.set_ylabel("Jitter (ms)")

    fig.suptitle(
        "Distribution du jitter des différentes sources de mouvement, \n selon l’intervalle de référence",
        fontsize=16,
        fontweight="bold",
        y = 1.2,
    )


    plt.show()



    # Création du tableau unique
    tableau_resultats = pd.DataFrame(resultats)

    ordre_sources = [
        "LSM9DS1",
        "CoMote",
        "R-IoT"
    ]

    tableau_resultats["Source"] = pd.Categorical(
        tableau_resultats["Source"],
        categories=ordre_sources,
        ordered=True
    )

    tableau_resultats = tableau_resultats.sort_values(
        by=[
            "Intervalle de référence (ms)",
            "Source"
        ]
    ).reset_index(drop=True)

    return tableau_resultats




#--------------- REFERENCE INTERVAL VS SENSOR TIMESTAMP --------------------
def plot_zoom_periodes_timestamp_ms(
    df,
    source_name,
    periode_reference_ms,
    t_debut,
    duree=0.2,
    afficher_segments=True
):
    """
    Affiche les instants d'échantillonnage réels reconstruits à
    partir de timestamp_ms et les compare à une référence idéale
    possédant une période constante.

    Paramètres
    ----------
    df : pandas.DataFrame
        DataFrame contenant au minimum les colonnes :
        - "time", en secondes ;
        - "timestamp_ms", en millisecondes.

    source_name : str
        Nom de la source affiché dans le graphique.

    periode_reference_ms : float
        Période théorique de référence, en millisecondes.
        Exemple : 10 pour une période de 10 ms.

    t_debut : float
        Début de la fenêtre d'analyse, basé sur la colonne
        "time", en secondes.

    duree : float, optionnel
        Durée de la fenêtre d'analyse, en secondes.

    afficher_segments : bool, optionnel
        Si True, trace un segment rouge entre chaque instant
        idéal et l'instant réel correspondant.

    Retour
    ------
    resultat : pandas.DataFrame
        Tableau contenant les périodes réelles, les instants
        reconstruits et les décalages par rapport à la référence.
    """

    # --------------------------------------------------
    # Vérification des paramètres
    # --------------------------------------------------

    colonnes_requises = [
        "time",
        "timestamp_ms"
    ]

    colonnes_manquantes = [
        colonne
        for colonne in colonnes_requises
        if colonne not in df.columns
    ]

    if colonnes_manquantes:
        raise ValueError(
            "Colonnes manquantes dans le DataFrame : "
            f"{colonnes_manquantes}"
        )

    if periode_reference_ms <= 0:
        raise ValueError(
            "La période de référence doit être "
            "strictement positive."
        )

    if duree <= 0:
        raise ValueError(
            "La durée doit être strictement positive."
        )

    # --------------------------------------------------
    # Préparation des données
    # --------------------------------------------------

    data = df.copy()

    data["time"] = pd.to_numeric(
        data["time"],
        errors="coerce"
    )

    data["timestamp_ms"] = pd.to_numeric(
        data["timestamp_ms"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["time", "timestamp_ms"]
    )

    data = data.sort_values("time")

    # --------------------------------------------------
    # Sélection de la fenêtre temporelle
    # --------------------------------------------------

    t_fin = t_debut + duree

    data = data[
        (data["time"] >= t_debut)
        & (data["time"] <= t_fin)
    ].copy()

    if len(data) < 2:
        raise ValueError(
            "La fenêtre sélectionnée ne contient pas "
            "assez de points pour calculer une période."
        )

    # --------------------------------------------------
    # Calcul des périodes réelles
    # --------------------------------------------------

    period_ms = (
        data["timestamp_ms"]
        .diff()
        .dropna()
    )

    # Suppression des périodes nulles ou négatives
    period_ms = period_ms[
        period_ms > 0
    ]

    if period_ms.empty:
        raise ValueError(
            "Aucune période strictement positive "
            "n'a été trouvée."
        )

    # --------------------------------------------------
    # Reconstruction du temps relatif
    # --------------------------------------------------

    # Le premier échantillon définit l'origine t = 0.
    temps_reel_ms = np.insert(
        np.cumsum(period_ms.to_numpy()),
        0,
        0.0
    )

    # Grille temporelle idéale
    temps_ideal_ms = (
        np.arange(len(temps_reel_ms))
        * periode_reference_ms
    )

    # Décalage cumulé entre les instants réels et idéaux
    decalage_ms = (
        temps_reel_ms - temps_ideal_ms
    )

    # --------------------------------------------------
    # Couleurs
    # --------------------------------------------------

    couleur_reel = "deepskyblue"
    couleur_ideal = "darkorange"
    couleur_ecart = "red"

    # --------------------------------------------------
    # Création du graphique
    # --------------------------------------------------

    fig, ax = plt.subplots(figsize=(14, 4))

    # Repères verticaux des instants réels
    for t in temps_reel_ms:
        ax.axvline(
            t,
            color=couleur_reel,
            alpha=0.25,
            linewidth=1.2,
            zorder=0
        )

    # Repères verticaux des instants idéaux
    for t in temps_ideal_ms:
        ax.axvline(
            t,
            color=couleur_ideal,
            alpha=0.5,
            linewidth=1.2,
            zorder=0
        )

    # Points réels
    ax.scatter(
        temps_reel_ms,
        np.ones(len(temps_reel_ms)),
        marker="o",
        s=70,
        color=couleur_reel,
        edgecolor="black",
        linewidth=0.4,
        label=f"Instant d'acquisition réel",
        zorder=4
    )

    # Points idéaux
    ax.scatter(
        temps_ideal_ms,
        np.zeros(len(temps_ideal_ms)),
        marker="x",
        s=70,
        color=couleur_ideal,
        linewidth=2,
        label=f"Instant d'acquisition théorique",
        zorder=5
    )

    # --------------------------------------------------
    # Segments représentant les décalages
    # --------------------------------------------------

    if afficher_segments:

        # On commence à l'indice 1 :
        # le point initial ne possède pas de période.
        for i, (t_ideal, t_reel) in enumerate(
            zip(
                temps_ideal_ms[1:],
                temps_reel_ms[1:]
            )
        ):
            ax.plot(
                [t_ideal, t_reel],
                [0, 1],
                color=couleur_ecart,
                alpha=0.5,
                linewidth=1.2,

                # Le label est ajouté une seule fois.
                label=(
                    "Écart entre référence et mesure"
                    if i == 0
                    else None
                ),

                zorder=2
            )

    # --------------------------------------------------
    # Mise en forme
    # --------------------------------------------------

    ax.set_yticks(
        [0, 1],
        [
            "Intervalle 10ms",
            source_name
        ]
    )

    ax.set_xlabel(
        "Temps relatif reconstruit (ms)"
    )

    ax.set_title(
        "Instants d’acquisition théoriques et mesurés, avant optimisation temporelle \n",
        pad=15
    )

    ax.grid(
        True,
        axis="x",
        alpha=0.2
    )

    ax.margins(
        x=0.02,
        y=0.25
    )

    ax.legend(
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0,
        frameon=True
    )

    # Réserve de l’espace à droite pour la légende
    fig.subplots_adjust(
        right=0.76
    )


    ax.xaxis.set_major_locator(
        MultipleLocator(10)
    )

    plt.show()

    # --------------------------------------------------
    # Construction du tableau résultat
    # --------------------------------------------------

    # Le point initial est exclu du tableau, car aucune
    # période ne peut être calculée avant le premier point.
    resultat = pd.DataFrame({
        "index_local": np.arange(
            1,
            len(temps_reel_ms)
        ),

        "periode_reelle_ms":
            period_ms.to_numpy(),

        "temps_reel_ms":
            temps_reel_ms[1:],

        "temps_ideal_ms":
            temps_ideal_ms[1:],

        "decalage_ms":
            decalage_ms[1:]
    })

    return resultat


