import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Nassau Candy | Profitability Dashboard",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/massua.csv")
    
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
    
    df["Gross_Margin_%"] = (df["Gross Profit"] / df["Sales"]) * 100
    df["Profit_per_Unit"] = df["Gross Profit"] / df["Units"]
    df["Cost_to_Sales_Ratio"] = (df["Cost"] / df["Sales"]) * 100
    
    df["Order_Year"] = df["Order Date"].dt.year
    df["Order_Month"] = df["Order Date"].dt.month
    df["Order_Quarter"] = df["Order Date"].dt.quarter
    
    factory_mapping = {
        "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
        "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
        "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
        "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
        "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
        "Laffy Taffy": "Sugar Shack",
        "SweeTARTS": "Sugar Shack",
        "Nerds": "Sugar Shack",
        "Fun Dip": "Sugar Shack",
        "Fizzy Lifting Drinks": "Sugar Shack",
        "Everlasting Gobstopper": "Secret Factory",
        "Lickable Wallpaper": "Secret Factory",
        "Wonka Gum": "Secret Factory",
        "Hair Toffee": "The Other Factory",
        "Kazookles": "The Other Factory"
    }
    
    df["Factory"] = df["Product Name"].map(factory_mapping)
    
    return df

df = load_data()

# ============================================
# SIDEBAR FILTERS
# ============================================
st.sidebar.image("https://img.icons8.com/color/96/chocolate-bar.png", width=80)
st.sidebar.title("🍫 Nassau Candy")
st.sidebar.markdown("---")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

divisions = ["All"] + sorted(df["Division"].unique().tolist())
selected_division = st.sidebar.selectbox("🏢 Division", divisions)

factories = ["All"] + sorted(df["Factory"].dropna().unique().tolist())
selected_factory = st.sidebar.selectbox("🏭 Factory", factories)

margin_threshold = st.sidebar.slider("📊 Min Margin %", 0, 100, 0)

product_search = st.sidebar.text_input("🔍 Search Product")

st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ by Kshitij")

# ============================================
# APPLY FILTERS
# ============================================
filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= date_range[0]) &
        (filtered_df["Order Date"].dt.date <= date_range[1])
    ]

if selected_division != "All":
    filtered_df = filtered_df[filtered_df["Division"] == selected_division]

if selected_factory != "All":
    filtered_df = filtered_df[filtered_df["Factory"] == selected_factory]

filtered_df = filtered_df[filtered_df["Gross_Margin_%"] >= margin_threshold]

if product_search:
    filtered_df = filtered_df[
        filtered_df["Product Name"].str.contains(product_search, case=False, na=False)
    ]

# ============================================
# NAVIGATION
# ============================================
pages = [
    "📊 Executive Overview",
    "🍫 Product Profitability",
    "🏢 Division Performance",
    "🏭 Factory Analysis",
    "📈 Pareto Analysis",
    "💰 Cost & Margin Diagnostics",
    "📅 Trend Analysis"
]

selected_page = st.sidebar.radio("📌 Navigate", pages)

