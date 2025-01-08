import pandas as pd
from sqlalchemy import create_engine

# Tạo connection string cho Redshift
connection_string = "postgresql+psycopg2://awsuser:RGYcH3Yoyqo5fKrk@poc-redshift-free-trial.cir6kkgprzvy.ap-southeast-1.redshift.amazonaws.com:5439/dwh_snowplow"

try:
    # Tạo engine
    engine = create_engine(connection_string)
    
    # Câu truy vấn của bạn
    query = """
    SELECT event_name, next_event_name, COUNT(event_id) as value
    FROM dwh_snowplow.fact_events_l3d_sp
    GROUP BY event_name, next_event_name 
    limit 10;
    """
    
    # Đọc dữ liệu vào DataFrame
    df = pd.read_sql_query(query, engine)
    
    # In kết quả
    print(df.head())
    
    # Vẽ biểu đồ Sankey với Plotly để visualize event flow
    import plotly.graph_objects as go
    
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = list(set(df['event_name'].tolist() + df['next_event_name'].tolist())),
        ),
        link = dict(
            source = [list(set(df['event_name'].tolist() + df['next_event_name'].tolist())).index(x) for x in df['event_name']],
            target = [list(set(df['event_name'].tolist() + df['next_event_name'].tolist())).index(x) for x in df['next_event_name']],
            value = df['value']
        )
    )])

    fig.update_layout(title_text="Event Flow Analysis", font_size=10)
    fig.show()

except Exception as e:
    print(f"Error: {e}")
finally:
    engine.dispose()  # Đóng kết nối