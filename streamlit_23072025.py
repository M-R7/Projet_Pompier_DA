import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit as st
from PIL import Image
import plotly.express as px
import base64
import time
import numpy as np
from folium import Popup
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api
from scipy.stats import kruskal

# logo = Image.open("https://github.com/M-R7/Projet_Pompier_DA/blob/main/img_pompiers.png")

st.sidebar.title("Temps de réponse de la Brigade des Pompiers de Londres")
pages = ["Introduction","Jeux de données","Data Visualisation","Cartographie","Modélisation"]
page=st.sidebar.radio("",pages)
st.markdown("""
    <style>
        /* Changer la largeur de la sidebar */
        section[data-testid="stSidebar"] {
            width: 350px !important;  /* Largeur souhaitée */
        }
        /* Redimensionner le contenu principal en conséquence */
        section.main {
            margin-left: 370px;  /* Adapter le décalage */
        }
    </style>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style='background-color:  #E6F2E6; padding: 20px; border-radius: 5px; color:  #1b1a1a; text-align: left;'>
        Auteurs : Morgane Rivière<br>
        Rémi Moulinas<br><br>
        Continu Data Analyst Novembre/Décembre 2024, 
        <a href='https://datascientest.com' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>
            Datascientest
        </a>
        <br><br>
        Données : <a href='https://data.london.gov.uk/dataset/london-fire-brigade-incident-records/' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>
            London Datastore
        </a>, 
        <a href='https://www.london-fire.gov.uk/community/your-borough/' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>
            London Fire Brigade
        </a>, 
        <a href='https://roadtraffic.dft.gov.uk/regions/6' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>
            London Road Traffic
        </a>
    </div>
""", unsafe_allow_html=True)

# hidden div with anchor
st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)

if page == pages[0]:
    logo = Image.open("img_pompiers.png")

    logo = logo.resize((345, 195))
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, use_container_width=False)  # conserve la taille choisie
    #st.title("Temps de réponse de la Brigade des Pompiers de Londres")
    st.markdown("<h3 style='text-align: center;'>Temps de réponse de la Brigade des Pompiers de Londres</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>de 2009 à 2024</h5>", unsafe_allow_html=True)

    st.markdown(
    """
    <div style="text-align: center; font-style: italic;">
        L’objectif de ce projet est d’analyser et d’estimer les temps de réponse et de mobilisation de la Brigade des Pompiers de Londres.
        La brigade des pompiers de Londres est le service d'incendie et de sauvetage le plus actif du Royaume-Uni et l'une des plus grandes organisations de lutte contre l'incendie et de sauvetage au monde.
    </div><br>
    """,
    unsafe_allow_html=True
)

    
    st.markdown("""
        <div style="background-color: white; border: 2px solid black; padding: 20px; border-radius: 5px; text-align: center; color: black; width: 80%; margin: auto;">
            Projet réalisé dans le cadre de la formation <span style="font-weight: 900;">Data Analyst</span> de 
            <a href='https://datascientest.com' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>
                Datascientest
            </a><br>
            Promotion Continu novembre/décembre 2024<br>
            Auteurs : <br><br>
            <span style="font-weight: 900;">Morgane Rivière</span> <a href='https://www.linkedin.com/in/morgane-riviere-5a908316b/' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>LinkedIn</a><br>
            <span style="font-weight: 900;">Rémi Moulinas</span> <a href='https://www.linkedin.com/in/r%C3%A9mi-moulinas-397553128/' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>LinkedIn</a><br><br>
            Source des données :<br>
            <a href='https://data.london.gov.uk/dataset/london-fire-brigade-incident-records/' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>
                London Datastore
            </a>, 
            <a href='https://www.london-fire.gov.uk/community/your-borough/' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>
                London Fire Brigade
            </a>, 
            <a href='https://roadtraffic.dft.gov.uk/regions/6' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>
                London Road Traffic
            </a>
        </div>
    """, unsafe_allow_html=True)

elif page == pages[1]:
    st.markdown("<a id='haut'></a>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Jeux de données</h3>", unsafe_allow_html=True)
