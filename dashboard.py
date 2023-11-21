import pandas as pd
import streamlit as st
import plotly.express as px
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Smart Electric Usage", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Smart Electric Usage Analytics 💡 ")
st.markdown('<style>div.block-container{padding-top:1.6rem}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file", type=({"csv","txt","xlsx","xls"}))

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(filename)
else:
    os.chdir(r"C:\Users\BEST\OneDrive\Desktop\projects\Electric - Copy")
    df = pd.read_excel("electricity.xlsx")






st.sidebar.header("Filter By:")

amount=st.sidebar.multiselect("Filter By Amount:",
                                 options=df["Amount"],
                                 default=df["Amount"])

selection_query=df.query(
    "Amount== @amount"
)

st.title("Electricity Dashboard")

total_amount=(selection_query["Amount"].sum())
total_units=(selection_query["Units"].sum()),

first_column,second_column=st.columns(2)

with first_column:
    st.markdown("### Total Amount:")
    st.subheader(f'{total_amount}KES')
with second_column:
    st.markdown("### Total Units")
    st.subheader(f'{total_units}')

st.markdown("---")
#Barchart
amount_by_category=(selection_query.groupby(by=["Amount"]).sum()[["Units"]])

amount_by_category_barchart=px.bar(amount_by_category,
                                   x="Units",
                                   y=amount_by_category.index,
                                   title="Amount By Category",
                                   color_discrete_sequence=["#17f50c"],
                                   )
amount_by_category_barchart.update_layout(plot_bgcolor ="rgba(0,0,0,0)",xaxis=(dict(showgrid=False)))
#Piechart
amount_by_category_piechart=px.pie(amount_by_category, names=amount_by_category.index,values="Units",title="Amount % By Category",hole=.3,color=amount_by_category.index,color_discrete_sequence=px.colors.sequential.RdPu_r)

left_column,right_column=st.columns(2)
left_column.plotly_chart(amount_by_category_barchart,use_container_width=True)
right_column.plotly_chart(amount_by_category_piechart,use_container_width=True)

