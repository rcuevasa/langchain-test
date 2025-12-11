import langchain_helper as lch
import streamlit as st

st.title("Pet Name Generator")

animal_type = st.sidebar.selectbox("Select Animal Type", ["cat", "dog", "hamster", "parrot", "cow"])

if animal_type == 'cat':
    pet_color = st.sidebar.text_area("What Color is your Cat?", max_chars=15)
elif animal_type == 'dog':
    pet_color = st.sidebar.text_area("What Color is your Dog?", max_chars=15)
elif animal_type == 'hamster':
    pet_color = st.sidebar.text_area("What Color is your Hamster?", max_chars=15)
elif animal_type == 'cow':
    pet_color = st.sidebar.text_area("What Color is your Cow?", max_chars=15)
else:
    pet_color = st.sidebar.text_area("What Color is your Parrot?", max_chars=15)


if pet_color:
    #response = lch.generate_pet_names(animal_type, pet_color)
    response = lch.generate_pet_names(animal_type, pet_color)
    st.subheader("Here are some name suggestions for your pet:")

    for index,name in enumerate(response['names']):
        st.write(f"{index + 1}. {name}")

    print(response)
