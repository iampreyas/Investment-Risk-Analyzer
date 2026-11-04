import streamlit as st 
import pandas as pd 
import plotly.express as px
import os
import numpy as np
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
if 'volatility' not in st.session_state:
    st.session_state.volatility=5.0
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
volatility=st.number_input("Expected Volatility / Risk (%)",min_value=0.0,step=0.5,key='volatility')
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
        new_data=pd.DataFrame([{"ID":inv_id,"Name":inv_name,"Amount":amount,"Rate (%)":rate,"Years":years,"Volatility (%)": volatility}])
        if os.path.exists(DATA_FILE):
            new_data.to_csv(DATA_FILE,mode='a',header=False,index=False)
        else:
            new_data.to_csv(DATA_FILE,mode='w',header=True,index=False)
        st.success(f"Investment '{inv_name}' saved successfully to {DATA_FILE}!")
if analyze_clicked:
    total= amount * ((1 + rate/100) ** years)
    profit = total - amount
    st.success(f"Expected Return Amount: Rs. {profit:,.2f}")
    st.info(f"Total Value After Return: Rs. {total:,.2f}")
    best_rate=rate + volatility
    worst_rate=max(0,rate - volatility)
    best_total=amount * ((1 + best_rate/100) ** years)
    worst_total=amount * ((1 + worst_rate/100) ** years)
    best_profit = best_total - amount
    worst_profit = worst_total - amount
    st.markdown("Scenario Analysis")
    col_s1,col_s2,col_s3=st.columns(3)
    with col_s1:
        st.success("Best Case")
        st.write(f"**Rate:** {best_rate:.1f}%")
        st.write(f"**Profit:** Rs. {best_profit:,.2f}")
        st.write(f"**Total:** Rs. {best_total:,.2f}")
    with col_s2:
        st.info("Expected Case")
        st.write(f"**Rate:** {rate:.1f}%")
        st.write(f"**Profit:** Rs. {profit:,.2f}")
        st.write(f"**Total:** Rs. {total:,.2f}")
    with col_s3:
        st.error("Worst Case")
        st.write(f"**Rate:** {worst_rate:.1f}%")
        st.write(f"**Profit:** Rs. {worst_profit:,.2f}")
        st.write(f"**Total:** Rs. {worst_total:,.2f}")
    st.markdown("Risk Level")
    if volatility >= 20:
        st.error("High Risk")
    elif volatility >= 10:
        st.warning("Medium Risk")
    else:
        st.success("Low Risk")
    if amount > 100000:
        st.warning("High Capital Allocation")
    else:
        st.success("Normal Capital Allocation")
    risk_score = volatility * 2.5
    if amount > 500000:
        risk_score += 25
    elif amount > 100000:
        risk_score += 15
    if years > 7:
        risk_score += 10
    elif years > 5:
        risk_score += 5
    risk_score=min(100,risk_score)
    st.markdown("Risk Score")
    st.progress(int(risk_score)/100)
    if risk_score >= 70:
        st.error(f"Risk Score: {risk_score:.1f}/100 -> High Risk")
    elif risk_score >= 40:
        st.warning(f"Risk Score: {risk_score:.1f}/100 -> Medium Risk")
    else:
        st.warning(f"Risk Score: {risk_score:.1f}/100 -> low Risk")
    st.markdown("Posible Future Results")
    np.random.seed(42)
    simulations=1000
    final_values=[]
    for i in range(simulations):
        random_return=np.random.normal(loc=rate,scale=volatility)
        random_return=max(0,random_return)
        final_val= amount * ((1 + random_return/100) ** years)
        final_values.append(final_val)
    final_values=np.array(final_values)
    avg_sim=np.mean(final_values)
    best_5=np.percentile(final_values,95)
    worst_5=np.percentile(final_values,5)
    prob_loss=(np.sum(final_values<amount)/simulations) * 100
    col_mc1,col_mc2,col_mc3,col_mc4=st.columns(4)
    with col_mc1:
        st.metric("Average Outcome",f"Rs. {avg_sim:,.0f}")
    with col_mc2:
        st.metric("Best 5% Case",f"Rs. {best_5:,.0f}")
    with col_mc3:
        st.metric("Worst 5% Case",f"Rs. {worst_5:,.0f}")
    with col_mc4:
        st.metric("Chance of Loss",f"{prob_loss:.1f}%")
    st.markdown("Project Growth Over Time")
    best_rate=rate + volatility
    worst_rate=max(0,rate - volatility)
    growth_data = []
    curr_expexted=amount
    curr_best=amount
    curr_worst=amount
    for y in range(1,years + 1):
        curr_expexted += (curr_expexted * rate) / 100
        curr_best += (curr_best * best_rate) / 100
        curr_worst += (curr_worst * worst_rate) / 100
        growth_data.append({"Year": f"Year {y}","Expected": curr_expexted,"Best Case":curr_best,"Worst Case":curr_worst})
    df_growth = pd.DataFrame(growth_data)
    fig=px.line(
        df_growth,
        x="Year",y=["Expected","Best Case","Worst Case"],title=f"Growth Projection:{inv_name}",markers=True,
    )
    fig.update_layout(yaxis_title="Portfolio Value (Rs.)")
    st.plotly_chart(fig,use_container_width=True)