# ============================================
# PAGE 1: EXECUTIVE OVERVIEW
# ============================================
if selected_page == "📊 Executive Overview":
    
    st.title("📊 Executive Overview")
    st.markdown("### Nassau Candy Distributor — Profitability Dashboard")
    st.markdown("---")
    
    total_revenue = filtered_df["Sales"].sum()
    total_profit = filtered_df["Gross Profit"].sum()
    total_units = filtered_df["Units"].sum()
    overall_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    total_orders = filtered_df["Order ID"].nunique()
    avg_profit_per_unit = filtered_df["Profit_per_Unit"].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("📈 Total Gross Profit", f"${total_profit:,.2f}")
    col3.metric("📦 Total Units Sold", f"{total_units:,}")
    
    col4, col5, col6 = st.columns(3)
    col4.metric("📊 Overall Margin", f"{overall_margin:.2f}%")
    col5.metric("🧾 Total Orders", f"{total_orders:,}")
    col6.metric("💵 Avg Profit/Unit", f"${avg_profit_per_unit:.2f}")
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("🏆 Top 5 Products by Profit")
        top5 = filtered_df.groupby("Product Name", as_index=False).agg(
            {"Gross Profit": "sum"}
        ).sort_values(by="Gross Profit", ascending=False).head(5)
        
        fig1 = px.bar(
            top5, x="Gross Profit", y="Product Name",
            orientation="h", color="Gross Profit",
            color_continuous_scale="greens",
            title="Top 5 Products by Gross Profit"
        )
        fig1.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_right:
        st.subheader("🏢 Revenue by Division")
        div_rev = filtered_df.groupby("Division", as_index=False).agg(
            {"Sales": "sum"}
        ).sort_values(by="Sales", ascending=False)
        
        fig2 = px.pie(
            div_rev, values="Sales", names="Division",
            title="Revenue Distribution by Division",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig2.update_layout(height=350)
        st.plotly_chart(fig2, use_container_width=True)

# ============================================
# PAGE 2: PRODUCT PROFITABILITY
# ============================================
elif selected_page == "🍫 Product Profitability":
    
    st.title("🍫 Product Profitability Analysis")
    st.markdown("---")
    
    product_summary = filtered_df.groupby(["Product Name", "Division"], as_index=False).agg({
        "Sales": "sum",
        "Units": "sum",
        "Gross Profit": "sum",
        "Cost": "sum"
    })
    product_summary["Gross_Margin_%"] = (product_summary["Gross Profit"] / product_summary["Sales"]) * 100
    product_summary["Profit_per_Unit"] = product_summary["Gross Profit"] / product_summary["Units"]
    
    st.subheader("🏆 Product Margin Leaderboard")
    leaderboard = product_summary.sort_values(by="Gross Profit", ascending=False)
    st.dataframe(
        leaderboard.style.format({
            "Sales": "${:,.2f}",
            "Gross Profit": "${:,.2f}",
            "Cost": "${:,.2f}",
            "Gross_Margin_%": "{:.2f}%",
            "Profit_per_Unit": "${:.2f}"
        }),
        use_container_width=True
    )
    
    st.markdown("---")
    
    st.subheader("📊 Product Quadrant Analysis")
    
    sales_median = product_summary["Sales"].median()
    margin_median = product_summary["Gross_Margin_%"].median()
    
    def assign_quadrant(row):
        if row["Sales"] >= sales_median and row["Gross_Margin_%"] >= margin_median:
            return "⭐ STAR"
        elif row["Sales"] >= sales_median and row["Gross_Margin_%"] < margin_median:
            return "⚠️ DANGER"
        elif row["Sales"] < sales_median and row["Gross_Margin_%"] >= margin_median:
            return "💎 HIDDEN GEM"
        else:
            return "❌ DEAD WEIGHT"
    
    product_summary["Quadrant"] = product_summary.apply(assign_quadrant, axis=1)
    
    color_map = {
        "⭐ STAR": "green",
        "⚠️ DANGER": "red",
        "💎 HIDDEN GEM": "blue",
        "❌ DEAD WEIGHT": "gray"
    }
    
    fig3 = px.scatter(
        product_summary,
        x="Sales",
        y="Gross_Margin_%",
        color="Quadrant",
        size="Gross Profit",
        hover_name="Product Name",
        color_discrete_map=color_map,
        title="Product Quadrant: Sales vs Margin (Bubble = Profit)",
        labels={"Sales": "Total Sales ($)", "Gross_Margin_%": "Gross Margin %"}
    )
    
    fig3.add_hline(y=margin_median, line_dash="dash", line_color="black", opacity=0.5)
    fig3.add_vline(x=sales_median, line_dash="dash", line_color="black", opacity=0.5)
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True)

