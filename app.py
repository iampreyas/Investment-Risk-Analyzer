import streamlit as st 
st.title ("Investment Risk Analyzer")
st.subheader("Calculate Return & Analyze Risk")
inv_id =st.number_input("Investment ID", min_value=1,step=1)
inv_name=st.text_input("Investment Name")
amount=st.number_input("Investment Amount (Rs.)",min_value=0.0,step=5000.0)
rate=st.number_input("Expected Return Rate (%)",min_value=0.0,step=0.5)
if st.button("Analyze Investment"):
    profit = (amount * rate)/100
    total=amount + profit
    st.success(f"Expected Return Amount: Rs. {profit:,.2f}")
    st.info(f"Total Value After Return: Rs. {total:,.2f}")
    st.markdown("Risk Level")
    if amount > 100000:
        st.warning("High Capital Allocation (Amount > 1,00,000)")
    else:
        st.success("Normal Capital Allocation")
