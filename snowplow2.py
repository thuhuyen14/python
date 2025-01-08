import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os


# Cấu hình trang
st.set_page_config(
    page_title="Dashboard Snowplow",
    page_icon=":bar_chart:",
    layout="wide"
)

# Tiêu đề
st.title(":bar_chart: Snowplow Dashboard")
st.markdown("##")

st.cache_data.clear()  # Xóa cache dữ liệu
# Đường dẫn file mặc định
default_file = r"D:\\VSCode_Python\\event_data.csv"

# Đọc file CSV mặc định
try:
    df = pd.read_csv(default_file)
    st.write("Using default file:", default_file)  # Hiển thị thông báo file mặc định được sử dụng
except FileNotFoundError:
    st.error(f"File not found: {default_file}")
    st.stop()  # Dừng ứng dụng nếu file không tồn tại


# Xử lý dữ liệu thời gian
df["event_time"] = pd.to_datetime(df["event_time"], errors='coerce')
df['event_date'] = df['event_time'].dt.date

# Date range picker
col1, col2 = st.columns(2)
startDate = pd.to_datetime(df["event_time"]).min()
endDate = pd.to_datetime(df["event_time"]).max()
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

# Filter dữ liệu theo ngày
# df = df[(df["event_time"] >= date1) & (df["event_time"] <= date2)].copy()

# Sidebar filters
st.sidebar.header("Filter event:")
event_name = st.sidebar.multiselect(
    "Chọn event:",
    options=df["event_name"].unique(),
    default=df["event_name"].unique()
)
platform = st.sidebar.multiselect(
    "Chọn platform:",
    options=df["platform"].unique(),
    default=df["platform"].unique()
)

# Apply filters
df_selection = df.query("event_name == @event_name & platform == @platform")

# Hiển thị thông tin về filters đã được áp dụng
st.markdown("### Filters Applied:")
col1, col2 = st.columns(2)
with col1:
    st.write("Selected Events:", ", ".join(event_name) if event_name else "All")
with col2:
    st.write("Selected Platforms:", ", ".join(platform) if platform else "All")

# Hiển thị số lượng records sau khi filter
st.info(f"Showing {len(df_selection)} records after filtering")

# Xử lý dữ liệu cho Bar Chart
grouped_data = (
    df_selection.groupby(["event_date", "platform"], as_index=False)
    .agg({"event_id": "nunique"})
    .rename(columns={"event_id": "số events"})
)
# Xử lý dữ liệu cho Line Chart (đếm event_name theo ngày và theo platform)
line_data = (
    df_selection.groupby(["event_date", "platform"], as_index=False)
    .agg({"event_name": "count"})
    .rename(columns={"event_name": "số events"})
)



# Xử lý dữ liệu cho Sankey Chart Events
event_counts = df_selection.groupby(["event_name", "next_event_name"]).size().reset_index(name="value")
event_counts = event_counts[event_counts['value'] >= 3]
event_counts = event_counts[event_counts["event_name"] != event_counts["next_event_name"]]

# Loại bỏ các event không mong muốn
excluded_events = ['page_ping', 'screen_viewed', 'application_background', 
                  'application_foreground', 'page_view']
filtered_event_counts = event_counts[
    ~event_counts["event_name"].isin(excluded_events) & 
    ~event_counts["next_event_name"].isin(excluded_events)
]

# Xử lý dữ liệu cho Sankey Chart Screens
screen_data = df_selection.groupby(["screen_name", "next_screen_name"]).size().reset_index(name="value")
screen_data = screen_data[screen_data['value'] >= 3]
screen_data = screen_data[screen_data["screen_name"] != screen_data["next_screen_name"]]

# Layout tabs
tab1, tab2 = st.tabs(["Charts", "Data"])

