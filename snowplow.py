import dash
from dash import dcc, html, dash_table
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc  # Import Bootstrap Components

# Load DataFrame from a CSV file
file_path = 'D:\\sqllab_query_dwh_snowplowfact_events_l3d_sp_20250105T170411.csv'
df = pd.read_csv(file_path, encoding='utf-8')

#Xử lý dữ liệu Bar Chart
df['event_time'] = pd.to_datetime(df['event_time'], format='ISO8601', errors='coerce')
  # Chuyển event_time sang datetime
df['event_date'] = df['event_time'].dt.date          # Lấy ngày từ event_time

# Nhóm dữ liệu giống logic SQL
grouped_data = (
    df.groupby(["event_date", "platform"], as_index=False)
    .agg({"event_id": "nunique"})  # Đếm số lượng event_id duy nhất
    .rename(columns={"event_id": "số events"})
)
print(grouped_data)


#Xử lý dữ liệu Sankey_Chart_1
#Transform data: đếm số event_id
event_counts = df.groupby(["event_name", "next_event_name"]).size().reset_index(name="value")
event_counts = event_counts[event_counts['value'] >= 3] # Lọc sự kiện có giá trị (đếm) >= 3
event_counts = event_counts[event_counts["event_name"] != event_counts["next_event_name"]] # Lọc bỏ các hàng mà event_name = next_event_name
# print(event_counts) #In ra xem thử kết quả trong log

# Tính tổng số sự kiện
total_value = event_counts['value'].sum()

# Thêm hàng "Total" vào dataframe
total_row = pd.DataFrame({
    "event_name": ["Total"], 
    "next_event_name": [None], 
    "value": [total_value]
})


event_counts = pd.concat([event_counts, total_row], ignore_index=True)


# Lọc bỏ hàng "Total" khi chuẩn bị dữ liệu cho Sankey chart
sankey_data = event_counts[event_counts["event_name"] != "Total"]

print(sankey_data)

# Thêm code này vào phần xử lý dữ liệu ban đầu để đảm bảo có cột platform trong các dataframe Sankey
sankey_data = pd.merge(
    sankey_data,
    df[["event_name", "platform"]].drop_duplicates(),
    on="event_name",
    how="left"
)



# Chuẩn bị dữ liệu cho Sankey diagram
source = sankey_data["event_name"]
target = sankey_data["next_event_name"]
value = sankey_data["value"]

# Tạo danh sách duy nhất các nodes (danh sách duy nhất từ cả 2 cột)
all_nodes = list(set(source).union(set(target)))

# Tạo mapping từ tên node -> index
node_map = {node: idx for idx, node in enumerate(all_nodes)}

# Chuyển đổi source và target thành index
source_idx = sankey_data["event_name"].map(node_map)
target_idx = sankey_data["next_event_name"].map(node_map)

# Vẽ Sankey Chart
fig = go.Figure(go.Sankey(
    node=dict(
        pad=30,# Khoảng cách giữa các node
        thickness=20,  # Độ dày của node
        line=dict(color="black", width=0.5),
        label=all_nodes
    ),
    link=dict(
        source=source_idx,
        target=target_idx,
        value=value
    )
))

fig.update_layout(title_text="Sankey Diagram", font_size=15)

#########

# Xử lý dữ liệu Sankey_Chart_2 cho chuyển đổi giữa các màn hình
screen_data = df.groupby(["screen_name", "next_screen_name"]).size().reset_index(name="value")
screen_data = screen_data[screen_data['value'] >= 3]  # Lọc những chuyển đổi có số lần >= 3
screen_data = screen_data[screen_data["screen_name"] != screen_data["next_screen_name"]]  # Loại bỏ trường hợp screen_name = next_screen_name


# Tính tổng số sự kiện cho các chuyển đổi màn hình
total_screen_value = screen_data['value'].sum()

