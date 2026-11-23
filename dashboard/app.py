from pathlib import Path
import os

import pandas as pd
import psycopg
import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parent / ".env")
st.set_page_config(page_title="E-commerce Intelligence", page_icon="🛒", layout="wide")
st.markdown("<style>" + (ROOT / "style.css").read_text(encoding="utf-8") + "</style>", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def query(sql):
    with psycopg.connect(
        host=os.getenv("DASHBOARD_DB_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
        options="-c default_transaction_read_only=on",
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return pd.DataFrame(cur.fetchall(), columns=[c.name for c in cur.description])

left, right = st.columns([3, 1])
with left:
    st.title("E-commerce Intelligence")
    st.markdown("Business performance overview")
    st.caption("PostgreSQL · dbt analytical marts · Synthetic dataset")
with right:
    st.image(str(ROOT / "ecommerce.svg"), use_container_width=True)
if st.button("Refresh data"):
    query.clear()

try:
    customers = query("""
        select count(*) filter (where completed_orders > 0) as buyers,
               100.0 * count(*) filter (where is_repeat_customer)
                   / nullif(count(*) filter (where completed_orders > 0), 0) as repeat_rate
        from analytics_marts.mart_customer_360
    """).iloc[0]
    sales = query("""
        select date_trunc('month', order_date)::date as month,
               sum(net_amount) as net_sales
        from analytics_marts.fct_daily_sales
        group by 1 order by 1
    """)
    cohorts = query("""
        select cohort_month, months_since_first_purchase as month_offset,
               cohort_customers, active_customers, retention_rate_pct
        from analytics_marts.mart_customer_cohort_retention
        where activity_month < date_trunc('month', current_date)
          and months_since_first_purchase <= 12
        order by 1, 2
    """)
except (psycopg.Error, KeyError):
    st.error("Unable to load analytical marts. Check PostgreSQL settings and run dbt build.")
    st.stop()

for col in ["cohort_customers", "active_customers", "retention_rate_pct"]:
    cohorts[col] = pd.to_numeric(cohorts[col])
retention = cohorts.groupby("month_offset")[["active_customers", "cohort_customers"]].sum()
retention["Retention (%)"] = 100 * retention.active_customers / retention.cohort_customers
sales["net_sales"] = pd.to_numeric(sales["net_sales"])

def pct(value):
    return f"{value:.2f}%" if pd.notna(value) else "—"

def compact_amount(value):
    for divisor, suffix in [(1e9, "B"), (1e6, "M"), (1e3, "K")]:
        if abs(value) >= divisor:
            return f"{value / divisor:,.2f}{suffix}"
    return f"{value:,.2f}"

net_sales = sales.net_sales.sum()
a, b, c, d = st.columns(4)
a.metric("Net sales", compact_amount(net_sales), help=f"Total net sales: {net_sales:,.2f}")
b.metric("Repeat purchase rate", pct(customers.repeat_rate))
c.metric("M1 retention", pct(retention["Retention (%)"].get(1)))
d.metric("Purchasing customers", f"{int(customers.buyers):,}")

st.caption("Lifetime metrics from the latest marts. Net sales exclude cancelled orders; customer metrics use completed orders.")
st.subheader("Monthly net sales")
st.line_chart(sales.set_index("month")["net_sales"])
st.subheader("Customer retention")
st.line_chart(retention.loc[retention.index > 0, ["Retention (%)"]])
st.caption("Weighted monthly retention; eligible cohort composition varies by month offset.")
st.subheader("Cohort analysis")
matrix = cohorts.pivot(index="cohort_month", columns="month_offset", values="retention_rate_pct")
matrix.index = pd.to_datetime(matrix.index).strftime("%Y-%m")
matrix.columns = [f"M{x}" for x in matrix.columns]
if not matrix.empty:
    st.dataframe(matrix.style.background_gradient(cmap="Blues", vmin=0, vmax=100).format("{:.1f}%", na_rep="—"), use_container_width=True)
else:
    st.info("No completed cohort months available.")
st.caption("Current calendar month excluded from retention. Run with the default dbt reference date; historical builds are not intended for this dashboard.")
