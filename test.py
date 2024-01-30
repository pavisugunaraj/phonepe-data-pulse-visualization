import streamlit as st
import os
import json
import pandas as pd
import psycopg2
import numpy as np
import requests
import subprocess
import plotly.express as px

mydb=psycopg2.connect(host="localhost",
                                user="postgres",
                                password="dev@0905",
                                database="phonepe_data",
                                port="5432"
                                )
cursor=mydb.cursor()

#STREAMLIT CODE
st.set_page_config(layout='wide')
st.title(":blue[PHONEPE PULSE DATA VISUALIZATION]")
option=st.radio('Select your option:',("All India","State","Top 10 Categories"),horizontal=True)


if option=='All India':
    tab1,tab2 = st.tabs(['Transaction','User'])
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            year_1 = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'))
        with col2:
            quarter_1 = st.selectbox('**Select Quarter**', ('1','2','3','4'))
        with col3:
            type_1 = st.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments',
            'Merchant payments','Financial Services','Others'))
## Transaction Analysis bar chart query
        cursor.execute(f"select States, Transaction_amount FROM aggregated_transaction WHERE Years = '{year_1}' AND Quarter = '{quarter_1}' AND Transaction_type = '{type_1}';")
        t1 = cursor.fetchall()
        df = pd.DataFrame(np.array(t1), columns=['State', 'Transaction_amount'])
        df_result = df.set_index(pd.Index(range(1, len(df)+1)))

# Transaction Analysis table query
        cursor.execute(f"SELECT States, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE Years = '{year_1}' AND Quarter = '{quarter_1}' AND Transaction_type = '{type_1}';")
        t2 = cursor.fetchall()
        df1 = pd.DataFrame(np.array(t2), columns=['State','Transaction_count','Transaction_amount'])
        df_result1 = df1.set_index(pd.Index(range(1, len(df1)+1)))