# Thêm hàng "Total" vào dataframe
total_screen_row = pd.DataFrame({
    "screen_name": ["Total"], 
    "next_screen_name": [None], 
    "value": [total_screen_value]
})

# Thêm dòng tổng vào dữ liệu
screen_data = pd.concat([screen_data, total_screen_row], ignore_index=True)

# Lọc bỏ hàng "Total" khi chuẩn bị dữ liệu cho Sankey chart
sankey_screen_data = screen_data[screen_data["screen_name"] != "Total"]

# Kiểm tra kết quả (optional)
print(sankey_screen_data)
# Thêm code này vào phần xử lý dữ liệu ban đầu để đảm bảo có cột platform trong các dataframe Sankey
sankey_screen_data = pd.merge(
    sankey_screen_data,
    df[["screen_name", "platform"]].drop_duplicates(),
    on="screen_name",
    how="left"
)
# Chuẩn bị dữ liệu cho Sankey chart cho chuyển đổi giữa các màn hình
screen_source = sankey_screen_data["screen_name"]
screen_target = sankey_screen_data["next_screen_name"]
screen_value = sankey_screen_data["value"]

# Tạo danh sách duy nhất các nodes (danh sách duy nhất từ cả 2 cột)
all_screen_nodes = list(set(screen_source).union(set(screen_target)))

# Tạo mapping từ tên node -> index
screen_node_map = {node: idx for idx, node in enumerate(all_screen_nodes)}

# Chuyển đổi source và target thành index
screen_source_idx = sankey_screen_data["screen_name"].map(screen_node_map)
screen_target_idx = sankey_screen_data["next_screen_name"].map(screen_node_map)

# Vẽ Sankey Chart cho chuyển đổi màn hình (screen_name -> next_screen_name)
screen_fig = go.Figure(go.Sankey(
    node=dict(
        pad=30,  # Khoảng cách giữa các node
        thickness=20,  # Độ dày của node
        line=dict(color="black", width=0.5),
        label=all_screen_nodes  # Nhãn của các node (màn hình)
    ),
    link=dict(
        source=screen_source_idx,
        target=screen_target_idx,
        value=screen_value
    )
))

screen_fig.update_layout(title_text="Sankey Diagram for Screen Transitions", font_size=15)


# Khởi tạo ứng dụng Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # Sử dụng Bootstrap

# Loại bỏ các event_name và next_event_name không mong muốn từ dữ liệu bảng
excluded_events = ['page_ping', 'screen_viewed', 'application_background', 
                   'application_foreground', 'page_view']

# Lọc bỏ các sự kiện này khỏi event_counts
filtered_event_counts = event_counts[
    ~event_counts["event_name"].isin(excluded_events) & 
    ~event_counts["next_event_name"].isin(excluded_events)
]
# Hàm tạo bảng dữ liệu đẹp hơn
def generate_table(dataframe, max_rows=10):
    return dbc.Table(
        # Header của bảng
        [html.Thead(html.Tr([html.Th(col) for col in dataframe.columns]))] +
        # Body của bảng
        [html.Tbody([
            html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]) for i in range(min(len(dataframe), max_rows))
        ])],
        bordered=True,      # Thêm viền
        hover=True,         # Hiệu ứng hover
        striped=True,       # Giao diện bảng kẻ sọc
        responsive=True,    # Tự động điều chỉnh kích thước
    )