if os.path.exists(DATA_FILE):
    st.markdown("---")
    st.markdown("Portfolio Summary & Metrics")
    saved_df=pd.read_csv(DATA_FILE)
    if not saved_df.empty:
        total_invested=saved_df["Amount"].sum()
        avg_rate=saved_df["Rate (%)"].mean()
        avg_volatility=saved_df["Volatility (%)"].mean() if "Volatility (%)" in saved_df.columns else 0
        col_m1,col_m2,col_m3,col_m4=st.columns(4)
        with col_m1:
            st.metric(label="Total Invested Amount",value=f"Rs. {total_invested:,.2f}")
        with col_m2:
            st.metric(label="Average Return Rate",value=f"{avg_rate:.2f}%")
        with col_m3:
            st.metric(label="Average Volatility",value=f"{avg_volatility:.2f}%")
        with col_m4:
            st.metric(label="Total Saved Assets",value=len(saved_df))
    st.markdown("Saved Investments")
    st.dataframe(saved_df,use_container_width=True)
    if not saved_df.empty:
        csv=saved_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Portfolio as CSV",
            data=csv,
            file_name="my_portfolio.csv",
            mime="text/csv"
        )
    st.markdown("Compare Two Investments")
    if not saved_df.empty and len(saved_df) >= 2:
        col_c1,col_c2=st.columns(2)
        with col_c1:
            inv1=st.selectbox("Select First Investment",saved_df["Name"].unique(),key="comp1")
        with col_c2:
            inv2=st.selectbox("Select Second Investment",saved_df["Name"].unique(),key="comp2")
        if inv1 != inv2:
            row1=saved_df[saved_df["Name"]==inv1].iloc[0]
            row2=saved_df[saved_df["Name"]==inv2].iloc[0]
            def get_final_value(row):
                return row["Amount"] * ((1 + row["Rate (%)"]/100) ** row["Years"])
            val1=get_final_value(row1)
            val2=get_final_value(row2)
            st.markdown("Comparison Result")
            comp_col1,comp_col2=st.columns(2)
            with comp_col1:
                st.info(f"**{inv1}**")
                st.write(f"Amount: Rs. {row1['Amount']:,.0f}")
                st.write(f"Rate: {row1['Rate (%)']}%")
                st.write(f"Years: {row1['Years']}")
                st.write(f"Volatility: {row1['Volatility (%)']}%")
                st.write(f"Final Value: Rs. {val1:,.2f}")
            with comp_col2:
                st.info(f"**{inv2}**")
                st.write(f"Amount: Rs. {row2['Amount']:,.0f}")
                st.write(f"Rate: {row2['Rate (%)']}%")
                st.write(f"Years: {row2['Years']}")
                st.write(f"Volatility: {row2['Volatility (%)']}%")
                st.write(f"Final Value: Rs. {val2:,.2f}")
            if val1 > val2:
                st.success(f"Winner based on Final Value: **{inv1}**")
            elif val2 > val1:
                st.success(f"Winner based on Final Value: **{inv2}**")
            else:
                st.warning("Both have same Final Value")
        else:
            st.warning("Please select two different investments")
    else:
        st.info("At least 2 investments required for comparison")
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