![226621611-58ea743a-9f9d-43cd-880f-39e0f4e45b9c](https://github.com/pavisugunaraj/phonepe-data-pulse-visualization/assets/156047936/4eae0ae3-891a-48eb-b642-4c9f15a22c52)

<h1>Data Visualization and Exploration : A User-Friendly Tool Using Streamlit and Plotly</h1>


      I have create a web app to analyse the Phonepe transaction and users depending on various Years, Quarters, States, and Types of transaction and give a Geographical and Geo visualization output based on given requirements.


<h3>THE MAIN COMONENTS OF THE DASHBOARD ARE:</h3>
       
          1 GEO-VISUALIZATION

          2 TRANSACTIONS ANALYSIS

          3 USERS ANALYSIS

          4 TOP STATES DATA


![image](https://github.com/pavisugunaraj/phonepe-data-pulse-visualization/assets/156047936/d4ffbb8d-2612-419b-9f8d-ffc2fb587040)

<h3>Import Libraries</h3>

<h4>Clone Libraries</h4>

    import requests
    import subprocess

<h4>Pandas, Numpy and File handling libraries</h4>

    import pandas as pd
    import numpy as np
    import os
    import json

<h4>SQL libraries</h4>

    import mysql.connector
    import sqlalchemy
    from sqlalchemy import create_engine
    import pymysql

<h4>Dashboard libraries</h4>

    import streamlit as st
    import plotly.express as px


<h1>Workflow</h1>

<h2>Step 1:</h2>

Importing the libraries. As I have already mentioned above the list of libraries/modules needed for the project. First we have to import all those libraries. If the libraries are not installed already use the below piece of code to install

    !pip install ["Name of the library"]
    
If the libraries are already installed then we have to import those into our script by mentioning the below codes.

    import pandas as pd
    import mysql.connector as sql
    import streamlit as st
    import plotly.express as px
    import os
    import json
    from streamlit_option_menu import option_menu
    from PIL import Image
    from git.repo.base import Repo.

<h2>Step 2:</h2>

Data extraction:

Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as JSON. Use the below syntax to clone the phonepe github repository into your local drive.

    from git.repo.base import Repo
    Repo.clone_from("GitHub Clone URL","Path to get the cloded files")

<h2>Step 3:</h2>

Data transformation:

In this step the JSON files that are available in the folders are converted into the readeable and understandable DataFrame format by using the for loop and iterating file by file and then finally the DataFrame is created. In order to perform this step I've used os, json and pandas packages. And finally converted the dataframe into CSV file and storing in the local drive.

path1 = "Path of the JSON files"
agg_trans_list = os.listdir(path1)


columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],'Transaction_amount': []}

Looping through each and every folder and opening the json files appending only the required key and values and creating the dataframe.

for state in agg_trans_list:
    cur_state = path1 + state + "/"
    agg_year_list = os.listdir(cur_state)

    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)

        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            A = json.load(data)

            for i in A['data']['transactionData']:
                name = i['name']
                count = i['paymentInstruments'][0]['count']
                amount = i['paymentInstruments'][0]['amount']
                columns1['Transaction_type'].append(name)
                columns1['Transaction_count'].append(count)
                columns1['Transaction_amount'].append(amount)
                columns1['State'].append(state)
                columns1['Year'].append(year)
                columns1['Quarter'].append(int(file.strip('.json')))
            
df = pd.DataFrame(columns1)

Converting the dataframe into csv file

df.to_csv('filename.csv',index=False)

<h2>Step 4:</h2>

Database insertion:

To insert the datadrame into SQL first I've created a new database and tables using "postgres SQL" library in Python to connect to a MySQL database and insert the transformed data using SQL commands.

Creating the connection between python and mysql

    mydb=psycopg2.connect(host="localhost",
                                user="postgres",
                                password="dev@0905",
                                database="phonepe_data",
                                port="5432"
                                )
    cursor=mydb.cursor()

Creating tables

        create_query= '''create table if not exists aggregated_transaction (States varchar(100),
                                                        Years int,
                                                        Quarter int,
                                                        Transaction_Type text,
                                                        Transaction_Count bigint,
                                                        Transaction_Amount bigint
                                                         )'''
        cursor.execute(create_query)
        mydb.commit()
        for index,row in aggregated_transaction.iterrows():
            insert_query=''' insert into aggregated_transaction (States,
                                                        Years,
                                                        Quarter,
                                                        Transaction_Type,
                                                        Transaction_Count,
                                                        Transaction_Amount)
                                                    values(%s,%s,%s,%s,%s,%s)'''
                                                    
            values=(row['States'],
            row['Years'],
            row['Quarter'],
            row['Transaction_Type'],
            row['Transaction_Count'],
            row['Transaction_Amount']
            )
    cursor.execute(insert_query,values)
    mydb.commit()


<H2>Step 5:</H2>

Dashboard creation:

To create colourful and insightful dashboard I've used Plotly libraries in Python to create an interactive and visually appealing dashboard. Plotly's built-in Pie, Bar, Geo map functions are used to display the data on a charts and map and Streamlit is used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.

<H2>Step 6:</H2>

Data retrieval:

Finally if needed Using the "postgres-connector-python" library to connect to the MySQL database and fetch the data into a Pandas dataframe.
