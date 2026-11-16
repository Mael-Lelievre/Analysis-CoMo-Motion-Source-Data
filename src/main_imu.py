
import module.imu as imu
from IPython.display import display



    #----------------------------------------------------------------------------------------
    #                                || FICHIERS DE DONNÉES ||
    #----------------------------------------------------------------------------------------

all_files = {


# ------------ AU REPO --------------
    "lsm9ds1_repo_10ms_rep1" : (
        "data/imu/repo/rep_01/"
        "lsm9ds1_imu_repo_10ms_rep1.txt"
    ),
    "lsm9ds1_repo_10ms_rep2" : (
        "data/imu/repo/rep_02/"
        "lsm9ds1_imu_repo_10ms_rep2.txt"
    ),

    "comote_repo_10ms_rep1" : (
        "data/imu/repo/rep_01/"
        "comote_imu_repo_10ms_rep1.txt"
    ),
    "comote_repo_10ms_rep2" : (
        "data/imu/repo/rep_02/"
        "comote_imu_repo_10ms_rep2.txt"
    ),

    "riot_repo_10ms_rep1" : (
        "data/imu/repo/rep_01/"
        "riot_imu_repo_10ms_rep1.txt"
    ),
    "riot_repo_10ms_rep2" : (
        "data/imu/repo/rep_02/"
        "riot_imu_repo_10ms_rep2.txt"
    ),


# ----------------- GYROSCOPE -----------------
    "lsm9ds1_gyro_10ms_rep1" : (
        "data/imu/gyro/rep_01/"
        "lsm9ds1_imu_gyro_10ms_rep1.txt"
    ),
    "lsm9ds1_gyro_10ms_rep2" : (
        "data/imu/gyro/rep_02/"
        "lsm9ds1_imu_gyro_10ms_rep2.txt"
    ),

    "comote_gyro_10ms_rep1" : (
        "data/imu/gyro/rep_01/"
        "comote_imu_gyro_10ms_rep1.txt"
    ),
    "comote_gyro_10ms_rep2" : (
        "data/imu/gyro/rep_02/"
        "comote_imu_gyro_10ms_rep2.txt"
    ),

    "riot_gyro_10ms_rep1" : (
        "data/imu/gyro/rep_01/"
        "riot_imu_gyro_10ms_rep1.txt"
    ),
    "riot_gyro_10ms_rep2" : (
        "data/imu/gyro/rep_02/"
        "riot_imu_gyro_10ms_rep2.txt"
    ),



# ---------- ACCELEROMETRE --------------------
  "lsm9ds1_accel_10ms_rep1" : (
        "data/imu/accel/rep_01/"
        "lsm9ds1_imu_accel_10ms_rep1.txt"
    ),
    "lsm9ds1_accel_10ms_rep2" : (
        "data/imu/accel/rep_02/"
        "lsm9ds1_imu_accel_10ms_rep2.txt"
    ),

    "comote_accel_10ms_rep1" : (
        "data/imu/accel/rep_01/"
        "comote_imu_accel_10ms_rep1.txt"
    ),
    "comote_accel_10ms_rep2" : (
        "data/imu/accel/rep_02/"
        "comote_imu_accel_10ms_rep2.txt"
    ),

    "riot_accel_10ms_rep1" : (
        "data/imu/accel/rep_01/"
        "riot_imu_accel_10ms_rep1.txt"
    ),
    "riot_accel_10ms_rep2" : (
        "data/imu/accel/rep_02/"
        "riot_imu_accel_10ms_rep2.txt"
    ),


# -------------- LIBRE --------------------
      "lsm9ds1_libre_10ms_rep1" : (
        "data/imu/libre/rep_01/"
        "lsm9ds1_imu_libre_10ms_rep1.txt"
    ),
    "lsm9ds1_libre_10ms_rep2" : (
        "data/imu/libre/rep_02/"
        "lsm9ds1_imu_libre_10ms_rep2.txt"
    ),

    "comote_libre_10ms_rep1" : (
        "data/imu/libre/rep_01/"
        "comote_imu_libre_10ms_rep1.txt"
    ),
    "comote_libre_10ms_rep2" : (
        "data/imu/libre/rep_02/"
        "comote_imu_libre_10ms_rep2.txt"
    ),

    "riot_libre_10ms_rep1" : (
        "data/imu/libre/rep_01/"
        "riot_imu_libre_10ms_rep1.txt"
    ),
    "riot_libre_10ms_rep2" : (
        "data/imu/libre/rep_02/"
        "riot_imu_libre_10ms_rep2.txt"
    ),

}


    #----------------------------------------------------------------------------------------
    #                                || LECTURE DE FICHIER ||
    #----------------------------------------------------------------------------------------


data_frames = {
    nom: imu.read_imu_file(filename=chemin)
    for nom, chemin in all_files.items()
}


# ------------- Repo -----------------
df_lsm9ds1_repo_rep1  = data_frames["lsm9ds1_repo_10ms_rep1"]
df_comote_repo_rep1  = data_frames["comote_repo_10ms_rep1"]
df_riot_repo_rep1  = data_frames["riot_repo_10ms_rep1"]

