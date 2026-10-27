import streamlit as st 
import pandas as pd 
import plotly.express as px
import os
st.title ("Investment Risk Analyzer")
st.subheader("Calculate Return & Analyze Risk")
DATA_FILE="investments.csv"
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
col1,col2,col3=st.columns(3)
with col1:
    analyze_clicked = st.button("Analyze Investment")
with col2:
    save_clicked=st.button("Save Investment")
with col3:
    st.button("Clear Data",on_click=clear_data)
if save_clicked:
    if inv_name.strip()=="":
        st.error("Please enter a valid Investment Name before saving.")
    else:
        new_data=pd.DataFrame([{"ID":inv_id,"Name":inv_name,"Amount":amount,"Rate (%)":rate,"years":years}])
        if os.path.exists(DATA_FILE):
            new_data.to_csv(DATA_FILE,mode='a',header=False,index=False)
        else:
            new_data.to_csv(DATA_FILE,mode='w',header=True,index=False)
        st.success(f"Investment '{inv_name}' saved successfully to {DATA_FILE}!")
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
if os.path.exists(DATA_FILE):
    st.markdown("Saved Investments")
    saved_df=pd.read_csv(DATA_FILE)
    st.dataframe(saved_df,use_container_width=True)
    if not saved_df.empty:
        st.markdown("Asset Allocation Breakdown")
        fig_pie=px.pie(saved_df,values="Amount",names="Name",title="Portfolio Asset Allocation by Amount",hole=0.4)
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie,use_container_width=True)
    col_del1,col_del2=st.columns(2)
    with col_del1:
        if not saved_df.empty:
            del_id=st.selectbox("Select Investment ID to Delete",saved_df["ID"].unique())
            if st.button("Delete Selected Record"):
                saved_df=saved_df[saved_df["ID"]!=del_id]
                saved_df.to_csv(DATA_FILE,index=False)
                st.success(f"Record with ID {del_id} deleted successfully!")
                st.rerun()
    with col_del2:
        if st.button("Delete All Saved Data"):
            os.remove(DATA_FILE)
            st.success("All Saved Investments deleted successfully!")
            st.rerun()