import streamlit as st 
import pandas as pd
import numpy as np


"""import sys
from streamlit import cli as stcli
import streamlit"""
    
#def main():

st.set_page_config(page_title = 'Streamlit Dashboard', 
    layout='wide',
    page_icon='💹')

### top row 

st.markdown("## Main KPIs")

first_kpi, second_kpi, third_kpi = st.beta_columns(3)


with first_kpi:
    st.markdown("**First KPI**")
    number1 = 111 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown("**Second KPI**")
    number2 = 222 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown("**Third KPI**")
    number3 = 333 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)


"""if __name__ == '__main__':
    if streamlit._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())"""