# Copyright 2022 by Contributors

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PDSUtilities.plotly import ColorblindSafeColormaps

def get_categories_and_counts(df, column, target, value):
    categories = df[column].unique()
    df = df[df[target] == value]
    counts = [df[df[column] == category][column].count() for category in categories]
    return categories, counts

# Plotly is too smart and converts strings to numbers when
# possible but we're smarter: wrap numbers in <span></span>!
def to_string(value):
    if isinstance(value, str):
        return value
    return f"<span>{value}</span>"

def get_categories_and_counts(df, column, target = None, value = None):
    categories = df[column].unique()
    if target is not None:
        df = df[df[target] == value]
    counts = [df[df[column] == category][column].count() for category in categories]
    categories = [to_string(category) for category in categories]
    return categories, counts

def get_width(index):
    WIDTHS = [0.0, 0.1, 0.23, 0.34, 0.46, 0.65, 0.8]
    width = WIDTHS[index] if index < len(WIDTHS) else WIDTHS[-1]
    return width

def apply_default(parameter, default):
    if parameter:
        return { **default, **parameter }
    return default

def get_histogram(x, color, show_legend, name, cumulative):
    return go.Histogram(
        x = x, marker_color = color, showlegend = show_legend,
        name = name, cumulative_enabled = cumulative,
        legendgroup = name,
    )

def get_bar(categories, counts, color, show_legend, name):
    return go.Bar(
        x = categories, y = counts,
        marker_color = color,
        showlegend = show_legend,
        name = name,
        width = get_width(len(categories)),
        legendgroup = name,
    )

def get_rcwh(rows, cols, width, height, columns, values):
    columns = len(columns)
    w, h = 250, 200
    if rows is None and cols is None:
        cols = max(2, min(5, int(np.ceil(np.sqrt(columns)))))
        rows = int(np.ceil(columns/cols))
    elif cols is None:
        cols = int(np.ceil(columns/rows))
    elif rows is None:
        rows = int(np.ceil(columns/cols))
    if width is None:
        if cols > 2 or cols == 2 and len(values) < 4:
            width = w*cols
        else:
            width = w*(cols + 1)
    if height is None:
        if cols > 2 or cols == 2 and len(values) < 4:
            height = 100 + h*rows
        else:
            height = h*rows
    return rows, cols, width, height

def plot_histograms(df, target = None, rows = None, cols = None, width = None, height = None,
    title = None, cumulative = None, barmode = "stack", opacity = 0.65, hovermode = None, template = None,
    colors = 0, font = {}, title_font = {}, legend_font = {}):
    DEFAULT_FONT = {
        'family': "Verdana, Helvetica, Verdana, Calibri, Garamond, Cambria, Arial",
        'size': 14,
        'color': "#000000"
    }
    font = apply_default(font, DEFAULT_FONT)
    legend_font = apply_default(legend_font, font)
    title_font = apply_default(title_font,
        apply_default({ 'size': font.get('size', 16) + 4 }, font)
    )
    colors = 0 if colors is None else colors
    colormaps = ColorblindSafeColormaps()
    colors = colormaps.get_colors(colors)
    if isinstance(colors, int):
        colors = min(max(0, colors), len(DEFAULT_COLORS) - 1)
        colors = DEFAULT_COLORS[colors]
    if hovermode is None:
        hovermode = "x unified"
    #
    values = [] if target is None else [value for value in df[target].unique()]
    columns = [column for column in df.columns if column != target]
    if target is not None and target in columns:
        columns.remove(target)
    rows, cols, width, height = get_rcwh(rows, cols, width, height, columns, values)
    fig = make_subplots(rows = rows, cols = cols,
        horizontal_spacing = 0.25/cols,
        vertical_spacing = 0.37/rows,
        subplot_titles = columns,
    )
    for index, column in enumerate(columns):
        for value in values:
            name = f"{target} = {value}"
            color = colors[values.index(value) % len(colors)]
            if df[column].dtypes == object or len(df[column].unique()) <= len(colors):
                categories, counts = get_categories_and_counts(df, column, target, value)
                trace = get_bar(categories, counts, color, index == 0, name)
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
            else:
                x = df[df[target] == value][column]
                trace = get_histogram(x, color, index == 0, name, cumulative)
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
        if target is None:
            if df[column].dtypes == object or len(df[column].unique()) <= len(colors):
                categories, counts = get_categories_and_counts(df, column)
                trace = get_bar(categories, counts, colors[0], False, column)
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
            else:
                trace = get_histogram(df[column], colors[0], False, column, cumulative)
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
    # barmode = ['stack', 'group', 'overlay', 'relative']
    # barmode = "stack"
    if barmode == "overlay":
        fig.update_traces(opacity = opacity)
    fig.update_annotations(font = font)
    fig.update_traces(marker_line_color = "#000000")
    fig.update_traces(marker_line_width = 0.5)
    if title is not None and isinstance(title, str):
        title = { 'text': title, 'x': 0.5, 'xanchor': "center" }
    if title is not None:
        fig.update_layout(title = title)
    if template is not None:
        fig.update_layout(template = template)
    if cols > 2 or cols == 2 and len(values) < 4:
        fig.update_layout(width = width, height = height, barmode = barmode,
            legend = dict(
                orientation = "h",
                yanchor = "bottom",
                y = 1.0 + 2.0*cols/100.0,
                xanchor = "center",
                x = 0.5
            ),
            margin = { 't': 160 },
        )
    fig.update_layout(hovermode = hovermode)
    fig.update_layout(width = width, height = height, barmode = barmode,
        font = font, title_font = title_font, legend_font = legend_font,
        # margin = { 't': 160 },
        # bargap = 0.2, # gap between bars of adjacent location coordinates
        # bargroupgap = 0*0.2, # gap between bars of the same location coordinates
    )
    # This is literally the dumbest thing I've seen in years...
    # This puts space between the ticks and tick labels. SMFH.
    fig.update_yaxes(ticksuffix = " ")
    return fig
