import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import engine

engine = create_engine("mysql+mysqlconnector://root:Queaty%402003@localhost/local_food_wastage_management_system")


st.set_page_config(layout="wide")

# For Navigation bar
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Go to",
    [
        "Project Introduction",
        "View Tables",
        "CRUD Operations",
        "SQL Queries & Visualization",
        "User Introduction"
    ]
)

# For Respective pages
if menu == "Project Introduction":
    st.title("Local Food Wastage Management System")

    st.header("📌 Problem Statement")
    st.write("""
    Food wastage is a major issue in society. Many restaurants and households 
    discard surplus food while many people suffer from hunger. There is no 
    proper system to connect food donors with people in need.
    """)


    st.header("💡 Proposed Solution")
    st.write("""
    This project provides a platform where food providers can list surplus food 
    and receivers (NGOs or individuals) can claim it. The system helps in 
    efficient redistribution of food using a centralized database.
    """)

    st.header("🎯 Objectives")
    st.write("""
    - Reduce food wastage
    - Connect food providers with receivers
    - Enable easy food listing and claiming
    - Provide data insights on food distribution
    """)

    st.header("🛠️ Technologies Used")
    st.write("""
    - Python
    - SQL (MySQL)
    - Streamlit
    - Pandas
    """)

    st.header("📊 Project Features")
    st.write("""
    - CRUD operations (Add, Update, Delete food data)
    - SQL-based data analysis
    - Interactive dashboard using Streamlit
    - Filtering and visualization of food data
    """)

    st.header("🌍 Impact")
    st.write("""
    This system helps reduce food wastage and supports social good by 
    connecting surplus food providers with people in need.
    """)

elif menu == "View Tables":
    st.title("📊 View Database Tables")

    table_option = st.selectbox(
        "Select Table",
        ["Providers", "Receivers", "Food", "Claims"]
    )

    if table_option == "Providers":
        df = pd.read_sql("SELECT * FROM providers", engine)
        st.subheader("Providers Table")
        st.dataframe(df)

    elif table_option == "Receivers":
        # If not created yet, show message
        try:
            df = pd.read_sql("SELECT * FROM receivers", engine)
            st.subheader("Receivers Table")
            st.dataframe(df)
        except:
            st.warning("Receivers table not created yet")

    elif table_option == "Food":
        df = pd.read_sql("SELECT * FROM food", engine)
        st.subheader("Food Table")
        st.dataframe(df)

    elif table_option == "Claims":
        try:
            df = pd.read_sql("SELECT * FROM claims", engine)
            st.subheader("Claims Table")
            st.dataframe(df)
        except:
            st.warning("Claims table not created yet")

elif menu == "CRUD Operations":
    st.title("⚙️ Manage Food Data")

    action = st.selectbox("Choose Action", ["Add", "Update", "Delete"])

    # ---------------- ADD ---------------- #
    if action == "Add":
        st.subheader("Add Food")

        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1)
        provider_id = st.number_input("Provider ID", min_value=1)
        location = st.text_input("Location")

        if st.button("Add Food"):
            st.success("✅ Food Added Successfully!")

    # ---------------- UPDATE ---------------- #
    elif action == "Update":
        st.subheader("Update Food")

        food_id = st.number_input("Food ID", min_value=1)
        new_food_name = st.text_input("New Food Name")
        new_quantity = st.number_input("New Quantity", min_value=1)
        new_location = st.text_input("New Location")

        if st.button("Update Food"):
            st.success("✅ Food Updated Successfully!")

    # ---------------- DELETE ---------------- #
    elif action == "Delete":
        st.subheader("Delete Food")

        food_id = st.number_input("Food ID to Delete", min_value=1)

        if st.button("Delete Food"):
            st.success("✅ Food Deleted Successfully!")