# Radio sans label

    choix = st.radio(label="",options=["Dataset Principal", "Dataset Secondaire"],label_visibility="collapsed")
    
    if choix == "Dataset Principal":
        st.markdown("<h4>Dataset Principal</h4>", unsafe_allow_html=True)
        st.markdown("<h4>1. Source</h4>", unsafe_allow_html=True)
        st.markdown("""Nous avons deux jeux de données principaux : <a href='https://data.london.gov.uk/dataset/london-fire-brigade-mobilisation-records' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>Mobilisation</a> et <a href='https://data.london.gov.uk/dataset/london-fire-brigade-incident-records' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>Incident</a>. Ils proviennent de la <a href='https://data.london.gov.uk/' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>London Datastore</a>""", unsafe_allow_html=True)
        st.markdown("<h4>2. Exploration des données</h4>", unsafe_allow_html=True)
        
        choix_colonnes = st.radio(label="",options=["Toutes les colonnes", "Colonnes utilisées pour la modélisation","Colonnes non utilisées"],label_visibility="collapsed")
        if choix_colonnes == "Toutes les colonnes":
        
            st.markdown("<h5>Dataset Incident</h5>", unsafe_allow_html=True)
            st.markdown("""
            - Dataset (1) LFB Incident data from 2009 – 2017.csv<br>
            Ce jeu de données reprend toutes les informations relatives aux appels passés par la population pour demander une intervention des pompiers entre 2009 et 2017.
            Ce jeu comporte 988279 entrées, pour 39 colonnes.<br>
            - Dataset (2) LFB Incident data from 2018 onwards.csv
            Ce jeu de données reprend toutes les informations relatives aux appels passés par la population pour demander une intervention des pompiers depuis 2018.
            Ce jeu comporte 805036 entrées, pour 39 colonnes.<br>
            Les différentes colonnes de ces jeux de données reprennent les informations suivantes :

            """, unsafe_allow_html=True)
            # Radio sans label


            html_incident = """
            <table style="width: 100%; border-collapse: collapse; margin: 20px auto;">
                <thead>
                    <tr>
                        <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Nom de la colonne</th>
                        <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Description</th>
                        <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Type de variable</th>
                    </tr>
                </thead>
                <tbody>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentNumber</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Numéro d'incident (index)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #D9EAF7;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DateOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date de l'appel</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Temporelle</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">CalYear</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Année d'enregistrement de l’appel</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - 5 à 10 catégories</td></tr>
                    <tr style="background-color: #D9EAF7;"><td style="border: 1px solid black; padding: 8px; text-align: center;">TimeOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Heure de l'appel (hh:mm:ss)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Temporelle</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">HourOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Heure de l'appel (nombre unique)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentGroup</td><td style="border: 1px solid black; padding: 8px; text-align: center;">High level incident category</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - 3 à 5 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">StopCodeDescription</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Detailed incident category</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">SpecialServiceType</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Further detail for special services incident categories</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">PropertyCategory</td><td style="border: 1px solid black; padding: 8px; text-align: center;">High level property descriptor</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - 5 à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">PropertyType</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Detailed property descriptor</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">AddressQualifier</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Qualifies location of actual incident relevant to category above</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">Postcode_full</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Postcode</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">Postcode_district</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Postcode District</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">UPRN</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Unique Property Reference Number</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">USRN</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Unique Street Reference Number</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">IncGeo_BoroughCode</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Borough Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">IncGeo_BoroughName</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Borough Name</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">ProperCase</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Borough Name</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">IncGeo_WardCode</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Ward Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">IncGeo_WardName</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Ward Name</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">IncGeo_WardNameNew</td><td style="border: 1px solid black; padding: 8px; text-align: center;">New Ward Name</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">Easting_m</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Easting</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">Northing_m</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Northing</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">Easting_rounded</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Easting rounded up to nearest 50</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">Northing_rounded</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Northing rounded up to nearest 50</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">Latitude</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Latitude</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">Longitude</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Longitude</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">FRS</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Fire Service ground</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Valeur unique</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentStationGround</td><td style="border: 1px solid black; padding: 8px; text-align: center;">LFB Station ground</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #F7EAD9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">FirstPumpArriving_AttendanceTime</td><td style="border: 1px solid black; padding: 8px; text-align: center;">First Pump attendance time in seconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quantitative</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">FirstPumpArriving_DeployedFromStation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">First Pump deployed from station</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #F7EAD9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">SecondPumpArriving_AttendanceTime</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Second Pump attendance time in seconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quantitative</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">SecondPumpArriving_DeployedFromStation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Second Pump deployed from station</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">NumStationsWithPumpsAttending</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Number of stations with pumps in attendance</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">NumPumpsAttending</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Number of pumps in attendance</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                     <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PumpCount</td><td style="border: 1px solid black; padding: 8px; text-align: center;">No metadata</td><td style="border: 1px solid black; padding: 8px; text-align: center;"></td></tr>
                    <tr style="background-color: #F7EAD9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">PumpMinutesRounded</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Time spent at incident by pumps, rounded up to 60 if less than an hour</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quantitative</td></tr>
                    <tr style="background-color: #F7EAD9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">Notional Cost (£)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Time spent multiplied by notional annual cost of a pump</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quantitative</td></tr>
                    <tr style="background-color: #F7EAD9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">NumCalls</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Number of calls received about the incident</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quantitative</td></tr>
                </tbody>
            </table>
            """
            st.markdown(html_incident, unsafe_allow_html=True)
            
            st.markdown("<h5>Dataset Mobilisation</h5>", unsafe_allow_html=True)
            st.markdown("""
            - Dataset (4) LFB Mobilisation data from January 2009 – 2014.xslx
            Ce jeu de données reprend toutes les informations relatives aux interventions des pompiers entre 2009 et 2014.
            Ce jeu comporte 901788 entrées, pour 22 colonnes.<br>
            - Dataset (5) LFB Mobilisation data from 2015 – 2020.csv
            Ce jeu de données reprend toutes les informations relatives aux interventions des pompiers entre 2015 et 2020.
            Ce jeu comporte 883641 entrées, pour 22 colonnes.<br>
            - Dataset (6) LFB Mobilisation data from 2021 – 2024.csv
            Ce jeu de données reprend toutes les informations relatives aux interventions des pompiers entre 2021 et 2024.
            Ce jeu comporte 727747 entrées, pour 24 colonnes.
            Sur ce jeu de données, les colonnes “date” (en bleu dans le tableau ci-dessous) ne sont pas au bon format, nous modifierons ce point lors du preprocessing.<br>
            Les différentes colonnes de ces jeux de données reprennent les informations suivantes :
            """, unsafe_allow_html=True)
            html_mobilisation = """
            <table style="width: 100%; border-collapse: collapse; margin: 20px auto;">
                <thead>
                    <tr>
                        <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Nom de la colonne</th>
                        <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Description</th>
                        <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Type de variable</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentNumber</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Numéro d'incident (index)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">CalYear</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Année d'enregistrement</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - 3 à 5 catégories</td></tr>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">BoroughName*</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Nom de la personne</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">WardName*</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quartier de l'incident</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">HourOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Heure de l'appel</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">ResourceMobilisationId</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Id des ressources mobilisées</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">Resource_Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code de ces ressources</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">PerformanceReporting</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Notation de la performance</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - 3 à 5 catégories</td></tr>
                    <tr style="background-color: #D9EAF7;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeMobilised</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure de la mobilisation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Temporelle</td></tr>
                    <tr style="background-color: #D9EAF7;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeMobile</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure du départ de la caserne</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Temporelle</td></tr>
                    <tr style="background-color: #D9EAF7;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeArrived</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure d'arrivée</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Temporelle</td></tr>
                    <tr style="background-color: #F7EAD9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">TurnoutTimeSeconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Durée entre mobilisation et départ (secondes)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quantitative</td></tr>
                    <tr style="background-color: #F7EAD9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">TravelTimeSeconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Durée du trajet (secondes)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quantitative</td></tr>
                    <tr style="background-color: #F7EAD9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">AttendanceTimeSeconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Temps de présence (secondes)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quantitative</td></tr>
                    <tr style="background-color: #D9EAF7;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeLeft</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure de départ du lieu d'inter</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Temporelle</td></tr>
                    <tr style="background-color: #D9EAF7;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeReturned</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure de retour à la caserne</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Temporelle</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DeployedFromStation_Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code de la station de déploiement</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DeployedFromStation_Name</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Nom de la station de déploiement</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DeployedFromLocation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Lieu de départ du déploiement</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - Binaire</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">PumpOrder</td><td style="border: 1px solid black; padding: 8px; text-align: center;">No metadata</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">PlusCode_Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code Mobilisation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - 3 à 5 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">PlusCode_Description</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Description Mobilisation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - 3 à 5 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DelayCodeId</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code de retard pour intervention</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - 5 à 10 catégories</td></tr>
                    <tr style="background-color: #EAF7D9;"><td style="border: 1px solid black; padding: 8px; text-align: center;">DelayCode_Description</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Commentaires sur ce retard</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Catégorielle - sup. à 10 catégories</td></tr>
                </tbody>
            </table>
            """

            st.markdown(html_mobilisation, unsafe_allow_html=True)

            st.write("*Colonnes uniquement présentes dans Dataset (6) LFB Mobilisation data from 2021 – 2024.csv")
            
            # st.markdown("<h4>5. Traitement des données</h4>", unsafe_allow_html=True)
            st.markdown("<h4>3. Ajout de variables</h4>", unsafe_allow_html=True)
            st.markdown("""
            Pour alimenter et réduire la complexité de notre jeu de données, nous avons procédé à des ajouts de variables.<br>
            - ResponseTime : Somme des colonnes TurnoutTimeSeconds (temps de mobilisation des pompiers) et TravelTimeSeconds (temps de trajet des pompiers).<br>
            - Jour de la semaine / Numéro de la semaine / Mois : Obtenues à partir de la colonne DateAndTimeMobilised.<br>
            - PropertyCategory_bis : Split en 3 catégories de PropertyCategory, les deux les plus présentes et regroupement des autres catégories dans une catégorie other.<br>
            - AddressQualifier_bis : Split en 3 catégories de AddressQualifier, les deux les plus présentes et regroupement des autres catégories dans une catégorie other.<br><br>
            """, unsafe_allow_html=True)
            # Ouvre l'image et encode en base64
            with open("NicePng_arrow-png_101114.png", "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode()
            st.markdown(f"""
                <div style="text-align: left; margin-top: 0px;">
                    <a href="#haut">
                        <img src="data:image/png;base64,{img_base64}" alt="Retour en haut" width="25" />
                    </a>
                </div>
            """, unsafe_allow_html=True)

        
        elif choix_colonnes == "Colonnes utilisées pour la modélisation":
            
            html_incident_modelisation2 = """
            <table style="width: 100%; border-collapse: collapse; margin: 20px auto;">
              <thead>
                <tr>
                  <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Nom de la colonne</th>
                  <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Description</th>
                  <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Source</th>
                </tr>
              </thead>
              <tbody>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">CalYear</td><td style="border: 1px solid black; padding: 8px; text-align: center;">année d'enregistrement</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Incident & Mobilisation</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HourOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Heure de l'appel</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Incident & Mobilisation</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DeployedFromLocation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Lieu de départ du déploiement</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Mobilisation</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PlusCode_Description</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Description Mobilisation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Mobilisation</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">ResponseTime</td><td style="border: 1px solid black; padding: 8px; text-align: center;">addition des colonnes TurnoutTimeSeconds et TravelTimeSeconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Mobilisation</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Day</td><td style="border: 1px solid black; padding: 8px; text-align: center;">jour de la semaine</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Dataset secondaire</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentGroup</td><td style="border: 1px solid black; padding: 8px; text-align: center;">High level incident category</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Incident</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">NumCalls</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Number of calls received about the incident</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Incident</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DistanceMetrique</td><td style="border: 1px solid black; padding: 8px; text-align: center;">calcul de la distance entre incident et station de pompiers</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Dataset secondaire</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Month</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Mois de l'année</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Dataset secondaire</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Week</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Semaine de l'année</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Dataset secondaire</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">gpe_geo</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Orientation géographique (sud-est, sud-ouest, nord-est, nord-ouest)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Dataset secondaire</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PropertyCategory_bis</td><td style="border: 1px solid black; padding: 8px; text-align: center;">reprend la variable PropertyCategory séparée en 3 catégories</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Incident</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">AddressQualifier_bis</td><td style="border: 1px solid black; padding: 8px; text-align: center;">reprend la variable AddressQualifier séparée en 3 catégories</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Incident</td></tr>
              </tbody>
            </table>


            """

            st.markdown(html_incident_modelisation2, unsafe_allow_html=True)
             # Ouvre l'image et encode en base64
            with open("NicePng_arrow-png_101114.png", "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode()
            st.markdown(f"""
                <div style="text-align: left; margin-top: 0px;">
                    <a href="#haut">
                        <img src="data:image/png;base64,{img_base64}" alt="Retour en haut" width="25" />
                    </a>
                </div>
            """, unsafe_allow_html=True)
        elif choix_colonnes == "Colonnes non utilisées":
            st.markdown("<h5>Dataset Incident</h5>", unsafe_allow_html=True)
            html_incident_non_utilisé = """
            <table style="width: 100%; border-collapse: collapse; margin: 20px auto;">
              <thead>
                <tr>
                  <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Nom de la colonne</th>
                  <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Description</th>
                </tr>
              </thead>
              <tbody>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentNumber</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Numéro d'incident (index)</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date de l'appel</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">TimeOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Heure de l'appel (hh:mm:ss)</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">StopCodeDescription</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Detailed incident category</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">SpecialServiceType</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Further detail for special services incident categories</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PropertyCategory</td><td style="border: 1px solid black; padding: 8px; text-align: center;">High level property descriptor</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PropertyType</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Detailed property descriptor</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">AddressQualifier</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Qualifies location of actual incident relevant to category above</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Postcode_full</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Postcode</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Postcode_district</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Postcode District</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">UPRN</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Unique Property Reference Number</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">USRN</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Unique Street Reference Number</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncGeo_BoroughCode</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Borough Code</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncGeo_BoroughName</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Borough Name</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">ProperCase</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Borough Name</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncGeo_WardCode</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Ward Code</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncGeo_WardName</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Ward Name</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncGeo_WardNameNew</td><td style="border: 1px solid black; padding: 8px; text-align: center;">New Ward Name</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Easting_m</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Easting</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Northing_m</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Northing</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Easting_rounded</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Easting rounded up to nearest 50</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Northing_rounded</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Northing rounded up to nearest 50</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Latitude</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Latitude</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Longitude</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Longitude</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">FRS</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Fire Service ground</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentStationGround</td><td style="border: 1px solid black; padding: 8px; text-align: center;">LFB Station ground</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">FirstPumpArriving_AttendanceTime</td><td style="border: 1px solid black; padding: 8px; text-align: center;">First Pump attendance time in seconds</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">FirstPumpArriving_DeployedFromStation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">First Pump deployed from station</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">SecondPumpArriving_AttendanceTime</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Second Pump attendance time in seconds</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">SecondPumpArriving_DeployedFromStation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Second Pump deployed from station</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">NumStationsWithPumpsAttending</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Number of stations with pumps in attendance</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">NumPumpsAttending</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Number of pumps in attendance</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PumpCount</td><td style="border: 1px solid black; padding: 8px; text-align: center;">No metadata</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PumpMinutesRounded</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Time spent at incident by pumps, rounded up to 60 if less than an hour</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Notional Cost (£)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Time spent multiplied by notional annual cost of a pump</td></tr>
              </tbody>
            </table>


            """

            st.markdown(html_incident_non_utilisé, unsafe_allow_html=True)
        
            st.markdown("<h5>Dataset Mobilisation</h5>", unsafe_allow_html=True)
            html_mobilisation_non_utilisé = """
            <table style="width: 100%; border-collapse: collapse; margin: 20px auto;">
              <thead>
                <tr>
                  <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Nom de la colonne</th>
                  <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Description</th>
                </tr>
              </thead>
              <tbody>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentNumber</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Numéro d'incident (index)</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">BoroughName</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Nom de la personne</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">WardName</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quartier de l'incident</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">ResourceMobilisationId</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Id des ressources mobilisées</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Resource_Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code de ces ressources</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PerformanceReporting</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Notation de la performance</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeMobilised</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure de la mobilisation</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeMobile</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure du départ de la caserne</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeArrived</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure d'arrivée</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">TurnoutTimeSeconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Durée entre mobilisation et départ (secondes)</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">TravelTimeSeconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Durée du trajet (secondes)</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">AttendanceTimeSeconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Temps de présence (secondes)</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeLeft</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure de départ du lieu d'intervention</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeReturned</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure de retour à la caserne</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DeployedFromStation_Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code de la station de déploiement</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DeployedFromStation_Name</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Nom de la station de déploiement</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PumpOrder</td><td style="border: 1px solid black; padding: 8px; text-align: center;">No metadata</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PlusCode_Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code Mobilisation</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DelayCodeId</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code de retard pour intervention</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DelayCode_Description</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Commentaires sur ce retard</td></tr>
              </tbody>
            </table>



            """

            st.markdown(html_mobilisation_non_utilisé, unsafe_allow_html=True)
             # Ouvre l'image et encode en base64
            with open("NicePng_arrow-png_101114.png", "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode()
            st.markdown(f"""
                <div style="text-align: left; margin-top: 0px;">
                    <a href="#haut">
                        <img src="data:image/png;base64,{img_base64}" alt="Retour en haut" width="25" />
                    </a>
                </div>
            """, unsafe_allow_html=True)

    elif choix == "Dataset Secondaire":
        st.markdown("<h4>Dataset Secondaire</h4>", unsafe_allow_html=True)
        st.markdown("<h4>1. Adresse de stations de pompiers londoniennes</h4>", unsafe_allow_html=True)
        st.markdown("""
        Ce dataset additionnel enrichit notre jeu de données avec les adresses des stations présentes dans la colonne 
        DeployedFromStation du dataset Mobilisation ainsi que leur coordonnées GPS en latitude/longitude et en easting/northing.
Les adresses des stations proviennent du site officiel du gouvernement britannique qui recense toutes les adresses des stations
 en activité à Londres : 
 <a href='https://www.london-fire.gov.uk/community/your-borough/' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>London Fire Brigade</a>
Certaines stations présentes dans notre dataset Mobilisation ont été fermées, leurs adresses ont été obtenues par une recherche sur google. 
<br><h5>Ajout des variables</h5>Les coordonnées GPS de ces stations ont été obtenues grâce à des librairies python, Photon pour obtenir les coordonnées GPS 
en latitude/longitude et Transformer pour les transformer au format easting/northing.


Ce jeu comporte 110 entrées, pour 6 colonnes. :<br>

        """, unsafe_allow_html=True)
        html_station_adress = """
        <table style="width: 100%; border-collapse: collapse; margin: 20px auto;">
            <thead>
                <tr>
                    <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Nom de la colonne</th>
                    <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">DeployedFromStation</td>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Nom de la station de déploiement</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Address</td>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Adresse de la station de déploiement</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Station_Latitude</td>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Coordonnées GPS de la station de déploiement en latitude</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Station_Longitude</td>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Coordonnées GPS de la station de déploiement en longitude</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Station_Easting</td>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Coordonnées GPS de la station de déploiement format easting</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Station_Northing</td>
                    <td style="border: 1px solid black; padding: 8px; text-align: center;">Coordonnées GPS de la station de déploiement format northing</td>
                </tr>
            </tbody>
        </table>
        """

        # Afficher le tableau HTML
        st.markdown(html_station_adress, unsafe_allow_html=True)
        st.markdown("<h4>2. Groupe géographique des quartiers londoniens</h4>", unsafe_allow_html=True)
        st.markdown("""
        Ce dataset reprend les correspondances entre les quartiers et les groupes géographiques pour les différents quartiers présents dans les datasets Incident et Mobilisation.
Il comporte 34 entrées et 2 colonnes.
<br>

        """, unsafe_allow_html=True)
        html_gpegeo = """
        <table style="width: 100%; border-collapse: collapse; margin: 20px auto;">
            <thead>
                <tr>
                    <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Borough</th>
                    <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">GPE Geo</th>
                </tr>
            </thead>
            <tbody>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">LAMBETH</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HARROW</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">WESTMINSTER</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">BROMLEY</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">BARNET</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">SOUTHWARK</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">KINGSTON UPON THAMES</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HILLINGDON</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">CAMDEN</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">BRENT</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">KENSINGTON AND CHELSEA</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">RICHMOND UPON THAMES</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HAVERING</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">CROYDON</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">LEWISHAM</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">ENFIELD</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">GREENWICH</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">BEXLEY</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">BARKING AND DAGENHAM</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">CITY OF LONDON</td><td style="border: 1px solid black; padding: 8px; text-align: center;">London</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">WALTHAM FOREST</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">EALING</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HACKNEY</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">NEWHAM</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HOUNSLOW</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">ISLINGTON</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">TOWER HAMLETS</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HAMMERSMITH AND FULHAM</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">SUTTON</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">MERTON</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">REDBRIDGE</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North East</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">WANDSWORTH</td><td style="border: 1px solid black; padding: 8px; text-align: center;">South West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HARINGEY</td><td style="border: 1px solid black; padding: 8px; text-align: center;">North West</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">NaN</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Other</td></tr>
            </tbody>
        </table>
        """


        # Affichage
        st.markdown(html_gpegeo, unsafe_allow_html=True)
        # Ouvre l'image et encode en base64
        with open("NicePng_arrow-png_101114.png", "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f"""
            <div style="text-align: left; margin-top: 0px;">
                <a href="#haut">
                    <img src="data:image/png;base64,{img_base64}" alt="Retour en haut" width="25" />
                </a>
            </div>
        """, unsafe_allow_html=True)
elif page == pages[2]:
    st.markdown("<a id='haut'></a>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Data Visualisation</h3>", unsafe_allow_html=True)
    #lecture du fichier merge pour la dataviz streamlit
    
    @st.cache_data #ajout du caching decorator pour le chargement du fichier
    def load_data(url):
        df = pd.read_csv(url)
        return df
    
    df_merge = load_data("fichier_dataviz_streamlit.csv")
  
    #séparation de la page en 5 partie pour ajouter les toggle pour chaque partie
    first, second, third, fourth, fifth = st.columns(5)
    
    if first.toggle("Visualisation :calendar:") :
        st.markdown(":blue-background[Visualisations en lien avec des variables de temps et de date] :calendar:")

        x_columns = ['CalYear_x','month', 'week', 'Day', 'HourOfCall_x']
        x_axis_val = st.pills(":blue-background[Selectionner l'échelle de temps]", options=x_columns)
        
        if x_axis_val == None :
            st.text("Rien ne s'affiche ? Il faut choisir une échelle de temps.")
        else:
            df = df_merge.groupby(x_axis_val, as_index=False).agg(mean=("ResponseTime", "mean"))
            mean = df["mean"]
            fig = px.line(df, x=x_axis_val, y=mean, line_shape='linear', range_y=(320,380))
            fig.update_layout(title="Temps de réponse moyen par {}".format(x_axis_val),yaxis_title="Temps de réponse moyen")
            st.plotly_chart(fig)

        if x_axis_val == "CalYear_x" :
        
            expander_first_year = st.expander("Cliquez pour voir l'interprétation")
            expander_first_year.write('<div style="text-align: justify;">Le temps de réponse moyen est stable au cours des années \
                                           et est de 350s.</div>', unsafe_allow_html=True)

            #nombre de mobilisation par année
            df_year = df_merge.groupby(["CalYear_x"], as_index=False).agg(count=("IncidentNumber","count"))  
            #représentation en histogramme avec plotly
            fig1 = px.histogram(df_year,x = 'CalYear_x', y='count',nbins=30, title="Nombre de mobilisations par année")
            fig1.update_layout(bargap=0.2, yaxis_title="Nombre de mobilisations", xaxis_title='Année')
            st.plotly_chart(fig1)

            expander_second_year = st.expander("Cliquez pour voir l'interprétation")
            expander_second_year.write('<div style="text-align: justify;">Baisse du nombre de mobilisations entre 2009 et 2014. Légère augmentation, \
                                           stabilisation jusqu’en 2021 puis forte augmentation jusqu’en 2024.Entre 2019 et 2024 augmentation du nombre de \
                                            mobilisation de 28.64%.</div>', unsafe_allow_html=True)

            #analyse temps moyen de mobilisation et de trajet par année
            year_travel_time = df_merge.groupby("CalYear_x")["TravelTimeSeconds"].mean()
            year_turnout_time = df_merge.groupby("CalYear_x")["TurnoutTimeSeconds"].mean()
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x = year_travel_time.index, y = year_travel_time.values,mode='lines',name='TravelTimeSeconds', line=dict(color='Indigo')))
            fig2.add_trace(go.Scatter(x = year_turnout_time.index, y = year_turnout_time.values,mode='lines',name='TurnoutTimeSeconds', line=dict(color='LightBlue')))
            fig2.update_layout(title='Temps moyen de mobilisation et de trajet par année', yaxis_title='Temps moyen', xaxis_title='Année')
            st.plotly_chart(fig2)

            expander_third_year = st.expander("Cliquez pour voir l'interprétation")
            expander_third_year.write('<div style="text-align: justify;">Le temps de mobilisation a baissé entre 2009 et 2012 et est resté constant depuis. \
                                      Le temps de trajet présente plus de variabilité avec une augmentation entre 2009 et 2014 et reste relativement \
                                      constant depuis 2014.</div>', unsafe_allow_html=True)

        elif x_axis_val == "month" :

            #analyse de la répartition des temps de mobilisation et trajet par mois
            @st.cache_data #ajout du caching decorator pour le chargement du graph
            def afficher_fig21():
                fig21 = go.Figure()
                fig21.add_trace(go.Box(x=df_merge['month'], y=df_merge['TurnoutTimeSeconds'], name='Mobilisation'))
                fig21.add_trace(go.Box(x=df_merge['month'], y=df_merge['TravelTimeSeconds'], name='Trajet'))
                fig21.update_layout(title="Répartition des temps de mobilisation et trajet par mois", boxmode='group')
                st.plotly_chart(fig21)
            afficher_fig21()

            expander_first_month = st.expander("Cliquez pour voir l'interprétation")
            expander_first_month.write('<div style="text-align: justify;">Le temps de réponse moyen et le temps de trajet moyen par mois sont très stables. \
                                       La répartition est également très stable sur les temps de mobilisation et de trajet avec une médiane entre \
                                       72 et 74 secondes pour la mobilisation et 241 à 256 secondes pour le temps de trajet. On constate \
                                       un certain nombre de valeurs extrêmes qui peuvent s’expliquer par des difficultés de traffic, de localisation de l’incident \
                                       pour les valeurs extrêmes de trajet et pour des raisons telles que "en service à l’extérieur" ou "en exercice" pour les valeurs \
                                       extrêmes de mobilisation. </div>', unsafe_allow_html=True)

        elif x_axis_val == "week" :

            #Répartition des temps de réponse par semaine
            @st.cache_data #ajout d'un cache decorator pour le chargement de la figure 8
            def afficher_fig8():
                fig8 = px.box(x=df_merge['week'], y=df_merge['ResponseTime'], title='Répartition des temps de réponse par semaine')
                fig8.update_layout(xaxis_title='Semaine', yaxis_title='Temps de réponse')
                st.plotly_chart(fig8)
            afficher_fig8()

            expander_first_week = st.expander("Cliquez pour voir l'interprétation")
            expander_first_week.write('<div style="text-align: justify;">Le temps de réponse moyen est très stable tout au long de l’année. \
                                      On note tout de même une très légère baisse en fin d’année. La répartition du responsetime est également très stable \
                                      avec une légère diminution des valeurs médiane et maximale en fin d’année.</div>', unsafe_allow_html=True)

        elif x_axis_val == "Day" :
        
            #analyse du temps de trajet moyen par jour de la semaine
            day_response_time = df_merge.groupby(["Day","CalYear_x"], as_index=False).agg(mean=("ResponseTime",'mean'))
            mean=day_response_time['mean']
            fig9 = px.bar(x=day_response_time['Day'], y=mean, title='Temps de réponse moyen par jour de la semaine', animation_frame=day_response_time['CalYear_x'])
            fig9.update_layout(xaxis_title='Jour', yaxis_title='Temps de réponse moyen')
            st.plotly_chart(fig9)

            expander_first_day = st.expander("Cliquez pour voir l'interprétation")
            expander_first_day.write('<div style="text-align: justify;">Les pompiers interviennent plus rapidement le dimanche que les autres jours de la semaine, \
                                      probablement dû à un trafic routier réduit.</div>', unsafe_allow_html=True)

        elif x_axis_val == "HourOfCall_x" :
        
            #analyse du temps de réponse moyen par heure de la journée, évolution par année
            hour_response_time = df_merge.groupby(["HourOfCall_x", "CalYear_x"],as_index=False).agg(mean=("ResponseTime","mean"))
            mean = hour_response_time["mean"]
            fig11 = px.bar(x=hour_response_time.HourOfCall_x, y=mean, 
                title='Temps de réponse moyen par heure',
                animation_frame = hour_response_time["CalYear_x"])
            fig11.update_layout(xaxis_title='Heure', yaxis_title='Temps de réponse')
            st.plotly_chart(fig11)

            expander_first_hour = st.expander("Cliquez pour voir l'interprétation")
            expander_first_hour.write('<div style="text-align: justify;">Le temps de réponse moyen est fonction de l’heure de la journée, \
                                      avec un temps de réponse minimum à 22h (330s).</div>', unsafe_allow_html=True)

    if second.toggle("Visualisation :fire_engine:") :
        st.markdown(":blue-background[Analyse par type d'incident] :fire_engine:")
    
        #affichage du nombre d'intervention par 'IncidentGroup' et par année
        nb_incident_by_group = df_merge.groupby(["IncidentGroup","CalYear_x"], as_index=False).agg(
            count=("IncidentGroup","count"))      
        fig12 = px.pie(nb_incident_by_group, values='count',names='IncidentGroup',
                       color_discrete_map={'False Alarm':'royalblue', 'Special Service':'LightBlue', 'Fire':'FireBrick'},
                       title="Nombre d'incident par groupe d'incident",)
        fig12.update_layout(xaxis_title='CalYear',yaxis_title='IncidentGroup')
        st.plotly_chart(fig12)

        #affichage du responsetime moyen par 'IncidentGroup' et par année
        resptime_incident_by_group = df_merge.groupby(["IncidentGroup","CalYear_x"], as_index=False).agg(mean=("ResponseTime","mean"))
        fig13 = px.bar(x = resptime_incident_by_group["IncidentGroup"] ,y = resptime_incident_by_group['mean'],
             title="Temps moyen de réponse par groupe d'incident",
             animation_frame = resptime_incident_by_group['CalYear_x'])
        fig13.update_layout(xaxis_title='CalYear',yaxis_title='Mean ResponseTime')
        st.plotly_chart(fig13)

        expander_first_incident = st.expander("Cliquez pour voir l'interprétation")
        expander_first_incident.write('<div style="text-align: justify;">Nombre très important de fausses alertes. Ces fausses alertes regroupent les appels de bonne foi \
                                      ainsi que les appels malveillants. \n \
                                      Le temps de réponse moyen est similaire pour les différentes catégories d’incidents.</div>', unsafe_allow_html=True)

        st.write("\n \n ")

        #affichage du nombre d'intervention par type d'incident dans le groupe 'Special Service' et par année
        fig14 = plt.figure(figsize=(10,5))
        sns.countplot(x = df_merge['SpecialServiceType'], hue = df_merge['CalYear_x'], palette="Spectral")
        plt.title("Nombre d'incident par groupe d'incident Special Service")
        plt.xticks(rotation=90)
        st.pyplot(fig14)

        expander_second_incident = st.expander("Cliquez pour voir l'interprétation")
        expander_second_incident.write('<div style="text-align: justify;">Les types d’interventions majoritaires sont Effecting entry/exit, RTC, Flooding. \
                Sur les années plus récentes on remarque également les types Assist other agencies et no action. Le nombre important de catégories dans cette variable \
                imposera peut-être de ne pas la garder ou de la transformer pour la modélisation.</div>', unsafe_allow_html=True)

    if third.toggle("Visualisation :globe_with_meridians:") :
        st.markdown(":blue-background[Analyses en lien avec des variables géographique] :globe_with_meridians:")

        #Nombre de mobilisation par groupe géographique par année
        df_merge_geo = df_merge.groupby(["gpe_geo","CalYear_x"], as_index=False).agg(
            count=("gpe_geo","count"))
        plt.figure(figsize=[200,200])
        fig15 = px.density_heatmap(df_merge, x='CalYear_x', y='gpe_geo', z='IncidentNumber',histfunc='count', color_continuous_scale='dense')
        fig15.update_layout(title="Nombre de mobilisations par groupe géographique par année", xaxis_title='Year',yaxis_title='gpe_geo')
        st.plotly_chart(fig15)

        expander_first_geo = st.expander("Cliquez pour voir l'interprétation")
        expander_first_geo.write('<div style="text-align: justify;">Le nombre de mobilisations est plus important à l’ouest et particulièrement au nord ouest. \
                                 On constate une baisse significative des interventions en 2015 toutes zones confondues puis une augmentation constante à partir \
                                    de 2015.</div>', unsafe_allow_html=True)

        #Responsetime moyen par groupe géographique et par année
        df_merge_geo_resptim = df_merge.groupby(["gpe_geo","CalYear_x"], as_index=False).agg(
            moyenne_temps=("ResponseTime","mean"))
        #graphique de df_merge_geo_resptim
        fig16 = px.bar(x=df_merge_geo_resptim['gpe_geo'], y=df_merge_geo_resptim['moyenne_temps'], animation_frame=df_merge_geo_resptim['CalYear_x'])
        fig16.update_layout(title="Temps moyen de réponse par groupe géographique par année", xaxis_title="gpe_geo", yaxis_title="moyenne_temps")
        st.plotly_chart(fig16)

        #Nombre de mobilisation par groupe géographique et par quartier
        df_merge_boroughcount = df_merge.groupby(['gpe_geo','IncGeo_BoroughName'], as_index=False).agg(count=('IncGeo_BoroughName','count'),mean_resptime=('ResponseTime','mean'))
        count = df_merge_boroughcount['count']
        mean_resptime = df_merge_boroughcount['mean_resptime']
        plt.figure(figsize=[200,200])
        fig20 = px.treemap(df_merge_boroughcount, path=[px.Constant("FRS"), 'gpe_geo','IncGeo_BoroughName'],values=count,
                           color=mean_resptime,
                           color_continuous_scale='dense')
        fig20.update_layout(margin=dict(t=50, l=25, r=25, b=25), title="Répartition du nombre d'incident et du temps de réponse moyen par quartier")
        st.plotly_chart(fig20)

        expander_second_geo = st.expander("Cliquez pour voir l'interprétation")
        expander_second_geo.write('<div style="text-align: justify;">Le temps de réponse moyen est similaire pour toutes les zones géographiques. \
                                  On constate une légère différence sur la zone ouest entre le nord et le sud, le temps de réponse moyen au sud étant \
                                  légèrement plus bas, ce qui peu s’expliquer par un nombre de mobilisation plus important au nord. \n \
                                  En revanche le temps de réponse moyen au nord-est est plus important qu’au sud-ouest malgré un nombre de mobilisation \
                                  moins important. Ceci peut s’expliquer par un nombre de stations plus important au sud qu’au nord.</div>', unsafe_allow_html=True)
        expander_second_geo.image("nombre_stations.png")

        #visualisation de distancemetrique vs responsetime avec plotly express
        @st.cache_data #ajout du caching decorator pour le chargement du graph
        def afficher_fig17():
            fig17 = sns.relplot(x = "ResponseTime", y = "DistanceMetrique", kind = 'line', data = df_merge)
            plt.title("DistanceMetrique vs ResponseTime")
            st.pyplot(fig17)
        afficher_fig17()

        expander_third_geo = st.expander("Cliquez pour voir l'interprétation")
        expander_third_geo.write('<div style="text-align: justify;">Ce graphique qui affiche la distance en fonction du temps de réponse moyen montre qu’il y a \
                                 3 catégories distinctes de temps d’intervention : entre 0 et 200s les distances d’intervention sont comprises entre 0 et 2km \
                                 et pas de relation directe avec le temps d’intervention, idem entre 600 et 1200s. Entre 200s et 600s on observe une relation \
                                 proportionnelle entre le temps de réponse et la distance entre le lieu de l’incident et la station de \
                                 pompiers.</div>', unsafe_allow_html=True)

    if fourth.toggle("Visualisation :fire_extinguisher:"):
        st.markdown(":blue-background[Autres analyses] :fire_extinguisher:")
    
        #analyse du nombre d'incident par AdressQualifier
        df_merge_address = df_merge.groupby(["AddressQualifier","CalYear_x"], as_index=False).agg(
            count=("AddressQualifier","count"))

        fig18 = px.bar(x = df_merge_address['AddressQualifier'], y=df_merge_address['count'], animation_frame=df_merge_address['CalYear_x'])
        fig18.update_layout(title="Nombre d'incident par type d'adresse", xaxis_title='AddressQualifier',yaxis_title='count')
        st.plotly_chart(fig18)
        
        expander_first_autre = st.expander("Cliquez pour voir l'interprétation")
        expander_first_autre.write('<div style="text-align: justify;">Les catégories les plus représentées sont ‘Correct location’ et ‘Within same building’. \
                                   Nous pourrons créer une nouvelle variable “AdressQualifier_bis” dans laquelle nous garderons ces deux catégories et \
                                   rassemblerons toutes les autres dans une variable ‘other’.</div>', unsafe_allow_html=True)

        #Analyse du nombre de stations mobilisées par année
        df_merge_year = df_merge.groupby(["CalYear_x"], as_index=False).agg(
            count=("DeployedFromStation_Name","nunique"))

        fig19 = px.bar(x=df_merge_year['CalYear_x'], y=df_merge_year['count'])
        fig19.update_layout(title="Nombre de stations mobilisées par année", xaxis_title='CalYear',yaxis_title='count')
        st.plotly_chart(fig19)

        expander_second_autre = st.expander("Cliquez pour voir l'interprétation")
        expander_second_autre.write('<div style="text-align: justify;">Très légère baisse du nombre de stations mobilisées sur les dernières années. \
                                    A partir de 2015, il y aura 8 stations en moins.</div>', unsafe_allow_html=True)

    if fifth.toggle("Visualisation :chart:") :
        st.markdown(":blue-background[Test de corrélation] :chart:")

        tests = ["Matrices de corrélation", "Tests statistiques"]
        selection = st.segmented_control("", tests)

        if selection == "Matrices de corrélation":
            st.write("Matrice de corrélation en incluant le regroupement géographique")
            #remplacement des valeurs de gpe_geo par 1,2,3,4,5 pour la prise en compte dans la matrice de corrélation
            df_corr = df_merge
            df_corr['gpe_geo'] = df_corr['gpe_geo'].replace({'North East': 1, 'North West': 2, 'South East': 3, 'South West': 4, 'London': 5})
            #selection des variables numériques de df_final pour application dans la matrice
            df_num = df_corr[['CalYear_x','HourOfCall_x','TurnoutTimeSeconds', 'TravelTimeSeconds', 'ResponseTime','NumCalls', 'gpe_geo', 'week', 'month']]
            #affichage d'une heatmap sur df_num
            fig22, ax = plt.subplots()
            ax = sns.heatmap(df_num.corr(), annot=True)
            st.pyplot(fig22)
            matrice1 = st.checkbox("Voir l'interprétation")
            if matrice1:
                st.write('<div style="text-align: justify;">Cette première matrice nous permet de voir que la variable cible ResponseTime ne présente pas de corrélation avec les autres variables numériques \
                         hormis les variables ayant été utilisées pour sa création (TravelTimeSeconds et TurnoutTimeSeconds). \
                         Sur ces deux variables on constate que l’une a plus de poids dans la variable cible, il s’agit de TravelTimeSeconds. \
                         Ce point est cohérent avec les visualisations qui ont pu être faites, TravelTime présentant plus de variabilité et étant numériquement plus élevée, \
                         il est logique que celle-ci impacte plus le temps de réponse global. \
                         Cependant il nous manque une variable dans cette matrice, la distance métrique.</div>', unsafe_allow_html=True)
            st.markdown(":blue-background[------------------------------------------------------------------------------------------------------------------------------------------]",width="content")
            st.write("Matrice de corrélation en incluant Distance Metrique")
            df_corr = df_merge
            #selection des variables numériques de df_final pour application dans la matrice
            df_num = df_corr[['CalYear_x','HourOfCall_x', 'ResponseTime','NumCalls', 'DistanceMetrique', 'week', 'month']]
            #affichage d'une heatmap sur df_num
            fig23, ax = plt.subplots()
            ax = sns.heatmap(df_num.corr(), annot=True)
            st.pyplot(fig23)
            matrice2 = st.checkbox("Voir  l'interprétation")
            if matrice2:
                st.write('<div style="text-align: justify;">Sur cette seconde matrice on constate que la variable présentant le plus de corrélation avec ResponseTime est DistanceMetrique.</div>', unsafe_allow_html=True)

        if selection == "Tests statistiques":
            st.markdown("**Test ANOVA**")
            st.write('<div style="text-align: justify;">Toutes les variables catégorielles testées ont un effet significatif sur la variable cible ResponseTime. \
                     Cela peut s’expliquer car un très grand nombre d’observations (ici, > 2,4 millions entrées), \
                     même un effet minuscule devient statistiquement significatif.</div>', unsafe_allow_html=True)
            view_ANOVA_result = st.checkbox("Voir les résultats brut ANOVA")
            if view_ANOVA_result:
                result = statsmodels.formula.api.ols('ResponseTime ~ CalYear_x + HourOfCall_x + DeployedFromLocation + PlusCode_Description', data=df_merge).fit()
                affiche_result = statsmodels.api.stats.anova_lm(result)
                st.write(affiche_result)
            st.markdown(":blue-background[------------------------------------------------------------------------------------------------------------------------------------------]",width="content")
            
            #définition des variables catégorielles
            cat_cols = ['DeployedFromLocation', 'PlusCode_Description', 'Day', 'IncidentGroup', 'PropertyCategory', 'AddressQualifier', 'gpe_geo']

            st.markdown("**Test Kruskal**")
            st.write('<div style="text-align: justify;">Le test de Kruskal-Wallis ne nécessite pas la normalité des données ni l’homogénéité des variances. \
                     Idem que pour l’Anova, toutes les variables testées sauf DeployedFromLocation apparaissent comme ayant un effet significatif\
                      avec la variable cible ResponseTime. Afin de connaitre la contribution relative de chaque variable au modèle, on utilise l’eta squared</div>', unsafe_allow_html=True)
            view_Kruskal_result = st.checkbox("Voir les résultats brut Kruskal")
            if view_Kruskal_result:
                @st.cache_data #ajout du caching decorator pour le chargement et affichage du test Kruskal
                def test_kruskal() :
                    for col in cat_cols:
                        groups = [df_merge[df_merge[col] == val]['DistanceMetrique'].dropna() for val in df_merge[col].unique()]
                        if len(groups) > 1:
                            stat, p = kruskal(*groups)
                            if p < 0.05:
                                st.write(col,": p = ",p," {'(significatif)")
                            else:
                                st.write(col,": p = ",p," {(non significatif)")
                test_kruskal()
            st.markdown(":blue-background[------------------------------------------------------------------------------------------------------------------------------------------]",width="content")
            
            st.markdown("**Test Eta squared**")
            st.write('<div style="text-align: justify;">Afin de connaître la contribution relative de chaque variable au modèle, on utilise l’eta squared. \
                     Une valeur η² > 0.01 est considérée faible, > 0.06 est moyenne, > 0.14 est forte. \
                     Ici toutes nos variables sont < 0.01 et donc non significatives.</div>', unsafe_allow_html=True)
            view_eta_squared_result = st.checkbox("Voir les résultats brut eta_squared")
            if view_eta_squared_result:
                def eta_squared(anova_groups):
                    all_data = np.concatenate(anova_groups)
                    grand_mean = np.mean(all_data)
                    ss_between = sum([len(g) * (np.mean(g) - grand_mean)**2 for g in anova_groups])
                    ss_total = sum((all_data - grand_mean)**2)
                    return ss_between / ss_total
            
                @st.cache_data #ajout du caching decorator pour le chargement et affichage du test Kruskal
                def Eta_squared() :
                    for col in cat_cols:
                        groups = [df_merge[df_merge[col] == val]['DistanceMetrique'].dropna() for val in df_merge[col].unique()]
                        if len(groups) > 1:
                            eta2 = eta_squared(groups)
                            st.write(f"{col} → η² = {eta2:.4f}")
                Eta_squared()

    # Ouvre l'image et encode en base64
    with open("NicePng_arrow-png_101114.png", "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <div style="text-align: left; margin-top: 0px;">
            <a href="#haut">
                <img src="data:image/png;base64,{img_base64}" alt="Retour en haut" width="25" />
            </a>
        </div>
    """, unsafe_allow_html=True)

elif page == pages[3]:
    #lecture du fichier mobilisation v2
    # df10 = pd.read_csv("/content/gdrive/MyDrive/Etudes/DataScientest/Projet/map_station_data.csv")#,sep="\t")
    st.markdown("<h3 style='text-align: center;'>Cartographie des stations de pompiers londoniennes</h3>", unsafe_allow_html=True)
    @st.cache_data
    def load_data():
        return pd.read_csv("map_station_data2.csv")

    df10 = load_data()
    list_years = df10['CalYear_x'].unique()
    print (list_years)

    option = st.selectbox('Année', list_years)
    st.write('L\'année choisie est :', option)
    df_2020 = df10[df10['CalYear_x'] == option]
    choix_carto = st.radio(label="",options=["Nombres d'appels", "Type d'appel","Cout des interventions"],label_visibility="collapsed")
    if choix_carto == "Nombres d'appels":

        
        #st.dataframe(df_2020)

        df2 = df_2020.groupby(['DeployedFromStation_Name','Station_Latitude','Station_Longitude'])['NumCalls'].sum().reset_index()
        df1 = df_2020.groupby('DeployedFromStation_Name')['ResponseTime'].mean().reset_index()

        # Fusion avec le DataFrame principal
        df = df2.merge(df1, on='DeployedFromStation_Name', suffixes=('', '_Avg'))
        #st.dataframe(df)

        # Création de la carte
        m = folium.Map(location=[df.iloc[0]['Station_Latitude'], df.iloc[0]['Station_Longitude']], zoom_start=11)

        for i, row in df.iterrows():
            # Cercle
            folium.CircleMarker(
                location=[row['Station_Latitude'], row['Station_Longitude']],
                radius=row['NumCalls'] / 200,
                color='crimson',
                fill=True,
                fill_color='orange',
                fill_opacity=0.6,
                popup=f"{row['DeployedFromStation_Name']}<br>Appels: {row['NumCalls']:.0f}"
            ).add_to(m)

            # Affichage de la moyenne du temps de réponse
            folium.map.Marker(
                [row['Station_Latitude'], row['Station_Longitude']],
                icon=folium.DivIcon(html=f"""
                    <div style="font-size: 10pt; color: black; text-align: center;
                    transform: translate(-5px, -5px);">
                        {row['ResponseTime']:.0f}
                    </div>
                """)
            ).add_to(m)

        # Affichage de la carte dans Streamlit
        st_folium(m, width=700, height=500)
    elif choix_carto == "Type d'appel":
        options = ["False Alarm", "Special Service", "Fire"]

        choix_multiples = st.multiselect(
            "Type d'appel : Fausse alarme, incendie ou service spécial",
            options
        )

        df12_pivot = pd.crosstab(
            index=[df_2020['DeployedFromStation_Name'], df_2020['Station_Latitude'], df_2020['Station_Longitude']],
            columns=df_2020['IncidentGroup']
        ).reset_index()

        colonnes_fixes = ['DeployedFromStation_Name', 'Station_Latitude', 'Station_Longitude']
        colonnes_selectionnees = [col for col in choix_multiples if col in df12_pivot.columns]
        colonnes_a_afficher = colonnes_fixes + colonnes_selectionnees

        df_affiche = df12_pivot[colonnes_a_afficher].copy()

        if colonnes_selectionnees:
            df_affiche['Total sélection'] = df_affiche[colonnes_selectionnees].sum(axis=1)

            df1 = df_2020.groupby('DeployedFromStation_Name')['ResponseTime'].mean().reset_index()

            df = df_affiche.merge(df1, on='DeployedFromStation_Name', how='left', suffixes=('', '_Avg'))
            if st.checkbox("Afficher le DataFrame"):
                st.dataframe(df)

            m = folium.Map(location=[df.iloc[0]['Station_Latitude'], df.iloc[0]['Station_Longitude']], zoom_start=11)

            for i, row in df.iterrows():
                radius = min(max(row['Total sélection'] / 50, 2), 20)
                
                # Construire le texte détaillé
                details = "".join(
                    f"<li>{col}: {row[col]:.0f}</li>" for col in colonnes_selectionnees
                )
                # Ajouter le texte au popup
                popup_html = f"""
                    <b>{row['DeployedFromStation_Name']}</b><br>
                    <ul>{details}</ul>
                """

                folium.CircleMarker(
                    location=[row['Station_Latitude'], row['Station_Longitude']],
                    radius=radius,
                    color='crimson',
                    fill=True,
                    fill_color='orange',
                    fill_opacity=0.6,
                    popup=Popup(popup_html, max_width=400)  # Par défaut c’est ~300px
                ).add_to(m)

                folium.map.Marker(
                    [row['Station_Latitude'], row['Station_Longitude']],
                    icon=folium.DivIcon(html=f"""
                        <div style="font-size: 10pt; color: black; text-align: center;
                        transform: translate(-5px, -5px);">
                            {row['ResponseTime']:.0f}
                        </div>
                    """)
                ).add_to(m)

            st_folium(m, width=700, height=500)

        else:
            st.warning("Veuillez sélectionner au moins un type d'incident pour afficher la carte.")
    elif choix_carto == "Cout des interventions":
        df2 = df_2020.groupby(['DeployedFromStation_Name','Station_Latitude','Station_Longitude'])['Notional Cost'].sum().reset_index()
        df1 = df_2020.groupby('DeployedFromStation_Name')['ResponseTime'].mean().reset_index()

        # Fusion avec le DataFrame principal
        df = df2.merge(df1, on='DeployedFromStation_Name', suffixes=('', '_Avg'))
        #st.dataframe(df)

        # Création de la carte
        m = folium.Map(location=[df.iloc[0]['Station_Latitude'], df.iloc[0]['Station_Longitude']], zoom_start=11)

        for i, row in df.iterrows():
            # Cercle
            radius = min(max(row['Notional Cost'] / 30000, 2), 25)
            folium.CircleMarker(
                location=[row['Station_Latitude'], row['Station_Longitude']],
                radius=radius,
                color='crimson',
                fill=True,
                fill_color='orange',
                fill_opacity=0.6,
                popup=f"{row['DeployedFromStation_Name']}<br>Couts des interventions: {row['Notional Cost']:.0f}£"
            ).add_to(m)

            # Affichage de la moyenne du temps de réponse
            folium.map.Marker(
                [row['Station_Latitude'], row['Station_Longitude']],
                icon=folium.DivIcon(html=f"""
                    <div style="font-size: 10pt; color: black; text-align: center;
                    transform: translate(-5px, -5px);">
                        {row['ResponseTime']:.0f}
                    </div>
                """)
            ).add_to(m)

        # Affichage de la carte dans Streamlit
        st_folium(m, width=700, height=500)

elif page == pages[4]:
    st.markdown("<a id='haut'></a>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Modélisation</h3>", unsafe_allow_html=True)

    #chargement des packages pour la modélisation
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    import joblib
    from sklearn.model_selection import train_test_split
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import FunctionTransformer

    st.markdown('''Notre variable cible est ResponseTime (variable additionnant le temps de mobilisation et le temps de trajet). 
                Cette variable est numérique et continue, nous faisons donc le **choix de tester des modèles de type régression** pour une première approche de modélisation.''')
    
    st.markdown('''Dans un second temps nous verrons une autre approche conditionnée par les premiers résultats obtenus.''')
    st.markdown(":blue-background[------------------------------------------------------------------------------------------------------------------------------------------]",width="content")
            
    st.markdown("**Paramètres de la première itération :**")
    texte = '''train-test-split avec :
    - Jeu de test : 20%
    - Application d'un random_state afin de figer les jeux d'entrainement et de test pour tous les modèles
                
    Dans un premier temps évaluation uniquement des scores pour déterminer les meilleurs modèles.
    '''
    st.text(texte)
    
    #lecture du fichier pour la modélisation
    @st.cache_data #ajout du caching decorator pour le chargement du fichier
    def load_data_final(url):
        df = pd.read_csv(url)
        return df
    
    df = load_data_final("Dataset_Final.csv")

    ###
    #1ère itération
    ###
    #@st.cache_data #ajout du cache decorator pour le preprocessing
    #def preprocessing_cont(df):
    #    #remplacement des noms des jours de la variable Day par les chiffres correspondant pour faciliter l'encodage des variables temporelles
    #    df['Day'] = df['Day'].replace({'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7})

    #    #sélection des variables explicatives et variables cibles
    #    X = df.drop('ResponseTime', axis = 1)
    #    y = df['ResponseTime']

        #séparation en jeu d'entrainement et de test, on fixe la séparation avec le paramètre random_state
    #    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        ##Préprocessing
        #séparation des colonnes numériques et catégorielles
    #    var_num = ['NumCalls', 'DistanceMetrique']
    #    var_cat = ['CalYear','DeployedFromLocation', 'PlusCode_Description', 'IncidentGroup', 'gpe_geo', 'PropertyCategory_bis', 'AddressQualifier_bis']
    #    var_time = ['HourOfCall', 'week', 'month', 'Day']

    #    X_train_num = X_train[var_num]
    #    X_train_cat = X_train[var_cat]
    #    X_train_time = X_train[var_time]
    #    X_test_num = X_test[var_num]
    #    X_test_cat = X_test[var_cat]
    #    X_test_time = X_test[var_time]

        #gestion des variables temps avec sinus et cosinus (variable cyclique)
    #    def sin_transformer(period):
    #        return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))

    #    def cos_transformer(period):
    #        return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))

    #    for var in X_train_time :
    #        X_train_time[var + '_sin'] = sin_transformer(24).fit_transform(X_train_time[var])
    #        X_train_time[var + '_cos'] = cos_transformer(24).fit_transform(X_train_time[var])
    #        X_train_time = X_train_time.drop(var, axis=1)

    #    for var in X_test_time :
    #        X_test_time[var + '_sin'] = sin_transformer(24).fit_transform(X_test_time[var])
    #        X_test_time[var + '_cos'] = cos_transformer(24).fit_transform(X_test_time[var])
    #        X_test_time = X_test_time.drop(var, axis=1)

    #        X_train_time.reset_index(drop=True, inplace=True)
    #        X_test_time.reset_index(drop=True, inplace=True)

        #remplissage des valeurs manquantes par simple imputer avec la stratégie median pour les variables numériques et le most frequent pour les variables catégorielles
        #gestion des données manquantes pour les variables numériques
    #    imputer_num = SimpleImputer(missing_values=np.nan, strategy='median')
    #    X_train_num = imputer_num.fit_transform(X_train_num)
    #    X_test_num = imputer_num.transform(X_test_num)

        #gestion des données manquantes pour les variables catégorielles
    #    imputer_cat = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    #    X_train_cat = imputer_cat.fit_transform(X_train_cat)
    #    X_test_cat = imputer_cat.transform(X_test_cat)

        #standardisation des variables numériques avec StandardScaler
    #    scaler = StandardScaler()
    #    X_train_num = scaler.fit_transform(X_train_num)
    #    X_test_num = scaler.transform(X_test_num)

        #encodage des variables catégorielles
    #    encoder = OneHotEncoder(drop = 'first', sparse_output=False)
    #    X_train_cat = encoder.fit_transform(X_train_cat)
    #    X_test_cat = encoder.transform(X_test_cat)

        ##passage en dataframe des tableaux récupérés après encodage
    #    X_train_num = pd.DataFrame(X_train_num)
    #    X_test_num = pd.DataFrame(X_test_num)
    #    X_train_cat = pd.DataFrame(X_train_cat)
    #    X_test_cat = pd.DataFrame(X_test_cat)

        #concaténation des jeux d'entraînement et de test
    #    X_train = pd.concat([X_train_num, X_train_cat, X_train_time], axis=1)
    #    X_test = pd.concat([X_test_num, X_test_cat, X_test_time], axis=1)

    #    X_train.columns = X_train.columns.astype(str)
    #    X_test.columns = X_test.columns.astype(str)

    #    return X_train, y_train, X_test, y_test

    #exécution de la fonction de preprocessing
    #X_train, y_train, X_test, y_test = preprocessing_cont(df)

    #chargement des modèles
    #@st.cache_data #ajout du cache decorator pour le chargement des modeles
    #def load_models():
    #    reglog_cont = joblib.load("model_reglog_cont")
    #    reglin_cont = joblib.load("model_reglin_cont")
    #    dtreg_cont = joblib.load("model_dtreg_cont")
    #    rf_reg_cont = joblib.load("model_rfreg_cont.joblib")
    #    ridge_cont = joblib.load("model_ridge_cont")
    #    lasso_cont = joblib.load("model_lasso_cont")
    #    return reglog_cont, reglin_cont, dtreg_cont, rf_reg_cont, ridge_cont, lasso_cont
    
    #reglog_cont, reglin_cont, dtreg_cont, rf_reg_cont, ridge_cont, lasso_cont = load_models()

    #ajout du model reduit 
    #@st.cache_data #ajout du cache decorator pour le preprocessing
    #def preprocessing_cont_red(df):
        #conservation uniquement de distancemetrique, gpe_geo et de la variable cible
    #    df_reduc = df[['DistanceMetrique', 'gpe_geo', 'ResponseTime']]

        #sélection des variables explicatives et variables cibles
    #    X = df_reduc.drop('ResponseTime', axis = 1)
    #    y = df_reduc['ResponseTime']

        #séparation en jeu d'entrainement et de test, on fixe la séparation avec le paramètre random_state
    #    X_train_red, X_test_red, y_train_red, y_test_red = train_test_split(X, y, test_size=0.2, random_state=42)

        ##Adaptation du préprocessing qui ne contient pas de variable temporelles
        #séparation des colonnes numériques et catégorielles
    #    var_num = ['DistanceMetrique']
    #    var_cat = ['gpe_geo']

    #    X_train_red_num = X_train_red[var_num]
    #    X_train_red_cat = X_train_red[var_cat]
    #    X_test_red_num = X_test_red[var_num]
    #    X_test_red_cat = X_test_red[var_cat]

        #remplissage des valeurs manquantes par simple imputer avec la stratégie median pour les variables numériques et le most frequent pour les variables catégorielles
        #gestion des données manquantes pour les variables numériques
    #    imputer_num = SimpleImputer(missing_values=np.nan, strategy='median')
    #    X_train_red_num = imputer_num.fit_transform(X_train_red_num)
    #    X_test_red_num = imputer_num.transform(X_test_red_num)

        #gestion des données manquantes pour les variables catégorielles
    #    imputer_cat = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    #    X_train_red_cat = imputer_cat.fit_transform(X_train_red_cat)
    #    X_test_red_cat = imputer_cat.transform(X_test_red_cat)

        #standardisation des variables numériques avec StandardScaler
    #    from sklearn.preprocessing import StandardScaler

    #    scaler = StandardScaler()
    #    X_train_red_num = scaler.fit_transform(X_train_red_num)
    #    X_test_red_num = scaler.transform(X_test_red_num)

        #encodage des variables catégorielles
    #    from sklearn.preprocessing import OneHotEncoder

    #    encoder = OneHotEncoder(drop = 'first', sparse_output=False)
    #    X_train_red_cat = encoder.fit_transform(X_train_red_cat)
    #    X_test_red_cat = encoder.transform(X_test_red_cat)

        ##passage en dataframe des tableaux récupérés après encodage
    #    X_train_red_num = pd.DataFrame(X_train_red_num)
    #    X_test_red_num = pd.DataFrame(X_test_red_num)
    #    X_train_red_cat = pd.DataFrame(X_train_red_cat)
    #    X_test_red_cat = pd.DataFrame(X_test_red_cat)

        #concaténation des jeux d'entraînement et de test
    #    X_train_red = pd.concat([X_train_red_num, X_train_red_cat], axis=1)
    #    X_test_red = pd.concat([X_test_red_num, X_test_red_cat], axis=1)

    #    X_train_red.columns = X_train_red.columns.astype(str)
    #    X_test_red.columns = X_test_red.columns.astype(str)

    #    return X_train_red, X_test_red, y_train_red, y_test_red

    #exécution de la fonction de preprocessing
    #X_train_red, X_test_red, y_train_red, y_test_red = preprocessing_cont_red(df)

    #chargement des modèles
    #@st.cache_data #ajout du cache decorator pour le chargement des modeles
    #def load_models_red():
    #    rfreg_cont_red = joblib.load("model_rfreg_cont_red.joblib")
    #    return rfreg_cont_red
    #rfreg_cont_red = load_models_red()

    #chargement des scores de chaque modele
    #@st.cache_data #ajout du cache decorator pour le chargement des scores de chaque modele
    #def load_scores():
    #    reglog_cont_score_train = reglog_cont.score(X_train, y_train)
    #    reglog_cont_score_test = reglog_cont.score(X_test, y_test)
    
    #    reglin_cont_score_train = reglin_cont.score(X_train, y_train)
    #    reglin_cont_score_test = reglin_cont.score(X_test, y_test)

    #    dtreg_cont_score_train = dtreg_cont.score(X_train, y_train)
    #    dtreg_cont_score_test = dtreg_cont.score(X_test,y_test)

    #    rf_reg_cont_score_train = rf_reg_cont.score(X_train, y_train)
    #    rf_reg_cont_score_test = rf_reg_cont.score(X_test, y_test)

    #    ridge_cont_score_train = ridge_cont.score(X_train, y_train)
    #    ridge_cont_score_test = ridge_cont.score(X_test, y_test)

    #    lasso_cont_score_train = lasso_cont.score(X_train, y_train)
    #    lasso_cont_score_test = lasso_cont.score(X_test, y_test)

    #    rfreg_cont_red_score_train = rfreg_cont_red.score(X_train_red, y_train_red)
    #    rfreg_cont_red_score_test = rfreg_cont_red.score(X_test_red, y_test_red)

    #    return reglog_cont_score_train, reglog_cont_score_test, reglin_cont_score_train, reglin_cont_score_test, dtreg_cont_score_train, dtreg_cont_score_test, \
    #        rf_reg_cont_score_train, rf_reg_cont_score_test, ridge_cont_score_train, ridge_cont_score_test,lasso_cont_score_train, lasso_cont_score_test, \
    #        rfreg_cont_red_score_train, rfreg_cont_red_score_test

    #reglog_cont_score_train, reglog_cont_score_test, reglin_cont_score_train, reglin_cont_score_test, dtreg_cont_score_train, dtreg_cont_score_test, \
    #    rf_reg_cont_score_train, rf_reg_cont_score_test, ridge_cont_score_train, ridge_cont_score_test,lasso_cont_score_train, lasso_cont_score_test,\
    #        rfreg_cont_red_score_train, rfreg_cont_red_score_test = load_scores()

    #affichage des scores pour comparatif
    results = st.button("Voir les résultats")
    if results :   
        table = st.data_editor([
            {"Modèle":"Régression Logistique", "Train Score" : 0.0148575, "Test Score" : 0.01379},
            {"Modèle":"Régression Linéaire", "Train Score" : 0.3598207230643351, "Test Score" : 0.3734535247570542},
            {"Modèle":"Decision Tree Regressor", "Train Score" : 0.9943303207331452, "Test Score" : -0.30552860823162686},
            {"Modèle":"Random Forest Regressor", "Train Score" : 0.9080998516734331, "Test Score" : 0.37704681657937933},
            {"Modèle":"Bayesian Ridge", "Train Score" : 0.3598201910327483, "Test Score" : 0.3734462383423547},
            {"Modèle":"Lasso Lars", "Train Score" : 0.3593327181107804, "Test Score" : 0.3727512314308593},
            {"Modèle":"Random Forest (nb réduit de variables*)", "Train Score" : 0.576147195832603, "Test Score" : 0.39160453480266266}
        ], column_config={
            "Test Score" : st.column_config.ProgressColumn(
                "Test Score",
                min_value=0,
                max_value=0.8000,
            ),
            "Train Score": st.column_config.ProgressColumn(
                "Train Score",
                min_value=0,
                max_value=0.8000,
            ),
        }, hide_index=True)

        st.markdown("(*)*conservation pour ce modèle uniquement des variables DistanceMetrique et gpe_geo en plus de la variable cible*")

    expander_first_iteration = st.expander("Cliquez pour voir l'interprétation")
    expander_first_iteration.write('<div style="text-align: justify;">Les résultats globaux des scores sur ce premier entrainement de modèles n’est pas concluant, \
                                   y compris en améliorant les paramètres.\n \
                                   Nous constatons sur le modèle RandomForestRegressor que la réduction du nombre de variable \
                                   en ne gardant que celles potentiellement les plus impactantes ne permet pas d’améliorer le score et notamment dégrade le score d’entraînement.\
                                   Nous pouvons en déduire qu’il est nécessaire d’avoir un certain nombre de variables explicatives pour entraîner \
                                   au mieux le modèle. \n \
                                   Il va être nécessaire d’envisager une nouvelle approche.</div>', unsafe_allow_html=True)
    st.markdown(":blue-background[------------------------------------------------------------------------------------------------------------------------------------------]",width="content")
            
    ###
    #ajout des modelisations avec réduction du jeu de données, split
    ###
    ##test avec réduction du jeu de données resptime >200
    #application du filtre sur le jeu de données
    #df200 = df.sample(500000, replace=False)
    #df200 = df200[df200["ResponseTime"] >= 200]
    #df200.dropna(subset=['ResponseTime'], inplace=True)

    #exécution de la fonction de preprocessing
    #X_train_200, y_train_200, X_test_200, y_test_200 = preprocessing_cont(df200)

    #chargement des modèles
    #@st.cache_data #ajout du cache decorator pour le chargement des modeles
    #def load_models_200():
    #    Random_Forest_200 = joblib.load("model_RandomForest_200.joblib")
    #    Ridge_200 = joblib.load("model_Ridge_200")
    #    Lasso_200 = joblib.load("model_Lasso_200")
    #    return Random_Forest_200, Ridge_200, Lasso_200
    #Random_Forest_200, Ridge_200, Lasso_200 = load_models_200()

    ##test avec réduction du jeu de données resptime <600
    #application du filtre sur le jeu de données
    #df600 = df.sample(500000, replace=False)
    #df600 = df600[df600["ResponseTime"] <= 600]
    #df600.dropna(subset=['ResponseTime'], inplace=True)

    #exécution de la fonction de preprocessing
    #X_train_600, y_train_600, X_test_600, y_test_600 = preprocessing_cont(df600)

    #chargement des modèles
    #@st.cache_data #ajout du cache decorator pour le chargement des modeles
    #def load_models_600():
    #    Random_Forest_600 = joblib.load("model_RandomForest_600.joblib")
    #    Ridge_600 = joblib.load("model_Ridge_600")
    #    Lasso_600 = joblib.load("model_Lasso_600")
    #    return Random_Forest_600, Ridge_600, Lasso_600
    #Random_Forest_600, Ridge_600, Lasso_600 = load_models_600()

    ##test avec réduction du jeu de données resptime entre 200 et 600
    #application du filtre sur le jeu de données
    #df200_600 = df.sample(500000, replace=False)
    #df200_600 = df200_600[(df200_600["ResponseTime"] >= 200) & (df200_600["ResponseTime"] <=600)]
    #df200_600.dropna(subset=['ResponseTime'], inplace=True)

    #exécution de la fonction de preprocessing
    #X_train_200_600, y_train_200_600, X_test_200_600, y_test_200_600 = preprocessing_cont(df200_600)

    #chargement des modèles
    #@st.cache_data #ajout du cache decorator pour le chargement des modeles
    #def load_models_200_600():
    #    Random_Forest_200_600 = joblib.load("model_RandomForest_200-600.joblib")
    #    Ridge_200_600 = joblib.load("model_Ridge_200-600")
    #    Lasso_200_600 = joblib.load("model_Lasso_200-600")
    #    return Random_Forest_200_600, Ridge_200_600, Lasso_200_600
    #Random_Forest_200_600, Ridge_200_600, Lasso_200_600 = load_models_200_600()

    ##chargement des scores des différents modeles
    #@st.cache_data #ajout du cache decorator pour le chargement des scores de chaque modele
    #def load_scores_split():
    #    Random_Forest_200_score_train = Random_Forest_200.score(X_train_200, y_train_200)
    #    Random_Forest_200_score_test = Random_Forest_200.score(X_test_200, y_test_200)
    #
    #    Ridge_200_score_train = Ridge_200.score(X_train_200, y_train_200)
    #    Ridge_200_score_test = Ridge_200.score(X_test_200, y_test_200)
    #
    #    Lasso_200_score_train = Lasso_200.score(X_train_200, y_train_200)
    #    Lasso_200_score_test = Lasso_200.score(X_test_200,y_test_200)
    #
    #    Random_Forest_600_score_train = Random_Forest_600.score(X_train_600, y_train_600)
    #    Random_Forest_600_score_test = Random_Forest_600.score(X_test_600, y_test_600)
    #
    #    Ridge_600_score_train = Ridge_600.score(X_train_600, y_train_600)
    #    Ridge_600_score_test = Ridge_600.score(X_test_600, y_test_600)
    #
    #    Lasso_600_score_train = Lasso_600.score(X_train_600, y_train_600)
    #    Lasso_600_score_test = Lasso_600.score(X_test_600, y_test_600)
    #
    #    Random_Forest_200_600_score_train = Random_Forest_200_600.score(X_train_200_600, y_train_200_600)
    #    Random_Forest_200_600_score_test = Random_Forest_200_600.score(X_test_200_600, y_test_200_600)
    #
    #    Ridge_200_600_score_train = Ridge_200_600.score(X_train_200_600, y_train_200_600)
    #    Ridge_200_600_score_test = Ridge_200_600.score(X_test_200_600, y_test_200_600)
    #
    #    Lasso_200_600_score_train = Lasso_200_600.score(X_train_200_600, y_train_200_600)
    #    Lasso_200_600_score_test = Lasso_200_600.score(X_test_200_600, y_test_200_600)
    #
    #    return Random_Forest_200_score_train, Random_Forest_200_score_test, Ridge_200_score_train, Ridge_200_score_test, Lasso_200_score_train, Lasso_200_score_test, \
    #        Random_Forest_600_score_train, Random_Forest_600_score_test, Ridge_600_score_train, Ridge_600_score_test,Lasso_600_score_train, Lasso_600_score_test, \
    #        Random_Forest_200_600_score_train, Random_Forest_200_600_score_test, Ridge_200_600_score_train, Ridge_200_600_score_test, Lasso_200_600_score_train, \
    #        Lasso_200_600_score_test

    #Random_Forest_200_score_train, Random_Forest_200_score_test, Ridge_200_score_train, Ridge_200_score_test, Lasso_200_score_train, Lasso_200_score_test, \
    #    Random_Forest_600_score_train, Random_Forest_600_score_test, Ridge_600_score_train, Ridge_600_score_test,Lasso_600_score_train, Lasso_600_score_test,\
    #        Random_Forest_200_600_score_train, Random_Forest_200_600_score_test, Ridge_200_600_score_train, Ridge_200_600_score_test, Lasso_200_600_score_train, \
    #            Lasso_200_600_score_test  = load_scores_split()

    st.markdown("**Paramètres de la seconde itération :**")
    st.markdown('<div style="text-align: justify;">Afin d’améliorer notre score de test, nous avons testé une nouvelle approche : ne conserver que les données ayant un ResponseTime de plus de 200s, \
                inférieur à 600s ou compris entre 200 et 600s. \n \
                En se basant sur le graphique montrant la distance métrique en fonction du temps de réponse on observe 3 profils de réponses distinctes, \
                l’idée étant d’exclure les données montrant un bruit élevé dans l’optique d’améliorer la prédiction du temps de réponse.</div>', unsafe_allow_html=True)
    graph = st.expander("Voir le graphique")
    graph.image("distancemetrique_vs_responsetime.png")
    
    #affichage des scores pour comparatif
    results_split = st.button("Voir les résultats avec le split")
    if results_split :
        table_split = st.data_editor([
            {"Modèle":"Random Forest", "ResponseTime>200" : 0.3853, "ResponseTime<600" : 0.4445,"ResponseTime>200 et <600" : 0.3825 },
            {"Modèle":"Ridge", "ResponseTime>200" : 0.3422, "ResponseTime<600" : 0.3865, "ResponseTime>200 et <600" : 0.3391},
            {"Modèle":"Lasso", "ResponseTime>200" : 0.3422, "ResponseTime<600" : 0.3865, "ResponseTime>200 et <600" : 0.3391},
        ], column_config={
            "ResponseTime>200" : st.column_config.ProgressColumn(
                "ResponseTime>200",
                min_value=0,
                max_value=0.8000,
            ),
            "ResponseTime<600": st.column_config.ProgressColumn(
                "ResponseTime<600",
                min_value=0,
                max_value=0.8000,
            ),
            "ResponseTime>200 et <600": st.column_config.ProgressColumn(
                "ResponseTime>200 et <600",
                min_value=0,
                max_value=0.8000,
            )
        }, hide_index=True)

    interpretation_second_iteration = st.toggle("Cliquez pour voir l'interprétation")
    if interpretation_second_iteration:
        st.write('<div style="text-align: justify;">L’exclusion des données avec un ResponseTime, bien qu’ayant amélioré la prédiction \
                                    ne permet pas d’atteindre un score correct et une autre approche doit être mise en place pour y parvenir.</div>', unsafe_allow_html=True)

    st.markdown(":blue-background[------------------------------------------------------------------------------------------------------------------------------------------]",width="content")
            
    ###
    #2nd itération avec split en plusieurs catégories
    ###

    #importation des packages pour la modelisation
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import FunctionTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import classification_report

    st.markdown("**Paramètres de la seconde itération, 2ème partie :**")
    st.markdown('<div style="text-align: justify;">Nous allons séparer notre variable cible en catégories. Nous choisissons d’effectuer ce découpage en suivant \
                les informations données par le graphique déjà utilisé pour la réduction du jeu de données.</div>', unsafe_allow_html=True)
    st.write("\n")
    st.markdown(":blue[Détermination du nombre de catégories]\n")
    st.markdown("Sur la base du graphique DistanceMetrique vs ResponseTime, nous pouvons déterminer comment séparer la variable cible.")
    graphs = st.expander("Voir les graphiques ")
    graphs.image("distance_responsetime_200.png", caption="ResponseTime < 200")
    graphs.image("distance_responsetime_200-600.png", caption="200>ResponseTime>600")
    graphs.image("distance_responsetime_600.png", caption="ResponseTime > 600")

    #split en 3 categories
    @st.cache_data #ajout du cache decorator pour le preprocessing
    def preprocessing_3cat(df):
        #remplacement des noms des jours de la variable Day par les chiffres correspondant
        df['Day'] = df['Day'].replace({'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7})
        #ajout d'une colonne ResponseTime_cat pour séparer la variable ResponseTime en trois catégories
        bin = [0,200,600,1200]
        label = ['short', 'medium', 'long']
        df['ResponseTime_cat'] = pd.cut(df['ResponseTime'], bins=bin, labels=label)
        #suppression de la variable responseTime
        df = df.drop('ResponseTime', axis=1)
        #sélection des variables explicatives et variables cibles
        X = df.drop('ResponseTime_cat', axis = 1)
        y = df['ResponseTime_cat']
        #séparation en jeu d'entrainement et de test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        #séparation des colonnes numériques et catégorielles
        var_num = ['NumCalls', 'DistanceMetrique']
        var_cat = ['CalYear','DeployedFromLocation', 'PlusCode_Description', 'IncidentGroup', 'gpe_geo', 'PropertyCategory_bis', 'AddressQualifier_bis']
        var_time = ['HourOfCall', 'week', 'month', 'Day']

        X_train_num = X_train[var_num]
        X_train_cat = X_train[var_cat]
        X_train_time = X_train[var_time]
        X_test_num = X_test[var_num]
        X_test_cat = X_test[var_cat]
        X_test_time = X_test[var_time]

        #gestion des variables temps avec sinus et cosinus (variable cyclique)
        def sin_transformer(period):
            return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))

        def cos_transformer(period):
            return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))

        for var in X_train_time :
            X_train_time[var + '_sin'] = sin_transformer(24).fit_transform(X_train_time[var])
            X_train_time[var + '_cos'] = cos_transformer(24).fit_transform(X_train_time[var])
            X_train_time = X_train_time.drop(var, axis=1)

        for var in X_test_time :
            X_test_time[var + '_sin'] = sin_transformer(24).fit_transform(X_test_time[var])
            X_test_time[var + '_cos'] = cos_transformer(24).fit_transform(X_test_time[var])
            X_test_time = X_test_time.drop(var, axis=1)

        X_train_time.reset_index(drop=True, inplace=True)
        X_test_time.reset_index(drop=True, inplace=True)

        #remplissage des valeurs manquantes par simple imputer avec la stratégie median pour les variables numériques et le most frequent pour les variables catégorielles
        #gestion des données manquantes pour les variables numériques
        imputer_num = SimpleImputer(missing_values=np.nan, strategy='median')
        X_train_num = imputer_num.fit_transform(X_train_num)
        X_test_num = imputer_num.transform(X_test_num)

        #gestion des données manquantes pour les variables catégorielles
        imputer_cat = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        X_train_cat = imputer_cat.fit_transform(X_train_cat)
        X_test_cat = imputer_cat.transform(X_test_cat)

        #standardisation des variables numériques avec StandardScaler
        scaler = StandardScaler()
        X_train_num = scaler.fit_transform(X_train_num)
        X_test_num = scaler.transform(X_test_num)

        #encodage des variables catégorielles
        encoder = OneHotEncoder(drop = 'first', sparse_output=False)
        X_train_cat = encoder.fit_transform(X_train_cat)
        X_test_cat = encoder.transform(X_test_cat)

        ##passage en dataframe des tableaux récupérés après encodage
        X_train_num = pd.DataFrame(X_train_num)
        X_test_num = pd.DataFrame(X_test_num)
        X_train_cat = pd.DataFrame(X_train_cat)
        X_test_cat = pd.DataFrame(X_test_cat)

        #concaténation des jeux d'entraînement et de test
        X_train = pd.concat([X_train_num, X_train_cat, X_train_time], axis=1)
        X_test = pd.concat([X_test_num, X_test_cat, X_test_time], axis=1)

        X_train.columns = X_train.columns.astype(str)
        X_test.columns = X_test.columns.astype(str)

         #encodage de la variable cible ResponseTime_cat dans l'ordre short, medium, long
        le = LabelEncoder()
        y_train = le.fit_transform(y_train)
        y_test = le.transform(y_test)

        return X_train, X_test, y_train, y_test
    X_train_3cat, X_test_3cat, y_train_3cat, y_test_3cat = preprocessing_3cat(df)

    #chargement des modèles
    @st.cache_data #ajout du cache decorator pour le chargement des modeles
    def load_3cat():
        reglog_3cat = joblib.load("model_reglog_3cat")
        dtc_3cat = joblib.load("model_dtc_3cat")
        rc_3cat = joblib.load("model_rc_3cat")
        rfc_3cat = joblib.load("model_rfc_3cat.joblib")
        mlpc_3cat = joblib.load("model_mlpc_3cat")
        gbc_3cat = joblib.load("model_gbc_3cat")
        return reglog_3cat, dtc_3cat, rc_3cat, rfc_3cat, mlpc_3cat, gbc_3cat
    reglog_3cat, dtc_3cat, rc_3cat, rfc_3cat, mlpc_3cat, gbc_3cat = load_3cat()

    #split en 7 categories
    @st.cache_data #ajout du cache decorator pour le preprocessing
    def preprocessing_7cat(df):
        #remplacement des noms des jours de la variable Day par les chiffres correspondant
        df['Day'] = df['Day'].replace({'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7})
        #ajout d'une colonne ResponseTime_cat pour séparer la variable ResponseTime en 7 catégories
        bin = [0,75,150,450,600,800,900,1200]
        label = ['xveryshort','veryshort','short', 'medium','xmedium', 'long','xlong']
        df['ResponseTime_cat'] = pd.cut(df['ResponseTime'], bins=bin, labels=label)
        #suppression de la variable responseTime
        df = df.drop('ResponseTime', axis=1)
        #sélection des variables explicatives et variables cibles
        X = df.drop('ResponseTime_cat', axis = 1)
        y = df['ResponseTime_cat']
        #séparation en jeu d'entrainement et de test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        #séparation des colonnes numériques et catégorielles
        var_num = ['NumCalls', 'DistanceMetrique']
        var_cat = ['CalYear','DeployedFromLocation', 'PlusCode_Description', 'IncidentGroup', 'gpe_geo', 'PropertyCategory_bis', 'AddressQualifier_bis']
        var_time = ['HourOfCall', 'week', 'month', 'Day']

        X_train_num = X_train[var_num]
        X_train_cat = X_train[var_cat]
        X_train_time = X_train[var_time]
        X_test_num = X_test[var_num]
        X_test_cat = X_test[var_cat]
        X_test_time = X_test[var_time]

        #gestion des variables temps avec sinus et cosinus (variable cyclique)
        def sin_transformer(period):
            return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))

        def cos_transformer(period):
            return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))

        for var in X_train_time :
            X_train_time[var + '_sin'] = sin_transformer(24).fit_transform(X_train_time[var])
            X_train_time[var + '_cos'] = cos_transformer(24).fit_transform(X_train_time[var])
            X_train_time = X_train_time.drop(var, axis=1)

        for var in X_test_time :
            X_test_time[var + '_sin'] = sin_transformer(24).fit_transform(X_test_time[var])
            X_test_time[var + '_cos'] = cos_transformer(24).fit_transform(X_test_time[var])
            X_test_time = X_test_time.drop(var, axis=1)

        X_train_time.reset_index(drop=True, inplace=True)
        X_test_time.reset_index(drop=True, inplace=True)

        #remplissage des valeurs manquantes par simple imputer avec la stratégie median pour les variables numériques et le most frequent pour les variables catégorielles
        #gestion des données manquantes pour les variables numériques
        imputer_num = SimpleImputer(missing_values=np.nan, strategy='median')
        X_train_num = imputer_num.fit_transform(X_train_num)
        X_test_num = imputer_num.transform(X_test_num)

        #gestion des données manquantes pour les variables catégorielles
        imputer_cat = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        X_train_cat = imputer_cat.fit_transform(X_train_cat)
        X_test_cat = imputer_cat.transform(X_test_cat)

        #standardisation des variables numériques avec StandardScaler
        scaler = StandardScaler()
        X_train_num = scaler.fit_transform(X_train_num)
        X_test_num = scaler.transform(X_test_num)

        #encodage des variables catégorielles
        encoder = OneHotEncoder(drop = 'first', sparse_output=False)
        X_train_cat = encoder.fit_transform(X_train_cat)
        X_test_cat = encoder.transform(X_test_cat)

        ##passage en dataframe des tableaux récupérés après encodage
        X_train_num = pd.DataFrame(X_train_num)
        X_test_num = pd.DataFrame(X_test_num)
        X_train_cat = pd.DataFrame(X_train_cat)
        X_test_cat = pd.DataFrame(X_test_cat)

        #concaténation des jeux d'entraînement et de test
        X_train = pd.concat([X_train_num, X_train_cat, X_train_time], axis=1)
        X_test = pd.concat([X_test_num, X_test_cat, X_test_time], axis=1)

        X_train.columns = X_train.columns.astype(str)
        X_test.columns = X_test.columns.astype(str)

        #encodage de la variable cible ResponseTime_cat dans l'ordre short, medium, long
        le = LabelEncoder()
        y_train = le.fit_transform(y_train)
        y_test = le.transform(y_test)
        return X_train, X_test, y_train, y_test
    X_train_7cat, X_test_7cat, y_train_7cat, y_test_7cat = preprocessing_7cat(df)

    #chargement du model
    reglog_7cat = joblib.load("model_reglog_7cat")

    #split en 5 categories
    @st.cache_data #ajout du cache decorator pour le preprocessing
    def preprocessing_5cat(df):
        #remplacement des noms des jours de la variable Day par les chiffres correspondant
        df['Day'] = df['Day'].replace({'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7})
        #ajout d'une colonne ResponseTime_cat pour séparer la variable ResponseTime en 5 catégories
        bin = [0,150,450,600,800,1200]
        label = ['veryshort','short', 'medium','xmedium', 'long']
        df['ResponseTime_cat'] = pd.cut(df['ResponseTime'], bins=bin, labels=label)
        #suppression de la variable responseTime
        df = df.drop('ResponseTime', axis=1)
        #sélection des variables explicatives et variables cibles
        X = df.drop('ResponseTime_cat', axis = 1)
        y = df['ResponseTime_cat']
        #séparation en jeu d'entrainement et de test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        #séparation des colonnes numériques et catégorielles
        var_num = ['NumCalls', 'DistanceMetrique']
        var_cat = ['CalYear','DeployedFromLocation', 'PlusCode_Description', 'IncidentGroup', 'gpe_geo', 'PropertyCategory_bis', 'AddressQualifier_bis']
        var_time = ['HourOfCall', 'week', 'month', 'Day']

        X_train_num = X_train[var_num]
        X_train_cat = X_train[var_cat]
        X_train_time = X_train[var_time]
        X_test_num = X_test[var_num]
        X_test_cat = X_test[var_cat]
        X_test_time = X_test[var_time]

        #gestion des variables temps avec sinus et cosinus (variable cyclique)
        def sin_transformer(period):
            return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))

        def cos_transformer(period):
            return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))

        for var in X_train_time :
            X_train_time[var + '_sin'] = sin_transformer(24).fit_transform(X_train_time[var])
            X_train_time[var + '_cos'] = cos_transformer(24).fit_transform(X_train_time[var])
            X_train_time = X_train_time.drop(var, axis=1)

        for var in X_test_time :
            X_test_time[var + '_sin'] = sin_transformer(24).fit_transform(X_test_time[var])
            X_test_time[var + '_cos'] = cos_transformer(24).fit_transform(X_test_time[var])
            X_test_time = X_test_time.drop(var, axis=1)

        X_train_time.reset_index(drop=True, inplace=True)
        X_test_time.reset_index(drop=True, inplace=True)

        #remplissage des valeurs manquantes par simple imputer avec la stratégie median pour les variables numériques et le most frequent pour les variables catégorielles
        #gestion des données manquantes pour les variables numériques
        imputer_num = SimpleImputer(missing_values=np.nan, strategy='median')
        X_train_num = imputer_num.fit_transform(X_train_num)
        X_test_num = imputer_num.transform(X_test_num)

        #gestion des données manquantes pour les variables catégorielles
        imputer_cat = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        X_train_cat = imputer_cat.fit_transform(X_train_cat)
        X_test_cat = imputer_cat.transform(X_test_cat)

        #standardisation des variables numériques avec StandardScaler
        scaler = StandardScaler()
        X_train_num = scaler.fit_transform(X_train_num)
        X_test_num = scaler.transform(X_test_num)

        #encodage des variables catégorielles
        encoder = OneHotEncoder(drop = 'first', sparse_output=False)
        X_train_cat = encoder.fit_transform(X_train_cat)
        X_test_cat = encoder.transform(X_test_cat)

        ##passage en dataframe des tableaux récupérés après encodage
        X_train_num = pd.DataFrame(X_train_num)
        X_test_num = pd.DataFrame(X_test_num)
        X_train_cat = pd.DataFrame(X_train_cat)
        X_test_cat = pd.DataFrame(X_test_cat)

        #concaténation des jeux d'entraînement et de test
        X_train = pd.concat([X_train_num, X_train_cat, X_train_time], axis=1)
        X_test = pd.concat([X_test_num, X_test_cat, X_test_time], axis=1)

        X_train.columns = X_train.columns.astype(str)
        X_test.columns = X_test.columns.astype(str)

        #encodage de la variable cible ResponseTime_cat dans l'ordre short, medium, long
        le = LabelEncoder()
        y_train = le.fit_transform(y_train)
        y_test = le.transform(y_test)
        return X_train, X_test, y_train, y_test
    X_train_5cat, X_test_5cat, y_train_5cat, y_test_5cat = preprocessing_5cat(df)

    #chargement du model
    reglog_5cat = joblib.load("model_reglog_5cat")

    #split en 2 categories
    @st.cache_data #ajout du cache decorator pour le preprocessing
    def preprocessing_2cat(df):
        #remplacement des noms des jours de la variable Day par les chiffres correspondant
        df['Day'] = df['Day'].replace({'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7})
        #ajout d'une colonne ResponseTime_cat pour séparer la variable ResponseTime en 7 catégories
        bin = [0,450,1200]
        label = ['short', 'medium-long']
        df['ResponseTime_cat'] = pd.cut(df['ResponseTime'], bins=bin, labels=label)
        #suppression de la variable responseTime
        df = df.drop('ResponseTime', axis=1)
        #sélection des variables explicatives et variables cibles
        X = df.drop('ResponseTime_cat', axis = 1)
        y = df['ResponseTime_cat']
        #séparation en jeu d'entrainement et de test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        #séparation des colonnes numériques et catégorielles
        var_num = ['NumCalls', 'DistanceMetrique']
        var_cat = ['CalYear','DeployedFromLocation', 'PlusCode_Description', 'IncidentGroup', 'gpe_geo', 'PropertyCategory_bis', 'AddressQualifier_bis']
        var_time = ['HourOfCall', 'week', 'month', 'Day']

        X_train_num = X_train[var_num]
        X_train_cat = X_train[var_cat]
        X_train_time = X_train[var_time]
        X_test_num = X_test[var_num]
        X_test_cat = X_test[var_cat]
        X_test_time = X_test[var_time]

        #gestion des variables temps avec sinus et cosinus (variable cyclique)
        def sin_transformer(period):
            return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))

        def cos_transformer(period):
            return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))

        for var in X_train_time :
            X_train_time[var + '_sin'] = sin_transformer(24).fit_transform(X_train_time[var])
            X_train_time[var + '_cos'] = cos_transformer(24).fit_transform(X_train_time[var])
            X_train_time = X_train_time.drop(var, axis=1)

        for var in X_test_time :
            X_test_time[var + '_sin'] = sin_transformer(24).fit_transform(X_test_time[var])
            X_test_time[var + '_cos'] = cos_transformer(24).fit_transform(X_test_time[var])
            X_test_time = X_test_time.drop(var, axis=1)

        X_train_time.reset_index(drop=True, inplace=True)
        X_test_time.reset_index(drop=True, inplace=True)

        #remplissage des valeurs manquantes par simple imputer avec la stratégie median pour les variables numériques et le most frequent pour les variables catégorielles
        #gestion des données manquantes pour les variables numériques
        imputer_num = SimpleImputer(missing_values=np.nan, strategy='median')
        X_train_num = imputer_num.fit_transform(X_train_num)
        X_test_num = imputer_num.transform(X_test_num)

        #gestion des données manquantes pour les variables catégorielles
        imputer_cat = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        X_train_cat = imputer_cat.fit_transform(X_train_cat)
        X_test_cat = imputer_cat.transform(X_test_cat)

        #standardisation des variables numériques avec StandardScaler
        scaler = StandardScaler()
        X_train_num = scaler.fit_transform(X_train_num)
        X_test_num = scaler.transform(X_test_num)

        #encodage des variables catégorielles
        encoder = OneHotEncoder(drop = 'first', sparse_output=False)
        X_train_cat = encoder.fit_transform(X_train_cat)
        X_test_cat = encoder.transform(X_test_cat)

        ##passage en dataframe des tableaux récupérés après encodage
        X_train_num = pd.DataFrame(X_train_num)
        X_test_num = pd.DataFrame(X_test_num)
        X_train_cat = pd.DataFrame(X_train_cat)
        X_test_cat = pd.DataFrame(X_test_cat)

        #concaténation des jeux d'entraînement et de test
        X_train = pd.concat([X_train_num, X_train_cat, X_train_time], axis=1)
        X_test = pd.concat([X_test_num, X_test_cat, X_test_time], axis=1)

        X_train.columns = X_train.columns.astype(str)
        X_test.columns = X_test.columns.astype(str)

        #encodage de la variable cible ResponseTime_cat dans l'ordre short, medium, long
        le = LabelEncoder()
        y_train = le.fit_transform(y_train)
        y_test = le.transform(y_test)
        return X_train, X_test, y_train, y_test
    X_train_2cat, X_test_2cat, y_train_2cat, y_test_2cat = preprocessing_2cat(df)

    #chargement du model
    reglog_2cat = joblib.load("model_reglog_2cat")
        
    ##chargement des scores de tous les modeles
    @st.cache_data #ajout du cache decorator pour le chargement des scores de tous les modeles
    def load_scores_cat():
        reglog_3cat_score_train = 0.8418432007459151 #reglog_3cat.score(X_train_3cat,y_train_3cat)
        reglog_3cat_score_test = 0.8426910494290104 #reglog_3cat.score(X_test_3cat,y_test_3cat)
        dtc_3cat_score_train = 0.8436867055333014 #dtc_3cat.score(X_train_3cat,y_train_3cat)
        dtc_3cat_score_test = 0.8444098963421802 #dtc_3cat.score(X_test_3cat,y_test_3cat)
        rc_3cat_score_train = 0.8285216236828037 #rc_3cat.score(X_train_3cat,y_train_3cat)
        rc_3cat_score_test = 0.8296618655164446 #rc_3cat.score(X_test_3cat,y_test_3cat)
        rfc_3cat_score_train = 0.9888842438108558 #rfc_3cat.score(X_train_3cat,y_train_3cat)
        rfc_3cat_score_test = 0.8501724927739513 #rfc_3cat.score(X_test_3cat,y_test_3cat)
        mlpc_3cat_score_train = 0.8494173805307044 #mlpc_3cat.score(X_train_3cat,y_train_3cat)
        mlpc_3cat_score_test = 0.8493900931177207 #mlpc_3cat.score(X_test_3cat,y_test_3cat)
        gbc_3cat_score_train = 0.8482143897760988 #gbc_3cat.score(X_train_3cat,y_train_3cat)
        gbc_3cat_score_test = 0.8485387774295942 #gbc_3cat.score(X_test_3cat,y_test_3cat)
        reglog_7cat_score_train = 0.7782995462476754 #reglog_7cat.score(X_train_7cat,y_train_7cat)
        reglog_7cat_score_test = 0.7788464890068093 #reglog_7cat.score(X_test_7cat,y_test_7cat)
        reglog_5cat_score_train = 0.7783200501936598 #reglog_5cat.score(X_train_5cat,y_train_5cat)
        reglog_5cat_score_test = 0.7789305551853454 #reglog_5cat.score(X_test_5cat,y_test_5cat)
        reglog_2cat_score_train = 0.8414434983012481 #reglog_2cat.score(X_train_2cat,y_train_2cat)
        reglog_2cat_score_test = 0.8422467403851871 #reglog_2cat.score(X_test_2cat,y_test_2cat)
        return reglog_3cat_score_train,reglog_3cat_score_test, dtc_3cat_score_train,dtc_3cat_score_test,rc_3cat_score_train,rc_3cat_score_test, \
            rfc_3cat_score_train, rfc_3cat_score_test,mlpc_3cat_score_train,mlpc_3cat_score_test,gbc_3cat_score_train,gbc_3cat_score_test, \
            reglog_7cat_score_train,reglog_7cat_score_test,reglog_5cat_score_train,reglog_5cat_score_test,reglog_2cat_score_train,reglog_2cat_score_test
        
    reglog_3cat_score_train,reglog_3cat_score_test, dtc_3cat_score_train,dtc_3cat_score_test,rc_3cat_score_train,rc_3cat_score_test, \
        rfc_3cat_score_train, rfc_3cat_score_test,mlpc_3cat_score_train,mlpc_3cat_score_test,gbc_3cat_score_train,gbc_3cat_score_test, \
        reglog_7cat_score_train,reglog_7cat_score_test,reglog_5cat_score_train,reglog_5cat_score_test,reglog_2cat_score_train,reglog_2cat_score_test = load_scores_cat()
        
        ##chargement des predictions de tous les modeles
        #@st.cache_data #ajout du cache decorator pour le chargement des scores de tous les modeles
        #def load_predict_cat():    
        #    y_pred_reglog_3cat = reglog_3cat.predict(X_test_3cat)
        #    y_pred_dtc_3cat = dtc_3cat.predict(X_test_3cat)
        #    y_pred_rc_3cat = rc_3cat.predict(X_test_3cat)
        #    y_pred_rfc_3cat = rfc_3cat.predict(X_test_3cat)
        #    y_pred_mlpc_3cat = mlpc_3cat.predict(X_test_3cat)
        #    y_pred_gbc_3cat = gbc_3cat.predict(X_test_3cat)
        #    y_pred_reglog_7cat = reglog_7cat.predict(X_test_7cat)
        #    y_pred_reglog_5cat = reglog_5cat.predict(X_test_5cat)
        #    y_pred_reglog_2cat = reglog_2cat.predict(X_test_2cat)
        #    return y_pred_reglog_3cat,y_pred_dtc_3cat,y_pred_rc_3cat,y_pred_rfc_3cat,y_pred_mlpc_3cat,y_pred_gbc_3cat,y_pred_reglog_7cat,y_pred_reglog_5cat,y_pred_reglog_2cat
        #y_pred_reglog_3cat,y_pred_dtc_3cat,y_pred_rc_3cat,y_pred_rfc_3cat,y_pred_mlpc_3cat,y_pred_gbc_3cat,y_pred_reglog_7cat,y_pred_reglog_5cat, \
        #    y_pred_reglog_2cat = load_predict_cat()

    ##chargement des pd.crosstab de tous les modeles
    @st.cache_data #ajout du cache decorator pour le chargement des scores de tous les modeles
    def load_crosstab_cat():
        crosstab_reglog_3cat = Image.open("crosstab_reglog_3cat.png") #pd.crosstab(y_test_3cat,y_pred_reglog_3cat, rownames=['Réalité'], colnames=['Prédictions'])
        crosstab_dtc_3cat = Image.open("crosstab_dtc_3cat.png") #pd.crosstab(y_test_3cat,y_pred_dtc_3cat, rownames=['Réalité'], colnames=['Prédictions'])
        crosstab_rc_3cat = Image.open("crosstab_rc_3cat.png") #pd.crosstab(y_test_3cat,y_pred_rc_3cat, rownames=['Réalité'], colnames=['Prédictions'])
        crosstab_rfc_3cat = Image.open("crosstab_rfc_3cat.png") #pd.crosstab(y_test_3cat,y_pred_rfc_3cat, rownames=['Réalité'], colnames=['Prédictions'])
        crosstab_mlpc_3cat = Image.open("crosstab_mlpc_3cat.png") #pd.crosstab(y_test_3cat,y_pred_mlpc_3cat, rownames=['Réalité'], colnames=['Prédictions'])
        crosstab_gbc_3cat = Image.open("crosstab_gbc_3cat.png") #pd.crosstab(y_test_3cat,y_pred_gbc_3cat, rownames=['Réalité'], colnames=['Prédictions'])
        crosstab_reglog_7cat = Image.open("crosstab_reglog_7cat.png") #pd.crosstab(y_test_7cat,y_pred_reglog_7cat, rownames=['Réalité'], colnames=['Prédictions'])
        crosstab_reglog_5cat = Image.open("crosstab_reglog_5cat.png") #pd.crosstab(y_test_5cat,y_pred_reglog_5cat, rownames=['Réalité'], colnames=['Prédictions'])
        crosstab_reglog_2cat = Image.open("crosstab_reglog_2cat.png") #pd.crosstab(y_test_2cat,y_pred_reglog_2cat, rownames=['Réalité'], colnames=['Prédictions'])
        return crosstab_reglog_3cat,crosstab_dtc_3cat,crosstab_rc_3cat,crosstab_rfc_3cat,crosstab_mlpc_3cat,crosstab_gbc_3cat,crosstab_reglog_7cat, \
            crosstab_reglog_5cat,crosstab_reglog_2cat
    crosstab_reglog_3cat,crosstab_dtc_3cat,crosstab_rc_3cat,crosstab_rfc_3cat,crosstab_mlpc_3cat,crosstab_gbc_3cat, \
        crosstab_reglog_7cat,crosstab_reglog_5cat,crosstab_reglog_2cat = load_crosstab_cat()
        
    ##chargement des classification_report de tous les modeles
    @st.cache_data #ajout du cache decorator pour le chargement des scores de tous les modeles
    def load_classificationreport_cat():
        classificationreport_reglog_3cat = Image.open("classificationreport_reglog_3cat.png") #classification_report(y_test_3cat,y_pred_reglog_3cat)
        classificationreport_dtc_3cat = Image.open("classificationreport_dtc_3cat.png") #classification_report(y_test_3cat,y_pred_dtc_3cat)
        classificationreport_rc_3cat = Image.open("classificationreport_rc_3cat.png") #classification_report(y_test_3cat,y_pred_rc_3cat)
        classificationreport_rfc_3cat = Image.open("classificationreport_rfc_3cat.png") #classification_report(y_test_3cat,y_pred_rfc_3cat)
        classificationreport_mlpc_3cat = Image.open("classificationreport_mlpc_3cat.png") #classification_report(y_test_3cat,y_pred_mlpc_3cat)
        classificationreport_gbc_3cat = Image.open("classificationreport_gbc_3cat.png") #classification_report(y_test_3cat,y_pred_gbc_3cat)
        classificationreport_reglog_7cat = Image.open("classificationreport_reglog_7cat.png") #classification_report(y_test_7cat,y_pred_reglog_7cat)
        classificationreport_reglog_5cat = Image.open("classificationreport_reglog_5cat.png") #classification_report(y_test_5cat,y_pred_reglog_5cat)
        classificationreport_reglog_2cat = Image.open("classificationreport_reglog_2cat.png") #classification_report(y_test_2cat,y_pred_reglog_2cat)
        return classificationreport_reglog_3cat,classificationreport_dtc_3cat,classificationreport_rc_3cat,classificationreport_rfc_3cat,classificationreport_mlpc_3cat, \
            classificationreport_gbc_3cat,classificationreport_reglog_7cat,classificationreport_reglog_5cat,classificationreport_reglog_2cat
    classificationreport_reglog_3cat,classificationreport_dtc_3cat,classificationreport_rc_3cat,classificationreport_rfc_3cat,classificationreport_mlpc_3cat, \
        classificationreport_gbc_3cat,classificationreport_reglog_7cat,classificationreport_reglog_5cat,classificationreport_reglog_2cat = load_classificationreport_cat()
              
    #séparation de la page en 4 partie pour ajouter les toggle pour chaque partie
    one, two, three, four = st.columns(4)
    cat_3 = one.toggle("3 catégories")
    cat_7 = two.toggle("7 catégories")
    cat_5 = three.toggle("5 catégories")
    cat_2 = four.toggle("2 catégories")

    st.write("Modélisations effectuées uniquement avec le modèle de régression logistique.")

    #initiation d'une table
    table_cat = st.table(pd.DataFrame(columns=("Train score", "Test score")))

    #affichage pour 3 catégories
    if cat_3 : 
        table_cat.add_rows(pd.DataFrame({"Train score": reglog_3cat_score_train,"Test score": reglog_3cat_score_test},index=['3 catégories']))
        one.image(crosstab_reglog_3cat, caption='Crosstab')
        one.image(classificationreport_reglog_3cat, caption='Classification Report')

    #affichage pour 7 catégories
    if cat_7:
        table_cat.add_rows(pd.DataFrame({"Train score": reglog_7cat_score_train,"Test score": reglog_7cat_score_test},index=['7 catégories']))
        two.image(crosstab_reglog_7cat, caption='Crosstab')
        two.image(classificationreport_reglog_7cat, caption='Classification Report')
            
    #affichage pour 5 catégories
    if cat_5:
        table_cat.add_rows(pd.DataFrame({"Train score": reglog_5cat_score_train,"Test score": reglog_5cat_score_test}, index=['5 catégories']))
        three.image(crosstab_reglog_5cat, caption='Crosstab')
        three.image(classificationreport_reglog_5cat, caption='Classification Report')
            
    #affichage pour 2 catégories
    if cat_2:
        table_cat.add_rows(pd.DataFrame({"Train score": reglog_2cat_score_train,"Test score": reglog_2cat_score_test}, index=['2 catégories']))
        four.image(crosstab_reglog_2cat, caption='Crosstab')
        four.image(classificationreport_reglog_2cat, caption='Classification Report')

    if cat_3 and cat_7 and cat_5 and cat_2:
        interpretation_cat = st.toggle("Cliquez pour voir l'interprétation des catégories")
        if interpretation_cat:
            st.write("Ces découpages ne permettent pas d’améliorer les résultats, nous restons donc sur un découpage de la variable cible avec 3 catégories.")
    else:
        st.info("Activez toutes les catégories pour voir l'interprétation")

    st.write("\n")
    st.markdown(":blue[Tests de plusieurs modèles]\n")

    
    # Listes de données fixes 
    model_names=["Régression Logistique","Decision Tree Classifier","Ridge Classifier","Random Forest Classifier","MLP Classifier","Gradient Boosting Classifier"]
    train_scores = {"Régression Logistique":reglog_3cat_score_train, "Decision Tree Classifier":dtc_3cat_score_train, "Ridge Classifier":rc_3cat_score_train, 
                    "Random Forest Classifier":rfc_3cat_score_train, "MLP Classifier":mlpc_3cat_score_train, "Gradient Boosting Classifier":gbc_3cat_score_train}
    test_scores = {"Régression Logistique":reglog_3cat_score_test, "Decision Tree Classifier":dtc_3cat_score_test, "Ridge Classifier":rc_3cat_score_test, 
                   "Random Forest Classifier":rfc_3cat_score_test, "MLP Classifier":mlpc_3cat_score_test, "Gradient Boosting Classifier":gbc_3cat_score_test}

    # Crosstab pour chaque index 
    crosstab_images = {
        "Régression Logistique": crosstab_reglog_3cat,
        "Decision Tree Classifier": crosstab_dtc_3cat,
        "Ridge Classifier": crosstab_rc_3cat,
        "Random Forest Classifier": crosstab_rfc_3cat,
        "MLP Classifier": crosstab_mlpc_3cat,
        "Gradient Boosting Classifier": crosstab_gbc_3cat
    }

    #classification report pour chaque index
    classification_images = {
        "Régression Logistique": classificationreport_reglog_3cat,
        "Decision Tree Classifier": classificationreport_dtc_3cat,
        "Ridge Classifier": classificationreport_rc_3cat,
        "Random Forest Classifier": classificationreport_rfc_3cat,
        "MLP Classifier": classificationreport_mlpc_3cat,
        "Gradient Boosting Classifier": classificationreport_gbc_3cat
    }

    # Création du DataFrame sans Crosstab pour affichage tabulaire
    df = pd.DataFrame({
        "Train Score": train_scores,
        "Test Score": test_scores,
    }, index=model_names)

    st.write("Cochez les modèles à afficher :")

    # Affichage dynamique ligne par ligne avec image
    for model in df.index:
        col1, col2 = st.columns([0.05, 0.95])
        with col1:
            show = st.checkbox("", key=f"chk_{model}")
        with col2:
            st.markdown(f"**{model}**")
            if show:
                st.markdown(f"- Train Score: `{df.loc[model, 'Train Score']}`")
                st.markdown(f"- Test Score: `{df.loc[model, 'Test Score']}`")
                # Affichage des deux images côte à côte
                img_col1, img_col2 = st.columns(2)
                img_col1.image(crosstab_images[model], caption=f"Crosstab de {model}", use_container_width=False)
                img_col2.image(classification_images[model], caption=f"Classification Report de {model}", use_container_width=False)
            st.markdown("---")

    interpretation_models = st.toggle("Cliquez pour voir l'interprétation des modèles")
    if interpretation_models:
        st.write('<div style="text-align: justify;">Les scores sont similaires pour la RegressionLogistic et pour le DecisionTreeClassifier et légèrement plus faible \
            pour le RidgeClassifier. En revanche le RandomForestClassifier présente un écart de 0.14 ce qui est plus important que pour les autres modèles. \
                Ces résultats nous indiquent une prédiction présentant un certain écart avec la réalité, ce qu’on peut constater avec le crosstab particulièrement \
                    sur les catégories situées dans la zone avec un fort bruit sur notre graphique de distancemetrique/responsetime.</div>', unsafe_allow_html=True)

    #affichage dans le streamlit
