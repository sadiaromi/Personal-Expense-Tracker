import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

st.set_page_config(page_title="Personal Expense Tracker", layout="wide", initial_sidebar_state="expanded")

st.title("📌 Personal Expense Tracker")

# Sidebar for Inputs
st.sidebar.header("🔹 Add a New Expense")
categories = [
    "Food & Dining", "Transportation", "Housing", "Utilities", "Entertainment", "Shopping", 
    "Healthcare", "Education", "Travel", "Personal Care", "Gifts & Donations", "Other"
]
category = st.sidebar.selectbox("Category", categories)
amount = st.sidebar.number_input("Amount", min_value=0.0, format="%.2f")
date = st.sidebar.date_input("Date", datetime.date.today())
description = st.sidebar.text_area("Description")

# Expense Data 
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# Add Expense Button
if st.sidebar.button("Add Expense"):
    if amount == 0.0:
        st.sidebar.warning("⚠️ Please enter an expense amount before adding.")
    else:
        new_expense = pd.DataFrame([[date, category, amount, description]], columns=["Date", "Category", "Amount", "Description"])
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
        st.success("✅ Expense Added Successfully!")

# Expenses in Proper Table Format
st.subheader("📊 Expense History")
if not st.session_state.expenses.empty:
    st.dataframe(st.session_state.expenses)
else:
    st.write("No expenses recorded yet.")

# Delete Expense Option
st.subheader("🗑️ Remove Expense")
if not st.session_state.expenses.empty:
    expense_to_remove = st.selectbox("Select an expense to remove", st.session_state.expenses.index)
    if st.button("❌ Delete Selected Expense"):
        st.session_state.expenses = st.session_state.expenses.drop(expense_to_remove).reset_index(drop=True)
        st.success("Expense removed successfully!")
        time.sleep(1)  
        st.rerun()

# Download CSV
if not st.session_state.expenses.empty:
    csv = st.session_state.expenses.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Report", data=csv, file_name="expense_report.csv", mime="text/csv")

# Visualization
st.subheader("📈 Expense Analysis")
if not st.session_state.expenses.empty and st.session_state.expenses["Amount"].sum() > 0:
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(6, 3))
        st.session_state.expenses.groupby("Category")["Amount"].sum().plot(kind="bar", ax=ax, color=["#E63946", "#457B9D", "#A8DADC", "#F4A261", "#2A9D8F"])
        ax.set_ylabel("Total Spent")
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(5, 5))
        data = st.session_state.expenses.groupby("Category")["Amount"].sum()
        if not data.empty:
            wedges, texts, autotexts = ax.pie(
                data, labels=data.index, autopct='%1.1f%%', startangle=140, colors=["#E63946", "#457B9D", "#A8DADC", "#F4A261", "#2A9D8F"]
            )
            for text in texts:
                text.set_size(10)
            for autotext in autotexts:
                autotext.set_size(10)
                autotext.set_color("white")
            plt.tight_layout()
            st.pyplot(fig)
else:
    st.write("No data available for analysis.")

