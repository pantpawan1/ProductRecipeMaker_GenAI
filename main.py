## Integrate our code OpenAI API
import os
import load_dotenv
import streamlit as st
import pandas as pd
from constants import openai_key
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain import PromptTemplate
import json

load_dotenv()
os.environ["OPENAI_API_KEY"]=openai_key

# read by default 1st sheet of an excel file
df = pd.read_excel(r'C:\Users\XJ768PU\Downloads\ProductList.xlsx')

 
# Get the unique values of a particular column
selected_column = "Alcoholic Drinks"
unique_values = df[selected_column].unique()

# select the recepie
recepie_type = st.selectbox("Select Menu",["Starter","Drinks","Main Course"])

if recepie_type =='Drinks':
    drinktype = st.selectbox("Alcoholic/Non-Alcoholic",["Alcoholic","Non Alcoholic"])
    if drinktype =="Alcoholic":
        selected_column = "Alcoholic Drinks"
    else:    
        selected_column = "Non Alcoholic"
     
        
elif recepie_type =='Starter':
    selected_column = "Starter"
    
elif recepie_type =='Main Course':
    selected_column = "Main Course"

unique_values = df[selected_column].unique()

# Filter out "NaN" values from unique_values
unique_values = [value for value in unique_values if not pd.isna(value)]


# streamlit framework
st.title('Select the ingirdients which you want to use for making dish')

## OPENAI LLMS
llm=OpenAI(temperature=0.8)

# Create a multi-select dropdown using Streamlit
selected_values = st.multiselect("Select Values", options=unique_values)

# Create a text input box
user_input = st.text_input("Enter additional ingridients here:")

# Create a text input box
user_preference = st.text_input("nutrition instruction here:")


# Apply custom CSS to highlight selected values
elected_style = "background-color: lightblue"
default_style = ""

# Filter the DataFrame based on the selected values
filtered_df = df[df[selected_column].isin(selected_values)]

# Create a "Submit" button
submit_button = st.button("Submit")


# Display the filtered DataFrame with highlighted rows after clicking "Submit"
if submit_button:
    user_input = user_input+","
    selected_products = ", ".join(filtered_df[selected_column].tolist())  # Comma-separated product names
    user_input += "\n"  # Add a newline before adding ingredients
    user_input += selected_products
    
    if recepie_type =='Drinks':
        if selected_column == 'Alcoholic':
            template = '''you are an expereinced bar tender.
            Please generate a JSON representation of a {recepie} with alcoholic drink name that aligns with '{user_preference}' nutrition preferences. Include ingredient quantities, preparation instructions, and nutrition details by ensuring that both the nutrition detils and ingredient quantities are enclosed in double quotes. Use the following ingredients: {ingredients}. Instructions: {instructions} .'''
        else:
            template = '''you are an expereinced bar tender.
            Please generate a JSON representation of a {recepie} with drink name that aligns with '{user_preference}' nutrition preferences. Include ingredient quantities, preparation instructions, and nutrition details by ensuring that both the nutrition detils and ingredient quantities are enclosed in double quotes. Use the following ingredients: {ingredients}. Instructions: {instructions} . '''
    
    else:
       #creating prompt template for sending input 
       template = '''You are an experienced chef.
       Please generate a JSON representation of a {recepie} with recepie name that aligns with '{user_preference}' nutrition preferences. Include ingredient quantities, preparation instructions, and nutrition details by ensuring that both the nutrition detils and ingredient quantities are enclosed in double quotes. Use the following ingredients: {ingredients}. Instructions: {instructions} .
       '''
    #give instructions
    instructions = """1.Create a recipe using ONLY the following ingredients:{user_input}..
                  2.Do NOT include any additcoional ingredients apart from {user_input}.
                  3.Ensure that the recipe focuses on {user_preference} nutrition with given {user_input} ingredients only..
                  4.In recepie name word do not include keyword {user_preference}.
                  """   
     
    promp = PromptTemplate(
    input_variables=['recepie','user_preference','ingredients','instructions'],
    template=template
    )
    llm = OpenAI(model='text-davinci-003',temperature=0.1)
    output = llm(promp.format(recepie=recepie_type,user_preference=user_preference,ingredients=user_input,instructions=instructions))
    print("Before Strips")
    print(output)
    print("after strips")
    output = output.strip()
    # Correct the JSON format
    output = json.dumps(json.loads(output), indent=4)
    json_string = json.loads(output)
    print(json_string)
    st.json(json_string)
    #st.write(json_string(0))