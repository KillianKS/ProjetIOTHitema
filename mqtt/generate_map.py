import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json
from datetime import datetime
import altair as alt
import os

# Titre
st.set_page_config(layout="wide")
st.title("🌍 Dashboard des Capteurs IoT")

# Charger les données JSON
file_path = "capteurs_data.json"
if not os.path.exists(file_path):
    st.warning("Fichier JSON non trouvé.")
    st.stop()

with open(file_path, "r") as f:
    data_json = json.load(f)

# Parser les données dans un DataFrame
data_list = []
for entry in data_json:
    capteur_id = entry.get("id_capteur")
    position = entry.get("position")
    mesures = entry.get("mesures", {})
    temperature = entry.get("temperature")
    humidite = entry.get("humidite")
    timestamp = entry.get("timestamp", datetime.now().isoformat())
    
    # Facultatif : convertir la position en coordonnées
    # Exemple fixe (à adapter si besoin)
    positions_dict = {
        "serre_nord": [48.8566, 2.3522],
        "serre_sud": [43.6045, 1.4440],
        "serre_est": [45.7640, 4.8357],
        "serre_ouest": [47.2184, -1.5536],
    }
    coords = positions_dict.get(position, [0.0, 0.0])

    data_list.append({
        "id_capteur": capteur_id,
        "position": position,
        "latitude": coords[0],
        "longitude": coords[1],
        "temperature": temperature,
        "humidite": humidite,
        "timestamp": timestamp
    })

df = pd.DataFrame(data_list)

# Convertir timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Filtres utilisateur (sidebar)
st.sidebar.title("🔧 Filtres")
capteurs_ids = df["id_capteur"].unique().tolist()
types_mesures = ["temperature", "humidite"]

selected_capteurs = st.sidebar.multiselect("Choisir les capteurs", capteurs_ids, default=capteurs_ids)
selected_type = st.sidebar.selectbox("Type de mesure", types_mesures)

# Filtrage
df_filtered = df[df["id_capteur"].isin(selected_capteurs)]

# Carte interactive
st.subheader("🗺️ Carte des capteurs")
m = folium.Map(location=[46.603354, 1.888334], zoom_start=5)
for _, row in df_filtered.iterrows():
    popup = f"""
    <b>ID Capteur:</b> {row['id_capteur']}<br>
    <b>Position:</b> {row['position']}<br>
    <b>Température:</b> {row['temperature']} °C<br>
    <b>Humidité:</b> {row['humidite']} %
    """
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=popup,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
folium_static(m, width=900)

# Graphique des mesures
st.subheader("📈 Graphique des mesures")
if selected_type in df_filtered:
    chart = alt.Chart(df_filtered).mark_line(point=True).encode(
        x="timestamp:T",
        y=alt.Y(f"{selected_type}:Q", title=selected_type.capitalize()),
        color="id_capteur:N"
    ).properties(width=900, height=400)
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning(f"Aucune donnée pour {selected_type}")

# Statistiques par capteur
st.subheader("📊 Statistiques")
for mesure in types_mesures:
    if mesure in df_filtered:
        st.write(f"**Statistiques pour `{mesure}`**")
        stats = df_filtered.groupby("id_capteur")[mesure].agg(["mean", "min", "max", "std"]).reset_index()
        stats.columns = ["Capteur", "Moyenne", "Min", "Max", "Écart-type"]
        st.dataframe(stats, use_container_width=True)

# Dernières données brutes
st.subheader("📝 Données brutes (dernières lignes)")
st.dataframe(df_filtered.sort_values("timestamp", ascending=False).head(10), use_container_width=True)