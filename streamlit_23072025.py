import pandas as pd
import streamlit as st
import numpy as np
import folium
from streamlit_folium import st_folium
import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api
from scipy.stats import kruskal

# logo = Image.open("https://github.com/M-R7/Projet_Pompier_DA/blob/main/img_pompiers.png")
logo = Image.open("img_pompiers.png")

logo = logo.resize((345, 195))
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo, use_container_width=False)  # conserve la taille choisie
#st.title("Temps de réponse de la Brigade des Pompiers de Londres")
st.markdown("<h3 style='text-align: center;'>Temps de réponse de la Brigade des Pompiers de Londres</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>de 2009 à 2024</h5>", unsafe_allow_html=True)

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
st.sidebar.title("Temps de réponse de la Brigade des Pompiers de Londres")

pages = ["Introduction","Jeux de données","Data Visualisation","Cartographie","Modélisation"]
page=st.sidebar.radio("",pages)
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

# hidden div with anchor
st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)

if page == pages[0]:
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
    st.markdown("<h4 style='font-size:20px; margin-bottom: 0px;'>Jeux de données</h4>", unsafe_allow_html=True)
# Radio sans label

    choix = st.radio(label="",options=["Dataset Principal", "Dataset Secondaire"],label_visibility="collapsed")
   
    if choix == "Dataset Principal":
        st.markdown("<h4>Dataset Principal</h4>", unsafe_allow_html=True)
        st.markdown("<h4>1. Source</h4>", unsafe_allow_html=True)
        st.markdown("""Nous avons deux jeux de données principaux : <a href='https://data.london.gov.uk/dataset/london-fire-brigade-mobilisation-records' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>Mobilisation</a> et <a href='https://data.london.gov.uk/dataset/london-fire-brigade-incident-records' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>Incident</a>. Ils proviennent de la <a href='https://data.london.gov.uk/' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>London Datastore</a>""", unsafe_allow_html=True)
        st.markdown("<h4>2. Exploration des données</h4>", unsafe_allow_html=True)
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

        choix_colonnes = st.radio(label="",options=["Toutes les colonnes", "Uniquement pour modélisation"],label_visibility="collapsed")
        if choix_colonnes == "Toutes les colonnes":
            html_incident = """
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
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">CalYear</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Année d'enregistrement de l’appel</td></tr>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">TimeOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Heure de l'appel (hh:mm:ss)</td></tr>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HourOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Heure de l'appel (nombre unique)</td></tr>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentGroup</td><td style="border: 1px solid black; padding: 8px; text-align: center;">High level incident category</td></tr>
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
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">NumCalls</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Number of calls received about the incident</td></tr>
                </tbody>
            </table>
            """

            st.markdown(html_incident, unsafe_allow_html=True)
        elif choix_colonnes == "Uniquement pour modélisation":
            
            html_incident_modelisation = """
            <table style="width: 100%; border-collapse: collapse; margin: 20px auto;">
                <thead>
                    <tr>
                        <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Nom de la colonne</th>
                        <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;"><span style="color: red; text-decoration: line-through;">IncidentNumber</span></td><td style="border: 1px solid black; padding: 8px; text-align: center;"><span style="color: red; text-decoration: line-through;">Numéro d'incident (index)</span></td></tr>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date de l'appel</td></tr>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">CalYear</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Année d'enregistrement de l’appel</td></tr>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">TimeOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Heure de l'appel (hh:mm:ss)</td></tr>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HourOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Heure de l'appel (nombre unique)</td></tr>
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentGroup</td><td style="border: 1px solid black; padding: 8px; text-align: center;">High level incident category</td></tr>
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
                    <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">NumCalls</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Number of calls received about the incident</td></tr>
                </tbody>
            </table>
            """

            st.markdown(html_incident_modelisation, unsafe_allow_html=True)
            
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
                </tr>
            </thead>
            <tbody>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">IncidentNumber</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Numéro d'incident (index)</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">CalYear</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Année d'enregistrement</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">BoroughName (*)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Nom de la personne</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">WardName (*)</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Quartier de l'incident</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">HourOfCall</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Heure de l'appel</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">ResourceMobilisationId</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Id des ressources mobilisées</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">Resource_Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code de ces ressources</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PerformanceReporting</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Notation de la performance</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeMobilised</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure de la mobilisation</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeMobile</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure du départ de la caserne</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeArrived</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure d'arrivée</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">TurnoutTimeSeconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Durée entre mobilisation et départ (secondes)</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">TravelTimeSeconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Durée du trajet (secondes)</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">AttendanceTimeSeconds</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Temps de présence (secondes)</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeLeft</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure de départ du lieu d'inter</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DateAndTimeReturned</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Date et heure de retour à la caserne</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DeployedFromStation_Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code de la station de déploiement</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DeployedFromStation_Name</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Nom de la station de déploiement</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DeployedFromLocation</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Lieu de départ du déploiement</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PumpOrder</td><td style="border: 1px solid black; padding: 8px; text-align: center;">No metadata</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PlusCode_Code</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code Mobilisation</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">PlusCode_Description</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Description Mobilisation</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DelayCodeId</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Code de retard pour intervention</td></tr>
                <tr><td style="border: 1px solid black; padding: 8px; text-align: center;">DelayCode_Description</td><td style="border: 1px solid black; padding: 8px; text-align: center;">Commentaires sur ce retard</td></tr>
            </tbody>
        </table>
        """

        st.markdown(html_mobilisation, unsafe_allow_html=True)
        
        # st.markdown("<h4>5. Traitement des données</h4>", unsafe_allow_html=True)
        st.markdown("<h4>3. Ajout de variables</h4>", unsafe_allow_html=True)
        st.markdown("""
        Pour alimenter et réduire la complexité de notre jeu de données, nous avons procédé à des ajouts de variables.<br>
        - ResponseTime : Somme des colonnes TurnoutTimeSeconds (temps de mobilisation des pompiers) et TravelTimeSeconds (temps de trajet des pompiers).<br>
        - Jour de la semaine / Numéro de la semaine / Mois : Obtenues à partir de la colonne DateAndTimeMobilised.<br>
        - PropertyCategory_bis : Split en 3 catégories de PropertyCategory, les deux les plus présentes et regroupement des autres catégories dans une catégorie other.<br>
        - AddressQualifier_bis : Split en 3 catégories de AddressQualifier, les deux les plus présentes et regroupement des autres catégories dans une catégorie other.<br><br>
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

