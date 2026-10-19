import streamlit as st 
import pandas as pd 
import plotly.express as px
st.title ("Investment Risk Analyzer")
st.subheader("Calculate Return & Analyze Risk")
if 'inv_id' not in st.session_state:
    st.session_state.inv_id=1
if 'inv_name' not in st.session_state:
    st.session_state.inv_name="Portfolio Asset"
if 'amount' not in st.session_state:
    st.session_state.amount=10000.0
if 'rate' not in st.session_state:
    st.session_state.rate=10.0
if 'years' not in st.session_state:
    st.session_state.years=5
def clear_data():
    st.session_state.inv_id=1
    st.session_state.inv_name=""
    st.session_state.amount=0.0
    st.session_state.rate=0.0
    st.session_state.years=1
    st.session_state.volatility=0.0
inv_id =st.number_input("Investment ID", min_value=1,step=1,key='inv_id')
inv_name=st.text_input("Investment Name", key='inv_name')
amount=st.number_input("Investment Amount (Rs.)",min_value=0.0,step=5000.0,key='amount')
rate=st.number_input("Expected Return Rate (%)",min_value=0.0,step=0.5,key='rate')
years = st.slider("Investment Horizon (Years)",min_value=1,max_value=10,key='years')
col1,col2=st.columns(2)
with col1:
    analyze_clicked = st.button("Analyze Investment")
with col2:
    st.button("Clear Data",on_click=clear_data)
if analyze_clicked:
    profit = (amount * rate)/100
    total=amount + profit
    st.success(f"Expected Return Amount: Rs. {profit:,.2f}")
    st.info(f"Total Value After Return: Rs. {total:,.2f}")
    st.markdown("Risk Level")
    if amount > 100000:
        st.warning("High Capital Allocation")
    else:
        st.success("Normal Capital Allocation")
    st.markdown("Project Growth Over Time")
    growth_data = []
    current_val = amount
    for y in range(1,years + 1):
        current_val += (current_val * rate) / 100
        growth_data.append({"Year":f"Year {y}","Portfolio Value": current_val})
    df_growth = pd.DataFrame(growth_data)
    fig = px.line(df_growth, x="Year", y="Portfolio Value",title=f"Compounded Return Projection ({inv_name})", markers=True)
    st.plotly_chart(fig, use_container_width=True)
