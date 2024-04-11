import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json
from PIL import Image

#SQL Connection

mydb=mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe_Data",port="3306")
mycursor=mydb.cursor()

#Aggre_insurance df

mycursor.execute("select * from agg_insurance")
#mydb.commit()
table1=mycursor.fetchall()

Agg_insurance=pd.DataFrame(table1,columns=("States","Years", "Quarter","Transaction_type","Transaction_count","Transaction_amount"))


#Aggre_transaction df

mycursor.execute("select * from agg_transaction")
#mydb.commit()
table2=mycursor.fetchall()

Agg_transaction=pd.DataFrame(table2,columns=("States","Years", "Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#Aggre_user df

mycursor.execute("select * from agg_user")
#mydb.commit()
table3=mycursor.fetchall()

Agg_user=pd.DataFrame(table3,columns=("States","Years", "Quarter","Brands","Transaction_count","Percentage"))


#Map_insurance df

mycursor.execute("select * from map_insurance")
#mydb.commit()
table4=mycursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("States","Years", "Quarter","Districts","Transaction_count","Transaction_amount"))

#Map_trasaction df

mycursor.execute("select * from map_transaction")
#mydb.commit()
table5=mycursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("States","Years", "Quarter","Districts","Transaction_count","Transaction_amount"))

#Map_user df

mycursor.execute("select * from map_user")
#mydb.commit()
table6=mycursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("States","Years", "Quarter","Districts","registeredUsers","appOpens"))

#Top_insurance df

mycursor.execute("select * from top_insurance")
#mydb.commit()
table7=mycursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("States","Years", "Quarter","Pincodes","Transaction_count","Transaction_amount"))

#Top_transaction

mycursor.execute("select * from top_transaction")
#mydb.commit()
table8=mycursor.fetchall()

Top_transac=pd.DataFrame(table8,columns=("States","Years", "Quarter","Pincodes","Transaction_count","Transaction_amount"))



#Top_user df

mycursor.execute("select * from top_user")
#mydb.commit()
table9=mycursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("States","Years", "Quarter","Pincodes","registeredUsers"))


