import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Les Sales Online", page_icon=":bar_chart:", layout="wide")

# Charger les données
@st.cache_data
def load_data():
    try:
        return pd.read_csv("C:/Users/youmn/OneDrive/Bureau/FAC/Master 1/Formation/DataViz/file_clean.csv")
    except FileNotFoundError:
        st.error("Failed to load data. The specified file path does not exist.")
        return pd.DataFrame()

df1 = load_data().copy()

# Fonctions pour chaque page
def page1():
    st.title("Voici l'application du Projet Data Management")
    st.markdown("""
    <div style='background-color: black; padding: 10px; border-radius: 10px;'>
        <h2>Introduction</h2>
        <p>L'application partagée présente ensemble riche et varié de données relatives à des transactions d'achat en ligne auprès de quelques villes d'Etats-Unis.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader('Statistiques descriptives')
    st.write(df1.describe())

    st.subheader("Description de nos variables présentes au sein de notre base de données")
    st.write("Detailed description here...")

    df1['Transaction_Date'] = pd.to_datetime(df1['Transaction_Date'])
    df1['Month'] = df1['Transaction_Date'].dt.month
    gender_coupon_table = pd.crosstab(df1['Gender'], df1['Coupon_Status'])

    st.subheader("Correlation Categorical")
    st.write(gender_coupon_table)

    fig = px.histogram(df1, x='Online_Spend', color='Gender',
                       title='Distribution of Online Spend by Gender')
    fig.update_layout(xaxis_title='Online Spend', yaxis_title='Count')
    st.plotly_chart(fig)

    st.subheader("Fréquence et Distribution")
    st.write(df1['Gender'].value_counts())
    st.write(df1['Location'].value_counts())

    gender_counts = df1['Gender'].value_counts()
    fig, ax = plt.subplots()
    gender_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Number of Transactions by Gender')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Number of Transactions')
    st.pyplot(fig)

def page2():
    st.markdown("<h1 style='color: skyblue;'>Visualisations</h1>", unsafe_allow_html=True)

    # Supposons que df1 contient déjà 'Loyalty_Score' et 'Total_Spend'
    fig = px.scatter(df1, x='Loyalty_Score', y='Total_Spend',
                     color='Loyalty_Score', size='Total_Spend',
                     hover_data=['CustomerID'],
                     title='Score de Fidélité vs Dépense Totale')
    fig.update_layout(xaxis_title='Score de Fidélité', yaxis_title='Dépense Totale ($)')
    st.plotly_chart(fig)

    # Calcul du montant moyen dépensé en ligne par mois
    monthly_online_spend = df1.groupby('Month')['Online_Spend'].mean()

    # Visualisation
    fig = px.line(monthly_online_spend, title='Dépense Moyenne en Ligne par Mois',
                  labels={'value': 'Dépense Moyenne en Ligne ($)', 'variable': 'Mois'})
    fig.update_layout(xaxis_title='Mois', yaxis_title='Dépense Moyenne en Ligne ($)')
    st.plotly_chart(fig)

    # Groupement par mois et genre, puis calcul de la moyenne des dépenses en ligne
    monthly_gender_online_spend = df1.groupby(['Month', 'Gender'])['Online_Spend'].mean().unstack()

    # Visualisation avec un graphique à lignes
    fig = px.line(monthly_gender_online_spend, title='Montant Moyen Dépensé en Ligne par Mois et par Genre',
                  labels={'value': 'Dépense Moyenne en Ligne ($)', 'variable': 'Mois'})
    fig.update_layout(xaxis_title='Mois', yaxis_title='Dépense Moyenne en Ligne ($)')
    st.plotly_chart(fig)

    # Groupement par catégorie de produit et somme des quantités
    category_quantity = df1.groupby('Product_Category')['Quantity'].sum()

    # Visualisation en diagramme à barres
    fig = px.bar(category_quantity, title='Quantité Totale Vendue par Catégorie de Produit',
                 labels={'value': 'Quantité Vendue', 'variable': 'Catégorie de Produit'})
    fig.update_layout(xaxis_title='Catégorie de Produit', yaxis_title='Quantité Vendue')
    st.plotly_chart(fig)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Sélectionnez une page", ["Statistiques descriptives", "Visualisations"])

if page == "Statistiques descriptives":
    page1()
elif page == "Visualisations":
    page2()

st.sidebar.title("Options supplémentaires")
if st.sidebar.checkbox("Show/Hide"):
    st.sidebar.text('Showing or hiding Widget')

status = st.sidebar.radio("What is your status", ['Activate', 'Inactivate'])
if status == 'Activate':
    st.sidebar.success("You're activated")
else:
    st.sidebar.warning("Inactivate")

occupation = st.sidebar.selectbox("Your occupation", ['Banquier', 'Data engineer', 'Etudiant'])
st.sidebar.write('You selected this option', occupation)

location = st.sidebar.multiselect("Where do you work", ['Lille', 'Marseille', 'Paris', 'Autre'])
st.sidebar.write(f"You have selected {len(location)} location/s")

level = st.sidebar.slider("What is your level", 1, 5)

# Download data
if st.sidebar.button('Télécharger les données'):
    csv = df1.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Télécharger CSV</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
