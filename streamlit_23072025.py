import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

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

pages = ["Introduction","Jeux de données","Data Visualisation","Cartographie","Prédiction du temps de réponse"]
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
        st.markdown("<h4>2. Période</h4>", unsafe_allow_html=True)
        st.markdown("<h4>3. Remarques</h4>", unsafe_allow_html=True)
        st.markdown("<h4>4. Exploration des données</h4>", unsafe_allow_html=True)
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
        
        st.markdown("<h4>5. Traitement des données</h4>", unsafe_allow_html=True)
        st.markdown("<h4>6. Ajout de variables</h4>", unsafe_allow_html=True)
        st.markdown("""
        Pour alimenter et réduire la complexité de notre jeu de données, nous avons procédé à des ajouts de variables.<br>
        - ResponseTime : Somme des colonnes TurnoutTimeSeconds (temps de mobilisation des pompiers) et TravelTimeSeconds (temps de trajet des pompiers).<br>
        - Jour de la semaine / Numéro de la semaine / Mois : Obtenues à partir de la colonne DateAndTimeMobilised.<br>
        - PropertyCategory_bis : Split en 3 catégories de PropertyCategory, les deux les plus présentes et regroupement des autres catégories dans une catégorie other.<br>
        - AddressQualifier_bis : Split en 3 catégories de AddressQualifier, les deux les plus présentes et regroupement des autres catégories dans une catégorie other.<br><br>
        <span style="font-weight: 900;">Extrait du DataFrame</span>
        """, unsafe_allow_html=True)
        
    elif choix == "Dataset Secondaire":
        st.markdown("<h4>Dataset Secondaire</h4>", unsafe_allow_html=True)
        st.markdown("<h4>1. Source</h4>", unsafe_allow_html=True)
        st.markdown("""Le deuxième jeu de données est construit à partir des informations présentes sur le site <a href='https://www.london-fire.gov.uk/community/your-borough/' target='_blank' style='color: #1b1a1a; text-decoration: underline;'>London Fire Brigade</a>.<br>""", unsafe_allow_html=True)
        st.markdown("<h4>2. Période</h4>", unsafe_allow_html=True)
        st.markdown("<h4>3. Remarques</h4>", unsafe_allow_html=True)
        st.markdown("<h4>4. Exploration des données</h4>", unsafe_allow_html=True)

