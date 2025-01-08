import taipy.gui.builder as tgb
from taipy.gui import Gui, notify
import taipy.gui.builder as tgb
from datetime import date, timedelta
import datetime
import math



def on_button_action(state):
    notify(state, 'info', f'The text is: {state.text}')
    state.text = 'Button Pressed'

def on_change(state, var_name, var_value):
    if var_name == "text" and var_value == "Reset":
        state.text = ""
        return

def on_change(state, _, var_value):
    # Update the text controls
    state.start_sel = all_dates[var_value[0]]
    state.end_sel = all_dates[var_value[1]]


# Create the list of dates (all year 2000)
all_dates = {}
all_dates_str = []
start_date = date(2000, 1, 1)
end_date = date(2001, 1, 1)
a_date = start_date
while a_date < end_date:
    date_str = a_date.strftime("%Y/%m/%d")
    all_dates_str.append(date_str)
    all_dates[date_str] = a_date
    a_date += timedelta(days=1)

# Initial selection: first and last day
dates = [all_dates_str[1], all_dates_str[-1]]
# These two variables are used in text controls
start_sel = all_dates[dates[0]]
end_sel = all_dates[dates[1]]

#Tạo ngày tháng
start_date = datetime.date(1756, 1, 27).strftime('yy-mm-dd')
end_date   = datetime.date(1791, 12, 5).strftime('yy-mm-dd')
dates = [start_date, end_date]

# x values: [-10..10]
x_range = range(-10, 11)
data = {
    "X": [x for x in x_range], 
    "Y": [x * x for x in x_range]
}



types = [("bar", "Bar"), ("line", "Line")]
selected_type = types[0]

if __name__ == "__main__":
    text = "Original text"
    value = "Nhập vào đây"

    # Definition of the page
    with tgb.Page() as page:
        tgb.text("Đây là Python")
        tgb.text("# Getting started with Taipy GUI", mode="md")
        tgb.text("My text: {text}")

        tgb.input("{text}")
        tgb.button("Run local", on_action=on_button_action)
        tgb.button("Đây là button")
        tgb.input("{value}")

        tgb.number("{value}", min=10, max=60, step = 10) #chọn number min 10, max 60, bước nhảy 10
        tgb.input("{dates}") #tạo ô input với giá trị mặc định lấy từ slider bên dưới
        tgb.slider("{dates}", lov="{all_dates_str}")
        tgb.toggle("{value}", lov="Item 1;Item 2;Item 3", unselected_value="No Value")
        
        tgb.date("{dates}",with_time=True)
        print(data)
        tgb.chart("{data}", type=selected_type[0], x="X", y="Y") #ban đầu sai khi để data = data, phải đổi thành "{data}" như thế kia
        tgb.toggle(selected_type, lov=types)

    Gui(page).run(debug=True,title="Dùng python builder")

