import pandas as pd
import streamlit as st
import plotly.express as px
import os 
import warnings
import base64
from io import StringIO, BytesIO

dataset=pd.read_excel('electricity.xlsx')


st.sidebar.header("Filter By:")

county=st.sidebar.multiselect("Filter By County:",
                                 options=dataset["County"],
                                 default=dataset["County"])

selection_query=dataset.query(
    "County== @county"
)

st.title("Electricity Consumption per County")

total_wattage=(selection_query["watts"].sum())
counties=(selection_query["County"]).sum(),

first_column,second_column=st.columns(2)

with first_column:
    st.markdown("### Total watts")
    st.subheader(f'{total_wattage}KWH')
#with second_column:
   # st.markdown("### County")
   # st.subheader(f'{counties}')

st.markdown("---")
#Barchart
amount_by_category=(selection_query.groupby(by=["watts"]).sum()[["County"]])

amount_by_category_barchart=px.bar(amount_by_category,
                                   x="County",
                                   y=amount_by_category.index,
                                   title="Watts By Category",
                                   color_discrete_sequence=["#17f50c"],
                                   )
amount_by_category_barchart.update_layout(plot_bgcolor ="rgba(0,0,0,0)",xaxis=(dict(showgrid=False)))
#Piechart
amount_by_category_piechart=px.pie(amount_by_category, names=amount_by_category.index,values="County",title="Watts % By Category",hole=.3,color=amount_by_category.index,color_discrete_sequence=px.colors.sequential.RdPu_r)

left_column,right_column=st.columns(2)
left_column.plotly_chart(amount_by_category_barchart,use_container_width=True)
right_column.plotly_chart(amount_by_category_piechart,use_container_width=True)

st.line_chart(dataset, x="County", y="watts")
print(dataset)