# Total Transaction Amount table query
        cursor.execute(f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE Years = '{year_1}' AND Quarter = '{quarter_1}' AND Transaction_type = '{type_1}';")
        t3 = cursor.fetchall()
        df2 = pd.DataFrame(np.array(t3), columns=['Total','Average'])
        df_result2 = df2.set_index(['Average'])
        
 # Total Transaction Count table query
        cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE Years = '{year_1}' AND Quarter = '{quarter_1}' AND Transaction_type = '{type_1}';")
        t4 = cursor.fetchall()
        df3 = pd.DataFrame(np.array(t4), columns=['Total','Average'])
        df_result3 = df3.set_index(['Average'])

    # ------    /  Geo visualization dashboard for Transaction /   ---- #
        df.drop(columns=['State'], inplace=True)    
        # Clone the gio data
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        # Extract state names and sort them in alphabetical order
        state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
        state_names_tra.sort()
        # Create a DataFrame with the state names column
        df_state_names_tra = pd.DataFrame({'State': state_names_tra})
        # Combine the Gio State name with df_in_tr_tab_qry_rslt
        df_state_names_tra['Transaction_amount']=df
        # convert dataframe to csv file
        df_state_names_tra.to_csv('State_trans.csv', index=False)
        # Read csv
        df_tra = pd.read_csv('State_trans.csv')
        # Geo plot
        fig_tra = px.choropleth(
                    df_tra,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',locations='State',color='Transaction_amount',color_continuous_scale='thermal',title = 'Transaction Analysis')
        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
        st.plotly_chart(fig_tra,use_container_width=True)
        # ---------   /   All India Transaction Analysis Bar chart  /  ----- #
        df_result['State'] = df_result['State'].astype(str)
        df_result['Transaction_amount'] = df_result['Transaction_amount'].astype(float)
        df_result_fig = px.bar(df_result , x = 'State', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'thermal', title = 'Transaction Analysis Chart', height = 700,)
        df_result_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_result_fig,use_container_width=True)

        # -------  /  All India Total Transaction calculation Table   /   ----  #
        st.header(':violet[Total calculation]')

        col4, col5 = st.columns(2)
        with col4:
            st.subheader('Transaction Analysis')
            st.dataframe(df_result1)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(df_result2)
            st.subheader('Transaction Count')
            st.dataframe(df_result3)

#---------All India User---------- #

    with tab2:
            
            col1, col2 = st.columns(2)
            with col1:
                user_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='user_year')
            with col2:
                user_quarter = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='user_qaurter')

    # SQL Query

            # User Analysis Bar chart query
            cursor.execute(f"SELECT States, SUM(transaction_count) FROM aggregated_user WHERE Years = '{user_year}' AND Quarter = '{user_quarter}' GROUP BY States;")
            t5= cursor.fetchall()
            df4 = pd.DataFrame(np.array(t5), columns=['State', 'User Count'])
            df_result4= df4.set_index(pd.Index(range(1, len(df4)+1)))

            # Total User Count table query
            cursor.execute(f"SELECT SUM(transaction_count), AVG(transaction_count) FROM aggregated_user WHERE Years = '{user_year}' AND Quarter = '{user_quarter}';")
            t6 = cursor.fetchall()
            df5 = pd.DataFrame(np.array(t6), columns=['Total','Average'])
            df_result5 = df5.set_index(['Average'])

            # ---------  /  Output  /  -------- #

            # ------    /  Geo visualization dashboard for User  /   ---- #
            df4.drop(columns=['State'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)

            # Extract state names and sort them in alphabetical order
            state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_use.sort()

            # Create a DataFrame with the state names column
            df_state_names_use = pd.DataFrame({'State': state_names_use})

            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_use['User Count']=df4

            # convert dataframe to csv file
            df_state_names_use.to_csv('State_user.csv', index=False)
            # Read csv
            df_use = pd.read_csv('State_user.csv')

            # Geo plot
            fig_use = px.choropleth(
                df_use,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',locations='State',color='User Count',color_continuous_scale='thermal',title = 'User Analysis')
            fig_use.update_geos(fitbounds="locations", visible=False)
            fig_use.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
            st.plotly_chart(fig_use,use_container_width=True)

            # ----   /   All India User Analysis Bar chart   /     -------- #
            df_result4['State'] = df_result4['State'].astype(str)
            df_result4['User Count'] = df_result4['User Count'].astype(int)
            df_result1_fig = px.bar(df_result4 , x = 'State', y ='User Count', color ='User Count', color_continuous_scale = 'thermal', title = 'User Analysis Chart', height = 700,)
            df_result1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(df_result1_fig,use_container_width=True)

            # -----   /   All India Total User calculation Table   /   ----- #
            st.header(':violet[Total calculation]')

            col3, col4 = st.columns(2)
            with col3:
                st.subheader('User Analysis')
                st.dataframe(df_result4)
            with col4:
                st.subheader('User Count')
                st.dataframe(df_result5)
#----------- State wise-------------
elif option =='State':

    # Select tab
    tab3, tab4 = st.tabs(['Transaction','User'])

    with tab3:
        col1, col2,col3 = st.columns(3)
        with col1:
            state_wise = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='state_wise')
        with col2:
            state_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='state_year')
        with col3:
            state_quarter = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='state_quarter')
        
        # Transaction Analysis bar chart query
        cursor.execute(f"SELECT Transaction_type, Transaction_amount FROM aggregated_transaction WHERE States = '{state_wise}' AND Years = '{state_year}' AND Quarter = '{state_quarter}';")
        t7 = cursor.fetchall()
        df_result6 = pd.DataFrame(np.array(t7), columns=['Transaction_type', 'Transaction_amount'])
        df_result7= df_result6.set_index(pd.Index(range(1, len(df_result6)+1)))

        # Transaction Analysis table query
        cursor.execute(f"SELECT Transaction_type, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE States = '{state_wise}' AND Years = '{state_year}' AND Quarter = '{state_quarter}';")
        t8 = cursor.fetchall()
        df_result8 = pd.DataFrame(np.array(t8), columns=['Transaction_type','Transaction_count','Transaction_amount'])
        df_result9 = df_result8.set_index(pd.Index(range(1, len(df_result8)+1)))

        # Total Transaction Amount table query
        cursor.execute(f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE States = '{state_wise}' AND Years = '{state_year}' AND Quarter = '{state_quarter}';")
        t9 = cursor.fetchall()
        df_result10 = pd.DataFrame(np.array(t9), columns=['Total','Average'])
        df_result11 = df_result10.set_index(['Average'])

        #Total Transaction Count table query
        cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE States = '{state_wise}' AND Years ='{state_year}' AND Quarter = '{state_quarter}';")
        t12 = cursor.fetchall()
        df_result12 = pd.DataFrame(np.array(t12), columns=['Total','Average'])
        df_result13 = df_result12.set_index(['Average'])

         # ---------  /  Output  /  -------- #

        # -----    /   State wise Transaction Analysis bar chart   /   ------ #
        df_result7['Transaction_type'] =df_result7['Transaction_type'].astype(str)
        df_result7['Transaction_amount'] = df_result7['Transaction_amount'].astype(float)
        df_result2_fig = px.bar(df_result7 , x = 'Transaction_type', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'thermal', title = 'Transaction Analysis Chart', height = 500,)
        df_result2_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_result2_fig,use_container_width=True)

        st.header(':violet[Total calculation]')

        col4, col5 = st.columns(2)
        with col4:
            st.subheader('Transaction Analysis')
            st.dataframe(df_result9)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(df_result11)
            st.subheader('Transaction Count')
            st.dataframe(df_result13)
        
    with tab4:
        
        col5, col6 = st.columns(2)

        with col5:
            state_user = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='state_user')
        with col6:
            state_user_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='state_user_yr')
        
          # User Analysis Bar chart query
        cursor.execute(f"SELECT Quarter, SUM(Transaction_Count) FROM aggregated_user WHERE States = '{state_user}' AND Years = '{state_user_yr}' GROUP BY Quarter;")
        t13 = cursor.fetchall()
        df13 = pd.DataFrame(np.array(t13), columns=['Quarter', 'Transaction_Count'])
        df_result14 = df13.set_index(pd.Index(range(1, len(df13)+1)))

          # Total User Count table query
        cursor.execute(f"SELECT SUM(Transaction_Count), AVG(Transaction_Count) FROM aggregated_user WHERE States = '{state_user}' AND Years = '{state_user_yr}';")
        t14 = cursor.fetchall()
        df14 = pd.DataFrame(np.array(t14), columns=['Total','Average'])
        df_result15 = df14.set_index(['Average'])

        # ---------  /  Output  /  -------- #
        df_result14['Quarter'] = df_result14['Quarter'].astype(int)
        df_result14['Transaction_Count'] = df_result14['Transaction_Count'].astype(int)
        df_result3_fig = px.bar(df_result14 , x = 'Quarter', y ='Transaction_Count', color ='Transaction_Count', color_continuous_scale = 'thermal', title = 'User Analysis Chart', height = 500,)
        df_result3_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_result3_fig,use_container_width=True)

        # ------    /   State wise User Total User calculation Table   /   -----#
        st.header(':violet[Total calculation]')

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('User Analysis')
            st.dataframe(df_result14)
        with col4:
            st.subheader('User Count')
            st.dataframe(df_result15)

