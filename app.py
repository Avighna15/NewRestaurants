import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# LuLu / Restaurant Franchise Expansion Dashboard
# Hypothesis project:
# Food cost, labour, rent and utilities are assumed to be AED 0.
# Therefore "Illustrative Profit" = Net Revenue after platform
# commission. This is NOT a full accounting profit measure.
# ============================================================

st.set_page_config(
    page_title="Franchise Expansion Dashboard",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------- STYLE -----------------------------
st.markdown("""
<style>
:root{
  --bg:#07111F;
  --bg2:#0D1728;
  --panel:#111D2E;
  --panel2:#162338;
  --accent:#27D3C2;
  --contrast:#FFB547;
  --white:#F7FAFC;
  --muted:#9EABBC;
  --line:rgba(255,255,255,.09);
}
.stApp{
  background:
    radial-gradient(circle at 82% 4%,rgba(39,211,194,.13),transparent 22%),
    radial-gradient(circle at 12% 88%,rgba(255,181,71,.09),transparent 25%),
    radial-gradient(circle at 55% 45%,rgba(73,108,168,.07),transparent 32%),
    linear-gradient(135deg,#050B14 0%,#091321 48%,#0E1929 100%);
  color:var(--white);
}
.stApp:before{
  content:"";position:fixed;inset:0;pointer-events:none;opacity:.028;
  background-image:radial-gradient(#fff .65px,transparent .65px);
  background-size:11px 11px;z-index:0;
}
.block-container{padding:1.35rem 2rem 3rem;max-width:1550px;position:relative;z-index:1;}
[data-testid="stHeader"]{background:transparent;}

.hero{
  position:relative;overflow:hidden;border:1px solid var(--line);border-radius:26px;
  padding:2rem 2.25rem 1.85rem;margin-bottom:1rem;
  background:
    linear-gradient(115deg,rgba(8,16,28,.98) 0%,rgba(12,28,43,.94) 55%,rgba(19,49,57,.84) 100%);
  box-shadow:0 25px 80px rgba(0,0,0,.35);
}
.hero:before{
  content:"";position:absolute;width:420px;height:420px;right:-150px;top:-210px;
  border:1px solid rgba(39,211,194,.20);border-radius:50%;
  box-shadow:0 0 0 38px rgba(39,211,194,.035),0 0 0 76px rgba(39,211,194,.018);
}
.hero:after{
  content:"";position:absolute;width:180px;height:4px;left:2.25rem;bottom:0;
  background:linear-gradient(90deg,var(--accent),var(--contrast));border-radius:10px;
}
.brand{display:flex;align-items:center;gap:.65rem;color:#fff;font-weight:800;font-size:1rem;margin-bottom:.8rem}
.brandmark{
  width:36px;height:36px;border-radius:10px;
  background:linear-gradient(135deg,var(--accent),#168FA6);
  display:inline-flex;align-items:center;justify-content:center;color:#061019;
  font-weight:950;box-shadow:0 8px 24px rgba(39,211,194,.20)
}
.kicker{font-size:.70rem;letter-spacing:.20em;text-transform:uppercase;color:var(--accent);font-weight:800}
.hero-title{
  font-family:Georgia,'Times New Roman',serif;font-size:2.65rem;line-height:1.05;
  font-weight:700;color:#F8FBFF;margin:.35rem 0 .55rem
}
.hero-title span{color:var(--accent)}
.hero-sub{max-width:920px;color:#C8D2DE;font-size:1rem;line-height:1.55}

.stTabs [data-baseweb="tab-list"]{gap:.55rem;background:transparent;padding:.25rem 0 .8rem}
.stTabs [data-baseweb="tab"]{
  height:2.65rem;padding:0 1.15rem;border-radius:999px;color:#B8C3D1;
  background:rgba(255,255,255,.045);border:1px solid var(--line);font-weight:700
}
.stTabs [data-baseweb="tab"]:hover{color:#fff;border-color:rgba(39,211,194,.45)}
.stTabs [aria-selected="true"]{
  background:linear-gradient(90deg,var(--accent),#1DB3C5)!important;color:#061019!important;
  border-color:var(--accent)!important;box-shadow:0 8px 24px rgba(39,211,194,.20)
}

.section{
  display:flex;align-items:center;gap:.65rem;font-family:Georgia,'Times New Roman',serif;
  font-size:1.45rem;font-weight:700;color:#F5F9FF;margin:1.1rem 0 .7rem
}
.section:before{
  content:"";width:4px;height:1.45rem;background:linear-gradient(var(--accent),var(--contrast));
  border-radius:5px;box-shadow:0 0 18px rgba(39,211,194,.28)
}
.note{color:#9EABBC!important}

div[data-testid="stMetric"]{
  position:relative;overflow:hidden;
  background:linear-gradient(145deg,rgba(20,34,53,.97),rgba(12,24,39,.97));
  border:1px solid var(--line);border-radius:17px;padding:16px 17px 14px;
  box-shadow:0 15px 38px rgba(0,0,0,.20)
}
div[data-testid="stMetric"]:before{
  content:"";position:absolute;left:0;top:0;width:100%;height:3px;
  background:linear-gradient(90deg,var(--accent),var(--contrast))
}
div[data-testid="stMetricLabel"]{color:#AAB7C7!important;font-weight:700}
div[data-testid="stMetricValue"]{color:#F7FAFC!important;font-weight:850;letter-spacing:-.02em}

[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#111D2E}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div,[data-testid="stDateInput"]>div>div{
  background:#101C2C!important;border-color:rgba(255,255,255,.12)!important;
  color:#F5F7FA!important;border-radius:10px!important
}
label{color:#C1CCD9!important;font-weight:650!important}

div[data-testid="stAlert"]{
  background:rgba(255,181,71,.08);border:1px solid rgba(255,181,71,.35);
  color:#F4E8D5;border-radius:14px
}
.insight-ribbon{
  margin:1rem 0 1.3rem;padding:1rem 1.2rem;border:1px solid rgba(39,211,194,.28);
  border-radius:16px;background:linear-gradient(100deg,rgba(39,211,194,.10),rgba(255,181,71,.055));
  color:#DCE6EF
}
.insight-ribbon b{color:var(--accent)}
.premium-footer{
  margin-top:2rem;padding-top:1rem;border-top:1px solid var(--line);
  color:#7F8EA1;font-size:.75rem;display:flex;justify-content:space-between
}
</style>
""", unsafe_allow_html=True)

# ------------------------- DATA ------------------------------
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def find_data_file(filename):
    # First check the recommended /data folder, then the repository root,
    # then search subfolders. This makes Streamlit Cloud deployment robust
    # to minor GitHub folder-placement differences.
    candidates = [
        BASE_DIR / "data" / filename,
        BASE_DIR / filename,
    ]

    for path in candidates:
        if path.is_file():
            return path

    matches = list(BASE_DIR.rglob(filename))
    if matches:
        return matches[0]

    raise FileNotFoundError(
        f"Missing required file: {filename}. "
        f"Upload {filename} to the GitHub repository, preferably inside a "
        f"'data' folder next to app.py."
    )

@st.cache_data
def load_data():
    areas = pd.read_csv(find_data_file("areas.csv"))
    menu = pd.read_csv(find_data_file("menu.csv"))
    orders = pd.read_csv(find_data_file("orders.csv"))
    items = pd.read_csv(find_data_file("order_items.csv"))
    platforms = pd.read_csv(find_data_file("platforms.csv"))

    orders["order_datetime"] = pd.to_datetime(orders["order_datetime"])
    for c in ["preparing_at", "ready_at", "dispatched_at", "completed_at"]:
        if c in orders.columns:
            orders[c] = pd.to_datetime(orders[c], errors="coerce")

    return areas, menu, orders, items, platforms

areas, menu, orders, items, platforms = load_data()

# Only Delivered orders are treated as realised sales.
delivered_orders = orders[orders["status"].eq("Delivered")].copy()

# Attach order-level fields to every item.
item_data = items.merge(
    orders[
        [
            "order_id", "order_datetime", "channel_type", "platform",
            "order_type", "area", "status", "gross_amount",
            "commission_amount", "net_revenue"
        ]
    ],
    on="order_id",
    how="left",
)

# Attach menu characteristics.
item_data = item_data.merge(
    menu[
        ["dish", "dish_id", "cuisine", "category", "price_aed",
         "prep_minutes", "popularity"]
    ].drop_duplicates("dish"),
    on="dish",
    how="left",
    suffixes=("", "_menu"),
)

# Allocate order commission across items in proportion to item revenue.
# This creates a transparent item-level net revenue proxy.
order_item_gross = item_data.groupby("order_id")["line_total"].transform("sum")
item_data["allocated_commission"] = (
    item_data["commission_amount"]
    * item_data["line_total"]
    / order_item_gross.replace(0, pd.NA)
).fillna(0)

item_data["item_net_revenue"] = item_data["line_total"] - item_data["allocated_commission"]

# Project assumption requested by the user.
FOOD_COST = 0
LABOUR_COST = 0
RENT_COST = 0
UTILITIES_COST = 0

item_data["illustrative_profit"] = (
    item_data["item_net_revenue"]
    - FOOD_COST
    - LABOUR_COST
    - RENT_COST
    - UTILITIES_COST
)

# ------------------------- HELPERS ---------------------------
def aed(v):
    if pd.isna(v):
        return "AED 0"
    v = float(v)
    if abs(v) >= 1_000_000:
        return f"AED {v/1_000_000:.2f}M"
    if abs(v) >= 1_000:
        return f"AED {v/1_000:.1f}K"
    return f"AED {v:,.0f}"

def pct(v):
    return "—" if pd.isna(v) else f"{v:.1f}%"

def growth(current, previous):
    if previous is None or previous == 0:
        return None
    return (current - previous) / previous * 100

def order_metrics(d):
    revenue = d["gross_amount"].sum()
    net = d["net_revenue"].sum()
    n = d["order_id"].nunique()
    cancellations = (d["status"] == "Cancelled").sum()
    return revenue, net, n, (cancellations / len(d) * 100 if len(d) else 0)

# ------------------------- CHART THEME -----------------------
ORANGE="#FF5F00"; AMBER="#FFB000"; CREAM="#F7F3EE"; MUTED="#AEB3BA"
def style_fig(fig,height=350,showlegend=None):
    fig.update_layout(height=height,margin=dict(l=12,r=12,t=18,b=12),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="Arial",color=CREAM,size=12),hoverlabel=dict(bgcolor="#17191B",bordercolor=ORANGE,font_color=CREAM),xaxis=dict(gridcolor="rgba(255,255,255,.08)",zerolinecolor="rgba(255,255,255,.08)",tickfont_color=MUTED),yaxis=dict(gridcolor="rgba(255,255,255,.08)",zerolinecolor="rgba(255,255,255,.08)",tickfont_color=MUTED),legend=dict(font=dict(color=CREAM),bgcolor="rgba(0,0,0,0)"))
    if showlegend is not None: fig.update_layout(showlegend=showlegend)
    return fig

