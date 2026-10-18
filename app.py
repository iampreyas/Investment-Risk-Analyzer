import streamlit as st 
import pandas as pd 
import plotly.express as px
st.title ("Investment Risk Analyzer")
st.subheader("Calculate Return & Analyze Risk")
inv_id =st.number_input("Investment ID", min_value=1,step=1)
inv_name=st.text_input("Investment Name")
amount=st.number_input("Investment Amount (Rs.)",min_value=0.0,step=5000.0)
rate=st.number_input("Expected Return Rate (%)",min_value=0.0,step=0.5)
years = st.slider("Investment Horizon (Years)",min_value=1,max_value=10,value=5)
if st.button("Analyze Investment"):
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