elif page == pages[2]:
    st.write("Data Visualisation")
    #lecture du fichier merge pour la dataviz streamlit
    df_merge = pd.read_csv("fichier_dataviz_streamlit.csv")

    st.markdown("<h4 style='font-size:20px; margin-bottom: 0px;'>Data Visualisation</h4>", unsafe_allow_html=True)
    choix = st.selectbox("Wich analyse would you see ?",("Analyse en lien avec des variables de temps et de date", "Analyse par type d'incident", 
                                                               "Analyses en lien avec des variables géographique","Autres analyses"))

    if choix == "Analyse en lien avec des variables de temps et de date":
        
        second_choice = st.radio("",options=["Année", "Mois", "Semaine", "Jour", "Heure"])

        if second_choice == "Année" :

            #nombre de mobilisation par année
            df_year = df_merge.groupby(["CalYear_x"], as_index=False).agg(count=("IncidentNumber","count"))  
            #représentation en histogramme avec plotly
            fig = px.histogram(df_year,x = 'CalYear_x', y='count',nbins=30, title="Nombre de mobilisations par année")
            fig.update_layout(bargap=0.2)
            st.plotly_chart(fig)

            #analyse temps moyen de mobilisation et de trajet par année
            year_travel_time = df_merge.groupby("CalYear_x")["TravelTimeSeconds"].mean()
            year_turnout_time = df_merge.groupby("CalYear_x")["TurnoutTimeSeconds"].mean()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = year_travel_time.index, y = year_travel_time.values,mode='lines',name='TravelTimeSeconds'))
            fig.add_trace(go.Scatter(x = year_turnout_time.index, y = year_turnout_time.values,mode='lines',name='TurnoutTimeSeconds'))
            fig.update_layout(title='Temps moyen de mobilisation et de trajet par année')
            st.plotly_chart(fig)

            #Analyse du temps de réponse moyen par année
            year_response_time = df_merge.groupby("CalYear_x")["ResponseTime"].mean()
            fig=px.bar(x = year_response_time.index, y = year_response_time.values, title='Temps de réponse moyen par année')
            fig.update_layout(xaxis_title='Année', yaxis_title='Temps de réponse')
            st.plotly_chart(fig)
    
        elif second_choice == "Mois" :

            #analyse du temps de réponse moyen par mois
            df_month = df_merge.groupby(["month"], as_index=False).agg(count=("month","count"), moyenne_temps=("ResponseTime","mean"))
            fig = px.line(x=df_month['month'], y=df_month['moyenne_temps'], title='Temps de réponse moyen par mois')
            fig.update_layout(xaxis_title='Mois', yaxis_title='Temps de réponse moyen', yaxis_range=[300,400])
            fig.update_layout(xaxis_labelalias={1:'Janvier', 2:'Février', 3:'Mars', 4:'Avril', 5:'Mai', 6:'Juin', 7:'Juillet', 8:'Août', 9:'Septembre', 10:'Octobre', 11:'Novembre', 12:'Décembre'})
            st.plotly_chart(fig)

            #analyse de la répartition des temps de réponse par mois
            fig = px.box(x=df_merge['month'], y=df_merge['ResponseTime'], title='Répartition des temps de réponse par mois')
            fig.update_layout(xaxis_title='Mois', yaxis_title='Temps de réponse')
            fig.update_layout(xaxis_labelalias={1:'Janvier', 2:'Février', 3:'Mars', 4:'Avril', 5:'Mai', 6:'Juin', 7:'Juillet', 8:'Août', 9:'Septembre', 10:'Octobre', 11:'Novembre', 12:'Décembre'})
            st.plotly_chart(fig)

            #analyse de la répartition du temps de trajet par mois
            fig = px.box(x=df_merge['month'], y=df_merge['TravelTimeSeconds'], title='Répartition du temps de trajet par mois')
            fig.update_layout(xaxis_title='Mois', yaxis_title='Temps de trajet')
            fig.update_layout(xaxis_labelalias={1:'Janvier', 2:'Février', 3:'Mars', 4:'Avril', 5:'Mai', 6:'Juin', 7:'Juillet', 8:'Août', 9:'Septembre', 10:'Octobre', 11:'Novembre', 12:'Décembre'})
            st.plotly_chart(fig)

        elif second_choice == "Semaine" :

            #analyse du temps de réponse moyen par semaine
            df_week = df_merge.groupby(["week"], as_index=False).agg(count=("week","count"), moyenne_temps=("ResponseTime","mean"))
            fig = px.line(x=df_week['week'], y=df_week['moyenne_temps'], title='Temps de réponse moyen par semaine')
            fig.update_layout(xaxis_title='Semaine', yaxis_title='Temps de réponse moyen', yaxis_range=[300,400])
            st.plotly_chart(fig)

            #Répartition des temps de réponse par semaine
            fig = px.box(x=df_merge['week'], y=df_merge['ResponseTime'], title='Répartition des temps de réponse par semaine')
            fig.update_layout(xaxis_title='Semaine', yaxis_title='Temps de réponse')
            st.plotly_chart(fig)

        elif second_choice == "Jour" :

            #analyse du temps de trajet moyen par jour de la semaine
            day_response_time = df_merge.groupby("Day")["TravelTimeSeconds"].mean()
            fig = px.bar(x=day_response_time.index, y=day_response_time.values, title='Temps de trajet moyenne par jour de la semaine')
            fig.update_layout(xaxis_title='Jour', yaxis_title='Temps de trajet')
            st.plotly_chart(fig)

        elif second_choice == "Heure" :
            
            #temps de réponse moyen par heure de la journée
            df_hour = df_merge.groupby(["HourOfCall_x"], as_index=False).agg(ResponseTime_moyen=("ResponseTime","mean"))
            #affichage temps moyen intervention
            fig = px.line(df_hour, x='HourOfCall_x', y='ResponseTime_moyen', title='Temps de réponse moyen par heure de la journée')
            fig.update_layout(xaxis_title='Heure de la journée', yaxis_title='Temps de réponse moyen')
            st.plotly_chart(fig)

            #analyse du temps de réponse moyen par heure de la journée, évolution par année
            hour_response_time = df_merge.groupby(["HourOfCall_x", "CalYear_x"],as_index=False).agg(mean=("ResponseTime","mean"))
            mean = hour_response_time["mean"]
            fig = px.bar(x=hour_response_time.HourOfCall_x, y=mean, 
                title='Temps de réponse moyen par heure',
                animation_frame = hour_response_time["CalYear_x"])
            fig.update_layout(xaxis_title='Heure', yaxis_title='Temps de réponse')
            st.plotly_chart(fig)


    elif choix == "Analyse par type d'incident" :

        #affichage du nombre d'intervention par 'IncidentGroup' et par année
        nb_incident_by_group = df_merge.groupby(["IncidentGroup","CalYear_x"], as_index=False).agg(
            count=("IncidentGroup","count"))
        fig = px.bar(x = nb_incident_by_group["IncidentGroup"] ,y = nb_incident_by_group['count'],
             title="Nombre d'incident par groupe d'incident",
             animation_frame = nb_incident_by_group['CalYear_x'])
        fig.update_layout(xaxis_title='CalYear',yaxis_title='IncidentGroup')
        st.plotly_chart(fig)

        #affichage du responsetime moyen par 'IncidentGroup' et par année
        resptime_incident_by_group = df_merge.groupby(["IncidentGroup","CalYear_x"], as_index=False).agg(mean=("ResponseTime","mean"))
        fig = px.bar(x = resptime_incident_by_group["IncidentGroup"] ,y = resptime_incident_by_group['mean'],
             title="Temps moyen de réponse par groupe d'incident",
             animation_frame = resptime_incident_by_group['CalYear_x'])
        fig.update_layout(xaxis_title='CalYear',yaxis_title='Mean ResponseTime')
        st.plotly_chart(fig)

        #affichage du nombre d'intervention par type d'incident dans le groupe 'Special Service' et par année
        fig = plt.figure(figsize=(10,5))
        sns.countplot(x = df_merge['SpecialServiceType'], hue = df_merge['CalYear_x'], palette="Spectral")
        plt.title("Nombre d'incident par groupe d'incident")
        plt.xticks(rotation=90)
        plt.show()

    elif choix == "Autres analyses" :

        #visualisation de distancemetrique vs responsetime avec plotly express
        fig = sns.relplot(x = "ResponseTime", y = "DistanceMetrique", kind = 'line', data = df_merge)
        plt.title("DistanceMetrique vs ResponseTime")
        st.show(fig)

elif page == pages[3]:
    #lecture du fichier mobilisation v2
    df10 = pd.read_csv("/content/gdrive/MyDrive/Etudes/DataScientest/Projet/map_station_data.csv")#,sep="\t")
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
