
import module.jitter as jitter
from IPython.display import display



    #----------------------------------------------------------------------------------------
    #                                || FICHIERS DE DONNÉES ||
    #----------------------------------------------------------------------------------------

all_files = {

 # ------------------------------ || I. FICHERS AVEC LA METHODE SET INTERVAL || ----------------------


# ---------- Interval 5ms --------------------
    "lsm9ds1_interval_5ms_rep1" : (
        "data/jitter/set_interval/interval_005ms/rep_01/"
        "lsm9ds1_jitter_interval_5ms_rep1.txt"
    ),
    "lsm9ds1_interval_5ms_rep2" : (
        "data/jitter/set_interval/interval_005ms/rep_02/"
        "lsm9ds1_jitter_interval_5ms_rep2.txt"
    ),


# --------------- Interval 10ms --------------
    "lsm9ds1_interval_10ms_rep1" : (
        "data/jitter/set_interval/interval_010ms/rep_01/"
        "lsm9ds1_jitter_interval_10ms_rep1.txt"
    ),
    "lsm9ds1_interval_10ms_rep2" : (
        "data/jitter/set_interval/interval_010ms/rep_02/"
        "lsm9ds1_jitter_interval_10ms_rep2.txt"
    ),


    "comote_interval_10ms_rep1" : (
        "data/jitter/set_interval/interval_010ms/rep_01/"
        "comote_jitter_interval_10ms_rep1.txt"
    ),
    "comote_interval_10ms_rep2" : (
        "data/jitter/set_interval/interval_010ms/rep_02/"
        "comote_jitter_interval_10ms_rep2.txt"
    ),


    "riot_interval_10ms_rep1" : (
        "data/jitter/set_interval/interval_010ms/rep_01/"
        "riot_jitter_interval_10ms_rep1.txt"
    ),
    "riot_interval_10ms_rep2" : (
        "data/jitter/set_interval/interval_010ms/rep_02/"
        "riot_jitter_interval_10ms_rep2.txt"
    ),

# ---------- Interval 20ms --------------------
    "lsm9ds1_interval_20ms_rep1" : (
        "data/jitter/set_interval/interval_020ms/rep_01/"
        "lsm9ds1_jitter_interval_20ms_rep1.txt"
    ),
    "lsm9ds1_interval_20ms_rep2" : (
        "data/jitter/set_interval/interval_020ms/rep_02/"
        "lsm9ds1_jitter_interval_20ms_rep2.txt"
    ),


    "comote_interval_20ms_rep1" : (
        "data/jitter/set_interval/interval_020ms/rep_01/"
        "comote_jitter_interval_20ms_rep1.txt"
    ),
    "comote_interval_20ms_rep2" : (
        "data/jitter/set_interval/interval_020ms/rep_02/"
        "comote_jitter_interval_20ms_rep2.txt"
    ),


    "riot_interval_20ms_rep1" : (
        "data/jitter/set_interval/interval_020ms/rep_01/"
        "riot_jitter_interval_20ms_rep1.txt"
    ),
    "riot_interval_20ms_rep2" : (
        "data/jitter/set_interval/interval_020ms/rep_02/"
        "riot_jitter_interval_20ms_rep2.txt"
    ),


# ---------- Interval 40ms --------------------
    "lsm9ds1_interval_40ms_rep1" :  (
        "data/jitter/set_interval/interval_040ms/rep_01/"
        "lsm9ds1_jitter_interval_40ms_rep1.txt"
    ),
    "lsm9ds1_interval_40ms_rep2" : (
        "data/jitter/set_interval/interval_040ms/rep_02/"
        "lsm9ds1_jitter_interval_40ms_rep2.txt"
    ),


    "comote_interval_40ms_rep1" : (
        "data/jitter/set_interval/interval_040ms/rep_01/"
        "comote_jitter_interval_40ms_rep1.txt"
    ),
    "comote_interval_40ms_rep2" : (
        "data/jitter/set_interval/interval_040ms/rep_02/"
        "comote_jitter_interval_40ms_rep2.txt"
    ),


    "riot_interval_40ms_rep1" : (
        "data/jitter/set_interval/interval_040ms/rep_01/"
        "riot_jitter_interval_40ms_rep1.txt"
    ),
    "riot_interval_40ms_rep2" : (
        "data/jitter/set_interval/interval_040ms/rep_02/"
        "riot_jitter_interval_40ms_rep2.txt"
    ),


       # ----------------------------- || II / FICHERS AVEC LA METHODE DES WORKERS || ----------------


#------------ Interval 5ms ----------------
    "lsm9ds1_workers_5ms_rep1" : (
        "data/jitter/workers/interval_005ms/rep_01/"
        "lsm9ds1_jitter_workers_5ms_rep1.txt"
    ),
    "lsm9ds1_workers_5ms_rep2" : (
        "data/jitter/workers/interval_005ms/rep_02/"
        "lsm9ds1_jitter_workers_5ms_rep2.txt"
    ),


# ---------- Interval 10ms -----------
    "lsm9ds1_workers_10ms_rep1" : (
        "data/jitter/workers/interval_010ms/rep_01/"
        "lsm9ds1_jitter_workers_10ms_rep1.txt"
    ),
    "lsm9ds1_workers_10ms_rep2" : (
        "data/jitter/workers/interval_010ms/rep_02/"
        "lsm9ds1_jitter_workers_10ms_rep2.txt"
    ),


    "comote_workers_10ms_rep1" : (
        "data/jitter/workers/interval_010ms/rep_01/"
        "comote_jitter_workers_10ms_rep1.txt"
    ),
    "comote_workers_10ms_rep2" : (
        "data/jitter/workers/interval_010ms/rep_02/"
        "comote_jitter_workers_10ms_rep2.txt"
    ),


    "riot_workers_10ms_rep1" : (
        "data/jitter/workers/interval_010ms/rep_01/"
        "riot_jitter_workers_10ms_rep1.txt"
    ),
    "riot_workers_10ms_rep2" : (
        "data/jitter/workers/interval_010ms/rep_02/"
        "riot_jitter_workers_10ms_rep2.txt"
    ),



    # ---------- Interval 20ms --------------------
    "lsm9ds1_workers_20ms_rep1" : (
        "data/jitter/workers/interval_020ms/rep_01/"
        "lsm9ds1_jitter_workers_20ms_rep1.txt"
    ),
    "lsm9ds1_workers_20ms_rep2" : (
        "data/jitter/workers/interval_020ms/rep_02/"
        "lsm9ds1_jitter_workers_20ms_rep2.txt"
    ),


    "comote_workers_20ms_rep1" : (
        "data/jitter/workers/interval_020ms/rep_01/"
        "comote_jitter_workers_20ms_rep1.txt"
    ),
    "comote_workers_20ms_rep2" : (
        "data/jitter/workers/interval_020ms/rep_02/"
        "comote_jitter_workers_20ms_rep2.txt"
    ),


    "riot_workers_20ms_rep1" : (
        "data/jitter/workers/interval_020ms/rep_01/"
        "riot_jitter_workers_20ms_rep1.txt"
    ),
    "riot_workers_20ms_rep2" : (
        "data/jitter/workers/interval_020ms/rep_02/"
        "riot_jitter_workers_20ms_rep2.txt"
    ),




    # ---------- Interval 40ms --------------------
    "lsm9ds1_workers_40ms_rep1" : (
        "data/jitter/workers/interval_040ms/rep_01/"
        "lsm9ds1_jitter_workers_40ms_rep1.txt"
    ),
    "lsm9ds1_workers_40ms_rep2" : (
        "data/jitter/workers/interval_040ms/rep_02/"
        "lsm9ds1_jitter_workers_40ms_rep2.txt"
    ),


    "comote_workers_40ms_rep1" : (
        "data/jitter/workers/interval_040ms/rep_01/"
        "comote_jitter_workers_40ms_rep1.txt"
    ),
    "comote_workers_40ms_rep2" : (
        "data/jitter/workers/interval_040ms/rep_02/"
        "comote_jitter_workers_40ms_rep2.txt"
    ),


    "riot_workers_40ms_rep1" : (
        "data/jitter/workers/interval_040ms/rep_01/"
        "riot_jitter_workers_40ms_rep1.txt"
    ),
    "riot_workers_40ms_rep2" : (
        "data/jitter/workers/interval_040ms/rep_02/"
        "riot_jitter_workers_40ms_rep2.txt"
    ),

}


    #----------------------------------------------------------------------------------------
    #                                || LECTURE DE FICHIER ||
    #----------------------------------------------------------------------------------------


