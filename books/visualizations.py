from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.embed import components
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256


def create_bokeh_plot(df):

    df = df.dropna(subset=['read_at'])
    
    df['num_pages'] = df['num_pages'].fillna(100)
    df['sizes'] = df['num_pages']/15

    TITLE = "Last 20 books ratings timeline"
    TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save"
    
    mapper = linear_cmap(field_name='average_rating', 
                         palette=Plasma256 ,
                         low=1 ,
                         high=5)
    
    p = figure(tools=TOOLS,
               title=TITLE,
               plot_width=1000,
               x_axis_type='datetime',
               y_range=(0,6))
    
    source = ColumnDataSource(df)
    
    p.circle("read_at", 
             "rating",
             size="sizes",
             line_color=mapper,
             color=mapper,
             source=source)
    
    p.hover.tooltips = [
        ("Title", "@title"),
        ("Author", "@author"),
        ("User rating", "@rating"),
        ("Average rating", "@average_rating"),
        ("Pages", "@num_pages")
        ]
        
    script, div = components(p)

    return script, div