# ============================================
# PAGE 3: DIVISION PERFORMANCE
# ============================================
elif selected_page == "🏢 Division Performance":
    
    st.title("🏢 Division Performance Dashboard")
    st.markdown("---")
    
    division_summary = filtered_df.groupby("Division", as_index=False).agg({
        "Sales": "sum",
        "Units": "sum",
        "Gross Profit": "sum",
        "Cost": "sum"
    })
    division_summary["Gross_Margin_%"] = (division_summary["Gross Profit"] / division_summary["Sales"]) * 100
    division_summary["Profit_Contribution_%"] = (division_summary["Gross Profit"] / division_summary["Gross Profit"].sum()) * 100
    
    for _, row in division_summary.iterrows():
        with st.expander(f"🏢 {row['Division']} Division", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Revenue", f"${row['Sales']:,.2f}")
            c2.metric("Profit", f"${row['Gross Profit']:,.2f}")
            c3.metric("Margin", f"{row['Gross_Margin_%']:.2f}%")
            c4.metric("Profit Share", f"{row['Profit_Contribution_%']:.2f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig4 = px.bar(
            division_summary,
            x="Division",
            y=["Sales", "Gross Profit"],
            barmode="group",
            title="Revenue vs Profit by Division",
            color_discrete_sequence=["#3498db", "#2ecc71"]
        )
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        fig5 = px.bar(
            division_summary,
            x="Division",
            y="Gross_Margin_%",
            color="Division",
            title="Gross Margin % by Division",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig5.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)
        
        # ============================================
# PAGE 4: FACTORY ANALYSIS
# ============================================
elif selected_page == "🏭 Factory Analysis":
    
    st.title("🏭 Factory Performance Analysis")
    st.markdown("---")
    
    factory_summary = filtered_df.groupby("Factory", as_index=False).agg({
        "Sales": "sum",
        "Units": "sum",
        "Gross Profit": "sum",
        "Cost": "sum"
    })
    factory_summary["Gross_Margin_%"] = (factory_summary["Gross Profit"] / factory_summary["Sales"]) * 100
    factory_summary["Profit_Contribution_%"] = (factory_summary["Gross Profit"] / factory_summary["Gross Profit"].sum()) * 100
    
    st.subheader("📋 Factory Summary Table")
    st.dataframe(
        factory_summary.sort_values(by="Gross Profit", ascending=False).style.format({
            "Sales": "${:,.2f}",
            "Gross Profit": "${:,.2f}",
            "Cost": "${:,.2f}",
            "Gross_Margin_%": "{:.2f}%",
            "Profit_Contribution_%": "{:.2f}%"
        }),
        use_container_width=True
    )
    
    st.markdown("---")
    
    st.subheader("🗺️ Factory Locations")
    
    factory_coords = pd.DataFrame({
        "Factory": ["Lot's O' Nuts", "Wicked Choccy's", "Sugar Shack", "Secret Factory", "The Other Factory"],
        "lat": [32.881893, 32.076176, 48.11914, 41.446333, 35.1175],
        "lon": [-111.768036, -81.088371, -96.18115, -90.565487, -89.971107]
    })
    
    factory_map = factory_summary.merge(factory_coords, on="Factory")
    
    fig6 = px.scatter_mapbox(
        factory_map,
        lat="lat",
        lon="lon",
        size="Gross Profit",
        color="Gross_Margin_%",
        hover_name="Factory",
        hover_data=["Sales", "Gross Profit", "Gross_Margin_%"],
        color_continuous_scale="RdYlGn",
        size_max=30,
        zoom=3,
        title="Factory Locations (Size = Profit, Color = Margin)"
    )
    fig6.update_layout(mapbox_style="open-street-map", height=500)
    st.plotly_chart(fig6, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig7 = px.bar(
            factory_summary.sort_values(by="Gross Profit", ascending=True),
            x="Gross Profit", y="Factory",
            orientation="h",
            color="Gross_Margin_%",
            color_continuous_scale="RdYlGn",
            title="Factory Profit & Margin"
        )
        fig7.update_layout(height=400)
        st.plotly_chart(fig7, use_container_width=True)
    
    with col2:
        fig8 = px.pie(
            factory_summary,
            values="Profit_Contribution_%",
            names="Factory",
            title="Profit Contribution by Factory",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig8.update_layout(height=400)
        st.plotly_chart(fig8, use_container_width=True)

# ============================================
# PAGE 5: PARETO ANALYSIS
# ============================================
elif selected_page == "📈 Pareto Analysis":
    
    st.title("📈 Profit Concentration (Pareto) Analysis")
    st.markdown("---")
    
    product_profit = filtered_df.groupby("Product Name", as_index=False).agg(
        {"Gross Profit": "sum", "Sales": "sum"}
    ).sort_values(by="Gross Profit", ascending=False).reset_index(drop=True)
    
    product_profit["Cumulative_Profit_%"] = (
        product_profit["Gross Profit"].cumsum() / product_profit["Gross Profit"].sum()
    ) * 100
    
    product_profit["Product_Count"] = product_profit.index + 1
    products_80 = product_profit[product_profit["Cumulative_Profit_%"] <= 80].shape[0] + 1
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Products", len(product_profit))
    col2.metric("🎯 Products for 80% Profit", products_80)
    col3.metric("📊 Concentration Ratio", f"{products_80}/{len(product_profit)}")
    
    st.markdown("---")
    
    fig9 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig9.add_trace(
        go.Bar(
            x=product_profit["Product Name"],
            y=product_profit["Gross Profit"],
            name="Gross Profit",
            marker_color="skyblue"
        ),
        secondary_y=False
    )
    
    fig9.add_trace(
        go.Scatter(
            x=product_profit["Product Name"],
            y=product_profit["Cumulative_Profit_%"],
            name="Cumulative Profit %",
            marker_color="red",
            mode="lines+markers"
        ),
        secondary_y=True
    )
    
    fig9.add_hline(y=80, line_dash="dash", line_color="green",
                   annotation_text="80% Threshold", secondary_y=True)
    
    fig9.update_layout(
        title="Pareto Analysis - Product Contribution to Total Profit",
        height=500,
        xaxis_tickangle=-45
    )
    fig9.update_yaxes(title_text="Gross Profit ($)", secondary_y=False)
    fig9.update_yaxes(title_text="Cumulative Profit %", secondary_y=True)
    
    st.plotly_chart(fig9, use_container_width=True)
    
    st.subheader("📋 Detailed Pareto Table")
    st.dataframe(
        product_profit.style.format({
            "Gross Profit": "${:,.2f}",
            "Sales": "${:,.2f}",
            "Cumulative_Profit_%": "{:.2f}%"
        }),
        use_container_width=True
    )

# ============================================
# PAGE 6: COST & MARGIN DIAGNOSTICS
# ============================================
elif selected_page == "💰 Cost & Margin Diagnostics":
    
    st.title("💰 Cost & Margin Diagnostics")
    st.markdown("---")
    
    product_cost = filtered_df.groupby(["Product Name", "Division"], as_index=False).agg({
        "Sales": "sum", "Cost": "sum", "Gross Profit": "sum"
    })
    product_cost["Gross_Margin_%"] = (product_cost["Gross Profit"] / product_cost["Sales"]) * 100
    product_cost["Cost_to_Sales_%"] = (product_cost["Cost"] / product_cost["Sales"]) * 100
    
    def margin_risk(margin):
        if margin < 20:
            return "🚨 Critical"
        elif margin < 40:
            return "⚠️ Watch"
        elif margin < 60:
            return "🟡 Moderate"
        else:
            return "✅ Healthy"
    
    product_cost["Risk_Flag"] = product_cost["Gross_Margin_%"].apply(margin_risk)
    
    risk_counts = product_cost["Risk_Flag"].value_counts()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("✅ Healthy", risk_counts.get("✅ Healthy", 0))
    col2.metric("🟡 Moderate", risk_counts.get("🟡 Moderate", 0))
    col3.metric("⚠️ Watch", risk_counts.get("⚠️ Watch", 0))
    col4.metric("🚨 Critical", risk_counts.get("🚨 Critical", 0))
    
    st.markdown("---")
    
    st.subheader("📊 Cost vs Sales Scatter")
    
    risk_color_map = {
        "🚨 Critical": "red",
        "⚠️ Watch": "orange",
        "🟡 Moderate": "gold",
        "✅ Healthy": "green"
    }
    
    fig10 = px.scatter(
        product_cost,
        x="Cost",
        y="Sales",
        color="Risk_Flag",
        size="Gross Profit",
        hover_name="Product Name",
        color_discrete_map=risk_color_map,
        title="Cost vs Sales (Size = Profit, Color = Risk)",
        labels={"Cost": "Total Cost ($)", "Sales": "Total Sales ($)"}
    )
    fig10.update_layout(height=500)
    st.plotly_chart(fig10, use_container_width=True)
    
    st.subheader("📊 Margin Risk by Product")
    sorted_cost = product_cost.sort_values(by="Gross_Margin_%", ascending=True)
    
    fig11 = px.bar(
        sorted_cost,
        x="Gross_Margin_%",
        y="Product Name",
        orientation="h",
        color="Risk_Flag",
        color_discrete_map=risk_color_map,
        title="Gross Margin % by Product (Risk Flagged)"
    )
    fig11.add_vline(x=20, line_dash="dash", line_color="red")
    fig11.add_vline(x=40, line_dash="dash", line_color="orange")
    fig11.add_vline(x=60, line_dash="dash", line_color="gold")
    fig11.update_layout(height=500)
    st.plotly_chart(fig11, use_container_width=True)
    
    st.subheader("📋 Risk Analysis Table")
    st.dataframe(
        product_cost.sort_values(by="Gross_Margin_%").style.format({
            "Sales": "${:,.2f}",
            "Cost": "${:,.2f}",
            "Gross Profit": "${:,.2f}",
            "Gross_Margin_%": "{:.2f}%",
            "Cost_to_Sales_%": "{:.2f}%"
        }),
        use_container_width=True
    )

# ============================================
# PAGE 7: TREND ANALYSIS
# ============================================
elif selected_page == "📅 Trend Analysis":
    
    st.title("📅 Time Trend Analysis")
    st.markdown("---")
    
    monthly = filtered_df.groupby(
        [filtered_df["Order Date"].dt.to_period("M").astype(str)],
        as_index=False
    ).agg({
        "Sales": "sum",
        "Gross Profit": "sum",
        "Units": "sum"
    })
    monthly.columns = ["Month", "Sales", "Gross Profit", "Units"]
    monthly["Gross_Margin_%"] = (monthly["Gross Profit"] / monthly["Sales"]) * 100
    monthly = monthly.sort_values(by="Month")
    
    st.subheader("📈 Monthly Sales Trend")
    fig12 = px.line(
        monthly, x="Month", y="Sales",
        markers=True,
        title="Monthly Sales Trend",
        labels={"Sales": "Sales ($)"}
    )
    fig12.update_layout(height=350)
    st.plotly_chart(fig12, use_container_width=True)
    
    st.subheader("📈 Monthly Profit Trend")
    fig13 = px.line(
        monthly, x="Month", y="Gross Profit",
        markers=True,
        title="Monthly Gross Profit Trend",
        color_discrete_sequence=["green"]
    )
    fig13.update_layout(height=350)
    st.plotly_chart(fig13, use_container_width=True)
    
    st.subheader("📈 Monthly Margin Trend")
    fig14 = px.line(
        monthly, x="Month", y="Gross_Margin_%",
        markers=True,
        title="Monthly Gross Margin % Trend",
        color_discrete_sequence=["red"]
    )
    fig14.update_layout(height=350, yaxis_range=[0, 100])
    st.plotly_chart(fig14, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 Quarterly Performance")
    
    quarterly = filtered_df.groupby(
        ["Order_Year", "Order_Quarter"], as_index=False
    ).agg({
        "Sales": "sum",
        "Gross Profit": "sum"
    })
    quarterly["Quarter_Label"] = quarterly["Order_Year"].astype(str) + " Q" + quarterly["Order_Quarter"].astype(str)
    quarterly["Gross_Margin_%"] = (quarterly["Gross Profit"] / quarterly["Sales"]) * 100
    
    fig15 = px.bar(
        quarterly,
        x="Quarter_Label",
        y=["Sales", "Gross Profit"],
        barmode="group",
        title="Quarterly Revenue vs Profit",
        color_discrete_sequence=["#3498db", "#2ecc71"]
    )
    fig15.update_layout(height=400)
    st.plotly_chart(fig15, use_container_width=True)