# Tạo danh sách sự kiện duy nhất từ cả event_name và next_event_name, loại bỏ None/NaN và "Total". Phần này dùng để xíu cho vào Filter
unique_events = sorted(
    set(filtered_event_counts["event_name"].dropna()).union(set(filtered_event_counts["next_event_name"].dropna())) - {"Total"}
)
# Giao diện web với 2 tab: Chart và Data
app.layout = html.Div([
    html.H1("Dashboard", style={"textAlign": "center"}),
    dcc.Tabs([
        dcc.Tab(label="Chart", children=[
            html.Div([
                html.Label("Chọn sự kiện:"),
                dcc.Dropdown(
                    id="event-filter",
                    # Tạo danh sách sự kiện duy nhất từ cả event_name và next_event_name
                    options=[{"label": e, "value": e} for e in unique_events],
                    multi=True,
                    placeholder="Select events to filter",
                ),
                html.Label("Chọn platform:"),
                dcc.Dropdown(
                    id="platform-filter",
                    # Tạo danh sách các giá trị platform duy nhất từ dữ liệu
                    options=[{"label": platform, "value": platform} for platform in grouped_data["platform"].unique()],
                    multi=True,
                    placeholder="Select platform(s)"
                ),

                # Bar chart
                html.Div([
                    dcc.Graph(id="bar-chart", style={"height": "400px"})  # Cố định chiều cao biểu đồ
                ], style={"margin-bottom": "20px"}),

                # Sankey chart
                html.Div([
                    html.H5("Sankey Diagram for Event", style={"textAlign": "center"}),
                    html.H5("Note: Chart này chỉ lấy các cặp event - next_event có số lượng lớn nhất để chart đỡ rối. Ngoài ra đã loại bỏ các event ít value", style={"textAlign": "left", "fontSize": "14px"}),
                    dcc.Graph(id="sankey-chart", style={"height": "400px"})  # Cố định chiều cao
                ], style={"margin-bottom": "20px"}),

                # Sankey chart cho screen name
                html.Div([
                    html.H5("Sankey Diagram for Screen Name", style={"textAlign": "center"}),
                    dcc.Graph(id="sankey-chart-2", style={"height": "400px", "overflow":"auto"})  # Cố định chiều cao
                ], style={"padding": "20px"})
            ])
        ]),
        dcc.Tab(label="Data", children=[
            html.Div([
                html.H5("Event Data", style={"margin-top": "0px"}),
                generate_table(filtered_event_counts, max_rows=20),  # Tạo bảng dữ liệu
                html.Button("Tải xuống CSV", id="download-btn", n_clicks=0),  # Nút tải xuống
                dcc.Download(id="download-data")  # Thành phần tải xuống
            ], style={"padding": "0px"})
        ])
    ])
])