#    options = ["","Régression Logistique", "Decision Tree Classifier", "Ridge Classifier", "Random Forest Classifier", "MLP Classifier","Gradient Boosting Classifier"]
#    select = st.selectbox("Choix du modèle :", options=options)



    #initiation d'une table
#    table_final = st.table(pd.DataFrame(columns=("Train score", "Test score","Crosstab")))

#    if select == "Régression Logistique":
#        table_final.add_rows(pd.DataFrame({"Train score": reglog_3cat_score_train,"Test score": reglog_3cat_score_test, "Crosstab":crosstab_reglog_3cat},index=['Régression Logistique']))
#        st.image([crosstab_reglog_3cat, classificationreport_reglog_3cat], caption=['Crosstab','Classification Report'])
        
#    if select == "Decision Tree Classifier":
#        st.table(pd.DataFrame({"Train score": dtc_3cat_score_train,"Test score": dtc_3cat_score_test},index=["Decision Tree Classifier"]))
#        st.image([crosstab_dtc_3cat, classificationreport_dtc_3cat], caption=['Crosstab','Classification Report'])

#    if select == "Ridge Classifier":
#        st.table(pd.DataFrame({"Train score": rc_3cat_score_train,"Test score": rc_3cat_score_test},index=["Ridge Classifier"]))
#        st.image([crosstab_rc_3cat, classificationreport_rc_3cat], caption=['Crosstab','Classification Report'])

