**Table of Contents**
	• [Overview]
	• [Features]
	• [Installation]
	• [Usage]
	• [Data Warehousing]
	• [Streamlit App]
	• [Sample Queries]
**Overview**
This project allows you to get datas of Phonepe pulse data visualization and exploration .Extracting the data  and process it to obtain information that can be visualized in a friendly manner .Stores it in MYSQL database, and provides a Streamlit web application to interact with the data and run SQL queries.
Features
**Data extraction and processing:**
	Extracted the  data from the Phonepe pulse Github repository through scripting and
	clone it..
**Database management:**
	Inserted the transformed data into a MySQL database for efficient storage and
	retrieval.
**Visualization and dashboard creation:**
	Created the live geo visualization dashboard using Streamlit and Plotly in Python
	to display the data in an interactive and visually appealing manner.
	
**Geo visualization:**
	Developed a Streamlit web application for data visualization and querying.
	
	Fetching the data from the MySQL database to display in the dashboard.
	10 different dropdown options for users to select different
	facts and figures to display on the dashboard.
**Installation**
	1. Clone this repository to your local machine.
	2. Install the required Python packages:
	
	import streamlit as st
	from streamlit_option_menu import option_menu
	import pandas as pd
	import mysql.connector
	import plotly.express as px
	import requests
	import json
	from PIL import Image
	
**Data Storage**
The project stores data in SQL database:
**MYSQL**
	• MYSQL is used for structured data storage.
	• It creates  9 tables:  Agg_Insurance,  Agg_Transaction,  Agg_user , Map_Insurance, Map_transaction , Map_User, Top_Insurance, Top_Transaction, Top_User in a database named PhonePe_Data.
**Streamlit App**
	• Run the Streamlit app using the following command:
streamlit run Phonepe.py
	• The app provides a user interface to:
		○ Retrieve data for a Phonepe user.
		○ View stored data in tables.
		○ Execute SQL queries on the data.
**Sample Queries**
	• The project includes sample SQL queries for data analysis and reporting. You can customize and expand these queries according to your requirements.
**Contributing**
Contributions to this project are welcome. You can contribute by opening issues, suggesting enhancements, or creating pull requests.
