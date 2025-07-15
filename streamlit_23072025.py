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

# logo = Image.open("https://github.com/M-R7/Projet_Pompier_DA/blob/main/img_pompiers.png")

st.sidebar.title("Temps de réponse de la Brigade des Pompiers de Londres")
pages = ["Introduction","Jeux de données","Data Visualisation","Cartographie","Prédiction du temps de réponse"]
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
    <div style='background-color:  #ffc2b5; padding: 20px; border-radius: 5px; color:  #1b1a1a; text-align: left;'>
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
    st.write("Data Visualisation")
    #lecture du fichier merge pour la dataviz streamlit
    # df_merge = pd.read_csv("/content/gdrive/MyDrive/PROJET POMPIER/Commun/Dataset/fichier_dataviz_streamlit.csv")
    df_merge = pd.read_csv("fichier_dataviz_streamlit.csv")

    #nombre de mobilisation par année
    df_year = df_merge.groupby(["CalYear_x"], as_index=False).agg(
        count=("IncidentNumber","count"))  
    
    #représentation en histogramme avec plotly
    fig = px.histogram(df_year,x = 'CalYear_x', y='count',nbins=30)
    fig.update_layout(bargap=0.2)
    st.pyplot(fig)

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