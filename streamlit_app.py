import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd


#Layout
st.set_page_config(
    page_title="SimiLo",
    layout="wide",
    initial_sidebar_state="expanded")

#Data Pull and Functions
st.markdown("""
<style>
.big-font {
    font-size:80px !important;
}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Upload", "Update", "Download"],
        icons=["house", "cloud-upload", "file", "download"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.title("Home")
    st.write("Welcome to the home page!")

elif selected == "Upload":
    st.title("Upload a File")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # Try to display the content of the file
        try:
            df = pd.read_csv(uploaded_file)
            edited_df = st.data_editor(df)
            
            # Button to save the edited DataFrame
            st.write("")
            if st.button("Save Changes"):
                edited_file_path = "edited_file.csv"
                edited_df.to_csv(edited_file_path, index=False)
                st.success("Changes saved successfully!")
                st.write("Download the edited file:")
                st.download_button(
                    label="Download CSV",
                    data=edited_df.to_csv(index=False),
                    file_name='edited_file.csv',
                    mime='text/csv'
                )
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif selected == "Update":
    st.title("Update Data ")
    st.write("This section can be used to update data.")
    
    if 'df' in locals():
        st.subheader("Current DataFrame")
        st.dataframe(df)
    else:
        st.info("Please upload a file in the 'Upload' section to see the data here.")

elif selected == "Download":
    st.title("Download Data")
    st.write("This section can be used to download data.")
