# ============================================================
# E-COMMERCE SALES ANALYTICS
# Step 6 — Streamlit App
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

st.markdown("""
<style>
    .main-title { font-size:2.2rem; font-weight:700; color:#1A56A0; }
    .sub-title  { font-size:1rem; color:#6B7280; margin-top:-10px; }
    .kpi-card   { background:#F0F7FF; border-left:4px solid #1A56A0;
                  padding:14px 18px; border-radius:8px; margin:4px 0; }
    .kpi-val    { font-size:1.7rem; font-weight:700; color:#1A56A0; }
    .kpi-lbl    { font-size:0.8rem; color:#6B7280; }
    .insight-blue  { background:#EBF4FF; border-left:4px solid #1A56A0;
                     padding:12px 16px; border-radius:8px; margin:6px 0;
                     word-wrap:break-word; white-space:normal; width:100%; color:#1A1A2E; }
    .insight-red   { background:#FEE2E2; border-left:4px solid #DC2626;
                     padding:12px 16px; border-radius:8px; margin:6px 0;
                     word-wrap:break-word; white-space:normal; width:100%; color:#1A1A2E; }
    .insight-green { background:#D1FAE5; border-left:4px solid #059669;
                     padding:12px 16px; border-radius:8px; margin:6px 0;
                     word-wrap:break-word; white-space:normal; width:100%; color:#1A1A2E; }
    .insight-amber { background:#FFF8E7; border-left:4px solid #F39C12;
                     padding:12px 16px; border-radius:8px; margin:6px 0;
                     word-wrap:break-word; white-space:normal; width:100%; color:#1A1A2E; }
    .section    { font-size:1.1rem; font-weight:600; color:#1A1A2E;
                  border-bottom:2px solid #1A56A0;
                  padding-bottom:4px; margin:20px 0 12px; }
    footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

BLUE, RED, GREEN, AMBER = "#1A56A0", "#E74C3C", "#27AE60", "#F39C12"

@st.cache_data
def load_data():
    DATA_URL = "https://raw.githubusercontent.com/Dilawar777/ecommerce-sales-analytics/main/ecommerce_cleaned.csv"
    try:
        df = pd.read_csv(DATA_URL)
    except Exception as e:
        st.error(f"Could not load dataset: {e}")
        st.stop()
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

df = load_data()

# ── Header ──────────────────────────────────────────────────
st.markdown('<p class="main-title">🛒 Brazilian E-Commerce Sales Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Olist Dataset · 2016–2018 · Python + SQL + Streamlit</p>', unsafe_allow_html=True)
st.markdown("")

# ── Sidebar filters ─────────────────────────────────────────
st.sidebar.markdown("### 🔧 Filters")
years = sorted(df["order_purchase_timestamp"].dt.year.unique())
year_filter = st.sidebar.multiselect("Year", options=years, default=years)
states = sorted(df["customer_state"].dropna().unique())
state_filter = st.sidebar.multiselect("State (optional)", options=states, default=[])

df_f = df[df["order_purchase_timestamp"].dt.year.isin(year_filter)]
if state_filter:
    df_f = df_f[df_f["customer_state"].isin(state_filter)]

conn = sqlite3.connect(":memory:")
df_f.to_sql("orders", conn, index=False, if_exists="replace")

# ── KPIs ────────────────────────────────────────────────────
total_revenue = df_f["total_payment"].sum()
total_orders  = df_f["order_id"].nunique()
avg_review    = df_f["review_score"].mean()
avg_delivery  = df_f["delivery_days"].mean()
late_pct      = df_f["is_late"].mean() * 100

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-val">R${total_revenue/1e6:.1f}M</div><div class="kpi-lbl">Total Revenue</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-val">{total_orders:,}</div><div class="kpi-lbl">Total Orders</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-val">{avg_review:.2f}/5</div><div class="kpi-lbl">Avg Review Score</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-val">{avg_delivery:.1f} days</div><div class="kpi-lbl">Avg Delivery Time</div></div>', unsafe_allow_html=True)
with k5:
    st.markdown(f'<div class="kpi-card"><div class="kpi-val">{late_pct:.1f}%</div><div class="kpi-lbl">Late Deliveries</div></div>', unsafe_allow_html=True)

st.markdown(""); st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Revenue Trends", "📦 Categories & Products", "🚚 Delivery & Reviews", "💡 Business Insights", "📄 Business Memo"])
# ════════════════════════════════════════════════════════════
# TAB 1 — REVENUE TRENDS
# ════════════════════════════════════════════════════════════
with tab1:
    monthly = pd.read_sql("""
        SELECT strftime('%Y-%m', order_purchase_timestamp) AS month,
               ROUND(SUM(total_payment),2) AS revenue
        FROM orders GROUP BY month ORDER BY month
    """, conn)
    monthly["month"] = pd.to_datetime(monthly["month"])

    st.markdown('<p class="section">Monthly Revenue Trend</p>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.fill_between(monthly["month"], monthly["revenue"], alpha=0.25, color=BLUE)
    ax.plot(monthly["month"], monthly["revenue"], color=BLUE, linewidth=2.5, marker="o", markersize=4)
    ax.set_title("Monthly Revenue Trend", fontweight="bold")
    ax.set_ylabel("Revenue (R$)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"R${x/1000:.0f}K"))
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    plt.tight_layout(); st.pyplot(fig); plt.close()

    seasonal = pd.read_sql("""
        SELECT CAST(strftime('%m', order_purchase_timestamp) AS INTEGER) AS month_num,
               ROUND(SUM(total_payment),2) AS revenue
        FROM orders GROUP BY month_num ORDER BY month_num
    """, conn)
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    seasonal["month_name"] = seasonal["month_num"].apply(lambda x: month_names[x-1])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<p class="section">Seasonal Pattern</p>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(7, 4))
        colors_season = [RED if v == seasonal["revenue"].max() else BLUE for v in seasonal["revenue"]]
        ax.bar(seasonal["month_name"], seasonal["revenue"], color=colors_season, alpha=0.85)
        ax.set_title("Revenue by Month (All Years)", fontweight="bold")
        ax.tick_params(axis="x", rotation=45)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"R${x/1000:.0f}K"))
        for s in ["top","right"]: ax.spines[s].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()

    with c2:
        st.markdown('<p class="section">Top 10 States by Revenue</p>', unsafe_allow_html=True)
        top_states = pd.read_sql("""
            SELECT customer_state AS state, ROUND(SUM(total_payment),2) AS revenue
            FROM orders GROUP BY state ORDER BY revenue DESC LIMIT 10
        """, conn)
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(top_states["state"], top_states["revenue"], color=BLUE, alpha=0.85)
        ax.set_title("Top 10 States by Revenue", fontweight="bold")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"R${x/1000:.0f}K"))
        for s in ["top","right"]: ax.spines[s].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════════
# TAB 2 — CATEGORIES & PRODUCTS
# ════════════════════════════════════════════════════════════
with tab2:
    top_categories = pd.read_sql("""
        SELECT product_category_name_english AS category,
               ROUND(SUM(total_payment),2) AS revenue,
               COUNT(DISTINCT order_id) AS orders
        FROM orders WHERE product_category_name_english != 'Unknown'
        GROUP BY category ORDER BY revenue DESC LIMIT 10
    """, conn)

    st.markdown('<p class="section">Top 10 Categories by Revenue</p>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12, 5))
    colors_cat = [RED if i < 3 else BLUE for i in range(len(top_categories))]
    ax.barh(top_categories["category"][::-1], top_categories["revenue"][::-1],
            color=colors_cat[::-1], alpha=0.85)
    ax.set_title("Top 10 Product Categories by Revenue", fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"R${x/1000:.0f}K"))
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    plt.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown('<p class="section">Worst Rated Categories (100+ orders)</p>', unsafe_allow_html=True)
    worst_categories = pd.read_sql("""
        SELECT product_category_name_english AS category,
               COUNT(*) AS cnt, ROUND(AVG(review_score),2) AS avg_review
        FROM orders WHERE product_category_name_english != 'Unknown'
        GROUP BY category HAVING cnt > 100 ORDER BY avg_review ASC LIMIT 8
    """, conn)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.barh(worst_categories["category"][::-1], worst_categories["avg_review"][::-1],
            color=RED, alpha=0.85)
    ax.set_title("8 Lowest Rated Categories (min 100 orders)", fontweight="bold")
    ax.set_xlim(0, 5)
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    plt.tight_layout(); st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════════
# TAB 3 — DELIVERY & REVIEWS
# ════════════════════════════════════════════════════════════
with tab3:
    delivery_review = pd.read_sql("""
        SELECT CASE WHEN delivery_days<=7 THEN '0-7 days'
                    WHEN delivery_days<=14 THEN '8-14 days'
                    WHEN delivery_days<=21 THEN '15-21 days'
                    ELSE '22+ days' END AS bucket,
               ROUND(AVG(review_score),2) AS avg_review,
               COUNT(*) AS cnt
        FROM orders GROUP BY bucket
    """, conn)
    order_buckets = ["0-7 days","8-14 days","15-21 days","22+ days"]
    delivery_review["bucket"] = pd.Categorical(delivery_review["bucket"], categories=order_buckets, ordered=True)
    delivery_review = delivery_review.sort_values("bucket")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<p class="section">Delivery Time vs Review Score</p>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(delivery_review["bucket"], delivery_review["avg_review"],
                      color=[GREEN,BLUE,AMBER,RED], alpha=0.85)
        ax.set_title("Delivery Time vs Avg Review Score", fontweight="bold")
        ax.set_ylim(0, 5)
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
                    f"{bar.get_height():.2f}", ha="center", fontweight="bold")
        for s in ["top","right"]: ax.spines[s].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()

    with c2:
        st.markdown('<p class="section">Payment Type Distribution</p>', unsafe_allow_html=True)
        payment_dist = pd.read_sql("""
            SELECT payment_type, COUNT(*) AS cnt
            FROM orders WHERE payment_type IS NOT NULL
            GROUP BY payment_type ORDER BY cnt DESC
        """, conn)
        fig, ax = plt.subplots(figsize=(7, 4))
        colors_pay = [BLUE,RED,GREEN,AMBER,"#8E44AD"]
        ax.pie(payment_dist["cnt"], labels=payment_dist["payment_type"],
               colors=colors_pay[:len(payment_dist)], autopct="%1.1f%%", startangle=90)
        ax.set_title("Payment Type Distribution", fontweight="bold")
        plt.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown('<p class="section">Top 10 Sellers by Revenue</p>', unsafe_allow_html=True)
    top_sellers = pd.read_sql("""
        SELECT seller_id, seller_state,
               ROUND(SUM(total_payment),2) AS revenue,
               ROUND(AVG(review_score),2) AS avg_review
        FROM orders GROUP BY seller_id ORDER BY revenue DESC LIMIT 10
    """, conn)
    top_sellers["seller_short"] = top_sellers["seller_id"].str[:8]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.barh(top_sellers["seller_short"][::-1], top_sellers["revenue"][::-1],
            color=BLUE, alpha=0.85)
    ax.set_title("Top 10 Sellers by Revenue", fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"R${x/1000:.0f}K"))
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    plt.tight_layout(); st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════════
# TAB 4 — BUSINESS INSIGHTS
# ════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section">Key Findings</p>', unsafe_allow_html=True)

    st.markdown('<div class="insight-red"><b>🛏️ Bed/Bath/Table Leads Revenue</b><br>Household goods (bed_bath_table category) generate the highest revenue of any product category — Brazilian consumers spend heavily on home essentials through e-commerce.</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-blue"><b>📍 São Paulo Dominates</b><br>São Paulo (SP) state leads all regions in revenue by a wide margin — reflecting its status as Brazil\'s largest economic and population center.</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-green"><b>🚚 Delivery Speed Drives Satisfaction</b><br>Orders delivered in 0-7 days score 4.33/5 on average, while orders taking 22+ days score significantly lower. Faster logistics directly translates to happier customers.</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-amber"><b>📉 Underserved Remote States</b><br>The 10 lowest-revenue states (RR, AP, AC, AM, RO, TO, SE, AL, RN) show 17-25 day average delivery times — nearly double the fastest bucket. This logistics gap likely suppresses demand in remote regions.</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-blue"><b>📅 May = Peak Revenue Month</b><br>May consistently generates the highest revenue across the dataset — useful for inventory and marketing planning.</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-red"><b>🪑 Office Furniture Underperforms</b><br>Among categories with 100+ orders, office_furniture has the lowest average review score (3.52/5) — suggesting quality, packaging, or shipping damage issues worth investigating.</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-amber"><b>⚠️ Data Limitation — Customer Tracking</b><br>Olist assigns a unique customer_id per order for privacy reasons, making true repeat-purchase analysis impossible with this dataset alone. Any "repeat customer" metric should be treated as a known limitation, not a real 0% retention rate.</div>', unsafe_allow_html=True)

    st.markdown('<p class="section">Business Recommendations</p>', unsafe_allow_html=True)
    st.markdown("""
    1. **Invest in logistics for remote states** (North/Northeast Brazil) — reducing delivery time from 20+ days to under 14 days could meaningfully lift both revenue and review scores in underperforming regions.
    2. **Audit office_furniture category** — investigate packaging and shipping processes given its low review score despite reasonable order volume.
    3. **Plan inventory around May peak** — ensure adequate stock of bed_bath_table and other top categories ahead of seasonal demand.
    4. **Promote credit card payment options** — it's the dominant payment method; ensure checkout flow is optimized for it.
    """)

# ════════════════════════════════════════════════════════════
# TAB 5 — BUSINESS MEMO
# ════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<p class="section">Business Memo</p>', unsafe_allow_html=True)
    st.markdown("""
    **To:** Operations & Strategy Leadership  
    **From:** Dilawar Mahar, Data Analyst  
    **Re:** Key findings and recommendations from 2016–2018 sales data analysis

    ---

    ## Summary

    An analysis of 96,426 delivered orders (R$19.8M in revenue) from the Olist marketplace reveals three structural issues limiting growth: a severe regional logistics gap, inconsistent product quality in specific categories, and a heavy revenue concentration in a single state.

    ---

    ## Key Findings

    **1. Delivery speed is the strongest driver of customer satisfaction.**  
    Orders delivered within 7 days average a 4.33/5 review score, while orders taking 22+ days average just 3.01/5 — a 1.3 point drop.

    **2. Remote states are underserved and underperforming.**  
    The 10 lowest-revenue states show average delivery times of 17–25 days, nearly double the fastest delivery bucket — very likely suppressing demand rather than reflecting genuinely lower interest.

    **3. Revenue is heavily concentrated in São Paulo.**  
    São Paulo alone generates more revenue than the next four highest states combined.

    **4. office_furniture underperforms on quality.**  
    Among categories with 100+ orders, office_furniture has the lowest average review score (3.52/5) — suggesting packaging, durability, or shipping damage issues.

    **5. May is the peak revenue month.**  
    Demand consistently peaks in May — useful for inventory and marketing planning.

    **6. Data limitation.**  
    Olist assigns a unique customer ID per order, making true repeat-purchase analysis impossible with this dataset alone.

    ---

    ## Recommendations

    1. **Prioritize logistics investment in the 10 lowest-revenue states.** Reducing delivery time from 20+ days toward 14 days could improve both order volume and review scores.

    2. **Audit the office_furniture supply chain.** Investigate packaging standards and carrier handling specifically for this category.

    3. **Diversify regional marketing investment.** Reduce dependency on São Paulo by testing targeted promotions in mid-tier states (RJ, MG, RS).

    4. **Plan inventory and staffing around the May peak.** Ensure adequate stock of top categories (bed_bath_table, health_beauty, computers_accessories) ahead of this period.

    5. **Invest in proper customer-level tracking** to enable accurate repeat-purchase and lifetime-value analysis going forward.

    ---
    *Full methodology and interactive dashboard: [github.com/Dilawar777/ecommerce-sales-analytics](https://github.com/Dilawar777/ecommerce-sales-analytics)*
    """)

st.divider()
st.markdown(
    '<p style="text-align:center;color:#9CA3AF;font-size:0.8rem;">'
    'Built by <b>Dilawar Mahar</b> · Data Analyst · Sukkur IBA University · '
    'Data: Olist via Kaggle · Python + SQL + Streamlit · '
    '<a href="https://github.com/Dilawar777" style="color:#1A56A0">GitHub</a></p>',
    unsafe_allow_html=True
)
