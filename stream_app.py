import streamlit as st
import pandas as pd
st.title("My First Streamlit App")
st.header('Breakfast Menu')
st.text('Omega 3 & Blueberry Oatmeal')
st.text('Kale, Spinach & Rocket Smoothie')
st.text('Hard-Boiled Free-Range Egg')
st.text("🥣 🥗 🐔 🥑🍞")
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
st.dataframe(my_fruit_list)
st.multiselect("Pick some fruits:", list(my_fruit_list.index))
my_fruit_list = my_fruit_list.set_index('Fruit')
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)
streamlit.header("Fruityvice Fruit Advice!")