data_frames = {
    nom: jitter.read_jitter_file(filename=chemin)
    for nom, chemin in all_files.items()
}


#----------------- Interval -------------
df_lsm9ds1_interval_10ms_rep1 = data_frames["lsm9ds1_interval_10ms_rep1"]
df_lsm9ds1_interval_20ms_rep1 = data_frames["lsm9ds1_interval_20ms_rep1"]
df_lsm9ds1_interval_40ms_rep1 = data_frames["lsm9ds1_interval_40ms_rep1"]


df_comote_interval_10ms_rep1 = data_frames["comote_interval_10ms_rep1"]
df_comote_interval_20ms_rep1 = data_frames["comote_interval_20ms_rep1"]
df_comote_interval_40ms_rep1 = data_frames["comote_interval_40ms_rep1"]


df_riot_interval_10ms_rep1 = data_frames["riot_interval_10ms_rep1"]
df_riot_interval_20ms_rep1 = data_frames["riot_interval_20ms_rep1"]
df_riot_interval_40ms_rep1 = data_frames["riot_interval_40ms_rep1"]
#----------------------------------------------

#----------------- Workers -------------
df_lsm9ds1_workers_10ms_rep1 = data_frames["lsm9ds1_workers_10ms_rep1"]
df_lsm9ds1_workers_20ms_rep1 = data_frames["lsm9ds1_workers_20ms_rep1"]
df_lsm9ds1_workers_40ms_rep1 = data_frames["lsm9ds1_workers_40ms_rep1"]