# ------------- Gyroscope -----------------
df_lsm9ds1_gyro_rep1  = data_frames["lsm9ds1_gyro_10ms_rep1"]
df_comote_gyro_rep1  = data_frames["comote_gyro_10ms_rep1"]
df_riot_gyro_rep1  = data_frames["riot_gyro_10ms_rep1"]


# ------------- Accelerometre -----------------
df_lsm9ds1_accel_rep1  = data_frames["lsm9ds1_accel_10ms_rep1"]
df_comote_accel_rep1  = data_frames["comote_accel_10ms_rep1"]
df_riot_accel_rep1  = data_frames["riot_accel_10ms_rep1"]


# ------------- Libre ----------------
df_lsm9ds1_libre_rep1  = data_frames["lsm9ds1_libre_10ms_rep1"]
df_comote_libre_rep1  = data_frames["comote_libre_10ms_rep1"]
df_riot_libre_rep1  = data_frames["riot_libre_10ms_rep1"]


# --------------------------------------
#             | CROP |
# --------------------------------------
df_repo_rep1_crop = imu.select_time_window (
    t_debut = 30, # seconde (float)
    duree = 180.0,  # seconde (float)
    data_frame_lsm9ds1 = df_lsm9ds1_repo_rep1,
    data_frame_comote = df_comote_repo_rep1,
    data_frame_riot = df_riot_repo_rep1,
)


df_gyro_rep1_crop = imu.select_time_window (
    t_debut = 30, # seconde (float)
    duree = 180.0,  # seconde (float)
    data_frame_lsm9ds1 = df_lsm9ds1_gyro_rep1,
    data_frame_comote = df_comote_gyro_rep1,
    data_frame_riot = df_riot_gyro_rep1,
)


df_accel_rep1_crop = imu.select_time_window (
    t_debut = 30, # seconde (float)
    duree = 180.0,  # seconde (float)
    data_frame_lsm9ds1 = df_lsm9ds1_accel_rep1,
    data_frame_comote = df_comote_accel_rep1,
    data_frame_riot = df_riot_accel_rep1,
)

df_libre_rep1_crop = imu.select_time_window (
    t_debut = 30, # seconde (float)
    duree = 180.0,  # seconde (float)
    data_frame_lsm9ds1 = df_lsm9ds1_libre_rep1,
    data_frame_comote = df_comote_libre_rep1,
    data_frame_riot = df_riot_libre_rep1,
)



df_lsm_repo_rep1_crop = df_repo_rep1_crop["lsm9ds1"]
df_comote_repo_rep1_crop = df_repo_rep1_crop["comote"]
df_riot_repo_rep1_crop = df_repo_rep1_crop["riot"]


df_lsm_gyro_rep1_crop = df_gyro_rep1_crop["lsm9ds1"]
df_comote_gyro_rep1_crop = df_gyro_rep1_crop["comote"]
df_riot_gyro_rep1_crop = df_gyro_rep1_crop["riot"]


df_lsm_accel_rep1_crop = df_accel_rep1_crop["lsm9ds1"]
df_comote_accel_rep1_crop = df_accel_rep1_crop["comote"]
df_riot_accel_rep1_crop = df_accel_rep1_crop["riot"]


df_lsm_libre_rep1_crop = df_libre_rep1_crop["lsm9ds1"]
df_comote_libre_rep1_crop = df_libre_rep1_crop["comote"]
df_riot_libre_rep1_crop = df_libre_rep1_crop["riot"]




# --------------------------------------
#       | INTERPOLATION LINEAIRE |
# --------------------------------------

(df_lsm_repo_crop_sync_rep1,
 df_com_repo_crop_sync_rep1,
 df_riot_repo_crop_sync_rep1) = imu.interpolation_lineaire(
    df_lsm_repo_rep1_crop,
    df_comote_repo_rep1_crop,
    df_riot_repo_rep1_crop)



(df_lsm_gyro_crop_sync_rep1,
 df_com_gyro_crop_sync_rep1,
 df_riot_gyro_crop_sync_rep1) = imu.interpolation_lineaire(
    df_lsm_gyro_rep1_crop,
    df_comote_gyro_rep1_crop,
    df_riot_gyro_rep1_crop)

(df_lsm_accel_crop_sync_rep1,
 df_com_accel_crop_sync_rep1,
 df_riot_accel_crop_sync_rep1) = imu.interpolation_lineaire(
    df_lsm_accel_rep1_crop,
    df_comote_accel_rep1_crop,
    df_riot_accel_rep1_crop)


(df_lsm_libre_crop_sync_rep1,
 df_com_libre_crop_sync_rep1,
 df_riot_libre_crop_sync_rep1) = imu.interpolation_lineaire(
    df_lsm_libre_rep1_crop,
    df_comote_libre_rep1_crop,
    df_riot_libre_rep1_crop)



# -------------- Erreur Repo ------------
tableau_erreurs_repo = imu.calcul_erreurs_inertielles(
    df_lsm9ds1=df_lsm_repo_crop_sync_rep1,
    df_riot=df_riot_repo_crop_sync_rep1,
    df_comote=df_com_repo_crop_sync_rep1,
    capteurs_types=[
        "accelerometre",
        "gyroscope"
    ],
    unites={
        "accelerometre": "m/s²",
        "gyroscope": "rad/s"
    }
)