#    if select == "Random Forest Classifier":
#        st.table(pd.DataFrame({"Train score": dtc_3cat_score_train,"Test score": dtc_3cat_score_test},index=["Random Forest Classifier"]))
#        st.image([crosstab_dtc_3cat, classificationreport_dtc_3cat], caption=['Crosstab','Classification Report'])

#    if select == "MLP Classifier":
#        st.table(pd.DataFrame({"Train score": dtc_3cat_score_train,"Test score": dtc_3cat_score_test},index=["MLP Classifier"]))
#        st.image([crosstab_dtc_3cat, classificationreport_dtc_3cat], caption=['Crosstab','Classification Report'])

#    if select == "Gradient Boosting Classifier":
#        st.table(pd.DataFrame({"Train score": dtc_3cat_score_train,"Test score": dtc_3cat_score_test},index=["Gradient Boosting Classifier"]))
#        st.image([crosstab_dtc_3cat, classificationreport_dtc_3cat], caption=['Crosstab','Classification Report'])

    # Ouvre l'image et encode en base64
    with open("NicePng_arrow-png_101114.png", "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <div style="text-align: left; margin-top: 0px;">
            <a href="#haut">
                <img src="data:image/png;base64,{img_base64}" alt="Retour en haut" width="25" />
            </a>
        </div>
    """, unsafe_allow_html=True)
