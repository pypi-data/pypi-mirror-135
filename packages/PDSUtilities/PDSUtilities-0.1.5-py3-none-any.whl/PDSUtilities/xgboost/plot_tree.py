# Copyright 2022 by Contributors

import numpy as np
from igraph import Graph
import plotly.graph_objects as go

def get_leaf(index, line):
    return (int(index), float(line.split("=")[1]))

def get_node(index, line):
    node, line = line.split(" ")
    feature, value = node.strip("[]").split("<")
    y, n, m = line.split(",")
    y, n, m = [y.split("=")[1], n.split("=")[1], m.split("=")[1]]
    return(int(index), feature.upper(), float(value), int(y), int(n), int(m))

def get_node_labels(nodes, features, precision):
    return [
        features.get(feature, feature) + " < " + str(round(value, precision)) for _, feature, value in nodes
    ]

def get_leaf_labels(leaves, precision):
    return [
        str(round(value, precision)) for _, value in leaves
    ]

def get_unique_edges(index, y, n, m):
    if y == n and n == m:
        assert False, "Should never have Yes = No = Missing..."
        # return[(index, y, "Yes/No/Missing")]
    if y == n:
        assert False, "Should never have Yes = No..."
        # return[(index, y, "Yes/No"), (index, m, "Missing")]
    if n == m:
        return[(index, y, "Yes"), (index, n, "No/Missing")]
    if y == m:
        return[(index, y, "Yes/Missing"), (index, n, "No")]
    return [(index, y, "Yes"), (index, n, "No"), (index, m, "Missing")]

def get_min_max_delta(v, indent):
    min_v, max_v = np.min(v), np.max(v)
    delta_v = max_v - min_v
    min_v = min_v - indent*delta_v
    max_v = max_v + indent*delta_v
    return min_v, max_v, max_v - min_v

def get_features(features):
    return { f"F{f}": features[f] for f in range(len(features))}

def get_graph(dump):
    lines = [line.strip().split(":") for line in dump.splitlines()]
    indexes, lines =[
        [i for i, _ in lines ],
        [j for _, j in lines ]
    ]
    leaves = [get_leaf(i, line)
        for i, line in zip(indexes, lines)
        if line.startswith("leaf")
    ]
    nodes = [get_node(i, line)
        for i, line in zip(indexes, lines)
        if not line.startswith("leaf")
    ]
    edges = [
        get_unique_edges(index, y, n, m)
        for index, _, _, y, n, m in nodes
    ]
    edges = [item for edge in edges for item in edge]
    nodes = [(index, feature, float(value)) for index, feature, value, _, _, _ in nodes]
    graph = Graph([(i, j) for i, j, _ in edges])
    xy = graph.layout_reingold_tilford(root = 0)
    return leaves, nodes, edges, graph, xy

def apply_default(parameter, default):
    if parameter:
        return { **default, **parameter }
    return default

def get_edge_annotation(edge, xy, w, labels = {}, colors = {}, arrow = {}, label = {}, font = {}):
    i, j, text = edge
    xi, yi = xy[i]
    xj, yj = xy[j]
    xm, ym = (xi + xj)/2.0, (yi + yj)/2.0
    font['color'] = colors[text]
    arrow['arrowcolor'] = colors[text]
    arrow['arrowwidth'] = 1
    return [dict(
            x  = xj - w / 2.0, y  = yj, xref  = "x", yref  = "y",
            ax = xj - w / 2.0 - 0.05, ay = yj, axref = "x", ayref = "y",
            font = font, **arrow,
            hovertext = text,
        ), dict(
            x  = xm, y  = ym, xref  = "x", yref  = "y",
            ax = xm, ay = ym, axref = "x", ayref = "y",
            showarrow = False, **label,
            font = font, text = labels.get(text, text),
        )
    ]

def get_edge_shapes(edges, xy, w, colors = {}, line = {}):
    shapes = []
    for edge in edges:
        i, j, text = edge
        xi, yi = xy[i]
        xj, yj = xy[j]
        xi, xj = xi + w/2.0, xj - w/2.0
        dx, dy = np.maximum(xj - xi, 0.2), 0.02*np.sign(yj - yi)
#         line['color'] = colors[text]
        line = { **line, 'color': colors[text]}
        shapes.append(dict(
            type = 'path', layer = 'below', line = line, #{ **line },
            path = f"M{xi} {yi + dy}, C {xi + dx} {yi + dy}, {xj - dx} {yj}, {xj - 0.02} {yj}",
        ))
    return shapes

