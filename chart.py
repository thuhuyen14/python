#thêm các thư viện
import taipy.gui.builder as tgb
from taipy.gui import Gui # Import trực tiếp class Gui
import math # Import toàn bộ module math
import numpy
import pandas 
import random
import yfinance
from sklearn.datasets import make_classification
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

#Tạo data cho chart
# x values: [-10..10]
x_range = range(-10, 11)
data1 = {
    "X": [x for x in x_range], 
    "Y": [x * x for x in x_range]
}
x_range2 = range(-10, 11)
data2 = {
    "X":[x for x in x_range2],
    "Y":[x * 2 - 5 for x in x_range2]
}
types = [("bar", "Bar"), ("line", "Line")]
selected_type = types[0]

def on_change(state, var_name, var_value):
    state.selected_type = var_value
#data cho scatter chart
features, label = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0) #tạo 2 bảng với mỗi bảng là 1000 mẫu dữ liệu giả lập, có 2 đặc trưng, không có đặc trưng dư thừa

random_data = pandas.DataFrame({"x": features[:, 0], "y": features[:, 1], "label": label}) #Tạo một DataFrame tên là random_data với 3 cột: x,y,label
#Cú pháp của NumPy [:, 0]---- ":": Lấy toàn bộ các hàng trong mảng. 0: Lấy cột đầu tiên (index = 0) từ mảng features.
data_x = random_data["x"]
class_A = [
    random_data.loc[i, "y"] if random_data.loc[i, "label"] == 0 else numpy.nan for i in range(len(random_data))
] 
'''
Đoạn mã này tạo ra một danh sách class_A chứa các giá trị y từ random_data, nhưng chỉ chọn các giá trị của y 
khi giá trị trong cột label tương ứng bằng 0 (đại diện cho lớp A). Nếu label không phải là 0, thì giá trị đó sẽ là numpy.nan.
'''

class_B = [
    random_data.loc[i, "y"] if random_data.loc[i, "label"] == 1 else numpy.nan for i in range(len(random_data))
]
'''
Đoạn mã này tạo ra một danh sách class_B chứa các giá trị y từ random_data, nhưng chỉ chọn các giá trị của y 
khi giá trị trong cột label tương ứng bằng 1 (đại diện cho lớp B). Nếu label không phải là 1, thì giá trị đó sẽ là numpy.nan.
'''

data3 = {"x": random_data["x"], "Class A": class_A, "Class B": class_B}

#Data 4 cho scatter with linear
n_samples = 300
X, y, coef = make_regression(n_samples=n_samples, n_features=1, n_informative=1, n_targets=1, noise=25, coef=True)

model = LinearRegression().fit(X, y)

x_data = X.flatten()
y_data = y.flatten()
predict = model.predict(X)

data3_2 = {"x": x_data, "y": y_data, "Regression": predict}

#Data 4 cho pie chart
data4 = {
    "Country": [
        "Rest of the world",
        "Russian Federation",
        "Brazil",
        "Canada",
        "United States of America",
        "China",
        "Australia",
        "Democratic Republic of the Congo",
        "Indonesia",
        "Peru",
    ],
    "Area": [1445674.66, 815312, 496620, 346928, 309795, 219978, 134005, 126155, 92133.2, 72330.4],
}
#Data 4.2 cho 2 pie chart
countries = [
        "US", "China", "European Union", "Russian Federation",
        "Brazil", "India", "Rest of World"
]

data4_2 = [
    {
        # Values for GHG Emissions
        "values": [16, 15, 12, 6, 5, 4, 42],
        "labels": countries
    },
    {
        # Values for CO2 Emissions
        "values": [27, 11, 25, 8, 1, 3, 25],
        "labels": countries
    }
]
options = [
    # First pie chart
    {
        # Show label value on hover
        "hoverinfo": "label",
        # Leave a hole in the middle of the chart
        "hole": 0.4,
        # Place the trace on the left side
        "domain": {"column": 0}
    },
    # Second pie chart
    {
        # Show label value on hover
        "hoverinfo": "label",
        # Leave a hole in the middle of the chart
        "hole": 0.4,
        # Place the trace on the right side
        "domain": {"column": 1}
    }
]