display(
    tableau_erreurs_repo
    .set_index([
        "Comparaison",
        "Capteur",
        "Axe"
    ])
    .round(3)
)

# -------------- Erreur Gyroscope ------------
tableau_erreurs_gyro = imu.calcul_erreurs_inertielles(
    df_lsm9ds1=df_lsm_gyro_crop_sync_rep1,
    df_riot=df_riot_gyro_crop_sync_rep1,
    df_comote=df_com_gyro_crop_sync_rep1,
    capteurs_types=[
        #"accelerometre",
        "gyroscope"
    ],
    unites={
        #"accelerometre": "m/s²",
        "gyroscope": "rad/s"
    }
)

display(
    tableau_erreurs_gyro
    .set_index([
        "Comparaison",
        "Capteur",
        "Axe"
    ])
    .round(3)
)


# -------------- Erreur Acceleromètre ------------
tableau_erreurs_accel = imu.calcul_erreurs_inertielles(
    df_lsm9ds1=df_lsm_accel_crop_sync_rep1,
    df_riot=df_riot_accel_crop_sync_rep1,
    df_comote=df_com_accel_crop_sync_rep1,
    capteurs_types=[
        "accelerometre"
        #"gyroscope"
    ],
    unites={
        "accelerometre": "m/s²"
        #"gyroscope": "rad/s"
    }
)

display(
    tableau_erreurs_accel
    .set_index([
        "Comparaison",
        "Capteur",
        "Axe"
    ])
    .round(3)
)



# -------------- Erreur Acceleromètre ------------
tableau_erreurs_libre = imu.calcul_erreurs_inertielles(
    df_lsm9ds1=df_lsm_libre_crop_sync_rep1,
    df_riot=df_riot_libre_crop_sync_rep1,
    df_comote=df_com_libre_crop_sync_rep1,
    capteurs_types=[
        "accelerometre",
        "gyroscope"
    ],
    unites={
        "accelerometre": "m/s²",
        "gyroscope": "rad/s"
    }
)

display(
    tableau_erreurs_libre
    .set_index([
        "Comparaison",
        "Capteur",
        "Axe"
    ])
    .round(3)
)




# ----------------------------------------
#           | Corrrelation |
# ----------------------------------------

# --------- Gyroscope ------------
tableau_correlations_gyro = imu.calcul_plot_correlations(
    df_lsm9ds1=df_lsm_gyro_crop_sync_rep1,
    df_riot=df_riot_gyro_crop_sync_rep1,
    df_comote=df_com_gyro_crop_sync_rep1,
    capteurs_types=[
        #"accelerometre",
        "gyroscope"
    ],
    unites={
        #"accelerometre": "m/s²",
        "gyroscope": "rad/s"
    },
    max_points_affiches=18000
)

display(
    tableau_correlations_gyro
    .set_index([
        "Comparaison",
        "Capteur",
        "Axe"
    ])
    .round(3)

)



# --------- Acceleromètre ------------
tableau_correlations_accel = imu.calcul_plot_correlations(
    df_lsm9ds1=df_lsm_accel_crop_sync_rep1,
    df_riot=df_riot_accel_crop_sync_rep1,
    df_comote=df_com_accel_crop_sync_rep1,
    capteurs_types=[
        "accelerometre"],
        #"gyroscope"
    unites={
        "accelerometre": "m/s²"},
        #"gyroscope": "rad/s"
    max_points_affiches=18000
)


display(
    tableau_correlations_accel
    .set_index([
        "Comparaison",
        "Capteur",
        "Axe"
    ])
    .round(3)
)


# --------- Libre ------------
tableau_correlations_libre = imu.calcul_plot_correlations(
    df_lsm9ds1=df_lsm_libre_crop_sync_rep1,
    df_riot=df_riot_libre_crop_sync_rep1,
    df_comote=df_com_libre_crop_sync_rep1,
    capteurs_types=[
        "accelerometre",
        "gyroscope"
    ],
    unites={
        "accelerometre": "m/s²",
        "gyroscope": "rad/s"
    },
    max_points_affiches=18000
)

display(
    tableau_correlations_libre
    .set_index([
        "Comparaison",
        "Capteur",
        "Axe"
    ])
    .round(3)
)

#-----------------------------------------


imu.plot_pas_temporel(
    df_lsm9ds1 = df_lsm_gyro_rep1_crop,
    df_comote = df_comote_gyro_rep1_crop,
    df_riot = df_riot_gyro_rep1_crop,
    capteur_type="gyroscope",
    axe="x",
    t_debut=70,
    duree_fenetre=0.15
)


imu.plot_pas_temporel(
    df_lsm9ds1 = df_lsm_gyro_crop_sync_rep1,
    df_comote = df_com_gyro_crop_sync_rep1,
    df_riot = df_riot_gyro_crop_sync_rep1,
    capteur_type="gyroscope",
    axe="x",
    t_debut=70,
    duree_fenetre=0.15
)

