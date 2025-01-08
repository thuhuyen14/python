import plotly.graph_objects as go
from taipy.gui import Gui

# Tạo một biểu đồ Plotly
fig = go.Figure(data=[
    go.Bar(name='Group A', x=['Jan', 'Feb', 'Mar'], y=[10, 20, 30]),
    go.Bar(name='Group B', x=['Jan', 'Feb', 'Mar'], y=[15, 25, 35])
])
fig.update_layout(barmode='group', title="Example Plotly Chart")

# Tích hợp vào Taipy
page = """
# Plotly in Taipy

<|plotly_chart|chart|>
"""

gui = Gui(page)
gui.run(data={'plotly_chart': fig})
