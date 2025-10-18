import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Database setup
conn = sqlite3.connect('billing.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        items TEXT,
        total REAL
    )
''')
conn.commit()

st.title("🛒 Departmental Store Billing System")

menu = ["Create New Bill", "View Bill History"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Create New Bill":
    st.subheader("🧾 Create a New Bill")

    # Product list
    items = []
    total = 0.0

    num_items = st.number_input("Number of items", min_value=1, max_value=50, step=1)

    for i in range(num_items):
        st.write(f"### Item {i+1}")
        name = st.text_input(f"Enter item name {i+1}", key=f"name_{i}")
        price = st.number_input(f"Price of {name or 'item'}", min_value=0.0, key=f"price_{i}")
        quantity = st.number_input(f"Quantity of {name or 'item'}", min_value=1, step=1, key=f"qty_{i}")
        amount = price * quantity
        items.append({"name": name, "price": price, "quantity": quantity, "amount": amount})
        total += amount

    if st.button("Generate Bill"):
        st.success("✅ Bill Generated Successfully!")
        st.write("### 🧾 Bill Details")
        df = pd.DataFrame(items)
        st.dataframe(df)
        st.subheader(f"Total Amount: ₹{total:.2f}")

        # Save to database
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO bills (date, items, total) VALUES (?, ?, ?)", (date, str(items), total))
        conn.commit()
        st.info("Bill saved to database!")

elif choice == "View Bill History":
    st.subheader("📚 Bill History")
    bills = pd.read_sql("SELECT * FROM bills", conn)
    st.dataframe(bills)

conn.close()
