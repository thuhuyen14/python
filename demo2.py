from taipy.gui import Gui
import pandas as pd
penguin_file_url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv"
penguin_df = pd.read_csv(penguin_file_url)
target_names = list(penguin_df.species.unique()) # ["Adelie", "Gentoo", "Chinstrap"]
species = target_names[0] # "Adelie"
df = penguin_df[penguin_df.species == species]

chart_properties = {
    "height": "35vh",
    "width": "40vw",
    "mode": "markers",
    "marker": {
        "size": 10,
        "color": "orange",
        "line": {"width": 3, "color": "black"},
    },
    "layout": {"margin": {"t": 0}},
    "options": {"unselected": {"marker": {"opacity": 1}}},
}


page = """
### Penguin species: 
<|{species}|selector|lov={target_names}|dropdown=True|width=100%|>
<br />
Selected penguins out of all penguins:  
<br />
<|{len(df)}|indicator|value={len(df)}|max={len(penguin_df)}|>
<br />
**Chart 1:** bill_depth_mm against bill_length_mm 
<|{df}|chart|x=bill_length_mm|y=bill_depth_mm|properties={chart_properties}|>
"""

Gui(page=page).run(dark_mode=False, use_reloader=True)