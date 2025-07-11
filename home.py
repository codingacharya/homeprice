import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="House Savings Planner", layout="wide")

# Title
st.title("🏠 House Savings Planner for Tier 2 Cities")

# Sidebar Inputs
st.sidebar.header("Personal Details")
income = st.sidebar.number_input("Monthly Salary (₹)", min_value=10000, max_value=100000, value=37000, step=500)
savings_percent = st.sidebar.slider("Savings % for House", 10, 60, 32)

# Calculations
monthly_saving = income * savings_percent / 100
annual_saving = monthly_saving * 12
years = 5
expected_return = 0.10  # 10% SIP returns

# Compound interest calculator
def calculate_sip_growth(monthly_amount, rate, years):
    future_value = 0
    for i in range(1, years * 12 + 1):
        future_value += monthly_amount * ((1 + rate / 12) ** (years * 12 - i + 1))
    return future_value

sip_projection = calculate_sip_growth(monthly_saving, expected_return, years)

# Budget Breakdown
essentials = income * 0.41
bills = income * 0.08
insurance = income * 0.05
emergency = income * 0.03
leisure = income - (essentials + bills + insurance + emergency + monthly_saving)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Monthly Budget Breakdown")
    budget_df = pd.DataFrame({
        "Category": ["Essentials", "Bills", "Insurance", "Emergency Fund", "Leisure/Misc", "House Savings"],
        "Amount (₹)": [essentials, bills, insurance, emergency, leisure, monthly_saving]
    })
    st.dataframe(budget_df, use_container_width=True)

    fig, ax = plt.subplots()
    ax.pie(budget_df["Amount (₹)"], labels=budget_df["Category"], autopct="%1.1f%%", startangle=140)
    ax.axis("equal")
    st.pyplot(fig)

with col2:
    st.subheader("📈 5-Year Savings Projection")
    savings_data = {
        "Year": list(range(1, years + 1)),
        "Without Investment (₹)": [round(annual_saving * y, 2) for y in range(1, years + 1)],
        "With SIP @10% Return (₹)": [round(calculate_sip_growth(monthly_saving, expected_return, y), 2) for y in range(1, years + 1)]
    }
    df_projection = pd.DataFrame(savings_data)
    st.dataframe(df_projection, use_container_width=True)

    st.line_chart(df_projection.set_index("Year"))

# Download Plan
st.subheader("📤 Export Savings Plan")
csv = df_projection.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Projection CSV", data=csv, file_name="house_savings_projection.csv", mime="text/csv")

# Tips
with st.expander("💡 Smart Tips to Reach Your Goal"):
    st.markdown("""
- Start with buying land if construction is too costly now.
- Use SIPs for higher returns instead of only fixed savings.
- Consider PMAY subsidy if you're a first-time homebuyer.
- Break down your construction into phases (1BHK → Expand later).
- Build an emergency fund so your house goal doesn't get derailed.
    """)

st.success(f"You're saving ₹{monthly_saving:.0f}/month. In 5 years, that becomes ₹{sip_projection:,.0f} with investment returns! 🎯")
