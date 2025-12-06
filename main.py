# app.py
import streamlit as st
from scoring import compute_scores
from api_fetch import search_cars_with_tavily
import pandas as pd
import altair as alt

st.set_page_config(page_title="Best-Fit Car Finder", layout="centered", initial_sidebar_state="expanded")

# Dark/Light mode toggle in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🏎 Baswheels Navigation")
    st.markdown("---")
    
    nav_choice = st.radio(
        "Choose Section:",
        ["🔍 Find Cars", "📊 Score Analysis", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Theme Settings")
    dark_mode = st.toggle("🌙 Dark Mode", value=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; margin-top:30px; font-size:12px; opacity:0.7;">
        <p>🚗 <b>Baswheels</b></p>
        <p>Powered by Tavily API</p>
    </div>
    """, unsafe_allow_html=True)

st.title("🚗 Baswheels - Best Fit Car Finder")
st.markdown("**Powered by Tavily API**")

# Apply theme based on toggle
if dark_mode:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0f24 0%, #1e2746 50%, #0f1629 100%);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #0d1220 0%, #1a2540 100%);
            border-right: 2px solid #00d5ff;
        }
        .stRadio > label {
            color: #e0e0e0 !important;
            font-weight: 600;
        }
        .stRadio [role="radio"] {
            accent-color: #00d5ff;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #00d5ff !important;
        }
        label, .stLabel {
            color: #ffffff !important;
            font-weight: 600;
        }
        [data-testid="stMarkdownContainer"] {
            color: #e0e0e0 !important;
        }
        .stSubheader {
            color: #00d5ff !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 50%, #f0f3f8 100%);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
            border-right: 2px solid #0066cc;
        }
        .stRadio > label {
            color: #1a1a1a !important;
            font-weight: 600;
        }
        .stRadio [role="radio"] {
            accent-color: #0066cc;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #0066cc !important;
        }
        label, .stLabel {
            color: #1a1a1a !important;
            font-weight: 600;
        }
        [data-testid="stMarkdownContainer"] {
            color: #333333 !important;
        }
        .stSubheader {
            color: #0066cc !important;
        }
    </style>
    """, unsafe_allow_html=True)


# -------------------------
# USER FORM
# -------------------------
with st.form("prefs"):
    st.subheader("Your preferences")

    col1, col2 = st.columns(2)

    with col1:
        min_price = st.number_input("Min price (PKR)", value=1000000, step=100000)
        max_price = st.number_input("Max price (PKR)", value=10000000, step=100000)
        new_used = st.selectbox("New or Used?", ["either", "new", "used"])

    with col2:
        fuel_type = st.selectbox("Fuel type", ["any", "petrol", "diesel", "hybrid", "ev"])
        purposes = st.multiselect(
            "Main purposes",
            ["commute", "family", "roadtrip", "fuel_saver", "luxury", "offroad"],
            default=["commute"]
        )

    st.subheader("Importance weights")
    colw1, colw2 = st.columns(2)

    with colw1:
        w_price = st.slider("Price importance", 0.0, 1.0, 0.30)
        w_fuel = st.slider("Fuel match importance", 0.0, 1.0, 0.15)
        w_new = st.slider("New/Used importance", 0.0, 1.0, 0.05)

    with colw2:
        w_purpose = st.slider("Purpose importance", 0.0, 1.0, 0.20)
        w_trunk = st.slider("Space importance", 0.0, 1.0, 0.10)
        w_econ = st.slider("Fuel economy importance", 0.0, 1.0, 0.10)
        w_rel = st.slider("Reliability importance", 0.0, 1.0, 0.10)

    submitted = st.form_submit_button("Find best cars")



# -------------------------
# ON SUBMIT
# -------------------------
if submitted:
    # Normalize weights
    wsum = w_price + w_fuel + w_new + w_purpose + w_trunk + w_econ + w_rel
    weights = {
        "price": w_price / wsum,
        "fuel": w_fuel / wsum,
        "new_used": w_new / wsum,
        "purpose": w_purpose / wsum,
        "trunk": w_trunk / wsum,
        "economy": w_econ / wsum,
        "reliability": w_rel / wsum,
    }

    user_prefs = {
        "min_price": float(min_price),
        "max_price": float(max_price),
        "fuel_type": fuel_type,
        "new_used": new_used,
        "purposes": purposes,
    }

    # Build query for API
    query = (
        f"best {fuel_type} cars in Pakistan priced between {min_price} and {max_price} PKR "
        f"for {', '.join(purposes)} use, with trunk space, specs and model details"
    )

    st.write("🔍 Fetching live results from Tavily API...")
    cars_list = search_cars_with_tavily(query)

    if not cars_list:
        st.error("❌ No results returned. Try expanding your filters.")
        st.stop()


    # ----------------------
    # Compute ranking scores
    # ----------------------
    results = compute_scores(cars_list, user_prefs, weights)


    # ----------------------
    # DISPLAY TOP RESULTS
    # ----------------------
    st.subheader("Top Results (Live API)")

    top_n = st.slider("How many top results to show:", 1, 10, 3)

    for idx, (car, score, breakdown, explanation) in enumerate(results[:top_n], start=1):
        st.markdown(f"### {idx}. {car['make_model']} — **{score}/100**")
        st.write(f"Price: {car['price_pkr']}")
        st.write(f"Fuel: {car['fuel_type']} — {car['fuel_economy_kmpl']} km/l")
        st.write(f"Trunk: {car['trunk_liters']} L | Seats: {car['seats']}")
        st.write(f"Notes: {car['notes']}")
        st.write(f"**Why:** {explanation}")

        with st.expander("Score Breakdown (Visual)"):
            st.write("Each score ranges from 0 to 1. Higher = better match.")

            labels = list(breakdown.keys())
            values = [float(breakdown[k]) for k in labels]

            df_break = pd.DataFrame({
                "Component": labels,
                "Score": values
            })

            # Color rules
            def color_rule(score):
                if score >= 0.75:
                    return "green"
                elif score >= 0.50:
                    return "gold"
                else:
                    return "red"

            df_break["Color"] = df_break["Score"].apply(color_rule)

            chart = (
                alt.Chart(df_break)
                .mark_bar()
                .encode(
                    x=alt.X("Score:Q", title="Score (0 to 1)"),
                    y=alt.Y("Component:N", sort="-x"),
                    color=alt.Color("Color:N", scale=None),
                    tooltip=["Component", "Score"]
                )
                .properties(height=300, width=500)
            )

            st.altair_chart(chart, use_container_width=True)

