# import redshift_connector
# conn = redshift_connector.connect(
#      host='poc-redshift-free-trial.cir6kkgprzvy.ap-southeast-1.redshift.amazonaws.com',
#      database='dev',
#      port=5439,
#      user='awsuser',
#      password='RGYcH3Yoyqo5fKrk'
#   )
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
#emoji: https://www.webfx.com/tools/emojiemoji-cheat-sheet/
conn_1 = "redshift://awsuser:RGYcH3Yoyqo5fKrk@poc-redshift-free-trial.cir6kkgprzvy.ap-southeast-1.redshift.amazonaws.com:5439/dev"


df = pd.read_sql_query("select * from  dwh_snowplow.fact_events_demo_margin_sp",conn_1)
# print(df)
# Cấu hình trang
st.set_page_config(
    page_title="Dashboard Demo Margin",
    page_icon=":money_bag:",
    layout="wide"
)
st.title(":bar_chart: Demo Margin Dashboard")
## Chart 1: Số người sử dụng demo margin

# Lọc dữ liệu theo điều kiện
# filtered_df = df[(df['is_from_demo_margin'].isnull()) | (df['is_from_demo_margin'] == 'true')]
filtered_df=df[df['is_from_demo_margin']!='false']

# Tính toán tổng số khách hàng (distinct investor_id)
total_customers = filtered_df['investor_id'].nunique()

# Chart 2: Tỷ lệ khách hàng đặt mua cổ phiếu trên tổng số khách hàng vào trang demo margin
create_deal_count = df[(df['funnel_step'] == '04.Create_Deal') & (df['is_from_demo_margin'] != 'false')]['investor_id'].nunique()
discover_count = df[(df['funnel_step'] == '01.Discover')]['investor_id'].nunique()
# Tránh chia cho 0
conversion_rate = create_deal_count / discover_count if discover_count > 0 else 0

#Chart 3:  Tính toán số lượng khách hàng duy nhất theo từng bước funnel
funnel_data = (
    df.groupby('funnel_step')['investor_id']
    .nunique()
    .reset_index()
    .rename(columns={'investor_id': 'unique_customers'})
    .sort_values('funnel_step')  # Sắp xếp theo thứ tự bước
)
# Tạo Funnel Chart bằng Plotly
fig_funnel = px.funnel(
    funnel_data,
    x='unique_customers',
    y='funnel_step',
    title="Funnel Chart: Số lượng khách hàng theo từng bước",
    labels={'unique_customers': 'Số lượng khách hàng', 'funnel_step': 'Bước Funnel'},
    color_discrete_sequence=px.colors.sequential.RdBu  # Tùy chọn màu sắc
)
#Chart 4: Bar chart 
# Tạo biểu đồ cột bằng Plotly

# Chuyển đổi cột root_time sang datetime và tạo root_date
filtered_df['root_time'] = pd.to_datetime(filtered_df['root_time'])
filtered_df['root_date'] = filtered_df['root_time'].dt.date  # Lấy ngày từ root_time

# Nhóm dữ liệu theo root_date và funnel_step, đếm số lượng khách hàng duy nhất
time_funnel_data = (
    filtered_df.groupby(['root_date', 'funnel_step'])['investor_id']
    .nunique()
    .reset_index()
    .rename(columns={'investor_id': 'unique_customers'})
)
fig_bar = px.bar(
    time_funnel_data,
    x='root_date',
    y='unique_customers',
    color='funnel_step',  # Phân biệt theo funnel_step
    title="Số lượng khách hàng theo thời gian và Funnel Step",
    labels={
        'root_date': 'Thời gian',
        'unique_customers': 'Số lượng khách hàng',
        'funnel_step': 'Bước Funnel'
    },
    barmode='group',  # Hiển thị dạng cột nhóm
    text='unique_customers',  # Hiển thị số liệu trên cột
    color_discrete_sequence=px.colors.sequential.RdBu  # Tùy chọn màu sắc
)
#Chart 5: 
donut_data = (
    df.groupby('place')['root_id']
    .nunique()
    .reset_index()
    .rename(columns={'root_id': 'Khách hàng'})  # Sắp xếp theo thứ tự bước
)
fig_pie = px.pie(donut_data, 
    names='place', 
    values='Khách hàng', 
    hole=0.3,  # Để tạo kiểu donut (giảm đường kính của phần giữa)
    title="Số lượt vào trang Discover theo các entry point"
)
#Chart 6: 
# Tạo dữ liệu cho Area chart, nhóm theo place và root_date
area_data = (
    filtered_df.groupby(['root_date', 'place'])['root_id']
    .nunique()
    .reset_index()
    .rename(columns={'root_id': 'Khách hàng'})  # Đổi tên cột
)

# Tạo Area Chart
fig_area = px.area(area_data, 
    x='root_date',  # Trục X: Thời gian (root_date)
    y='Khách hàng',  # Trục Y: Số lượng khách hàng
    color='place',  # Màu sắc phân biệt theo place
    title="Số lượng khách hàng theo địa điểm và thời gian",
    labels={
        'root_date': 'Thời gian',
        'Khách hàng': 'Số lượng khách hàng',
        'place': 'Địa điểm'
    }
)

             
# Hiển thị biểu đồ trong ứng dụng Streamlit
####
tab1, tab2 = st.tabs(["Charts", "Data"])
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        # Hiển thị Big Number
        st.metric(label="Tổng số người dùng", value=total_customers)
    with col2:
        st.metric(
        label="Tỷ lệ chuyển đổi từ Discover đến Create_Deal (Demo Margin)",
        value=f"{conversion_rate:.2%}"  # Hiển thị dưới dạng phần trăm
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.plotly_chart(fig_pie)
    st.plotly_chart(fig_area)
with tab2:
    st.dataframe(filtered_df)
# Tiêu đề
if __name__ == '__main__':
    pass