with tab1:
    # Bar Chart
    
    fig_bar = px.bar(
        grouped_data,
        x="event_date",
        y="số events",
        color="platform",
        labels={"event_date": "Event Date", "số events": "Number of Events"}
    )
    fig_bar.update_layout(
        xaxis_title="Event Date",
        yaxis_title="Number of Events",
        font_size=15,
        xaxis=dict(
            tickformat="%Y-%m-%d",
            tickangle=45
        )
    )

    #Line chart
    fig_line = px.line(
        line_data,
        x="event_date",
        y="số events",
        color="platform",
        labels={"event_date": "Event Date", "số events": "Number of Events"}
    )
    fig_line.update_layout(
        xaxis_title="Event Date",
        yaxis_title="Number of Events",
        font_size=15,
        xaxis=dict(
            tickformat="%Y-%m-%d",
            tickangle=45
        )
    )
    # Hiển thị cả hai biểu đồ
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Bar Chart: Số lượng event theo platform")
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.subheader("Line Chart: Số lượng event theo ngày và platform")
        st.plotly_chart(fig_line, use_container_width=True)

        # Xử lý dữ liệu cho bar chart (số lượng event_name mỗi ngày)
    event_count_per_day = df_selection.groupby(['event_date', 'event_name']).size().reset_index(name='event_count')

    # Xử lý dữ liệu cho line chart (số lượng loại event_name mỗi ngày)
    unique_event_per_day = df_selection.groupby('event_date')['event_name'].nunique().reset_index(name='unique_event_count')

    # Vẽ mixed chart với cột chồng (stacked bar chart) cho số lượng event_name và đường cho số loại event_name
    fig = go.Figure()

    # Cột chồng: Đếm số lượng từng event_name mỗi ngày
    for event_name in event_count_per_day['event_name'].unique():
        filtered_event = event_count_per_day[event_count_per_day['event_name'] == event_name]
        fig.add_trace(go.Bar(
            x=filtered_event['event_date'],
            y=filtered_event['event_count'],
            name=event_name,
            opacity=0.7  # Độ mờ để cột không quá dày
        ))

    # Đường: Đếm số loại event_name mỗi ngày
    fig.add_trace(go.Scatter(
        x=unique_event_per_day['event_date'],
        y=unique_event_per_day['unique_event_count'],
        mode='lines+markers',
        name='Số loại sự kiện',
        line=dict(color='black', width=2),
        marker=dict(size=5)
    ))

    # Cập nhật layout
    fig.update_layout(
        barmode='stack',  # Cột chồng
        title="Mixed Chart: Số lượng sự kiện và số loại sự kiện theo ngày",
        xaxis_title="Ngày",
        yaxis_title="Số lượng sự kiện",
        legend_title="Sự kiện",
        template="plotly",
        height=600,
    )

    # Hiển thị biểu đồ trong streamlit
    st.plotly_chart(fig, use_container_width=True)


    # Sankey Chart Events
    st.subheader("Sankey Diagram for Events")
    st.caption("Note: Chart này chỉ lấy các cặp event - next_event có số lượng lớn nhất để chart đỡ rối")
    
    # Tạo Sankey chart cho Events
    source = filtered_event_counts["event_name"]
    target = filtered_event_counts["next_event_name"]
    value = filtered_event_counts["value"]
    
    all_nodes = list(set(source).union(set(target)))
    node_map = {node: idx for idx, node in enumerate(all_nodes)}
    
    source_idx = filtered_event_counts["event_name"].map(node_map)
    target_idx = filtered_event_counts["next_event_name"].map(node_map)
    
    fig_sankey = go.Figure(go.Sankey(
        node=dict(
            pad=30,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes
        ),
        link=dict(
            source=source_idx,
            target=target_idx,
            value=value
        )
    ))
    fig_sankey.update_layout(height=600)
    st.plotly_chart(fig_sankey, use_container_width=True, key="sankey_events")

    # Sankey Chart Screens
    st.subheader("Sankey Diagram for Screen Transitions")
    top_screen_data = screen_data.nlargest(20, 'value')
    col_1, col_2 = st.columns(2)
    with col_1:
    # Lấy top 20 screen transitions
        st.write("Dữ liệu screen_name ban đầu",screen_data)
    with col_2:
        st.write("Lọc 20 screen_name có số lượng event lớn nhất:", top_screen_data)

    source = top_screen_data["screen_name"]
    target = top_screen_data["next_screen_name"]
    value = top_screen_data["value"]
    
    all_nodes = list(set(source).union(set(target)))
    node_map = {node: idx for idx, node in enumerate(all_nodes)}
    
    source_idx = top_screen_data["screen_name"].map(node_map)
    target_idx = top_screen_data["next_screen_name"].map(node_map)
    
    fig_screen = go.Figure(go.Sankey(
        node=dict(
            pad=30,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes
        ),
        link=dict(
            source=source_idx,
            target=target_idx,
            value=value
        )
    ))
    fig_screen.update_layout(height=600)
    st.plotly_chart(fig_screen, use_container_width=True, key="sankey_screens")

with tab2:
    st.subheader("Raw Data")
    st.dataframe(df_selection)
    
    # Download button
    csv = df_selection.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download CSV",
        csv,
        "data.csv",
        "text/csv",
        key='download-csv'
    )

if __name__ == '__main__':
    pass