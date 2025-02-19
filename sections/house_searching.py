import streamlit as st
import re
import pandas as pd
import numpy as np

data = pd.read_csv("dummyData.csv")

def show():
    st.title("🔍 House Searching")
    st.write("This section will help you search for houses based on different criteria.")

    # Initialize session state to keep search results persistent
    if 'filteredData' not in st.session_state:
        st.session_state['filteredData'] = pd.DataFrame()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Search Criteria")
        postcode = st.text_input("Outward Postcode:")
        borough = st.selectbox("Borough:", ["Show All", "Borough A", "Borough B", "Borough C"])
        houseType = st.selectbox("House Type:", ["Show All", "All", "Flat", "Detached", "Semi Detached", "Not Detached"])
        numBedrooms = st.slider("Number of Bedrooms:", min_value=1, max_value=10, value=2, step=1)
        maxPrice = st.slider("Maximum Price:", min_value=50000, max_value=2000000, value=500000, step=50000)
        displayType = st.radio("", ["Table", "Map"], index=0, horizontal=True)
        search_button = st.button("Search")
    
    with col2:
        st.markdown("### Results Table")
        
        # If search is clicked, process new search criteria and update session state
        if search_button:
            filteredData = data.copy()
            if postcode:
                filteredData = filteredData[filteredData["postcode"].str.contains(postcode, na=False, case=False)]
            if numBedrooms:
                filteredData = filteredData[filteredData["numberOfBedrooms"] == numBedrooms]
            if maxPrice:
                filteredData = filteredData[filteredData["price"] <= maxPrice]
            if houseType != "Show All":
                filteredData = filteredData[filteredData["houseType"] == houseType]
            if borough != "Show All":
                filteredData = filteredData[filteredData["borough"] == borough]
            
            # Store the new filtered data in session state
            filteredData = filteredData.sort_values(by="price", ascending=False).head(10)
            st.session_state['filteredData'] = filteredData

            if filteredData.empty:
                st.write("No matching results found.")
        
        elif not search_button and st.session_state['filteredData'].empty:
            st.write("Please enter search criteria")

        # Display either the table or the map based on user's selection
        if not st.session_state['filteredData'].empty:
            if displayType == "Table":
                st.dataframe(st.session_state['filteredData'], height=450)
            else:
                mapData = st.session_state['filteredData'].dropna(subset=["latitude", "longitude"])
                if not mapData.empty:
                    st.map(mapData, height=450)
                else:
                    st.write("No valid location data to display on the map.")

def is_valid_uk_postcode(postcode):
    """
    Validates a UK postcode using a regular expression.
    """
    # UK postcode regex pattern
    pattern = r"^([A-Za-z]{1,2}\d{1,2}[A-Za-z]? \d[A-Za-z]{2})$"
    return re.match(pattern, postcode) is not None