def get_shape_from_type(shape_type, xi, yi, w, h, px, py, shape, line):
    xi, yi, xj, yj = xi - w, yi - h, xi + w, yi + h
    if shape_type == "rounded":
        # Rounded rectangle...NB rx and ry are not quite correct...
        rx, ry = 8.0/px, 8.0/py
        rounded_bl = f" M {xi+rx}, {yi} Q {xi}, {yi} {xi}, {yi+ry}"
        rounded_tl = f" L {xi}, {yj-ry} Q {xi}, {yj} {xi+rx}, {yj}"
        rounded_tr = f" L {xj-rx}, {yj} Q {xj}, {yj} {xj}, {yj-ry}"
        rounded_br = f" L {xj}, {yi+ry} Q {xj}, {yi} {xj-rx}, {yi} Z"
        return dict(
            xref = "x", yref = "y",
            path = rounded_bl + rounded_tl + rounded_tr + rounded_br,
            layer = "below", line = line, **shape,
         )
    else:
        # Built-in shape type...
        return dict(
            x0 = xi, y0 = yi, x1 = xj, y1 = yj,
            layer = "below", line = line, **shape,
         )

def get_node_or_leaf_shapes(leaves_or_nodes, xy, w, h, px, py, shape = {}, line = {}):
    indexes = [leaf_or_node[0] for leaf_or_node in leaves_or_nodes]
    w, h = w / 2.0, h / 2.0
    shape_type = shape.get("type", "rect")
    if shape_type == "rounded":
        shape['type'] = "path"
    shapes = []
    for i in indexes:
        shapes.append(get_shape_from_type(shape_type, xy[i][0], xy[i][1], w, h, px, py, shape, line))
    return shapes

def get_nodes_scatter_plot(nodes, xy, features, precision, font = {}):
    x = [xy[i][0] for i, _, _ in nodes]
    y = [xy[i][1] for i, _, _ in nodes]
    return go.Scatter(x = x, y = y, mode = 'text', textfont = font,
        text = get_node_labels(nodes, features, precision),
    )

def get_leaves_scatter_plot(leaves, xy, precision, font = {}):
    x = [xy[i][0] for i, _ in leaves]
    y = [xy[i][1] for i, _ in leaves]
    return go.Scatter(x = x, y = y, mode = 'text', textfont = font,
        text = get_leaf_labels(leaves, precision),
    )

