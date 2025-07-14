import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import os

st.set_page_config(
    page_title="My FinTech Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======== Custom Aesthetic & Grid Layout ========
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Source Sans Pro', sans-serif;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #f0f2f6;
        color: #333;
        border-radius: 6px 6px 0 0;
        margin-right: 2px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #ffffff;
        color: #d32f2f;
        border-bottom: 3px solid #d32f2f;
    }
    h1, h2, h3, h4 {
        color: #1a1a1a;
        margin-top: 0;
    }
    .stDataFrame table {
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📊 My FinTech Dashboard")
    st.markdown("---")
    st.markdown("Navigate between views using the tabs above.")

    # Menggunakan st.columns untuk membuat kolom yang seimbang
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Export Trading Journal to PDF"):
            try:
                df = pd.read_csv("data/trading_journal.csv")
                df["Date"] = pd.to_datetime(df["Date"])
                month = datetime.now().strftime("%Y-%m")
                os.makedirs("pdf_reports", exist_ok=True)
                filepath = f"pdf_reports/trading_journal_{month}.pdf"
                with open(filepath, "w") as f:
                    f.write(f"Trading Journal Report ({month})\n\n")
                    f.write(df.to_string(index=False))
                st.success(f"✅ Trading Journal PDF saved to {filepath}")
            except Exception as e:
                st.error(f"❌ Failed to export PDF: {e}")

    with col2:
        if st.button("Export Budget to PDF"):
            try:
                df = pd.read_csv("data/budget.csv")
                df["Date"] = pd.to_datetime(df["Date"])
                month = datetime.now().strftime("%Y-%m")
                os.makedirs("pdf_reports", exist_ok=True)
                filepath = f"pdf_reports/budget_{month}.pdf"
                with open(filepath, "w") as f:
                    f.write(f"Budget Report ({month})\n\n")
                    f.write(df.to_string(index=False))
                st.success(f"✅ Budget PDF saved to {filepath}")
            except Exception as e:
                st.error(f"❌ Failed to export PDF: {e}")

    with col3:
        if st.button("Export Investments to PDF"):
            try:
                df = pd.read_csv("data/investments.csv")
                df["Date"] = pd.to_datetime(df["Date"])
                month = datetime.now().strftime("%Y-%m")
                os.makedirs("pdf_reports", exist_ok=True)
                filepath = f"pdf_reports/investments_{month}.pdf"
                with open(filepath, "w") as f:
                    f.write(f"Investment Report ({month})\n\n")
                    f.write(df.to_string(index=False))
                st.success(f"✅ Investments PDF saved to {filepath}")
            except Exception as e:
                st.error(f"❌ Failed to export PDF: {e}")

st.markdown("A modern and aesthetic dashboard to manage trading, budgeting, and investments.")

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Trading Journal", "💸 Budget Tracker", "📈 Investments"])

# Check and Create Monthly Report (Day 1)
def generate_monthly_report():
    today = date.today()
    if today.day == 1:
        prev_month = today.month - 1 if today.month > 1 else 12
        year = today.year if today.month > 1 else today.year - 1
        month_str = f"{year}-{prev_month:02d}"
        report_path = f"reports/report-{month_str}.txt"
        os.makedirs("reports", exist_ok=True)

        # Read data
        try:
            df_trades = pd.read_csv("data/trading_journal.csv")
            df_trades["Date"] = pd.to_datetime(df_trades["Date"])
            df_month = df_trades[df_trades["Date"].dt.month == prev_month]
            total_profit = df_month["ProfitLoss"].sum()
            win_rate = round((len(df_month[df_month["ProfitLoss"] > 0]) / len(df_month)) * 100, 2) if len(df_month) > 0 else 0
        except FileNotFoundError:
            total_profit, win_rate = 0, 0
            st.warning("Trading Journal data not found for monthly report.")

        try:
            df_budget = pd.read_csv("data/budget.csv")
            df_budget["Date"] = pd.to_datetime(df_budget["Date"])
            dfb = df_budget[df_budget["Date"].dt.month == prev_month]
            income = dfb[dfb["Type"] == "Income"]["Amount"].sum()
            spending = dfb[dfb["Type"] == "Spending"]["Amount"].sum()
        except FileNotFoundError:
            income, spending = 0, 0
            st.warning("Budget data not found for monthly report.")

        try:
            df_inv = pd.read_csv("data/investments.csv")
            df_inv["Date"] = pd.to_datetime(df_inv["Date"])
            invested = df_inv[df_inv["Date"].dt.month == prev_month]["Value"].sum()
        except FileNotFoundError:
            invested = 0
            st.warning("Investments data not found for monthly report.")

        # Save report
        with open(report_path, "w") as f:
            f.write(f"Monthly Report: {month_str}\n")
            f.write(f"Total Profit/Loss: Rp {total_profit:,.2f}\n")
            f.write(f"Win Rate: {win_rate}%\n")
            f.write(f"Total Income: Rp {income:,.2f}\n")
            f.write(f"Total Spending: Rp {spending:,.2f}\n")
            f.write(f"Total Investment Value Added: Rp {invested:,.2f}\n")

        st.success(f"📄 Monthly Report generated for {month_str}! (Saved in /reports folder)")

# Run only if today is the 1st
generate_monthly_report()

def show_trading_tab():
    st.header("📈 Trading Journal")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📝 Input Today’s Trade")
        pair_list = ["XAU/USD", "EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD", "ETH/USD", "SOL/USD", "BNB/USD", "USOIL", "UKOIL", "NGAS", "NASDAQ", "S&P500", "DJI", "VIX", "Other (type manually)"]
        with st.form("trade_form"):
            date = st.date_input("Date")
            pair = st.selectbox("Pair", pair_list)
            if pair == "Other (type manually)":
                pair = st.text_input("Enter your custom pair/symbol")
            position = st.radio("Position", ["Buy", "Sell"])
            entry = st.number_input("Entry Price", step=0.01)
            exit = st.number_input("Exit Price", step=0.01)
            rsi = st.slider("RSI Value", 0, 100, 50)
            ma = st.number_input("Moving Average", step=0.01)
            news = st.text_input("Important News")
            notes = st.text_area("Personal Notes")
            submitted = st.form_submit_button("Save Trade")

            if submitted:
                profit_loss = round((exit - entry) if position == "Buy" else (entry - exit), 2)
                new_data = pd.DataFrame([{ "Date": date, "Pair": pair, "Position": position, "Entry": entry, "Exit": exit, "RSI": rsi, "MA": ma, "News": news, "ProfitLoss": profit_loss, "Notes": notes }])
                csv_path = "data/trading_journal.csv"
                try:
                    existing = pd.read_csv(csv_path)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                except FileNotFoundError:
                    updated = new_data
                updated.to_csv(csv_path, index=False)
                st.success("✅ Trade saved successfully!")

    with col2:
        try:
            df = pd.read_csv("data/trading_journal.csv")
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date")

            st.subheader("📈 Profit/Loss Over Time")
            profit_chart = df[["Date", "ProfitLoss"]].groupby("Date").sum().reset_index()
            st.line_chart(profit_chart.set_index("Date"))

            st.subheader("📊 Total Profit/Loss per Pair")
            profit_by_pair = df.groupby("Pair")["ProfitLoss"].sum().sort_values(ascending=False)
            st.bar_chart(profit_by_pair)

            st.subheader("🍰 Win vs Loss")
            win_trades = len(df[df["ProfitLoss"] > 0])
            loss_trades = len(df[df["ProfitLoss"] < 0])
            win_vs_loss = pd.Series({"Win": win_trades, "Loss": loss_trades})
            fig1, ax1 = plt.subplots()
            ax1.pie(win_vs_loss, labels=win_vs_loss.index, autopct="%1.1f%%", startangle=90, colors=["#4CAF50", "#F44336"])
            ax1.axis("equal")
            st.pyplot(fig1)

            st.subheader("💡 Trade Highlights")
            best_trade = df.loc[df["ProfitLoss"].idxmax()]
            worst_trade = df.loc[df["ProfitLoss"].idxmin()]
            st.markdown(f"""
            🟢 **Best Trade:** `{best_trade['Date'].strftime('%Y-%m-%d')}` | {best_trade['Pair']} | {best_trade['Position']} → **+{best_trade['ProfitLoss']}**

            🔴 **Worst Trade:** `{worst_trade['Date'].strftime('%Y-%m-%d')}` | {worst_trade['Pair']} | {worst_trade['Position']} → **{worst_trade['ProfitLoss']}**
            """)

            st.subheader("📄 All Trade History")
            st.dataframe(df)

        except FileNotFoundError:
            st.info("No trading journal data available. Please add some trades.")
        except Exception as e:
            st.warning(f"⚠️ Error loading chart: {e}")

def show_budget_tab():
    st.header("💸 Budget Tracker")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📝 Add Budget Entry")
        with st.form("budget_form"):
            b_date = st.date_input("Date", value=datetime.today())
            b_type = st.radio("Type", ["Income", "Spending"])
            b_category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Shopping", "Health", "Salary", "Other"])
            b_amount = st.number_input("Amount", min_value=0.0, step=100.0)
            b_notes = st.text_area("Notes")
            b_submit = st.form_submit_button("Save Entry")
            if b_submit:
                new_budget = pd.DataFrame([{ "Date": b_date, "Type": b_type, "Category": b_category, "Amount": b_amount, "Notes": b_notes }])
                b_path = "data/budget.csv"
                try:
                    old = pd.read_csv(b_path)
                    updated = pd.concat([old, new_budget], ignore_index=True)
                except FileNotFoundError:
                    updated = new_budget
                updated.to_csv(b_path, index=False)
                st.success("✅ Budget entry saved!")

    with col2:
        try:
            budget_df = pd.read_csv("data/budget.csv")
            st.subheader("📈 Cashflow Over Time")
            budget_df["Date"] = pd.to_datetime(budget_df["Date"])
            cashflow = budget_df.groupby(["Date", "Type"])["Amount"].sum().unstack().fillna(0)
            cashflow["Net"] = cashflow.get("Income", 0) - cashflow.get("Spending", 0)
            st.line_chart(cashflow[["Income", "Spending", "Net"]])

            st.subheader("📊 Spending Breakdown")
            spending_df = budget_df[budget_df["Type"] == "Spending"]
            if not spending_df.empty:
                spending_by_category = spending_df.groupby("Category")["Amount"].sum()
                fig2, ax2 = plt.subplots()
                ax2.pie(spending_by_category, labels=spending_by_category.index, autopct="%1.1f%%", startangle=90)
                ax2.axis("equal")
                st.pyplot(fig2)
            else:
                st.info("No spending data to display breakdown.")
        except FileNotFoundError:
            st.info("No budget data available. Please add some entries.")
        except Exception as e:
            st.warning(f"⚠️ Error loading budget charts: {e}")

    try:
        budget_df = pd.read_csv("data/budget.csv")
        st.subheader("📄 All Budget Entries")
        st.dataframe(budget_df)
    except FileNotFoundError:
        pass
    except Exception as e:
        st.warning(f"⚠️ Error displaying budget entries: {e}")

def show_investment_tab():
    st.header("📈 Investment Overview")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("➕ Add or Update Asset")
        with st.form("investment_form"):
            inv_date = st.date_input("Date", value=datetime.today())
            inv_asset = st.text_input("Asset Name / Code", placeholder="e.g. BTC, AAPL, Gold")
            inv_cat = st.selectbox("Category", ["Crypto", "Stock", "Gold", "Cash", "Savings", "Other"])
            inv_value = st.number_input("Current Value (Rp)", min_value=0.0, step=10000.0)
            inv_notes = st.text_area("Notes")
            inv_submit = st.form_submit_button("Save Investment")
            if inv_submit:
                new_inv = pd.DataFrame([{ "Date": inv_date, "Asset": inv_asset, "Category": inv_cat, "Value": inv_value, "Notes": inv_notes }])
                inv_path = "data/investments.csv"
                try:
                    old = pd.read_csv(inv_path)
                    updated = pd.concat([old, new_inv], ignore_index=True)
                except FileNotFoundError:
                    updated = new_inv
                updated.to_csv(inv_path, index=False)
                st.success("✅ Investment saved!")

    with col2:
        try:
            inv_df = pd.read_csv("data/investments.csv")
            inv_df["Date"] = pd.to_datetime(inv_df["Date"])

            st.subheader("📊 Portfolio Summary (Latest Value)")
            latest_portfolio = inv_df.groupby("Asset")["Value"].last().sort_values(ascending=False)
            if not latest_portfolio.empty:
                fig3, ax3 = plt.subplots()
                ax3.pie(latest_portfolio, labels=latest_portfolio.index, autopct="%1.1f%%", startangle=90)
                ax3.axis("equal")
                st.pyplot(fig3)
            else:
                st.info("No investment data to display portfolio summary.")

            st.subheader("📈 Portfolio Value Over Time")
            portfolio_daily = inv_df.groupby("Date")["Value"].sum().reset_index()
            st.line_chart(portfolio_daily.set_index("Date"))

            st.subheader("💸 Withdrawn Assets")
            withdrawn_assets = st.multiselect("Mark withdrawn assets", inv_df["Asset"].unique())
            inv_df["Withdrawn"] = inv_df["Asset"].isin(withdrawn_assets)
            if not inv_df[inv_df["Withdrawn"] == True].empty:
                st.dataframe(inv_df[inv_df["Withdrawn"] == True])
            else:
                st.info("No assets marked as withdrawn.")

        except FileNotFoundError:
            st.info("No investment data available. Please add some entries.")
        except Exception as e:
            st.warning(f"⚠️ Error loading investment charts: {e}")

    try:
        inv_df = pd.read_csv("data/investments.csv")
        st.subheader("📄 All Investment Entries")
        st.dataframe(inv_df)
    except FileNotFoundError:
        pass
    except Exception as e:
        st.warning(f"⚠️ Error displaying investment entries: {e}")

with tab1:
    show_trading_tab()
with tab2:
    show_budget_tab()
with tab3:
    show_investment_tab()