layout = {
    # Chart title
    "title": "Global Emissions 1990-2011",
    # Show traces in a 1x2 grid
    "grid": {
        "rows": 1,
        "columns": 2
    },
    "annotations": [
        # Annotation for the first trace
        {
            "text": "GHG",
            "font": {
                "size": 20
            },
            # Hide annotation arrow
            "showarrow": False,
            # Move to the center of the trace
            "x": 0.22,
            "y": 0.5
        },
        # Annotation for the second trace
        {
            "text": "CO2",
            "font": {
                "size": 20
            },
            "showarrow": False,
            # Move to the center of the trace
            "x": 0.78,
            "y": 0.5
        }
    ],
    "showlegend": False
}
#Data 5 Histogram
data5 = {
  "Input": [random.gauss(0, 5) for i in range(100)]
}

#Data 6 Funnel Chart
data6 = {
    "Opps":  ["Hot leads", "Doc sent", "Quote", "Closed Won"],
    "Visits": [316, 238, 125, 83]
}
#Data 6_2
data6_2 = {
    # The stage names
    "Types": ["Website visit", "Downloads", "Prospects", "Invoice sent", "Closed"],
    # Volume for each stage, in the US
    "Visits_us": [13873, 10533, 5443, 2703, 908],
    # Volume for each stage, in the EU
    "Visits_eu": [ 7063, 4533, 3443, 1003, 1208 ],
    # Volume for each stage, in the AP region
    "Visits_ap": [ 6873, 2533, 3443, 1703, 508 ]
}

# Columns for each trace
x = ["Visits_us", "Visits_eu", "Visits_ap"]

# Legend text for each trace
names = ["US", "EU", "AP"]

#Data 7 cho Candle stick chart
ticker = yfinance.Ticker("AAPL")
stock = ticker.history(interval="1d", start="2018-08-18", end="2018-09-10")
stock["Date"] = stock.index
options2 = {
    "decreasing": {"line": {"color": "red"}},
    "increasing": {"line": {"color": "green"}},
}

layout2 = {
    "xaxis": {
        "rangeslider": {"visible": False}
    }
}

with tgb.Page() as page:
    
    tgb.text("# Đây là các chart tạo được từ Taipy. Data tự giả lập ở trên.", mode="md")
    tgb.text('''1.Bar chart 
             Bar chart với trục x nhận giá trị từ -10 đến 10, trục y là giá trị bình phương của trục x''')
    tgb.chart("{data1}", type = selected_type, x="X", y="Y",rebuild=True) #ban đầu sai khi để data = data, phải đổi thành "{data}" như thế kia
    tgb.toggle(selected_type, lov=types, on_change=on_change)
    #chưa hiểu tại sao data 1 này hiển thị cả 2 chart

    tgb.text('2.Line chart')
    tgb.chart("{data2}", type='line', x="X", y="Y")

    tgb.text('3. Scatter charts')
    tgb.chart("{data3}", mode="markers", x="x", y__1="Class A", y__2="Class B")

    tgb.text('3.2. Scatter chart with linear')
    tgb.chart("{data3_2}", mode__1="markers", x__1="x", y__1="y", mode__2="line", x__2="x", y__2="Regression")

    tgb.text('4. Piechart')
    tgb.chart("{data4}", type="pie", values="Area", labels="Country")
    tgb.text('4.2. Multiple piechart')
    tgb.chart("{data4_2}", type="pie", x__1="0/values", x__2="1/values", options="{options}", layout="{layout}")
    #"0/values" nghĩa là: 0: Truy cập phần tử đầu tiên của danh sách (data4_2[0]); values: Lấy cột giá trị values trong phần tử đó.

    tgb.text('5. Histogram chart')
    # print(data5)
    tgb.chart('{data5}',type='histogram') #Nếu viết hoa thành Histogram thì lại không chạy được

    tgb.text('6. Funnel Chart')
    tgb.chart("{data6}", type="funnel", x="Visits", y="Opps")

    tgb.text('6.2. multiple funnel')
    tgb.chart("{data6_2}", type="funnel", x="{x}", y="Types", name="{names}")

    tgb.text('7. Candlestick chart')
    tgb.chart("{stock}", type="candlestick", x="Date", open="Open", close="Close", low="Low", high="High", options="{options2}", layout="{layout2}")
   
Gui(page).run(debug=True,title="Dùng Taipy vẽ chart",use_reloader=True)
# Gui.run(data={'plotly_chart': fig})
    


