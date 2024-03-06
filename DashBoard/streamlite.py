import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

conn = mysql.connector.connect(
    host="processus.mysql.database.azure.com",
    user="oussama",
    password="oussama",
    database="OrderManagement"
)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css('style.css')

def run_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

def refresh_page(delay_seconds):
    time.sleep(delay_seconds)
    st.experimental_rerun()

st.title('Dashboard')

# Requête pour récupérer le nombre total de clients
query_customers = "SELECT COUNT(*) FROM customers"
total_customers = run_query(query_customers)[0][0]

# Requête pour récupérer le nombre total de commandes par client
query_orders = "SELECT customer_id, COUNT(*) as total_orders FROM orders GROUP BY customer_id"
orders_data = run_query(query_orders)

# Création des données pour le graphique
customer_ids = [data[0] for data in orders_data]
total_orders = [data[1] for data in orders_data]
#requete pour le chiffre d'affaires
query_chiffre_affaire = """
SELECT SUM(orderlines.quantity_ordered * products.unit_price) AS chiffre_affaire
FROM orderlines
JOIN products ON orderlines.product_id = products.product_id
JOIN orders ON orderlines.order_id = orders.order_id
WHERE orders.actual_status= 'validated' OR orders.actual_status= 'confiremd_by_customer';
"""
chiffre_affaire_data = run_query(query_chiffre_affaire)
chiffre_affaire = chiffre_affaire_data[0][0]

#requete pour le nombre d'ordre chaque jour
query_orders_per_day = """
SELECT DATE(order_date) AS order_date, COUNT(*) AS num_orders
FROM orders
GROUP BY DATE(order_date);
"""
orders_per_day_data = run_query(query_orders_per_day)
df_orders_per_day = pd.DataFrame(orders_per_day_data, columns=['order_date', 'num_orders'])
df_orders_per_day['order_date'] = pd.to_datetime(df_orders_per_day['order_date'])  

# Requête pour obtenir la quantité vendue et le montant total pour chaque produit
query_quantite_prix_produit = """
SELECT products.product_name, 
       SUM(orderlines.quantity_ordered) AS quantite_vendue,
       SUM(orderlines.quantity_ordered * products.unit_price) AS montant_total
FROM orderlines
JOIN products ON orderlines.product_id = products.product_id
JOIN orders ON orderlines.order_id = orders.order_id
WHERE orders.actual_status = 'validated' OR orders.actual_status= 'confiremd_by_customer'
GROUP BY products.product_name;
"""

quantite_prix_produit_data = run_query(query_quantite_prix_produit)
produits = [row[0] for row in quantite_prix_produit_data]
quantites = [row[1] for row in quantite_prix_produit_data]
montants = [row[2] for row in quantite_prix_produit_data]




st.markdown('<div class="info">', unsafe_allow_html=True)
st.markdown(f'<h2>Nombre total de clients : {total_customers}</h2>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<div class="info">', unsafe_allow_html=True)
st.markdown('<h2>Graphique : Nombre de commandes par client</h2>', unsafe_allow_html=True)
fig, ax = plt.subplots()
ax.bar(customer_ids, total_orders, color='orange')
ax.set_xlabel('ID Client')
ax.set_ylabel('Nombre de Commandes')
ax.set_title('Nombre de Commandes par Client')
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<div class="info">', unsafe_allow_html=True)
st.title('Chiffre d\'Affaires')
st.markdown(f'<div class="chiffre-affaire">{chiffre_affaire}</div>', unsafe_allow_html=True)
st.markdown('<h2>Graphique : Quantité Vendue et Montant Total pour Chaque Produit</h2>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(12, 8))
bar_width = 0.35
index = np.arange(len(produits))
bar1 = ax.bar(index, quantites, bar_width, label='Quantité Vendue', color='skyblue')
bar2 = ax.bar(index + bar_width, montants, bar_width, label='Montant Total', color='orange')
ax.set_xlabel('Produit')
ax.set_ylabel('Valeur')
ax.set_title('Quantité Vendue et Montant Total pour Chaque Produit')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(produits, rotation=45, ha='right')
plt.legend()
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<div class="info">', unsafe_allow_html=True)
st.markdown('<h2>Graphique : Nombre de commandes par jour</h2>', unsafe_allow_html=True)
plt.figure(figsize=(10, 6))
plt.plot(df_orders_per_day['order_date'], df_orders_per_day['num_orders'], marker='o', color='b')
plt.xlabel('Date de la Commande')
plt.ylabel('Nombre de Commandes')
plt.title('Nombre de Commandes par Jour')
plt.grid(True)
plt.xticks(df_orders_per_day['order_date'], [date.strftime('%Y-%m-%d') for date in df_orders_per_day['order_date']], rotation=45)
plt.xlim(df_orders_per_day['order_date'].min(), df_orders_per_day['order_date'].max())
plt.ylim(0, df_orders_per_day['num_orders'].max() + 5)
st.pyplot(plt)
st.markdown('</div>', unsafe_allow_html=True)

refresh_page(1000)