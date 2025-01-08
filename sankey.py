import plotly.graph_objects as go
from taipy.gui import Gui
import pandas


# Dữ liệu cho Sankey diagram
nodes = dict(
    label=["A", "B", "C", "D", "E", "F"],
    color=["blue", "red", "green", "yellow", "purple", "orange"]
)

# Định nghĩa các liên kết
links = dict(
    source=[0, 0, 1, 2, 2, 3, 5], # index của node nguồn
    target=[2, 3, 4, 4, 5, 5, 2], # index của node đích
    value=[8, 4, 2, 8, 4, 2, 5],  # độ lớn của luồng
    color=['rgba(0,0,255,0.4)', 'rgba(255,0,0,0.4)', 
           'rgba(0,255,0,0.4)', 'rgba(255,255,0,0.4)',
           'rgba(128,0,128,0.4)', 'rgba(255,165,0,0.4)']
)

# Tạo figure
figure = go.Figure(data=[go.Sankey(
    node=nodes,
    link=links,
    arrangement="snap"
)])

# Cập nhật layout
figure.update_layout(
    title="Sankey Diagram Example",
    font_size=12,
    height=600
)

page = """
<|Đây là Sankey chart|text|>
<|chart|figure={figure}|>
"""

if __name__ == "__main__":
    Gui(page).run(title="Sankey Chart Example", use_reloader=True)