df_comote_workers_10ms_rep1 = data_frames["comote_workers_10ms_rep1"]
df_comote_workers_20ms_rep1 = data_frames["comote_workers_20ms_rep1"]
df_comote_workers_40ms_rep1 = data_frames["comote_workers_40ms_rep1"]


df_riot_workers_10ms_rep1 = data_frames["riot_workers_10ms_rep1"]
df_riot_workers_20ms_rep1 = data_frames["riot_workers_20ms_rep1"]
df_riot_workers_40ms_rep1 = data_frames["riot_workers_40ms_rep1"]



#----------------- Interval ----------------------
df_interval_10ms_rep1_crop = jitter.select_time_window (
    t_debut = 30.0, # seconde (float)
    duree = 180.0,  # seconde (float)
    data_frame_lsm9ds1 = df_lsm9ds1_interval_10ms_rep1,
    data_frame_comote = df_comote_interval_10ms_rep1,
    data_frame_riot = df_riot_interval_10ms_rep1,
)


df_interval_20ms_rep1_crop = jitter.select_time_window (
    t_debut = 30.0, # seconde (float)
    duree = 180.0,  # seconde (float)
    data_frame_lsm9ds1 = df_lsm9ds1_interval_20ms_rep1,
    data_frame_comote = df_comote_interval_20ms_rep1,
    data_frame_riot = df_riot_interval_20ms_rep1,
)


df_interval_40ms_rep1_crop = jitter.select_time_window (
    t_debut = 30.0, # seconde (float)
    duree = 180.0,  # seconde (float)
    data_frame_lsm9ds1 = df_lsm9ds1_interval_40ms_rep1,
    data_frame_comote = df_comote_interval_40ms_rep1,
    data_frame_riot = df_riot_interval_40ms_rep1,
)
#-----------------------------------------------




#----------------- Workers ----------------------
df_workers_10ms_rep1_crop = jitter.select_time_window (
    t_debut = 30.0, # seconde (float)
    duree = 180.0,  # seconde (float)
    data_frame_lsm9ds1 = df_lsm9ds1_workers_10ms_rep1,
    data_frame_comote = df_comote_workers_10ms_rep1,
    data_frame_riot = df_riot_workers_10ms_rep1,
)


df_workers_20ms_rep1_crop = jitter.select_time_window (
    t_debut = 30.0, # seconde (float)
    duree = 180.0,  # seconde (float)
    data_frame_lsm9ds1 = df_lsm9ds1_workers_20ms_rep1,
    data_frame_comote = df_comote_workers_20ms_rep1,
    data_frame_riot = df_riot_workers_20ms_rep1,
)


df_workers_40ms_rep1_crop = jitter.select_time_window (
    t_debut = 30.0, # seconde (float)
    duree = 180.0,  # seconde (float)
    data_frame_lsm9ds1 = df_lsm9ds1_workers_40ms_rep1,
    data_frame_comote = df_comote_workers_40ms_rep1,
    data_frame_riot = df_riot_workers_40ms_rep1,
)
#--------------------------------------------

#---------------------- Interval ---------------------
df_lsm_interval_10ms_rep1_crop = df_interval_10ms_rep1_crop["lsm9ds1"]
df_comote_interval_10ms_rep1_crop = df_interval_10ms_rep1_crop["comote"]
df_riot_interval_10ms_rep1_crop = df_interval_10ms_rep1_crop["riot"]


df_lsm_interval_20ms_rep1_crop = df_interval_20ms_rep1_crop["lsm9ds1"]
df_comote_interval_20ms_rep1_crop = df_interval_20ms_rep1_crop["comote"]
df_riot_interval_20ms_rep1_crop = df_interval_20ms_rep1_crop["riot"]


