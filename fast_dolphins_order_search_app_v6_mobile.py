
import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# File path
file_path = "fastdolphins_merchandise-orders_250424141340.xlsx"

# Load data
df = pd.read_excel(file_path)

# Add 'Complete' column if it doesn't exist
if "Complete" not in df.columns:
    df["Complete"] = ""

# Page styling optimized for mobile (larger fonts, clean layout)
st.markdown(
    """
    <style>
    .main {background-color: #F0F8FF;}
    .title {color: #003366; font-size: 32px; font-weight: bold;}
    .subtitle {color: #003366; font-size: 22px; font-weight: bold;}
    .order {font-size: 20px;}
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<div class='title'>FAST Dolphins Orders</div>", unsafe_allow_html=True)

# Option to view completed orders
view_completed = st.toggle("Show Completed Orders Only")

if view_completed:
    completed_orders = df[df["Complete"] == "Yes"]
    if completed_orders.empty:
        st.write("✅ No completed orders yet.")
    else:
        st.markdown("<div class='subtitle'>✅ Completed Orders:</div>", unsafe_allow_html=True)
        for i in completed_orders.index:
            athlete_name = completed_orders.at[i, "for_athlete"] if completed_orders.at[i, "for_athlete"] else completed_orders.at[i, "athletes"]
            size = completed_orders.at[i, "option_name"]
            qty = completed_orders.at[i, "quantity"]
            st.markdown(f"<div class='order'>🟦 {athlete_name} — {size} — Qty {qty}</div>", unsafe_allow_html=True)
else:
    st.write("Search by athlete or parent name to view shirt sizes and mark complete.")
    search_term = st.text_input("Enter name (athlete or parent):")

    if search_term:
        results = df[
            df['athletes'].str.contains(search_term, case=False, na=False) |
            df['for_athlete'].str.contains(search_term, case=False, na=False) |
            df['parent1_first_name'].str.contains(search_term, case=False, na=False) |
            df['parent1_last_name'].str.contains(search_term, case=False, na=False)
        ].copy()

        if results.empty:
            st.write("No orders found for this person.")
        else:
            st.markdown("<div class='subtitle'>Shirt Orders:</div>", unsafe_allow_html=True)
            results["Mark Complete"] = False

            for i in results.index:
                athlete_name = results.at[i, "for_athlete"] if results.at[i, "for_athlete"] else results.at[i, "athletes"]
                size = results.at[i, "option_name"]
                qty = results.at[i, "quantity"]
                results.at[i, "Mark Complete"] = st.checkbox(
                    f"{athlete_name} — {size} — Qty {qty}",
                    key=i
                )

            if st.button("Mark Selected as Complete"):
                for i in results.index:
                    if results.at[i, "Mark Complete"]:
                        df.at[i, "Complete"] = "Yes"

                df.to_excel(file_path, index=False)

                wb = load_workbook(file_path)
                ws = wb.active

                green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")

                for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
                    complete_cell = row[len(df.columns) - 1]
                    if complete_cell.value == "Yes":
                        for cell in row:
                            cell.fill = green_fill

                wb.save(file_path)
                st.success("✅ Selected orders marked complete and Excel file updated!")
    else:
        st.write("Please enter a name to search.")
