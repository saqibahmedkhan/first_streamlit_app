import streamlit as st
import pandas as pd 
import plotly.express as px



uploaded_file=st.file_uploader('Choose a CSV file containing only numerical values', 
                 type='CSV', help='The file should contain only one column with no header', on_change=None)



if uploaded_file is not None:
    dfExpModel = pd.read_csv(uploaded_file,header=None, names=['Temp'])


alpha=st.slider(
    'Select value for Alpha',0.0,1.0,0.2,
)

st.write('')
st.write('')



beta=st.slider(
    'Select value for Beta',0.0,1.0,0.3,
)

st.write('')
st.write('')




dfExpModel.insert(0, 'DayNumber', range(1, len(dfExpModel) + 1))

dfHoltsMethod=dfExpModel.copy()

dfExpModel['S(t)'] = dfExpModel['Temp'].copy()
for i in range(1, len(dfExpModel)):
    dfExpModel.at[i, 'S(t)'] = alpha * dfExpModel.at[i, 'Temp'] + (1-(alpha)) * dfExpModel.at[i - 1, 'S(t)']



dfHoltsMethod['S(t)']=dfHoltsMethod['Temp'].copy()
dfHoltsMethod['T(t)']=dfHoltsMethod['Temp'].copy()
dfHoltsMethod['F(t)']=dfHoltsMethod['Temp'].copy()

for i in range(0, len(dfHoltsMethod)):
    if i==0:
        dfHoltsMethod.at[i, 'S(t)'] = alpha * dfHoltsMethod.at[i, 'Temp'] 
        dfHoltsMethod.at[i, 'T(t)'] = beta * dfHoltsMethod.at[i, 'S(t)'] 
        dfHoltsMethod.at[i, 'F(t)']= None
    else:
        dfHoltsMethod.at[i, 'S(t)'] = (alpha * dfHoltsMethod.at[i, 'Temp']) + ((1-(alpha)) * (dfHoltsMethod.at[i - 1, 'S(t)']+dfHoltsMethod.at[i - 1, 'T(t)']))
        dfHoltsMethod.at[i, 'T(t)'] = beta * ((dfHoltsMethod.at[i, 'S(t)'] - dfHoltsMethod.at[i-1, 'S(t)'])) + ((1-beta) * dfHoltsMethod.at[i - 1, 'T(t)']) 
        dfHoltsMethod.at[i, 'F(t)']=  dfHoltsMethod.at[i-1, 'S(t)'] + dfHoltsMethod.at[i-1, 'T(t)']






comparison_values = pd.concat([dfExpModel[['Temp','S(t)']], dfHoltsMethod['F(t)']], axis=1)

comparison_values = comparison_values.rename(columns={'Temp': 'Actual', 'S(t)': 'ExpResult', 'F(t)': 'HoltResult'})

comparison_values = comparison_values.drop(comparison_values.index[0]).reset_index(drop=True)




Comparison_fig = px.line(comparison_values[['Actual','ExpResult','HoltResult']], 
                title='Actual vs ExpResult vs HoltResult')
st.plotly_chart(Comparison_fig, use_container_width=True)



st.write('')
st.write('Data of first 10 records when using Exponential smoothing model:')
st.dataframe(dfExpModel.head(10))

st.write('Data of first 10 records whne using Holt''s Method:')
st.dataframe(dfHoltsMethod.head(10))


