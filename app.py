import streamlit as st
import pandas as pd
import altair as alt
from explore import load_and_prepare

st.set_page_config(page_title = "Transactions Dashboard", layout = "wide")
st.title("Transactions Dashboard")

@st.cache_data
def get_data():
    return load_and_prepare("financial_transactions.csv")

df = get_data()

# Filter tab on left sidebar
st.sidebar.header("Filters")

min_date = df['date'].min() if 'date' in df.columns else None
max_date = df['date'].max() if 'date' in df.columns else None
date_range = st.sidebar.date_input("Date range", [min_date, max_date])
if isinstance(date_range, (list, tuple)):
    if len(date_range) == 2:
        start, end = map(pd.to_datetime, date_range)
    elif len(date_range) == 1:
        start = end = pd.to_datetime(date_range[0])
    else:
        start, end = pd.to_datetime(min_date), pd.to_datetime(max_date)
else:
    start = end = pd.to_datetime(date_range)


category_options = df['category'].unique().tolist() if 'category' in df.columns else []
selected_cat = st.sidebar.multiselect("Category", options = category_options, default=category_options)

# Filter data according to selection by user
df_filtered = df.copy()
if 'date' in df.columns:
    df_filtered = df_filtered[(df_filtered['date'] >= start) & (df_filtered['date'] <= end + pd.Timedelta(days = 1))]
if 'category' in df.columns:
    if selected_cat:
        df_filtered = df_filtered[df_filtered['category'].isin(selected_cat)]
    else:
        df_filtered = df_filtered.iloc[0:0]

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trends", "Merchant & Payment", "Data Table"])

# Different tab functionalities
with tab1:
    st.subheader("Summary overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Transactions", len(df_filtered))
    col2.metric("Total amount", f"{df_filtered['amount'].sum():,.2f}")  
    df_filtered['month'] = df_filtered['date'].dt.to_period('M')

    monthly_avg = df_filtered.groupby('month')['amount'].sum().mean()

    col3.metric("Average per month", f"{monthly_avg:,.2f}")

    if 'category' in df_filtered.columns:
        by_category = df_filtered.groupby('category')['amount'].sum().reset_index().sort_values('amount', ascending = False)
        bar = alt.Chart(by_category).mark_bar().encode(
            x = 'amount:Q',
            y = alt.Y('category:N', sort = '-x'),
            tooltip = ['category', 'amount']
        ).properties(title = 'Total spending by Category')
        st.altair_chart(bar, use_container_width = True)

    if not by_category.empty:
        top_category = by_category.iloc[0]['category']
        st.markdown(f"**Most spending** occurs in **{top_category}** category.")

with tab2:
    st.subheader("Spending trends over Time")

    view = st.radio("View by:", ["Daily", "Weekly", "Monthly"], horizontal = True)

    if view == "Weekly":
        time_filtered = df_filtered.set_index('date').resample('W')['amount'].sum().reset_index()
    elif view == "Monthly":
        time_filtered = df_filtered.set_index('date').resample('M')['amount'].sum().reset_index()
    else:
        time_filtered = df_filtered.set_index('date').resample('D')['amount'].sum().reset_index()

    line = alt.Chart(time_filtered).mark_line(point = True).encode(
        x = 'date:T',
        y = 'amount:Q',
        tooltip = ['date:T', 'amount:Q']
    ).properties(title = f'{view} total amount trend')
    st.altair_chart(line, use_container_width = True)

    time_filtered_category = df_filtered.groupby([pd.Grouper(key = 'date', freq = 'W'), 'category'])['amount'].sum().reset_index()

    top_categories = df_filtered.groupby('category')['amount'].sum().nlargest(5).index
    time_filtered_category = time_filtered_category[time_filtered_category['category'].isin(top_categories)]

    area = alt.Chart(time_filtered_category).mark_area(opacity = 0.7).encode(
        x = 'date:T',
        y = 'amount:Q',
        color = 'category:N',
        tooltip = ['date:T', 'category', 'amount:Q']
    ).properties(title = 'Weekly spending by Top 5 Categories')
    st.altair_chart(area, use_container_width = True)

with tab3:
    st.subheader("Merchant & Payment Info")

    by_merchant = df_filtered.groupby('merchant')['amount'].sum().reset_index().sort_values('amount', ascending=False).head(10)
    merchant_bar = alt.Chart(by_merchant).mark_bar().encode(
        x = 'amount:Q',
        y = alt.Y('merchant:N', sort = '-x'),
        tooltip = ['merchant', 'amount']
    ).properties(title = 'Top 10 Merchants by total spend')
    st.altair_chart(merchant_bar, use_container_width = True)


    by_payment = df_filtered.groupby('payment_method')['amount'].sum().reset_index()
    pie = alt.Chart(by_payment).mark_arc(innerRadius = 70).encode(
        theta = 'amount:Q',
        color = 'payment_method:N',
        tooltip = ['payment_method', 'amount']
    ).properties(title = 'Payment method breakdown')
    st.altair_chart(pie, use_container_width = True)

    st.subheader("Category breakdown by Merchant")
    selected_category = st.selectbox("Select category for more information", category_options)
    if selected_category:
        subset = df_filtered[df_filtered['category'] == selected_category]
        by_merchant_detail = subset.groupby('merchant')['amount'].sum().reset_index().sort_values('amount', ascending = False)
        st.bar_chart(by_merchant_detail, x = 'merchant', y= 'amount')

with tab4:
    st.subheader("Filtered Data Table")

    negatives = df_filtered[df_filtered['amount'] < 0]
    if not negatives.empty:
        st.warning(f"{len(negatives)} transactions with negative amount detected.")
        st.dataframe(negatives)

    st.data_editor(
        df_filtered[['date', 'merchant', 'amount', 'category', 'payment_method', 'account_type', 'transaction_type', 'description']].head(300),
        use_container_width = True,
        height = 400
    )

    csv = df_filtered.to_csv(index = False).encode('utf-8')
    st.download_button("Download filtered CSV", csv, "filtered_transactions.csv", "text/csv")
