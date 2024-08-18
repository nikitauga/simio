import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import snowflake.connector

# Layout
st.set_page_config(
    page_title="SimiLo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Snowflake connection function
@st.cache_resource
def init_connection():
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )
    return conn

# Initialize connection.
conn = init_connection()

# Custom CSS to make the text area transparent



# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Upload", "Download", "Query"],
        icons=["house", "cloud-upload", "download", "database"],
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

elif selected == "Download":
    st.title("Download Data")
    st.write("This section can be used to download data.")

elif selected == "Query":
    st.title("Run a SQL Query")
    
    # Text area for SQL query input
    query = st.text_area("Enter your SQL query below:")
    
    if st.button("Run Query"):
        try:
            # Execute the user's query
            cur = conn.cursor()
            cur.execute(query)
            result_df = cur.fetch_pandas_all()
            
            # Allow the user to edit the DataFrame
            edited_df = st.data_editor(result_df)
            
            # Option to save the edited DataFrame back to the database
            if st.button("Save Changes"):
                # Construct and execute an SQL update or insert statement here
                # Example: Assuming the table name is 'your_table' and you are updating existing rows
                for index, row in edited_df.iterrows():
                    update_query = f"""
                    UPDATE your_table
                    SET column1 = '{row['column1']}', column2 = '{row['column2']}'
                    WHERE your_primary_key = '{row['your_primary_key']}';
                    """
                    cur.execute(update_query)
                
                conn.commit()  # Commit the transaction
                st.success("Changes saved successfully!")
                
        except Exception as e:
            st.error(f"An error occurred while executing the query: {e}")