# ------------------------- HEADER ----------------------------
st.markdown("""
<div class="hero">
  <div class="brand"><span class="brandmark">FI</span> Franchise Intelligence</div>
  <div class="kicker">Restaurant Chain · Franchise Expansion Analysis</div>
  <div class="hero-title">From <span>Insights</span> to the Next Location</div>
  <div class="hero-sub">A board-ready view of historical demand, product performance and location concentration — designed to support evidence-based expansion discussions.</div>
</div>
<div class="insight-ribbon"><b>BOARD LENS</b> &nbsp; Where is demand strongest? &nbsp; · &nbsp; What products drive it? &nbsp; · &nbsp; How concentrated is that demand? &nbsp; · &nbsp; What evidence supports a new branch?</div>
""", unsafe_allow_html=True)

st.warning("Project assumption: food cost, labour, rent and utilities are currently AED 0. Therefore, Illustrative Profit = Net Revenue after platform commission. This is a hypothesis metric, not audited accounting profit.")

# ------------------------- NAVIGATION -----------------------
tab1, tab2, tab3 = st.tabs([
    "🏢 Executive Overview",
    "📍 Expansion Analysis",
    "🍕 Product & Location Analysis",
])

# ============================================================
# TAB 1 — EXECUTIVE OVERVIEW
# ============================================================
with tab1:
    st.markdown('<div class="section">Overall business performance</div>', unsafe_allow_html=True)

    # Global date filter
    min_date = orders["order_datetime"].min().date()
    max_date = orders["order_datetime"].max().date()

    d1, d2 = st.columns([1, 2])
    with d1:
        date_range = st.date_input(
            "Analysis period",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
    with d2:
        st.markdown(
            '<div class="note" style="padding-top:30px;">Cancelled orders are excluded from realised revenue and order-value KPIs, but cancellation rate is shown separately.</div>',
            unsafe_allow_html=True,
        )

    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start = pd.Timestamp(date_range[0])
        end = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    else:
        start = pd.Timestamp(date_range)
        end = start + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    period_orders = orders[
        (orders["order_datetime"] >= start) &
        (orders["order_datetime"] <= end)
    ].copy()
    period_delivered = period_orders[period_orders["status"].eq("Delivered")].copy()

    gross = period_delivered["gross_amount"].sum()
    net = period_delivered["net_revenue"].sum()
    order_count = len(period_delivered)
    aov = net / order_count if order_count else 0
    cancellation_rate = (
        (period_orders["status"] == "Cancelled").mean() * 100
        if len(period_orders) else 0
    )
    commission = period_delivered["commission_amount"].sum()
    illustrative_profit = net  # all other costs assumed zero

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.metric("Gross Revenue", aed(gross))
    k2.metric("Net Revenue", aed(net))
    k3.metric("Orders", f"{order_count:,}")
    k4.metric("Average Order Value", aed(aov))
    k5.metric("Cancellation Rate", pct(cancellation_rate))
    k6.metric("Commission Cost", aed(commission))

    st.caption(
        f"Illustrative profit under current project assumptions: {aed(illustrative_profit)}."
    )

    # Revenue trend
    st.markdown('<div class="section">Revenue trend</div>', unsafe_allow_html=True)
    trend = (
        period_delivered.assign(Month=period_delivered["order_datetime"].dt.to_period("M").dt.to_timestamp())
        .groupby("Month", as_index=False)
        .agg(Gross_Revenue=("gross_amount","sum"), Net_Revenue=("net_revenue","sum"))
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend["Month"], y=trend["Gross_Revenue"], mode="lines+markers",
        name="Gross Revenue", line=dict(width=3,color=ORANGE),
        hovertemplate="Gross: AED %{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=trend["Month"], y=trend["Net_Revenue"], mode="lines+markers",
        name="Net Revenue", line=dict(width=2,color=CREAM),
        hovertemplate="Net: AED %{y:,.0f}<extra></extra>"
    ))
    style_fig(fig,350); fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown('<div class="section">Top dishes by units</div>', unsafe_allow_html=True)
        top_dishes = (
            item_data[
                (item_data["status"] == "Delivered") &
                (item_data["order_datetime"] >= start) &
                (item_data["order_datetime"] <= end)
            ]
            .groupby("dish", as_index=False)["quantity"].sum()
            .sort_values("quantity", ascending=False).head(8)
        )
        fig = px.bar(top_dishes.sort_values("quantity"), x="quantity", y="dish", orientation="h", color_discrete_sequence=[ORANGE])
        style_fig(fig,330,showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section">Revenue by area</div>', unsafe_allow_html=True)
        area_rev = (
            period_delivered.groupby("area", as_index=False)["net_revenue"]
            .sum().sort_values("net_revenue", ascending=False)
        )
        fig = px.bar(area_rev.sort_values("net_revenue"), x="net_revenue", y="area", orientation="h", color_discrete_sequence=[ORANGE])
        style_fig(fig,330,showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        st.markdown('<div class="section">Platform revenue mix</div>', unsafe_allow_html=True)
        plat = period_delivered.groupby("platform", as_index=False)["net_revenue"].sum()
        fig = px.pie(plat, names="platform", values="net_revenue", hole=.55, color_discrete_sequence=[ORANGE,AMBER,CREAM,"#7C858F","#8B2F1C"])
        style_fig(fig,330)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2 — EXPANSION ANALYSIS
# ============================================================
with tab2:
    st.markdown('<div class="section">New branch expansion analysis</div>', unsafe_allow_html=True)
    st.write(
        "Use this page to compare existing areas as evidence for a potential branch. "
        "It does not assume that the strongest historical area is automatically the right location."
    )

    area_list = sorted(areas["area"].dropna().unique())
    selected_area = st.selectbox("Select a candidate area to investigate", area_list)

    candidate = orders[orders["area"] == selected_area].copy()
    network = orders.copy()

    candidate_del = candidate[candidate["status"] == "Delivered"]
    network_del = network[network["status"] == "Delivered"]

    cand_gross = candidate_del["gross_amount"].sum()
    cand_net = candidate_del["net_revenue"].sum()
    cand_orders = len(candidate_del)
    cand_aov = cand_net / cand_orders if cand_orders else 0
    cand_cancel = (candidate["status"] == "Cancelled").mean() * 100 if len(candidate) else 0
    cand_commission = candidate_del["commission_amount"].sum()

    net_share = cand_net / network_del["net_revenue"].sum() * 100 if network_del["net_revenue"].sum() else 0

    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Area Gross Revenue", aed(cand_gross))
    m2.metric("Area Net Revenue", aed(cand_net))
    m3.metric("Delivered Orders", f"{cand_orders:,}")
    m4.metric("Average Order Value", aed(cand_aov))
    m5.metric("Cancellation Rate", pct(cand_cancel))

    st.caption(
        f"{selected_area} contributes {net_share:.1f}% of network net revenue in the available dataset. "
        f"Commission cost in this area is {aed(cand_commission)}."
    )

    # Area comparison table
    st.markdown('<div class="section">Area opportunity comparison</div>', unsafe_allow_html=True)

    area_summary = (
        orders.groupby("area")
        .apply(lambda g: pd.Series({
            "Orders": (g["status"] == "Delivered").sum(),
            "Gross_Revenue": g.loc[g["status"] == "Delivered", "gross_amount"].sum(),
            "Net_Revenue": g.loc[g["status"] == "Delivered", "net_revenue"].sum(),
            "AOV": (
                g.loc[g["status"] == "Delivered", "net_revenue"].sum()
                / max((g["status"] == "Delivered").sum(), 1)
            ),
            "Cancellation_Rate": (g["status"] == "Cancelled").mean() * 100,
            "Commission": g.loc[g["status"] == "Delivered", "commission_amount"].sum(),
        }), include_groups=False)
        .reset_index()
    )

    area_summary["Net_Revenue_Share"] = (
        area_summary["Net_Revenue"] / area_summary["Net_Revenue"].sum() * 100
    )

    area_summary = area_summary.merge(areas, on="area", how="left")
    area_summary = area_summary.sort_values("Net_Revenue", ascending=False)

    st.dataframe(
        area_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "area": "Area",
            "Orders": st.column_config.NumberColumn("Orders", format="%d"),
            "Gross_Revenue": st.column_config.NumberColumn("Gross Revenue", format="AED %.0f"),
            "Net_Revenue": st.column_config.NumberColumn("Net Revenue", format="AED %.0f"),
            "AOV": st.column_config.NumberColumn("AOV", format="AED %.0f"),
            "Cancellation_Rate": st.column_config.NumberColumn("Cancellation", format="%.1f%%"),
            "Commission": st.column_config.NumberColumn("Commission", format="AED %.0f"),
            "Net_Revenue_Share": st.column_config.NumberColumn("Net Revenue Share", format="%.1f%%"),
            "distance_km": st.column_config.NumberColumn("Distance (km)", format="%.0f"),
            "order_weight": st.column_config.NumberColumn("Order Weight", format="%.0f"),
        },
    )

    # Candidate area product mix
    st.markdown(f'<div class="section">What sells in {selected_area}?</div>', unsafe_allow_html=True)

    cand_items = item_data[
        (item_data["area"] == selected_area) &
        (item_data["status"] == "Delivered")
    ].copy()

    product_mix = (
        cand_items.groupby(["dish","category","cuisine"], as_index=False)
        .agg(
            Units=("quantity","sum"),
            Item_Revenue=("line_total","sum"),
            Item_Net_Revenue=("item_net_revenue","sum"),
        )
        .sort_values("Item_Net_Revenue", ascending=False)
    )

    product_mix["Revenue_Share"] = (
        product_mix["Item_Net_Revenue"] / product_mix["Item_Net_Revenue"].sum() * 100
    )

    p1,p2 = st.columns([1.3,1])

    with p1:
        top_area_products = product_mix.head(10).sort_values("Item_Net_Revenue")
        fig = px.bar(
            top_area_products,
            x="Item_Net_Revenue",
            y="dish",
            color="category",
            orientation="h",
            color_discrete_sequence=[ORANGE,AMBER,CREAM,"#7C858F"],
            labels={"Item_Net_Revenue":"Illustrative Net Revenue","dish":""}
        )
        style_fig(fig,390)
        st.plotly_chart(fig, use_container_width=True)

    with p2:
        st.markdown("**Top product mix**")
        st.dataframe(
            product_mix.head(10),
            use_container_width=True,
            hide_index=True,
            column_config={
                "dish":"Dish",
                "category":"Category",
                "cuisine":"Cuisine",
                "Units":st.column_config.NumberColumn("Units",format="%d"),
                "Item_Revenue":st.column_config.NumberColumn("Gross Item Revenue",format="AED %.0f"),
                "Item_Net_Revenue":st.column_config.NumberColumn("Illustrative Profit",format="AED %.0f"),
                "Revenue_Share":st.column_config.NumberColumn("Share",format="%.1f%%"),
            }
        )

    st.markdown("### Expansion evidence")
    top = product_mix.iloc[0] if not product_mix.empty else None

    if top is not None:
        overall_items = item_data[item_data["status"] == "Delivered"]
        overall_dish = overall_items[overall_items["dish"] == top["dish"]]
        overall_share = (
            overall_dish["item_net_revenue"].sum() / overall_items["item_net_revenue"].sum() * 100
            if overall_items["item_net_revenue"].sum() else 0
        )
        area_share = top["Revenue_Share"]
        concentration = area_share / overall_share if overall_share else 0

        e1,e2,e3 = st.columns(3)
        e1.metric("Top product in area", str(top["dish"]))
        e2.metric("Area product share", f"{area_share:.1f}%")
        e3.metric("Overall product share", f"{overall_share:.1f}%")

        if overall_share:
            st.info(
                f"{top['dish']} represents {area_share:.1f}% of illustrative item net revenue in "
                f"{selected_area}, versus {overall_share:.1f}% across the network "
                f"(about {concentration:.1f}× the overall concentration)."
            )

    st.caption(
        "Expansion evidence should be considered together: area demand, product concentration, "
        "AOV, cancellation rate and commission burden. The dashboard does not make an automatic "
        "branch-location decision."
    )

# ============================================================
# TAB 3 — PRODUCT & LOCATION ANALYSIS
# ============================================================
with tab3:
    st.markdown('<div class="section">Product & location intelligence</div>', unsafe_allow_html=True)
    st.write(
        "Test the core hypothesis: does a product perform disproportionately well in a particular area?"
    )

    q1,q2,q3,q4 = st.columns(4)

    cuisine_options = ["All"] + sorted(menu["cuisine"].dropna().unique().tolist())
    category_options = ["All"] + sorted(menu["category"].dropna().unique().tolist())

    with q1:
        cuisine_sel = st.selectbox("Cuisine", cuisine_options)
    with q2:
        category_sel = st.selectbox("Category", category_options)

    filtered_menu = menu.copy()
    if cuisine_sel != "All":
        filtered_menu = filtered_menu[filtered_menu["cuisine"] == cuisine_sel]
    if category_sel != "All":
        filtered_menu = filtered_menu[filtered_menu["category"] == category_sel]

    dish_options = ["All"] + sorted(filtered_menu["dish"].dropna().unique().tolist())
    with q3:
        dish_sel = st.selectbox("Dish", dish_options)
    with q4:
        area_sel = st.selectbox("Location", ["All"] + sorted(areas["area"].unique()))

    selected_items = item_data[item_data["status"] == "Delivered"].copy()

    if cuisine_sel != "All":
        selected_items = selected_items[selected_items["cuisine"] == cuisine_sel]
    if category_sel != "All":
        selected_items = selected_items[selected_items["category"] == category_sel]
    if dish_sel != "All":
        selected_items = selected_items[selected_items["dish"] == dish_sel]
    if area_sel != "All":
        selected_items = selected_items[selected_items["area"] == area_sel]

    if selected_items.empty:
        st.warning("No delivered item sales match the selected filters.")
        st.stop()

    total_units = selected_items["quantity"].sum()
    item_revenue = selected_items["line_total"].sum()
    item_net = selected_items["item_net_revenue"].sum()
    item_orders = selected_items["order_id"].nunique()
    avg_item_value = item_revenue / total_units if total_units else 0

    # Menu reference metrics when a single dish is selected.
    menu_match = menu[menu["dish"] == dish_sel] if dish_sel != "All" else pd.DataFrame()
    popularity = menu_match["popularity"].iloc[0] if not menu_match.empty else None
    prep = menu_match["prep_minutes"].iloc[0] if not menu_match.empty else None

    r1,r2,r3,r4,r5,r6 = st.columns(6)
    r1.metric("Units", f"{int(total_units):,}")
    r2.metric("Gross Item Revenue", aed(item_revenue))
    r3.metric("Illustrative Profit", aed(item_net))
    r4.metric("Orders Containing Item", f"{item_orders:,}")
    r5.metric("Avg Item Price", aed(avg_item_value))
    r6.metric("Popularity", f"{popularity:.0f}/10" if popularity is not None else "Multiple")

    if prep is not None:
        st.caption(
            f"Menu reference: preparation time {prep:.0f} minutes. "
            f"Food cost, labour, rent and utilities are assumed to be AED 0 in this project."
        )

    # Selected location vs overall benchmark
    st.markdown('<div class="section">Selected location vs overall</div>', unsafe_allow_html=True)

    benchmark_items = item_data[item_data["status"] == "Delivered"].copy()

    if dish_sel != "All":
        benchmark_items = benchmark_items[benchmark_items["dish"] == dish_sel]
    elif category_sel != "All":
        benchmark_items = benchmark_items[benchmark_items["category"] == category_sel]
    elif cuisine_sel != "All":
        benchmark_items = benchmark_items[benchmark_items["cuisine"] == cuisine_sel]

    overall_units = benchmark_items["quantity"].sum()
    overall_revenue = benchmark_items["line_total"].sum()
    overall_net = benchmark_items["item_net_revenue"].sum()
    overall_orders = benchmark_items["order_id"].nunique()

    if area_sel != "All":
        selected_bench = benchmark_items[benchmark_items["area"] == area_sel]
        location_name = area_sel
    else:
        selected_bench = benchmark_items
        location_name = "All areas"

    selected_units = selected_bench["quantity"].sum()
    selected_revenue = selected_bench["line_total"].sum()
    selected_net = selected_bench["item_net_revenue"].sum()
    selected_orders = selected_bench["order_id"].nunique()

    benchmark = pd.DataFrame({
        "Metric": ["Units", "Gross Item Revenue", "Illustrative Profit", "Orders Containing Item"],
        location_name: [selected_units, selected_revenue, selected_net, selected_orders],
        "Overall": [overall_units, overall_revenue, overall_net, overall_orders],
    })

    st.dataframe(
        benchmark,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Units": st.column_config.NumberColumn("Units", format="%.0f"),
            "Gross Item Revenue": st.column_config.NumberColumn("Gross Item Revenue", format="AED %.0f"),
            "Illustrative Profit": st.column_config.NumberColumn("Illustrative Profit", format="AED %.0f"),
            "Orders Containing Item": st.column_config.NumberColumn("Orders Containing Item", format="%.0f"),
        },
    )

    # Product distribution across areas
    st.markdown('<div class="section">Where does the selected product/category sell?</div>', unsafe_allow_html=True)

    area_product = (
        benchmark_items.groupby("area", as_index=False)
        .agg(Units=("quantity","sum"), Illustrative_Profit=("item_net_revenue","sum"))
        .sort_values("Units", ascending=False)
    )

    fig = px.bar(
        area_product,
        x="area",
        y="Units",
        hover_data=["Illustrative_Profit"],
        labels={"area":"","Units":"Units Sold"},
        color_discrete_sequence=[ORANGE],
    )
    style_fig(fig,360)
    st.plotly_chart(fig, use_container_width=True)

    # Compact cancellation view
    if dish_sel != "All":
        item_orders_all = item_data[item_data["dish"] == dish_sel].copy()
    elif category_sel != "All":
        item_orders_all = item_data[item_data["category"] == category_sel].copy()
    elif cuisine_sel != "All":
        item_orders_all = item_data[item_data["cuisine"] == cuisine_sel].copy()
    else:
        item_orders_all = item_data.copy()

    cancellation_by_area = (
        item_orders_all.groupby("area")
        .agg(
            Orders=("order_id","nunique"),
            Cancelled_Orders=("status", lambda s: (s == "Cancelled").sum()),
        )
        .reset_index()
    )
    cancellation_by_area["Cancellation_Rate"] = (
        cancellation_by_area["Cancelled_Orders"] / cancellation_by_area["Orders"] * 100
    ).fillna(0)

    st.markdown('<div class="section">Cancellation rate for selected product/category</div>', unsafe_allow_html=True)
    st.dataframe(
        cancellation_by_area.sort_values("Cancellation_Rate"),
        use_container_width=True,
        hide_index=True,
        column_config={
            "area":"Area",
            "Orders":st.column_config.NumberColumn("Orders",format="%d"),
            "Cancelled_Orders":st.column_config.NumberColumn("Cancelled",format="%d"),
            "Cancellation_Rate":st.column_config.NumberColumn("Cancellation",format="%.1f%%"),
        }
    )

st.divider()
st.caption(
    "Hypothesis dashboard • Source: areas, menu, orders, order_items and platforms datasets • "
    "Illustrative profit assumes AED 0 for food, labour, rent and utilities."
)


st.markdown("""<div class="premium-footer"><span>Franchise Intelligence · Expansion hypothesis</span><span>Data-driven decision support · Not an audited financial model</span></div>""", unsafe_allow_html=True)