elif page == pages[2]:
    st.markdown("<h4 style='font-size:20px; margin-bottom: 0px;'>Data Visualisation</h4>", unsafe_allow_html=True)
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
        
            #nombre de mobilisation par année
            df_year = df_merge.groupby(["CalYear_x"], as_index=False).agg(count=("IncidentNumber","count"))  
            #représentation en histogramme avec plotly
            fig1 = px.histogram(df_year,x = 'CalYear_x', y='count',nbins=30, title="Nombre de mobilisations par année")
            fig1.update_layout(bargap=0.2, yaxis_title="Nombre de mobilisations", xaxis_title='Année')
            st.plotly_chart(fig1)

            #analyse temps moyen de mobilisation et de trajet par année
            year_travel_time = df_merge.groupby("CalYear_x")["TravelTimeSeconds"].mean()
            year_turnout_time = df_merge.groupby("CalYear_x")["TurnoutTimeSeconds"].mean()
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x = year_travel_time.index, y = year_travel_time.values,mode='lines',name='TravelTimeSeconds', line=dict(color='Indigo')))
            fig2.add_trace(go.Scatter(x = year_turnout_time.index, y = year_turnout_time.values,mode='lines',name='TurnoutTimeSeconds', line=dict(color='LightBlue')))
            fig2.update_layout(title='Temps moyen de mobilisation et de trajet par année', yaxis_title='Temps moyen', xaxis_title='Année')
            st.plotly_chart(fig2)
   
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

        elif x_axis_val == "week" :

            #Répartition des temps de réponse par semaine
            fig8 = px.box(x=df_merge['week'], y=df_merge['ResponseTime'], title='Répartition des temps de réponse par semaine')
            fig8.update_layout(xaxis_title='Semaine', yaxis_title='Temps de réponse')
            st.plotly_chart(fig8)

        elif x_axis_val == "Day" :
        
            #analyse du temps de trajet moyen par jour de la semaine
            day_response_time = df_merge.groupby(["Day","CalYear_x"], as_index=False).agg(mean=("ResponseTime",'mean'))
            mean=day_response_time['mean']
            fig9 = px.bar(x=day_response_time['Day'], y=mean, title='Temps de réponse moyen par jour de la semaine', animation_frame=day_response_time['CalYear_x'])
            fig9.update_layout(xaxis_title='Jour', yaxis_title='Temps de réponse moyen')
            st.plotly_chart(fig9)

        elif x_axis_val == "HourOfCall_x" :
        
            #analyse du temps de réponse moyen par heure de la journée, évolution par année
            hour_response_time = df_merge.groupby(["HourOfCall_x", "CalYear_x"],as_index=False).agg(mean=("ResponseTime","mean"))
            mean = hour_response_time["mean"]
            fig11 = px.bar(x=hour_response_time.HourOfCall_x, y=mean, 
                title='Temps de réponse moyen par heure',
                animation_frame = hour_response_time["CalYear_x"])
            fig11.update_layout(xaxis_title='Heure', yaxis_title='Temps de réponse')
            st.plotly_chart(fig11)

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

        #affichage du nombre d'intervention par type d'incident dans le groupe 'Special Service' et par année
        fig14 = plt.figure(figsize=(10,5))
        sns.countplot(x = df_merge['SpecialServiceType'], hue = df_merge['CalYear_x'], palette="Spectral")
        plt.title("Nombre d'incident par groupe d'incident Special Service")
        plt.xticks(rotation=90)
        st.pyplot(fig14)

    if third.toggle("Visualisation :globe_with_meridians:") :
        st.markdown(":blue-background[Analyses en lien avec des variables géographique] :globe_with_meridians:")

        #Nombre de mobilisation par groupe géographique par année
        df_merge_geo = df_merge.groupby(["gpe_geo","CalYear_x"], as_index=False).agg(
            count=("gpe_geo","count"))
        plt.figure(figsize=[200,200])
        fig15 = px.density_heatmap(df_merge, x='CalYear_x', y='gpe_geo', z='IncidentNumber',histfunc='count', color_continuous_scale='dense')
        fig15.update_layout(title="Nombre de mobilisations par groupe géographique par année", xaxis_title='Year',yaxis_title='gpe_geo')
        st.plotly_chart(fig15)

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

        #visualisation de distancemetrique vs responsetime avec plotly express
        @st.cache_data #ajout du caching decorator pour le chargement du graph
        def afficher_fig17():
            fig17 = sns.relplot(x = "ResponseTime", y = "DistanceMetrique", kind = 'line', data = df_merge)
            plt.title("DistanceMetrique vs ResponseTime")
            st.pyplot(fig17)
        afficher_fig17()

    if fourth.toggle("Visualisation :fire_extinguisher:"):
        st.markdown(":blue-background[Autres analyses] :fire_extinguisher:")
    
        #analyse du nombre d'incident par AdressQualifier
        df_merge_address = df_merge.groupby(["AddressQualifier","CalYear_x"], as_index=False).agg(
            count=("AddressQualifier","count"))

        fig18 = px.bar(x = df_merge_address['AddressQualifier'], y=df_merge_address['count'], animation_frame=df_merge_address['CalYear_x'])
        fig18.update_layout(title="Nombre d'incident par type d'adresse", xaxis_title='AddressQualifier',yaxis_title='count')
        st.plotly_chart(fig18)
        
        #Analyse du nombre de stations mobilisées par année
        df_merge_year = df_merge.groupby(["CalYear_x"], as_index=False).agg(
            count=("DeployedFromStation_Name","nunique"))

        fig19 = px.bar(x=df_merge_year['CalYear_x'], y=df_merge_year['count'])
        fig19.update_layout(title="Nombre de stations mobilisées par année", xaxis_title='CalYear',yaxis_title='count')
        st.plotly_chart(fig19)

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
            st.write('<div style="text-align: justify;">Idem que pour l’Anova, toutes les variables testées sauf DeployedFromLocation apparaissent comme ayant un effet significatif\
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
            st.write('<div style="text-align: justify;">Une valeur η² > 0.01 est considérée faible, > 0.06 est moyenne, > 0.14 est forte. \
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

    # add the link at the bottom of each page
    st.markdown("<a href='#linkto_top'>Link to top</a>", unsafe_allow_html=True)

elif page == pages[3]:
    #lecture du fichier mobilisation v2
    # df10 = pd.read_csv("/content/gdrive/MyDrive/Etudes/DataScientest/Projet/map_station_data.csv")#,sep="\t")
    df10 = pd.read_csv("map_station_data.csv")#,sep="\t")
    list_years = df10['CalYear_x'].unique()
    print (list_years)

    option = st.selectbox('Année', list_years)
    st.write('L\'année choisie est :', option)

    df_2020 = df10[df10['CalYear_x'] == option]
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

elif page == pages[4]:
    st.markdown("<h4 style='font-size:20px; margin-bottom: 0px;'>Modélisation</h4>", unsafe_allow_html=True)

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
                Cette variable est numérique et continue, nous faisons donc le **choix de tester des modèles de type régression**.''')
    texte = '''train-test-split avec :
    - Jeu de test : 20%
    - Application d'un random_state afin de figer les jeux d'entrainement et de test pour tous les modèles
                
    Dans un premier temps évaluation uniquement des scores pour déterminer les meilleures modèles.
    '''
    st.text(texte)
    
    #lecture du fichier pour la modélisation
    @st.cache_data #ajout du caching decorator pour le chargement du fichier
    def load_data_final(url):
        df = pd.read_csv(url)
        return df
    
    df = load_data_final("Dataset_Final.csv")

    @st.cache_data #ajout du cache decorator pour le preprocessing
    def preprocessing_cont(df):
        #remplacement des noms des jours de la variable Day par les chiffres correspondant pour faciliter l'encodage des variables temporelles
        df['Day'] = df['Day'].replace({'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7})

        #sélection des variables explicatives et variables cibles
        X = df.drop('ResponseTime', axis = 1)
        y = df['ResponseTime']

        #séparation en jeu d'entrainement et de test, on fixe la séparation avec le paramètre random_state
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        ##Préprocessing
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

        return X_train, y_train, X_test, y_test

    #exécution de la fonction de preprocessing
    X_train, y_train, X_test, y_test = preprocessing_cont(df)

    #chargement des modèles
    @st.cache_data #ajout du cache decorator pour le chargement des modeles
    def load_models():
        reglog_cont = joblib.load("model_reglog_cont")
        reglin_cont = joblib.load("model_reglin_cont")
        dtreg_cont = joblib.load("model_dtreg_cont")
        rf_reg_cont = joblib.load("model_rfreg_cont.joblib")
        ridge_cont = joblib.load("model_ridge_cont")
        lasso_cont = joblib.load("model_lasso_cont")
        return reglog_cont, reglin_cont, dtreg_cont, rf_reg_cont, ridge_cont, lasso_cont
    
    reglog_cont, reglin_cont, dtreg_cont, rf_reg_cont, ridge_cont, lasso_cont = load_models()

    #ajout du model reduit 
    @st.cache_data #ajout du cache decorator pour le preprocessing
    def preprocessing_cont_red(df):
        #conservation uniquement de distancemetrique, gpe_geo et de la variable cible
        df_reduc = df[['DistanceMetrique', 'gpe_geo', 'ResponseTime']]

        #sélection des variables explicatives et variables cibles
        X = df_reduc.drop('ResponseTime', axis = 1)
        y = df_reduc['ResponseTime']

        #séparation en jeu d'entrainement et de test, on fixe la séparation avec le paramètre random_state
        X_train_red, X_test_red, y_train_red, y_test_red = train_test_split(X, y, test_size=0.2, random_state=42)

        ##Adaptation du préprocessing qui ne contient pas de variable temporelles
        #séparation des colonnes numériques et catégorielles
        var_num = ['DistanceMetrique']
        var_cat = ['gpe_geo']

        X_train_red_num = X_train_red[var_num]
        X_train_red_cat = X_train_red[var_cat]
        X_test_red_num = X_test_red[var_num]
        X_test_red_cat = X_test_red[var_cat]

        #remplissage des valeurs manquantes par simple imputer avec la stratégie median pour les variables numériques et le most frequent pour les variables catégorielles
        #gestion des données manquantes pour les variables numériques
        imputer_num = SimpleImputer(missing_values=np.nan, strategy='median')
        X_train_red_num = imputer_num.fit_transform(X_train_red_num)
        X_test_red_num = imputer_num.transform(X_test_red_num)

        #gestion des données manquantes pour les variables catégorielles
        imputer_cat = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        X_train_red_cat = imputer_cat.fit_transform(X_train_red_cat)
        X_test_red_cat = imputer_cat.transform(X_test_red_cat)

        #standardisation des variables numériques avec StandardScaler
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        X_train_red_num = scaler.fit_transform(X_train_red_num)
        X_test_red_num = scaler.transform(X_test_red_num)

        #encodage des variables catégorielles
        from sklearn.preprocessing import OneHotEncoder

        encoder = OneHotEncoder(drop = 'first', sparse_output=False)
        X_train_red_cat = encoder.fit_transform(X_train_red_cat)
        X_test_red_cat = encoder.transform(X_test_red_cat)

        ##passage en dataframe des tableaux récupérés après encodage
        X_train_red_num = pd.DataFrame(X_train_red_num)
        X_test_red_num = pd.DataFrame(X_test_red_num)
        X_train_red_cat = pd.DataFrame(X_train_red_cat)
        X_test_red_cat = pd.DataFrame(X_test_red_cat)

        #concaténation des jeux d'entraînement et de test
        X_train_red = pd.concat([X_train_red_num, X_train_red_cat], axis=1)
        X_test_red = pd.concat([X_test_red_num, X_test_red_cat], axis=1)

        X_train_red.columns = X_train_red.columns.astype(str)
        X_test_red.columns = X_test_red.columns.astype(str)

        return X_train_red, X_test_red, y_train_red, y_test_red

    #exécution de la fonction de preprocessing
    X_train_red, X_test_red, y_train_red, y_test_red = preprocessing_cont_red(df)

    #chargement des modèles
    @st.cache_data #ajout du cache decorator pour le chargement des modeles
    def load_models_red():
        rfreg_cont_red = joblib.load("model_rfreg_cont_red.joblib")
        return rfreg_cont_red
    rfreg_cont_red = load_models_red()

    #chargement des scores de chaque modele
    @st.cache_data #ajout du cache decorator pour le chargement des scores de chaque modele
    def load_scores():
        reglog_cont_score_train = reglog_cont.score(X_train, y_train)
        reglog_cont_score_test = reglog_cont.score(X_test, y_test)
    
        reglin_cont_score_train = reglin_cont.score(X_train, y_train)
        reglin_cont_score_test = reglin_cont.score(X_test, y_test)

        dtreg_cont_score_train = dtreg_cont.score(X_train, y_train)
        dtreg_cont_score_test = dtreg_cont.score(X_test,y_test)

        rf_reg_cont_score_train = rf_reg_cont.score(X_train, y_train)
        rf_reg_cont_score_test = rf_reg_cont.score(X_test, y_test)

        ridge_cont_score_train = ridge_cont.score(X_train, y_train)
        ridge_cont_score_test = ridge_cont.score(X_test, y_test)

        lasso_cont_score_train = lasso_cont.score(X_train, y_train)
        lasso_cont_score_test = lasso_cont.score(X_test, y_test)

        rfreg_cont_red_score_train = rfreg_cont_red.score(X_train_red, y_train_red)
        rfreg_cont_red_score_test = rfreg_cont_red.score(X_test_red, y_test_red)

        return reglog_cont_score_train, reglog_cont_score_test, reglin_cont_score_train, reglin_cont_score_test, dtreg_cont_score_train, dtreg_cont_score_test, \
            rf_reg_cont_score_train, rf_reg_cont_score_test, ridge_cont_score_train, ridge_cont_score_test,lasso_cont_score_train, lasso_cont_score_test, \
            rfreg_cont_red_score_train, rfreg_cont_red_score_test

    reglog_cont_score_train, reglog_cont_score_test, reglin_cont_score_train, reglin_cont_score_test, dtreg_cont_score_train, dtreg_cont_score_test, \
        rf_reg_cont_score_train, rf_reg_cont_score_test, ridge_cont_score_train, ridge_cont_score_test,lasso_cont_score_train, lasso_cont_score_test,\
            rfreg_cont_red_score_train, rfreg_cont_red_score_test = load_scores()

    #affichage des scores pour comparatif
    table = st.data_editor([
        {"Modèle":"Régression Logistique", "Train Score" : reglog_cont_score_train, "Test Score" : reglog_cont_score_test},
        {"Modèle":"Régression Linéaire", "Train Score" : reglin_cont_score_train, "Test Score" : reglin_cont_score_test},
        {"Modèle":"Decision Tree Regressor", "Train Score" : dtreg_cont_score_train, "Test Score" : dtreg_cont_score_test},
        {"Modèle":"Random Forest Regressor", "Train Score" : rf_reg_cont_score_train, "Test Score" : rf_reg_cont_score_test},
        {"Modèle":"Bayesian Ridge", "Train Score" : ridge_cont_score_train, "Test Score" : ridge_cont_score_test},
        {"Modèle":"Lasso Lars", "Train Score" : lasso_cont_score_train, "Test Score" : lasso_cont_score_test},
        {"Modèle":"Random Forest (nb réduit de variables*)", "Train Score" : rfreg_cont_red_score_train, "Test Score" : rfreg_cont_red_score_test}
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

    # add the link at the bottom of each page
    st.markdown("<a href='#linkto_top'>Link to top</a>", unsafe_allow_html=True)