df_lsm_interval_40ms_rep1_crop = df_interval_40ms_rep1_crop["lsm9ds1"]
df_comote_interval_40ms_rep1_crop = df_interval_40ms_rep1_crop["comote"]
df_riot_interval_40ms_rep1_crop = df_interval_40ms_rep1_crop["riot"]
# -----------------------------------------------------------

#-------------------------- Workers ------------------------
df_lsm_workers_10ms_rep1_crop = df_workers_10ms_rep1_crop["lsm9ds1"]
df_comote_workers_10ms_rep1_crop = df_workers_10ms_rep1_crop["comote"]
df_riot_workers_10ms_rep1_crop = df_workers_10ms_rep1_crop["riot"]


df_lsm_workers_20ms_rep1_crop = df_workers_20ms_rep1_crop["lsm9ds1"]
df_comote_workers_20ms_rep1_crop = df_workers_20ms_rep1_crop["comote"]
df_riot_workers_20ms_rep1_crop = df_workers_20ms_rep1_crop["riot"]


df_lsm_workers_40ms_rep1_crop = df_workers_40ms_rep1_crop["lsm9ds1"]
df_comote_workers_40ms_rep1_crop = df_workers_40ms_rep1_crop["comote"]
df_riot_workers_40ms_rep1_crop = df_workers_40ms_rep1_crop["riot"]
# -----------------------------------------------------------



#------------ SET INTERVAL --------------------
# ---- Calcul et affichage du Jitter -------
sources_10ms = [
    ("LSM9DS1", df_lsm_interval_10ms_rep1_crop, 10),
    ("CoMote", df_comote_interval_10ms_rep1_crop, 10),
    ("R-IoT", df_riot_interval_10ms_rep1_crop, 10)
]

sources_20ms = [
    ("LSM9DS1", df_lsm_interval_20ms_rep1_crop, 20),
    ("CoMote", df_comote_interval_20ms_rep1_crop, 20),
    ("R-IoT", df_riot_interval_20ms_rep1_crop, 20)
]

sources_40ms = [
    ("LSM9DS1", df_lsm_interval_40ms_rep1_crop, 40),
    ("CoMote", df_comote_interval_40ms_rep1_crop, 40),
    ("R-IoT", df_riot_interval_40ms_rep1_crop, 40)
]


groupes_sources = {
    "10 ms": sources_10ms,
    "20 ms": sources_20ms,
    "40 ms": sources_40ms
}

tableau_jitter = jitter.calcul_plot_jitter_intervalles(
    groupes_sources
)


tableau_affichage = tableau_jitter.set_index(
    [
        "Intervalle de référence (ms)",
        "Source"
    ]
)

display(tableau_affichage.round(3))




#------------ WORKERS --------------------
# ---- Calcul et affichage du Jitter -------
sources_workers_10ms = [
    ("LSM9DS1", df_lsm_workers_10ms_rep1_crop, 10),
    ("CoMote", df_comote_workers_10ms_rep1_crop, 10),
    ("R-IoT", df_riot_workers_10ms_rep1_crop, 10)
]

sources_workers_20ms = [
    ("LSM9DS1", df_lsm_workers_20ms_rep1_crop, 20),
    ("CoMote", df_comote_workers_20ms_rep1_crop, 20),
    ("R-IoT", df_riot_workers_20ms_rep1_crop, 20)
]

sources_workers_40ms = [
    ("LSM9DS1", df_lsm_workers_40ms_rep1_crop, 40),
    ("CoMote", df_comote_workers_40ms_rep1_crop, 40),
    ("R-IoT", df_riot_workers_40ms_rep1_crop, 40)
]


groupes_sources_workers = {
    "10 ms": sources_workers_10ms,
    "20 ms": sources_workers_20ms,
    "40 ms": sources_workers_40ms
}

tableau_jitter_workers = jitter.calcul_plot_jitter_intervalles(
    groupes_sources_workers
)


tableau_affichage_workers = tableau_jitter_workers.set_index(
    [
        "Intervalle de référence (ms)",
        "Source"
    ]
)

display(tableau_affichage_workers.round(3))



 # --------- Figure Comparaison Zoom Decalage ----------
resultat_interval = jitter.plot_zoom_periodes_timestamp_ms(
    df=df_lsm_interval_10ms_rep1_crop,
    source_name="LSM9DS1",
    periode_reference_ms=10,
    t_debut=97.0,
    duree=0.2,
    afficher_segments=True
)

display(resultat_interval.round(3))




resultat_workers = jitter.plot_zoom_periodes_timestamp_ms(
    df=df_lsm_workers_10ms_rep1_crop,
    source_name="LSM9DS1",
    periode_reference_ms=10,
    t_debut=97.0,
    duree=0.2,
    afficher_segments=True
)

display(resultat_workers.round(3))