def Transaction_Amount_Count_Year(df,year):

    transac_amount_count_y=df[df["Years"]==year]
    transac_amount_count_y.reset_index(drop=True,inplace=True)

    transac_amount_count_y_g=transac_amount_count_y.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    transac_amount_count_y_g.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

      fig_amount=px.bar(transac_amount_count_y_g,x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    
      st.plotly_chart(fig_amount)

    with col2:
          

      fig_count=px.bar(transac_amount_count_y_g,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                      color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
      st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        
      url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
      response=requests.get(url)
      data1=json.loads(response.content)
      states_names=[]
      for feature in data1["features"]:

          states_names.append(feature["properties"]["ST_NM"])
          
      states_names.sort()

      fig_india_1=px.choropleth(transac_amount_count_y_g,geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color= "Transaction_amount",color_continuous_scale="Rainbow",range_color=(transac_amount_count_y_g["Transaction_amount"].min(),transac_amount_count_y_g["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",height=600,width=500)
      fig_india_1.update_geos(visible=False)
      st.plotly_chart(fig_india_1)
    with col2:
        
      fig_india_2=px.choropleth(transac_amount_count_y_g,geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color= "Transaction_count",color_continuous_scale="Rainbow",range_color=(transac_amount_count_y_g["Transaction_count"].min(),transac_amount_count_y_g["Transaction_count"].max()),
                                hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",height=600,width=550)
      fig_india_2.update_geos(visible=False)
      st.plotly_chart(fig_india_2)


    return   transac_amount_count_y


def Transaction_Amount_Count_Year_Q(df,quarter):
    transac_amount_count_y=df[df["Quarter"]==quarter]
    transac_amount_count_y.reset_index(drop=True, inplace=True)

    transac_amount_count_y_g=transac_amount_count_y.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    transac_amount_count_y_g.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        
      fig_amount=px.bar(transac_amount_count_y_g,x="States",y="Transaction_amount",title=f"{transac_amount_count_y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                      color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
      st.plotly_chart(fig_amount)

    with col2:
         
      fig_count=px.bar(transac_amount_count_y_g,x="States",y="Transaction_count",title=f"{transac_amount_count_y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                      color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
      st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        
      url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
      response=requests.get(url)
      data1=json.loads(response.content)
      states_names=[]
      for feature in data1["features"]:

          states_names.append(feature["properties"]["ST_NM"])
          
      states_names.sort()

      fig_india_1=px.choropleth(transac_amount_count_y_g,geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color= "Transaction_amount",color_continuous_scale="Rainbow",range_color=(transac_amount_count_y_g["Transaction_amount"].min(),transac_amount_count_y_g["Transaction_amount"].max()),
                                hover_name="States",title=f"{transac_amount_count_y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",height=500,width=500)
      fig_india_1.update_geos(visible=False)
      st.plotly_chart(fig_india_1)
    
    with col2:
          
      fig_india_2=px.choropleth(transac_amount_count_y_g,geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color= "Transaction_count",color_continuous_scale="Rainbow",range_color=(transac_amount_count_y_g["Transaction_count"].min(),transac_amount_count_y_g["Transaction_count"].max()),
                                hover_name="States",title=f"{transac_amount_count_y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",height=500,width=500)
      fig_india_2.update_geos(visible=False)
      st.plotly_chart(fig_india_2)

    return transac_amount_count_y

def Agg_Tran_Transaction_type(df,state):    

    transac_amount_count_y=df[df["States"]==state]
    transac_amount_count_y.reset_index(drop=True, inplace=True)

    transac_amount_count_y_g=transac_amount_count_y.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    transac_amount_count_y_g.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:  

      fig_piechart_1=px.pie(data_frame=transac_amount_count_y_g, names="Transaction_type", values="Transaction_amount" , width=400, title=f"{state.upper()} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Bluered,hole=0.50)
      st.plotly_chart(fig_piechart_1)

    with col2:  

      fig_piechart_2=px.pie(data_frame=transac_amount_count_y_g, names="Transaction_type", values="Transaction_count" , width=400, title=f"{state.upper()} TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered,hole=0.50)
      st.plotly_chart(fig_piechart_2)  

# Aggregated user Analysis_Yearwise
def Agg_user_plot_1(df,year):

    Agg_user_year=df[df["Years"]==year]
    Agg_user_year.reset_index(drop=True,inplace=True)
    Agg_user_year_g=pd.DataFrame(Agg_user_year.groupby("Brands")["Transaction_count"].sum())
    Agg_user_year_g.reset_index(inplace=True)

    fig_barchart_1=px.bar(Agg_user_year_g, x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION AMOUNT",
                        width=800,color_discrete_sequence=px.colors.sequential.haline, hover_name="Brands",)
    st.plotly_chart(fig_barchart_1)

    return Agg_user_year

#Aggregated user Analysis_Quarterwise

def Agg_user_plot_2(df,quarter):    
    Agg_user_year_Q=df[df["Quarter"]==quarter]
    Agg_user_year_Q.reset_index(drop=True,inplace=True)
    Agg_user_year_Q_g=pd.DataFrame(Agg_user_year_Q.groupby("Brands")["Transaction_count"].sum())
    Agg_user_year_Q_g.reset_index(inplace=True)

    fig_barchart_1=px.bar(Agg_user_year_Q_g, x="Brands", y="Transaction_count", title=f"{quarter} QUARTER , BRANDS AND TRANSACTION AMOUNT",
                            width=800,color_discrete_sequence=px.colors.sequential.haline_r,hover_name="Brands")
    st.plotly_chart(fig_barchart_1)      

    return  Agg_user_year_Q 

# Aggregated user Analysis_Statewise

def Agg_user_plot_3(df,state):
    agg_user_y_Q_S=df[df["States"]==state]
    agg_user_y_Q_S.reset_index(drop=True,inplace=True)

    fig_line_1=px.line(agg_user_y_Q_S, x="Brands", y="Transaction_count", hover_data="Percentage",
                    title=f"{state.upper()}  BRANDS , TRANSACTION COUNT AND PERCENTAGE", width=900, color_discrete_sequence=px.colors.sequential.haline, markers=True)
    st.plotly_chart(fig_line_1)


#Map_insurance_district

def Map_insur_District(df,state):    

    transac_amount_count_y=df[df["States"]== state]
    transac_amount_count_y.reset_index(drop=True, inplace=True)

    transac_amount_count_y_g=transac_amount_count_y.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    transac_amount_count_y_g.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        
      fig_barchart_1=px.bar(transac_amount_count_y_g, x="Transaction_amount", y="Districts", orientation="h",height=600,title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
      st.plotly_chart(fig_barchart_1)

    with col2:
       
      fig_barchart_2=px.bar(transac_amount_count_y_g, x="Transaction_count", y="Districts", orientation="h",height=600,title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Magenta)
      st.plotly_chart(fig_barchart_2)


# Map user plot_1:
def Map_user_plot_1(df,year):
    
    Map_user_year=df[df["Years"]==year]
    Map_user_year.reset_index(drop=True,inplace=True)

    Map_user_year_g=Map_user_year.groupby("States")[["registeredUsers","appOpens"]].sum()
    Map_user_year_g.reset_index(inplace=True)

    fig_line_1=px.line(Map_user_year_g, x="States", y="registeredUsers",
                        title=f"{year} REGISTERED USER", width=900,height=800, color_discrete_sequence=px.colors.sequential.haline, markers=True)
    st.plotly_chart(fig_line_1)

    fig_line_2=px.line(Map_user_year_g, x="States", y="appOpens",
                        title=f"{year} APPOPENS", width=900,height=800, color_discrete_sequence=px.colors.sequential.Magenta, markers=True)
    st.plotly_chart(fig_line_2)

    return Map_user_year

# Map user plot_2:
def Map_user_plot_2(df,quarter):
    
    Map_user_year_Q=df[df["Quarter"]==quarter]
    Map_user_year_Q.reset_index(drop=True,inplace=True)

    Map_user_year_g=Map_user_year_Q.groupby("States")[["registeredUsers","appOpens"]].sum()
    Map_user_year_g.reset_index(inplace=True)

    fig_line_1=px.line(Map_user_year_g, x="States", y="registeredUsers",
                        title=f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USER", width=900,height=800, color_discrete_sequence=px.colors.sequential.haline, markers=True)
    st.plotly_chart(fig_line_1)

    fig_line_2=px.line(Map_user_year_g, x="States", y="appOpens",
                        title=f"{df['Years'].min()} YEAR {quarter} QUARTER APPOPENS", width=900,height=800, color_discrete_sequence=px.colors.sequential.Magenta, markers=True)
    st.plotly_chart(fig_line_2)

    return Map_user_year_Q

# Map_user_plot_3
def Map_user_plot_3(df,states):

    Map_user_year_S=df[df["States"]==states]
    Map_user_year_S.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
        
      fig_Map_user_barchart_1=px.bar(Map_user_year_S,x="registeredUsers",y="Districts",orientation="h",
                                      title=f"{states.upper()} REGISTERED USER",height=800,color_discrete_sequence=px.colors.sequential.Bluyl_r)
      st.plotly_chart(fig_Map_user_barchart_1)

    with col2: 
      fig_Map_user_barchart_2=px.bar(Map_user_year_S,x="appOpens",y="Districts",orientation="h",
                                      title=f"{states.upper()} APPOPENS",height=800,color_discrete_sequence=px.colors.sequential.Bluered)
      st.plotly_chart(fig_Map_user_barchart_2)


# Top_insurance_plot_1
def Top_insur_plot_1(df,states):
    Top_insur_tac_Y_Q=df[df["States"]==states]
    Top_insur_tac_Y_Q.reset_index(drop=True,inplace=True)

    Top_insur_tac_Y_Q_g=Top_insur_tac_Y_Q.groupby("Pincodes")[["Transaction_count","Transaction_amount"]].sum()
    Top_insur_tac_Y_Q_g.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        
      fig_Top_insur_barchart_1=px.bar(Top_insur_tac_Y_Q,x="Quarter",y="Transaction_amount",hover_data="Pincodes",
                                      title="TRANSACTION AMOUNT",height=600,width=400,color_discrete_sequence=px.colors.sequential.Aggrnyl)
      st.plotly_chart(fig_Top_insur_barchart_1)
    with col2:
        
      fig_Top_insur_barchart_2=px.bar(Top_insur_tac_Y_Q,x="Quarter",y="Transaction_count",hover_data="Pincodes",
                                      title="TRANSACTION COUNT",height=600,width=400,color_discrete_sequence=px.colors.sequential.Bluered_r)
      st.plotly_chart(fig_Top_insur_barchart_2)

#Top_user_plot_1
def Top_user_plot_1(df,year):
    Top_user_year=df[df["Years"]==year]
    Top_user_year.reset_index(drop=True,inplace=True)
    Top_user_year_g=pd.DataFrame(Top_user_year.groupby(["States","Quarter"])["registeredUsers"].sum())
    Top_user_year_g.reset_index(inplace=True)

  
    fig_Top_user_plot_1=px.bar(Top_user_year_g,x="States",y="registeredUsers",color="Quarter",width=700,height=800,
                                      color_discrete_sequence=px.colors.sequential.GnBu_r,hover_name="States",
                                      title=f"{year} REGISTERED USERS ")
    st.plotly_chart(fig_Top_user_plot_1)

    return Top_user_year 

#Top_user_plot_2
def Top_user_plot_2(df,state):
    Topuser_year_state=df[df["States"]==state]
    Topuser_year_state.reset_index(drop=True,inplace=True)

    fig_Top_user_plot_2=px.bar(Topuser_year_state,x="Quarter", y="registeredUsers",title="REGISTERED USERS,PINCODES,QUARTER",width=800, height=700,
                               color="registeredUsers",hover_data="Pincodes",color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_Top_user_plot_2)

# Top_Chart
def Top_chart_transaction_amount(table_name):

    mydb=mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe_Data",port="3306")
    mycursor=mydb.cursor()

    #Queries
    Query1=f'''SELECT states, SUM(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount desc
                limit 10'''
    mycursor.execute(Query1)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states","transaction_amount"))
    
    col1,col2=st.columns(2)
    with col1:

      fig_amount_1=px.bar(df_1,x="states",y="transaction_amount",title="TOP 10 OF TRANSACTION AMOUNT",hover_name="states",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=500)
      st.plotly_chart(fig_amount_1)

    #Plot_2
    Query2=f'''SELECT states, SUM(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount
                limit 10'''
    mycursor.execute(Query2)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states","transaction_amount"))
    
    with col2:
       
      fig_amount_2=px.bar(df_2,x="states",y="transaction_amount",title="LAST 10 OF TRANSACTION AMOUNT",hover_name="states",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=500)
      st.plotly_chart(fig_amount_2)


    #Plot_3
    Query3=f'''SELECT states, avg(transaction_amount) as transaction_amount
                    from {table_name}
                    group by states
                    order by transaction_amount '''
                
    mycursor.execute(Query3)
    table_3=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states","transaction_amount"))

    fig_amount_3=px.bar(df_3,y="states",x="transaction_amount",title="AVERAGE OF TRANSACTION AMOUNT",hover_name="states",
                        orientation="h",color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
    st.plotly_chart(fig_amount_3)

#Top_chart transaction_count
def Top_chart_transaction_count(table_name):

    mydb=mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe_Data",port="3306")
    mycursor=mydb.cursor()

    #Queries
    Query1=f'''SELECT states, SUM(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count desc
                limit 10'''
    mycursor.execute(Query1)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states","transaction_count"))
    
    col1,col2=st.columns(2)
    with col1:

      fig_amount_1=px.bar(df_1,x="states",y="transaction_count",title="TOP 10 OF TRANSACTION COUNT",hover_name="states",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
      st.plotly_chart(fig_amount_1)

    #Plot_2
    Query2=f'''SELECT states, SUM(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count
                limit 10'''
    mycursor.execute(Query2)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states","transaction_count"))
    with col2:
      fig_amount_2=px.bar(df_2,x="states",y="transaction_count",title="LAST 10 OF TRANSACTION COUNT",hover_name="states",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
      st.plotly_chart(fig_amount_2)


    #Plot_3
    Query3=f'''SELECT states, avg(transaction_count) as transaction_count
                    from {table_name}
                    group by states
                    order by transaction_count '''
                
    mycursor.execute(Query3)
    table_3=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states","transaction_count"))

    fig_amount_3=px.bar(df_3,y="states",x="transaction_count",title="AVERAGE OF TRANSACTION COUNT",hover_name="states",
                        orientation="h",color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

#Top_chart_RegisteredUser
def Top_chart_Registered_User(table_name,state):

    mydb=mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe_Data",port="3306")
    mycursor=mydb.cursor()

    #Queries
    Query1=f'''SELECT Districts, sum(registeredUsers) as registeredusers
                FROM {table_name}
                where states= '{state}'
                group by Districts
                order by registeredUsers desc
                limit 10;'''
    mycursor.execute(Query1)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("Districts","registeredusers"))
    
    col1,col2=st.columns(2)
    with col1:

      fig_amount_1=px.bar(df_1,x="Districts",y="registeredusers",title="TOP 10 OF REGISTERED USERS",hover_name="Districts",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
      st.plotly_chart(fig_amount_1)

    #Plot_2
    Query2=f'''SELECT Districts, sum(registeredUsers) as registeredusers
                FROM {table_name}
                where states= '{state}'
                group by Districts
                order by registeredUsers
                limit 10;'''
    mycursor.execute(Query2)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("Districts","registeredusers"))
    
    with col2:

      fig_amount_2=px.bar(df_2,x="Districts",y="registeredusers",title="LAST 10 OF REGISTERED USERS",hover_name="Districts",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
      st.plotly_chart(fig_amount_2)


    #Plot_3
    Query3=f'''SELECT Districts, avg(registeredUsers) as registeredusers
                FROM {table_name}
                where states= '{state}'
                group by Districts
                order by registeredUsers;'''
              
                
    mycursor.execute(Query3)
    table_3=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("Districts","registeredusers"))

    fig_amount_3=px.bar(df_3,y="Districts",x="registeredusers",title="AVERAGE OF REGISTERED USERS",hover_name="Districts",
                        orientation="h",color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

#Top_chart_Appopens
def Top_chart_Appopens(table_name,state):

    mydb=mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe_Data",port="3306")
    mycursor=mydb.cursor()

    #Queries
    Query1=f'''SELECT Districts, sum(appopens) as appopens
                FROM {table_name}
                where states= '{state}'
                group by Districts
                order by appopens desc
                limit 10;'''
    mycursor.execute(Query1)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("Districts","appopens"))
    
    col1,col2=st.columns(2)
    with col1:
       
      fig_amount_1=px.bar(df_1,x="Districts",y="appopens",title="TOP 10 OF APPOPENS",hover_name="Districts",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
      st.plotly_chart(fig_amount_1)

    #Plot_2
    Query2=f'''SELECT Districts, sum(appopens) as appopens
                FROM {table_name}
                where states= '{state}'
                group by Districts
                order by appopens
                limit 10;'''
    mycursor.execute(Query2)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("Districts","appopens"))
    
    with col2:
      fig_amount_2=px.bar(df_2,x="Districts",y="appopens",title="LAST 10 OF APPOPENS",hover_name="Districts",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
      st.plotly_chart(fig_amount_2)


    #Plot_3
    Query3=f'''SELECT Districts, avg(appopens) as appopens
                FROM {table_name}
                where states= '{state}'
                group by Districts
                order by appopens;'''
              
                
    mycursor.execute(Query3)
    table_3=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("Districts","appopens"))

    fig_amount_3=px.bar(df_3,y="Districts",x="appopens",title="AVERAGE OF APPOPENS",hover_name="Districts",
                        orientation="h",color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)


def Top_chart_Registered_Users(table_name):

    mydb=mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe_Data",port="3306")
    mycursor=mydb.cursor()

    #Queries
    Query1=f'''SELECT states,sum(registeredUsers) as registeredusers
                FROM {table_name}
                GROUP BY states
                order by registeredUsers desc
                limit 10;'''
    mycursor.execute(Query1)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states","registeredusers"))

    col1,col2=st.columns(2)
    with col1:
        
      fig_amount_1=px.bar(df_1,x="states",y="registeredusers",title="TOP 10 OF REGISTERED USERS",hover_name="states",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
      st.plotly_chart(fig_amount_1)

    #Plot_2
    Query2=f'''SELECT states,sum(registeredUsers) as registeredusers
                FROM {table_name}
                GROUP BY states
                order by registeredUsers 
                limit 10;'''
    mycursor.execute(Query2)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states","registeredusers"))

    with col2:
        
      fig_amount_2=px.bar(df_2,x="states",y="registeredusers",title="LAST 10 OF REGISTERED USERS",hover_name="states",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
      st.plotly_chart(fig_amount_2)


    #Plot_3
    Query3=f'''SELECT states,avg(registeredUsers) as registeredusers
                FROM {table_name}
                GROUP BY states
                order by registeredUsers;'''
                              
    mycursor.execute(Query3)
    table_3=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states","registeredusers"))

    fig_amount_3=px.bar(df_3,y="states",x="registeredusers",title="AVERAGE OF REGISTERED USERS",hover_name="states",
                        orientation="h",color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)




    
#STREAMLIT
st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
    
    col1,col2=st.columns(2)
    with col1:
      st.header("PHONEPE")
      st.subheader("INDIA'S BEST TRANSACTION APP")
      st.markdown("Phonepe is an Indian digital payments and financial technology company")
      st.write("*****FEATURES*****")
      st.write("*****Credit and Debit card linking*****")
      st.write("*****Bank balance Check*****")
      st.write("*****Money Storage*****")
      st.write("*****PIN Authorization*****")
      st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    with col2:  
      st.image(Image.open(r"D:\2023\PYTHON\GUVI FILES\New folder\download.jpg.png"),width=450)

    col3,col4=st.columns(2)
    with col3:  
       st.image(Image.open(r"D:\2023\PYTHON\GUVI FILES\New folder\phonepe images - Google Search_files\Phonepe motion grapics.jpeg"),width=450)
    with col4:
        st.write("*****Easy Transactions*****")
        st.write("*****One App For All your Payments*****")
        st.write("*****Your Bank is All You Need*****")
        st.write("*****Multiple Payment Modes*****")
        st.write("*****PhonePe Merchants*****")
        st.write("*****Multiple Ways To Pay*****")
        st.write("*****1.Direct  Transfer and More*****")
        st.write("*****2.QR Code*****")
        st.write("*****Earn Great Rewards*****")

    col5,col6=st.columns(2)
    with col5:
      st.markdown("  ")
      st.markdown("  ")
      st.markdown("  ")
      st.markdown("  ")
      st.markdown("  ")
      st.markdown("  ")
      st.write("*****No Wallet Top-Up Required*****")
      st.write("*****Pay Directly From Any Bank To Any Bank A/C*****")
      st.write("*****Instantly & Free*****")

    with col6:
      st.image(Image.open(r"D:\2023\PYTHON\GUVI FILES\New folder\phonepe images - Google Search_files\download2.jpeg"),width=450)

      
elif select=="DATA EXPLORATION":

        tab1,tab2,tab3 =st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

        with tab1:
             
             method_1=st.radio("Select the method",["Insurance Analysis","Transaction Analysis","User Analysis"])

             if method_1 =="Insurance Analysis":
                  
                  col1,col2=st.columns(2)
                  with col1:                      

                    years=st.slider("Select the year",Agg_insurance["Years"].min(),Agg_insurance["Years"].max(),Agg_insurance["Years"].min())
                  TAC_Y=Transaction_Amount_Count_Year(Agg_insurance,years)

                  col1,col2=st.columns(2)
                  with col1:
                      
                      quarters=st.slider("Select the Quarter",TAC_Y["Quarter"].min(),TAC_Y["Quarter"].max(),TAC_Y["Quarter"].min())
                  Transaction_Amount_Count_Year_Q(TAC_Y,quarters)

             elif method_1=="Transaction Analysis":
                  col1,col2=st.columns(2)
                  with col1:

                    years=st.slider("Select the year",Agg_transaction["Years"].min(),Agg_transaction["Years"].max(),Agg_transaction["Years"].min())
                  Agg_transac_TAC_Y=Transaction_Amount_Count_Year(Agg_transaction,years)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the state",Agg_transac_TAC_Y["States"].unique())

                  Agg_Tran_Transaction_type(Agg_transac_TAC_Y,states)

                  col1,col2=st.columns(2)
                  with col1:
                      
                      quarters=st.slider("Select the Quarter",Agg_transac_TAC_Y["Quarter"].min(),Agg_transac_TAC_Y["Quarter"].max(),Agg_transac_TAC_Y["Quarter"].min())
                  agg_transac_TAC_Y_Q=Transaction_Amount_Count_Year_Q(Agg_transac_TAC_Y,quarters)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the state_Ty",agg_transac_TAC_Y_Q["States"].unique())

                  Agg_Tran_Transaction_type(agg_transac_TAC_Y_Q,states)



             elif method_1=="User Analysis":
                  
                  col1,col2=st.columns(2)
                  with col1:

                    years=st.slider("Select the year",Agg_user["Years"].min(),Agg_user["Years"].max(),Agg_user["Years"].min())
                  Agg_user_Y=Agg_user_plot_1(Agg_user,years)

                  col1,col2=st.columns(2)
                  with col1:
                      
                      quarters=st.slider("Select the Quarter",Agg_user_Y["Quarter"].min(),Agg_user_Y["Quarter"].max(),Agg_user_Y["Quarter"].min())
                  agg_user_Y_Q=Agg_user_plot_2(Agg_user_Y,quarters)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the State",agg_user_Y_Q["States"].unique())

                  Agg_user_plot_3(agg_user_Y_Q,states)
           
                  
        with tab2: 

                method_2=st.radio("Select the method",["Map Insurance Analysis","Map Transaction Analysis","Map User Analysis"])  

                if method_2 =="Map Insurance Analysis":
                
                  col1,col2=st.columns(2)
                  with col1:

                    years=st.slider("Select the year_map_insur",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
                  Map_insur_Y=Transaction_Amount_Count_Year(Map_insurance,years)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the state_map_insur",Map_insur_Y["States"].unique())
                  Map_insur_District(Map_insur_Y,states)

                  col1,col2=st.columns(2)
                  with col1:
                      
                      quarters=st.slider("Select the Quarter_Map_insur",Map_insur_Y["Quarter"].min(),Map_insur_Y["Quarter"].max(),Map_insur_Y["Quarter"].min())
                  Map_insur_TAC_Y_Q=Transaction_Amount_Count_Year_Q(Map_insur_Y,quarters)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the state_Ty",Map_insur_TAC_Y_Q["States"].unique())

                  Map_insur_District(Map_insur_TAC_Y_Q,states)


                elif method_2=="Map Transaction Analysis":

                  col1,col2=st.columns(2)
                  with col1:

                    years=st.slider("Select the year_insur",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
                  Map_transac_Y=Transaction_Amount_Count_Year(Map_transaction,years)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the state_map_transac",Map_transac_Y["States"].unique())
                  Map_insur_District(Map_transac_Y,states)

                  col1,col2=st.columns(2)
                  with col1:
                      
                      quarters=st.slider("Select the Quarter",Map_transac_Y["Quarter"].min(),Map_transac_Y["Quarter"].max(),Map_transac_Y["Quarter"].min())
                  Map_transac_TAC_Y_Q=Transaction_Amount_Count_Year_Q(Map_transac_Y,quarters)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the state_Ty",Map_transac_TAC_Y_Q["States"].unique())

                  Map_insur_District(Map_transac_TAC_Y_Q,states)

                  
                elif method_2=="Map User Analysis":
                   
                  col1,col2=st.columns(2)
                  with col1:

                    years=st.slider("Select the year_Map",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
                  Map_user_Y=Map_user_plot_1(Map_user,years)

                  col1,col2=st.columns(2)
                  with col1:
                      
                      quarters=st.slider("Select the Quarter_Map_user",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
                  Map_user_Y_Q=Map_user_plot_2(Map_user_Y,quarters)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the state_Map_user",Map_user_Y_Q["States"].unique())

                  Map_user_plot_3(Map_user_Y_Q,states)


                                  

      
        with tab3: 

                method_3=st.radio("Select the method",["Top Insurance Analysis","Top Transaction Analysis","Top User Analysis"])  

                if method_3 =="Top Insurance Analysis":
                   
                  col1,col2=st.columns(2)
                  with col1:

                    years=st.slider("Select the year_insur",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
                  Top_insur_Y=Transaction_Amount_Count_Year(Top_insurance,years)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the state_Top_insur",Top_insur_Y["States"].unique())
                  Top_insur_plot_1(Top_insur_Y,states)

                  col1,col2=st.columns(2)
                  with col1:
                      
                      quarters=st.slider("Select the Quarter_Map_user",Top_insur_Y["Quarter"].min(),Top_insur_Y["Quarter"].max(),Top_insur_Y["Quarter"].min())
                  Top_insur_TAC_Y_Q=Transaction_Amount_Count_Year_Q(Top_insur_Y,quarters)
                  
                  
                elif method_3=="Top Transaction Analysis":

                  col1,col2=st.columns(2)
                  with col1:

                    years=st.slider("Select the year_transac",Top_transac["Years"].min(),Top_transac["Years"].max(),Top_transac["Years"].min())
                  Top_transac_Y=Transaction_Amount_Count_Year(Top_transac,years)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the state_Top_transac",Top_transac_Y["States"].unique())
                  Top_insur_plot_1(Top_transac_Y,states)

                  col1,col2=st.columns(2)
                  with col1:
                      
                      quarters=st.slider("Select the Quarter_Top_transac",Top_transac_Y["Quarter"].min(),Top_transac_Y["Quarter"].max(),Top_transac_Y["Quarter"].min())
                  Top_transac_TAC_Y_Q=Transaction_Amount_Count_Year_Q(Top_transac_Y,quarters)

                  
                elif method_3=="Top User Analysis":

                  Col1,col2=st.columns(2)
                  with col1:

                    years=st.slider("Select the year_TU",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
                  Top_user_Y=Top_user_plot_1(Top_user,years)

                  col1,col2=st.columns(2)
                  with col1:
                     states=st.selectbox("select the State_TU",Top_user_Y["States"].unique())

                  Top_user_plot_2(Top_user_Y,states)
                     
elif select=="TOP CHARTS":
   
  question=st.selectbox("Select the question",["1.Transaction Amount and Count of Aggregated Insurance",
                                                "2.Transaction Amount and Count of Map Insurance",
                                                "3.Transaction Amount and Count of Top Insurance",
                                                "4.Transaction Amount and Count of Aggregated Transaction",
                                                "5.Transaction Amount and Count of Map Transaction",
                                                "6.Transaction Amount and Count of Top Transaction",
                                                "7.Transaction count of Aggregated user",
                                                "8.Registered users of Map user",
                                                "9.App opens of Map user",
                                                "10.Registered users of Top user"])
                       
  if question== "1.Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("agg_insurance")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("agg_insurance")


  elif question== "2.Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("map_insurance")  

  elif question== "3.Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("top_insurance")    

  elif question== "4.Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("agg_transaction")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("agg_transaction")

  elif question== "5.Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("map_transaction")

  elif question== "6.Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("top_transaction") 

  elif question== "7.Transaction count of Aggregated user":
        
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("agg_user") 

  elif question== "8.Registered users of   Map user":
        
        states=st.selectbox("Select the state",Map_user['States'].unique())
        st.subheader("REGISTERED USERS")
        Top_chart_Registered_User("map_user",states)

  elif question== "9.App opens of Map user":
        
        states=st.selectbox("Select the state",Map_user['States'].unique())
        st.subheader("APPOPENS")
        Top_chart_Appopens("map_user",states)

  elif question== "10.Registered users of Top user":
        
        st.subheader("REGISTERED USERS")
        Top_chart_Registered_Users("top_user")                                                  
                                               
  