# Callback để tải dữ liệu , dùng cho Button Tải CSV bên tab Data
@app.callback(
    Output("download-data", "data"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_data(n_clicks):
    if n_clicks > 0:
        return dcc.send_data_frame(event_counts.to_csv, filename="event_data.csv")

# Callback để cập nhật biểu đồ
@app.callback(
    Output("bar-chart", "figure"),
    [Input("platform-filter", "value"),
     Input("event-filter", "value")]
)
def update_bar_chart(selected_events, selected_platforms):
   # Lọc dữ liệu theo platform và event được chọn
    filtered_data =  grouped_data.copy()  # Nên tạo copy để tránh ảnh hưởng đến dữ liệu gốc
    if selected_events:
        filtered_data = filtered_data[filtered_data["event_name"].isin(selected_events)]
    if selected_platforms:
        filtered_data = filtered_data[filtered_data["platform"].isin(selected_platforms)]
    

     # Đảm bảo event_date có kiểu ngày tháng
    #filtered_data['event_date'] = pd.to_datetime(filtered_data['event_time'], format='ISO8601', errors='coerce')
    # Tạo biểu đồ bar chart bằng Plotly Express
    fig = px.bar(
        filtered_data,
        x="event_date",
        y="số events",
        color="platform",
        title="Bar chart: Số lượng event theo platform",
        labels={"event_date": "Event Date", "số events": "Number of Events"}
    )
    fig.update_layout(xaxis_title="Event Date", yaxis_title="Number of Events", font_size=15,
    xaxis=dict(
            tickformat="%Y-%m-%d",  # Định dạng ngày theo kiểu YYYY-MM-DD
            tickangle=45  # Xoay nhãn trục X để dễ đọc hơn
        )
    )
    return fig

# Callback để cập nhật Sankey Chart
@app.callback(
    Output("sankey-chart", "figure"),  # Cập nhật biểu đồ Sankey
    [Input("event-filter", "value"),
     Input("platform-filter", "value")]  # Nhận giá trị từ Dropdown
)

def update_sankey(selected_events, selected_platforms):
    filtered_data = sankey_data.copy()
    # Loại bỏ các event_name và next_event_name không mong muốn
    excluded_events = ['page_ping', 'screen_viewed', 'application_background', 
                       'application_foreground', 'page_view']
    
    filtered_data = filtered_data[
        ~filtered_data["event_name"].isin(excluded_events) & 
        ~filtered_data["next_event_name"].isin(excluded_events)
    ]
    if selected_events:
        # Cần filter cả event_name và next_event_name
        filtered_data = filtered_data[
            (filtered_data["event_name"].isin(selected_events)) |
            (filtered_data["next_event_name"].isin(selected_events))
        ]
        if selected_platforms:
            filtered_data = filtered_data[filtered_data["platform"].isin(selected_platforms)]
    
    
    # Chuẩn bị dữ liệu cho Sankey từ filtered_data
    source = filtered_data["event_name"]
    target = filtered_data["next_event_name"]
    value = filtered_data["value"]

    # Tạo danh sách node duy nhất và mapping
    all_nodes = list(set(source).union(set(target)))
    node_map = {node: idx for idx, node in enumerate(all_nodes)}

    source_idx = filtered_data["event_name"].map(node_map)
    target_idx = filtered_data["next_event_name"].map(node_map)

    # Tạo biểu đồ Sankey
    fig = go.Figure(go.Sankey(
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
    fig.update_layout(title_text="Sankey Diagram for Event", font_size=15)
    return fig

@app.callback(
    Output("sankey-chart-2", "figure"),  # Cập nhật biểu đồ Sankey 2
    [Input("event-filter", "value"),
     Input("platform-filter", "value")
    ]     # Input từ Dropdown cho sự kiện (hoặc cái gì đó khác, tuỳ vào yêu cầu)
)
def update_sankey_2(selected_events, selected_platforms):
    filtered_data = sankey_screen_data.copy()
    if selected_events:
        # Cần filter cả event_name và next_event_name
        filtered_data = filtered_data[
            (filtered_data["event_name"].isin(selected_events)) |
            (filtered_data["next_event_name"].isin(selected_events))
        ]
        if selected_platforms:
            filtered_data = filtered_data[filtered_data["platform"].isin(selected_platforms)]
     # Lọc top N liên kết dựa trên giá trị :vì có quá nhiều screen_name nên cần chỉ hiển thị ra 20 screen_name th
    top_n_links = 20  # Hiển thị tối đa 20 link
    if len(filtered_data) > top_n_links:
        filtered_links = filtered_data.nlargest(top_n_links, 'value')  # Lấy top N
    else:
        filtered_links = filtered_data

  # Chuẩn bị dữ liệu cho Sankey từ filtered_data
    source = filtered_links["screen_name"]
    target = filtered_links["next_screen_name"]
    value = filtered_links["value"]

    # Tạo danh sách node duy nhất và mapping
    all_nodes = list(set(source).union(set(target)))
    node_map = {node: idx for idx, node in enumerate(all_nodes)}

    source_idx = filtered_links["screen_name"].map(node_map)
    target_idx = filtered_links["next_screen_name"].map(node_map)

    # Tạo biểu đồ Sankey
    screen_fig = go.Figure(go.Sankey(
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
    screen_fig.update_layout(title_text="Sankey Diagram for Screen Name", font_size=15)
    return screen_fig


# Chạy ứng dụng
if __name__ == '__main__':
    # app.run_server(host='0.0.0.0', port=8050, debug=True)
    app.run(debug=True)