# Non-grayscale defaults are from the vibrant colormap here:
# https://personal.sron.nl/~pault/
def plot_tree(booster, tree, features = {}, width = None, height = None,
    precision = 4, scale = 0.7, font = None, grayscale = False,
    node_shape = {}, node_line = {}, node_font = {},
    leaf_shape = {}, leaf_line = {}, leaf_font = {},
    edge_labels = {}, edge_colors = {}, edge_arrow = {},
    edge_line = {}, edge_label = {}, edge_font = {}):
    #
    DEFAULT_FONT = {
        # 'family': "Courier New, monospace",
        'family': "Verdana, Helvetica, Verdana, Calibri, Garamond, Cambria, Arial",
        'size': 16,
        'color': "#000000"
    }
    DEFAULT_NODE_SHAPE = {
        'type': "rect",
        'fillcolor': "#CBCBCB" if grayscale else "rgba(0,153,136,0.75)", #"#009988", #"#C2CA95",
        'opacity': 1.0,
    }
    DEFAULT_NODE_LINE = {
        'color': "#666666" if grayscale else "rgb(238,119,51)", #"olive",
        'width': 1,
        'dash': "solid", # ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    }
    DEFAULT_LEAF_SHAPE = {
        'type': "rounded",
        'fillcolor': "#EDEDED" if grayscale else "rgba(238,119,51,0.75)", #"#EE7733", #"#E8D8C0", #"#B5B97A",
        'opacity': 1.0,
    }
    DEFAULT_LEAF_LINE = {
        'color': "#777777" if grayscale else "rgb(0,153,136)", #"brown", #"olive",
        'width': 1,
        'dash': "solid", # ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    }
    DEFAULT_EDGE_LABELS = {
        'Yes': "Yes",
        'No': "No",
        'Missing': "Missing",
        'Yes/Missing': "Yes/Missing",
        'No/Missing': "No/Missing"
    }
    # COLORMAP = ["#005ab5", "#DC3220"]
    DEFAULT_EDGE_COLORS = {
        'Yes': "#222222" if grayscale else "rgb(0,153,136)",
        'No': "#888888" if grayscale else "rgb(238,119,51)",
        'Missing': "#AAAAAA",
        'Yes/Missing':  "#222222" if grayscale else "rgb(0,153,136)",
        'No/Missing': "#888888" if grayscale else "rgb(238,119,51)",
    }
    DEFAULT_EDGE_ARROW = {
        'arrowhead': 3, # Integer between or equal to 0 and 8
        'arrowsize': 1.5, # Relative to arrowwidth
        'arrowwidth': 1,
    }
    DEFAULT_EDGE_LINE = {
        'width': 1.5,
        'dash': "solid", # ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    }
    DEFAULT_EDGE_LABEL = {
        'align': "center",
        'bgcolor': "#FFFFFF",
        'bordercolor': "rgba(0,0,0,0)",
        'borderpad': 1,
        'borderwidth': 1,
        'opacity': 1.0,
        'textangle': 0,
        'valign': "middle",
        'visible': True,
    }
    font = apply_default(font, DEFAULT_FONT)
    #
    node_shape = apply_default(node_shape, DEFAULT_NODE_SHAPE)
    node_line = apply_default(node_line, DEFAULT_NODE_LINE)
    node_font = apply_default(node_font, font)
    #
    leaf_shape = apply_default(leaf_shape, DEFAULT_LEAF_SHAPE)
    leaf_line  = apply_default(leaf_line,  DEFAULT_LEAF_LINE)
    leaf_font = apply_default(leaf_font, font)
    #
    edge_labels = apply_default(edge_labels, DEFAULT_EDGE_LABELS)
    edge_colors = apply_default(edge_colors, DEFAULT_EDGE_COLORS)
    edge_arrow  = apply_default(edge_arrow,  DEFAULT_EDGE_ARROW)
    edge_line = apply_default(edge_line, DEFAULT_EDGE_LINE)
    edge_label = apply_default(edge_label, DEFAULT_EDGE_LABEL)
    edge_font = apply_default(edge_font,
        apply_default({ 'size': font.get('size', 16) - 2 }, font)
    )
    #
    if isinstance(features, list):
        features = get_features(features)
    #
    dump = booster.get_dump()[tree]
    leaves, nodes, edges, graph, xy = get_graph(dump)
    #
    xy = [[y, x] for x, y in xy]
    #
    _, layers, _ = graph.bfs(0)
    # Fix the root node's y position...
    # it's sometimes wrong...
    if len(layers) > 2:
        y = np.sum([xy[i][1] for i in range(layers[1], layers[2])])
        xy[0][1] = y/(layers[2] - layers[1])
    # Could instead do a dfs and then work from deepest layers
    # to the root setting all parents' y values to the mean of
    # their children. Here's the dfs() description:
    # def dfs(self, vid, mode=OUT):
    # Conducts a depth first search (DFS) on the graph.
    # Parameters	vid	the root vertex ID
    # mode	either "in" or "out" or "all", ignored for undirected graphs.
    # Returns	a tuple with the following items:
    # The vertex IDs visited (in order)
    # The parent of every vertex in the DFS
    #
    layers = [layers[i] - layers[i-1] for i in range(1, len(layers))]
    tree_depth, tree_width = len(layers), np.max(layers)
    #
    # KLUDGE: We need to get font metrics and do this right...
    w, h = scale*font.get('size', 14)*np.max([len(label)
        for label in get_node_labels(nodes, features, precision) + get_leaf_labels(leaves, precision)
    ]), 3*font.get('size', 14)
    #
    if width is None:
        width = w*tree_depth + 70*(tree_depth + 1) #// 4 # 5*height // 2
    if height is None:
        height = h*tree_width + int(2.5*h*np.sqrt(2.0 + (len(nodes) + len(leaves))/tree_depth))
    #
    x = [xy[i][0] for i, _, _ in nodes] + [xy[i][0] for i, _ in leaves]
    y = [xy[i][1] for i, _, _ in nodes] + [xy[i][1] for i, _ in leaves]
    #
    min_x, max_x, delta_x = get_min_max_delta(x, 0.1)
    min_y, max_y, delta_y = get_min_max_delta(y, 0.1)
    pixels_x, pixels_y = width/delta_x, height/delta_y
    # KLUDGE: We need to get font metrics and do this right...
    w, h = w/pixels_x, h/pixels_y
    #
    nodes_scatter_plot  = get_nodes_scatter_plot (nodes, xy, features, precision, node_font)
    leaves_scatter_plot = get_leaves_scatter_plot(leaves, xy, precision, leaf_font)
    #
    layout = go.Layout(
        font = font,
        showlegend = False,
        autosize = False,
        width = width,
        height = height,
        plot_bgcolor = "#FFFFFF",
        xaxis = dict(visible = False),
        yaxis = dict(visible = False),
        shapes = get_edge_shapes(
            edges, xy, w, colors = edge_colors, line = edge_line
        ) + get_node_or_leaf_shapes(
            nodes, xy, w, h, pixels_x, pixels_y, node_shape, node_line
        ) + get_node_or_leaf_shapes(
            leaves, xy, w, h, pixels_x, pixels_y, leaf_shape, leaf_line
        ),
        xaxis_range = [min_x, max_x],
        yaxis_range = [min_y, max_y],
    )
    #
    fig = go.Figure([nodes_scatter_plot, leaves_scatter_plot], layout)
    fig.update_layout(yaxis = {'autorange': True})
    fig.update_layout(xaxis = {'autorange': True})
    #
    for edge in edges:
        arrow, label = get_edge_annotation(edge, xy, w,
            labels = edge_labels, colors = edge_colors,
            arrow = edge_arrow, label = edge_label, font = edge_font,
        )
        fig.add_annotation(arrow)
        fig.add_annotation(label)
    #
    return fig