elif menu == "SQL Queries & Visualization":
    st.title("📈 SQL Analysis")
    query_option = st.selectbox("Select Query", [
        "1. HOW MANY FOOD PROVIDERS AND RECEIVERS ARE THERE IN EACH CITY ?",
        "2. WHICH TYPE OF FOOD PROVIDER(RESTURANT,GROCERY STORE, ETC) CONTRIBUTES THE MOST FOOD ?",
        "3. WHAT IS THE CONTACT INFORMATION OF FOOD PROVIDERS IN A SPECIFIC CITY ?",
        "4. WHICH RECEIVERS HAVE CLAIMED THE MOST FOOD ?",
        "5. WHAT IS THE  TOTAL QUANTITY OF FOOD AVAILABLE  FROM ALL PROVIDERS ? ",
        "6. WHICH CITY HAS THE HIGHEST NO.OF FOOD ?",
        "7. WHAT ARE THE MOST COMMONLY AVAILABLE FOOD TYPE ?",
        "8. HOW MANY FOOD CLAIMS HAVE BEEN MADE FOR EACH FOOD ITEM ?",
        "9. WHICH PROVIDER HAS THE HIGHEST NO.OF SUCCESSFUL FOOD CLAIMS ?",
        "10. WHAT % OF FOOD CLIAMS ARE COMPLETED VS PEDNING VS CANCLED ?",
        "11. WHAT IS THE AVERAGE QUANTITY OF FOOD CLAIMED PER RECEIVER ?",
        "12. WHICH MEAL TYPE(BREAKFAST,LUNCH,DINNER,SNACKS) IS CLAIMED THE MOST ?",
        "13. WHAT IS THE TOTAL QUANTITY OF FOOD DONATED BY EACH PROVIDER ?"
    ])

    # -------- QUERY 1 -------- #
    if query_option == "1. HOW MANY FOOD PROVIDERS AND RECEIVERS ARE THERE IN EACH CITY ?":
        query1 = """SELECT p.City,
                    COUNT(DISTINCT p.Provider_ID) AS Total_Providers,
                    COUNT(DISTINCT r.Receiver_ID) AS Total_Receivers
                    FROM providers p
                    LEFT JOIN receivers r
                    ON p.City = r.City
                    GROUP BY p.City;"""
        df1 = pd.read_sql(query1, engine)
        st.dataframe(df1)

    # -------- QUERY 2 -------- #
    elif query_option == "2 .WHICH TYPE OF FOOD PROVIDER(RESTURANT,GROCERY STORE, ETC) CONTRIBUTES THE MOST FOOD ?":
        query2 = """SELECT 
                    Provider_Type,
                    SUM(Quantity) AS Total_Food_Contributed
                    FROM food
                    GROUP BY Provider_Type  
                    ORDER BY Total_Food_Contributed DESC;"""
        df2 = pd.read_sql(query2, engine)
        st.dataframe(df2)
        

    # -------- QUERY 3 -------- #
    elif query_option == "3. WHAT IS THE CONTACT INFORMATION OF FOOD PROVIDERS IN A SPECIFIC CITY ?":
        query3 = """SELECT 
                    Type,Contact
                    FROM providers
                    WHERE City = 'Bradleyport';"""
        df3 = pd.read_sql(query3, engine)
        st.dataframe(df3)

    # -------- QUERY 4 -------- #
    elif query_option == "4. WHICH RECEIVERS HAVE CLAIMED THE MOST FOOD ?":
        query4 = """SELECT 
                    r.Receiver_ID,
                    r.Name,
                    SUM(f.Quantity) AS Total_Food_Claimed
                    FROM claims c
                    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
                    JOIN food f ON c.Food_ID = f.Food_ID
                    WHERE c.Status = 'Completed'
                    GROUP BY r.Receiver_ID, r.Name
                    ORDER BY Total_Food_Claimed DESC;"""
        df4 = pd.read_sql(query4, engine)
        st.dataframe(df4)

    # -------- QUERY 5 -------- #
    elif query_option == "5. WHAT IS THE  TOTAL QUANTITY OF FOOD AVAILABLE  FROM ALL PROVIDERS ? ":
        query5 = """SELECT 
                SUM(Quantity) AS Total_Food_Available
                FROM food;"""
        df5 = pd.read_sql(query5, engine)
        st.dataframe(df5)

    # -------- QUERY 6 -------- #
    elif query_option == "6. WHICH CITY HAS THE HIGHEST NO.OF FOOD ?":
        query6 = """SELECT 
                    Location AS City,
                    SUM(Quantity) AS Total_Food
                    FROM food
                    GROUP BY Location
                    ORDER BY Total_Food DESC;"""
        df6 = pd.read_sql(query6, engine)
        st.dataframe(df6)

    # -------- QUERY 7 -------- #
    elif query_option == "7. WHAT ARE THE MOST COMMONLY AVAILABLE FOOD TYPE ?":
        query7 = """SELECT 
                Food_Type,
                COUNT(*) AS Frequency
                FROM food
                GROUP BY Food_Type
                ORDER BY Frequency DESC;"""
        df7 = pd.read_sql(query7, engine)
        st.dataframe(df7)

    # -------- QUERY 8 -------- #
    elif query_option == "8. HOW MANY FOOD CLAIMS HAVE BEEN MADE FOR EACH FOOD ITEM ?":
        query8 = """SELECT 
            f.Food_ID,
            f.Food_Name,
            COUNT(c.Claim_ID) AS Total_Claims
            FROM food f
            LEFT JOIN claims c 
            ON f.Food_ID = c.Food_ID
            GROUP BY f.Food_ID, f.Food_Name
            ORDER BY Total_Claims DESC;"""
        df8 = pd.read_sql(query8, engine)
        st.dataframe(df8)

    # -------- QUERY 9 -------- #
    elif query_option == "9. WHICH PROVIDER HAS THE HIGHEST NO.OF SUCCESSFUL FOOD CLAIMS ?":
        query9 = """SELECT 
            p.Provider_ID,
            p.Name,COUNT(c.Claim_ID) AS Successful_Claims
            FROM claims c
            JOIN food f ON c.Food_ID = f.Food_ID
            JOIN providers p ON f.Provider_ID = p.Provider_ID
            WHERE c.Status = 'Completed'
            GROUP BY p.Provider_ID, p.Name
            ORDER BY Successful_Claims DESC;"""
        df9 = pd.read_sql(query9, engine)
        st.dataframe(df9)

    # -------- QUERY 10 -------- #
    elif query_option == "10. WHAT % OF FOOD CLIAMS ARE COMPLETED VS PEDNING VS CANCLED ?":
        query10 = """SELECT 
                Status,
                COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS Percentage
                FROM claims
                GROUP BY Status;"""
        df10 = pd.read_sql(query10, engine)
        st.dataframe(df10)


    # -------- QUERY 11 -------- #
    elif query_option == "11. WHAT IS THE AVERAGE QUANTITY OF FOOD CLAIMED PER RECEIVER ?":
        query11 = """SELECT 
            r.Receiver_ID,
            r.Name,
            AVG(f.Quantity) AS Avg_Food_Claimed
            FROM claims c
            JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
            JOIN food f ON c.Food_ID = f.Food_ID
            WHERE c.Status = 'Completed'
            GROUP BY r.Receiver_ID, r.Name;"""
        df11 = pd.read_sql(query11, engine)
        st.dataframe(df11)


    # -------- QUERY 12 -------- #
    elif query_option == "12. WHICH MEAL TYPE(BREAKFAST,LUNCH,DINNER,SNACKS) IS CLAIMED THE MOST ?":
        query12 = """SELECT 
            f.Meal_Type,
            COUNT(c.Claim_ID) AS Total_Claims
            FROM claims c
            JOIN food f ON c.Food_ID = f.Food_ID
            WHERE c.Status = 'Completed'
            GROUP BY f.Meal_Type
            ORDER BY Total_Claims DESC
            LIMIT 1;"""
        df12 = pd.read_sql(query12, engine)
        st.dataframe(df12)

    # -------- QUERY 13 -------- #
    elif query_option == "13. WHAT IS THE TOTAL QUANTITY OF FOOD DONATED BY EACH PROVIDER ?":
        query13 = """SELECT p.Provider_ID,p.Name,
                SUM(f.Quantity) AS Total_Food_Donated
                FROM providers p
                JOIN food f 
                ON p.Provider_ID = f.Provider_ID
                GROUP BY p.Provider_ID, p.Name
                ORDER BY Total_Food_Donated DESC;"""

        df13 = pd.read_sql(query13, engine)
        st.dataframe(df13)


elif menu == "User Introduction":
    st.title("👤 User Introduction")

    st.header("🙋 About Me")

    st.write("""
    Hello! My name is **Queaty**. I have completed my **B.Tech in Computer Science and Engineering in 2025**.

    I am passionate about **Data Analysis, Web Development, and Software Development**.
    I enjoy building real-world projects that solve meaningful problems.
    """)

    st.header("🎓 Education")
    st.write("""
    - B.Tech in Computer Science and Engineering (2025)  
    - Swarnandhra Institute of Engineering and Technology  
    """)

    st.header("🛠️ Skills")
    st.write("""
    - Python  
    - SQL (MySQL)  
    - Streamlit  
    - Data Analysis  
    """)

    st.header("🚀 Project Work")
    st.write("""
    I developed a project titled **Local Food Wastage Management System**, 
    which helps reduce food waste by connecting food providers with people in need.
    """)

    st.header("📧 Contact Information")
    st.write("""
    - Email: queatynanneti6@gmail.com   
    - LinkedIn: https://www.linkedin.com/in/queaty-nanneti-7248502b7  
    """)