else:
    tab5, tab6 = st.tabs(['Transaction','User'])
    with tab5:
        top_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='top_yr')
  
    # Top Transaction Analysis bar chart query
        cursor.execute(f"SELECT States, SUM(Transaction_amount) As Transaction_amount FROM top_transaction WHERE Years = '{top_yr}' GROUP BY States ORDER BY Transaction_amount DESC LIMIT 10;")
        t15 = cursor.fetchall()
        df15 = pd.DataFrame(np.array(t15), columns=['State', 'Top Transaction amount'])
        df_result16 = df15.set_index(pd.Index(range(1, len(df15)+1)))

     # Top Transaction Analysis table query
        cursor.execute(f"SELECT States, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM top_transaction WHERE Years = '{top_yr}' GROUP BY States ORDER BY Transaction_amount DESC LIMIT 10;")
        t16 = cursor.fetchall()
        df16 = pd.DataFrame(np.array(t16), columns=['State', 'Top Transaction amount','Total Transaction count'])
        df_result17 = df16.set_index(pd.Index(range(1, len(df16)+1)))

     # -----   /   All India Transaction Analysis Bar chart   /   ----- #
        df_result16['State'] = df_result16['State'].astype(str)
        df_result16['Top Transaction amount'] = df_result16['Top Transaction amount'].astype(float)
        df_result4_fig = px.bar(df_result16 , x = 'State', y ='Top Transaction amount', color ='Top Transaction amount', color_continuous_scale = 'thermal', title = 'Top Transaction Analysis Chart', height = 600,)
        df_result4_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart( df_result4_fig,use_container_width=True)
    # -----   /   All India Total Transaction calculation Table   /   ----- #
        st.header(':violet[Total calculation]')
        st.subheader('Top Transaction Analysis')
        st.dataframe(df_result17)

    # -------------------------       /     All India Top User        /        ------------------ #
    with tab6:
        top_us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='top_us_yr')
        # Top User Analysis bar chart query
        cursor.execute(f"SELECT States, SUM(Registered_User) AS Top_user FROM top_user WHERE Years='{top_us_yr}' GROUP BY States ORDER BY Top_user DESC LIMIT 10;")
        t17 = cursor.fetchall()
        df17 = pd.DataFrame(np.array(t17), columns=['State', 'Total User count'])
        df_result18 = df17.set_index(pd.Index(range(1, len(df17)+1)))

        # -----   /   All India User Analysis Bar chart   /   ----- #
        df_result18['State'] = df_result18['State'].astype(str)
        df_result18['Total User count'] = df_result18['Total User count'].astype(float)
        df_result4fig = px.bar(df_result18 , x = 'State', y ='Total User count', color ='Total User count', color_continuous_scale = 'thermal', title = 'Top User Analysis Chart', height = 600,)
        df_result4fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_result4fig,use_container_width=True)

        # -----   /   All India Total Transaction calculation Table   /   ----- #
        st.header(':violet[Total calculation]')
        st.subheader('Total User Analysis')
        st.dataframe(df_result18)





        

  