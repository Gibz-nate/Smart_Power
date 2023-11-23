import pandas as pd
import streamlit as st
import plotly.express as px
import os 
import warnings
import base64
from io import StringIO, BytesIO

def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)


st.set_page_config(page_title='Smart Electric Usage Analytics',page_icon=":zap:")
st.title('Smart Electric Usage Analytics :zap:')
st.subheader('Upload your Excel file')

uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df)
    groupby_column = st.selectbox(
        'What would you like to analyse?',
        ('Appliances','Hourly Usage Per Day', 'Consumption per Day', 'Consumption per Week', 'Consumption per Month', 'Wattage','Monthly Cost'),
    )

    # -- GROUP DATAFRAME
    output_columns = ['Appliances','Wattage','Hourly Usage Per Day']
    df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

    # -- PLOT DATAFRAME
    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y='Hourly Usage Per Day',
        color='Appliances',
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>Electricity Consumption by {groupby_column}</b>'
    ) 
    fig1 = px.histogram(
         df_grouped,
        x=groupby_column,
        y='Wattage',
        color='Appliances',
        template='plotly_white',
        title=f'<b>Electricity Consumption by {groupby_column}</b>'
    )
    st.line_chart(df, x="Appliances", y="Wattage")
    print(df_grouped)

    st.plotly_chart(fig)
    st.plotly_chart(fig1)

    # -- DOWNLOAD SECTION
    st.subheader('Downloads:')
    generate_excel_download_link(df_grouped)
    generate_html_download_link(fig)
    generate_html_download_link(fig1)



dataset=pd.read_excel('electricity.xlsx')


st.sidebar.header("Filter By:")

amount=st.sidebar.multiselect("Amount:",
                                 options=dataset["Amount"],
                                 default=dataset["Amount"])

selection_query=dataset.query(
    "Amount== @amount"
)

st.title("Price and Electricity Consumption Units")

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

dataset=pd.read_excel('electricity.xlsx')




SubCounty=st.sidebar.multiselect("SubCounty:",
                                 options=dataset["SubCounty"],
                                 default=dataset["SubCounty"])

selection_query=dataset.query(
    "SubCounty== @SubCounty"
)

st.title("Electricity Consumption per SubCounty")

total_wattage=(selection_query["watts(GWH)"].sum())
counties=(selection_query["SubCounty"]).sum(),

first_column,second_column=st.columns(2)

with first_column:
    st.markdown("### Total watts")
    st.subheader(f'{total_wattage} GWH')
#with second_column:
   # st.markdown("### County")
   # st.subheader(f'{counties}')

st.markdown("---")
#Barchart
watts_by_category=(selection_query.groupby(by=["SubCounty"]).sum()[["watts(GWH)"]])

watts_by_category_barchart=px.bar(watts_by_category,
                                   x="watts(GWH)",
                                   y=watts_by_category.index,
                                   title="watts(GWH) By Category",
                                   color_discrete_sequence=["#6495ED"],
                                   )
watts_by_category_barchart.update_layout(plot_bgcolor ="rgba(0,0,0,0)",xaxis=(dict(showgrid=False)))
#Piechart
watts_by_category_piechart=px.pie(watts_by_category, names=watts_by_category.index,values="watts(GWH)",title="watts(GWH) % By Category",hole=.3,color=watts_by_category.index,color_discrete_sequence=px.colors.sequential.Peach)

left_column,right_column=st.columns(2)
left_column.plotly_chart(watts_by_category_barchart,use_container_width=True)
right_column.plotly_chart(watts_by_category_piechart,use_container_width=True)

st.line_chart(dataset, x="SubCounty", y="watts(GWH)")
print(dataset)
