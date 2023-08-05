# Copyright 2022 by Contributors

from xgboost import XGBModel
from xgboost import Booster
import plotly.graph_objects as go

# The `PDSUtilities.xgboost.plot_importance()` function is a direct
# copy/paste/edit modification of `xgboost.plot_importance()` with a few
# minor tweaks to the API and relatively light changes to the code. The
# xgboost team deserves the vast majority of credit for this code!
# The xgboost license can be found here:
# https://github.com/dmlc/xgboost/blob/master/LICENSE
def plot_importance(booster, features = {}, width = 0.6, xrange = None, yrange = None,
                    title = 'Feature Importance', xlabel = 'F Score',
                    ylabel = 'Features', fmap = '', max_features = None,
                    importance_type = 'weight', show_grid = True, show_values = True):
    """Plot importance based on fitted trees using plotly.
    Parameters
    ----------
    booster : Booster, XGBModel or dict
        Booster or XGBModel instance, or dict taken by Booster.get_fscore()
	features: list or dict of feature names for displaying.
		* features dict maps default feature names ("f0", "f1", etc) to feature names
		* features list is a list of feature names
    show_grid : bool, Turn the axes grids on or off.  Default is True (On).
    importance_type : str, default "weight"
        How the importance is calculated: either "weight", "gain", or "cover"
        * "weight" is the number of times a feature appears in a tree
        * "gain" is the average gain of splits which use the feature
        * "cover" is the average coverage of splits which use the feature
          where coverage is defined as the number of samples affected by the split
    max_features : int, default None
        Maximum number of top features displayed on plot. If None, all features will be displayed.
    width : float, default 0.5
        Bar width
    xlimits : tuple, default None
        Tuple passed to axes.xlim()
    ylimits : tuple, default None
        Tuple passed to axes.ylim()
    title : str, default "Feature importance"
        Axes title. To disable, pass None.
    xlabel : str, default "F score"
        X axis title label. To disable, pass None.
    ylabel : str, default "Features"
        Y axis title label. To disable, pass None.
    fmap: str or os.PathLike (optional)
        The name of feature map file.
    show_values : bool, default True
        Show values on plot. To disable, pass False.
    Returns
    -------
    fig : plotly Figure object
    """
    try:
        import plotly.graph_objects as go
    except ImportError as e:
        raise ImportError('You must install plotly to plot importance') from e

    if isinstance(booster, XGBModel):
        importance = booster.get_booster().get_score(
            importance_type = importance_type, fmap = fmap)
    elif isinstance(booster, Booster):
        importance = booster.get_score(importance_type = importance_type, fmap = fmap)
    elif isinstance(booster, dict):
        importance = booster
    else:
        raise ValueError('tree must be Booster, XGBModel or dict instance')

    if not importance:
        raise ValueError(
            'Booster.get_score() results in empty.  ' +
            'This maybe caused by having all trees as decision dumps.')

    if isinstance(features, list):
        features = {
            f"f{f}": features[f] for f in range(len(features))
        }

    tuples = [(k, importance[k]) for k in importance]
    if max_features is not None:
        # pylint: disable=invalid-unary-operand-type
        tuples = sorted(tuples, key=lambda x: x[1])[-max_features:]
    else:
        tuples = sorted(tuples, key=lambda x: x[1])
    labels, values = zip(*tuples)

    text = [xlabel + ": " + str(value) for value in values]
    fig = go.Figure(go.Bar(
            y = [features.get(label, label.upper()) for label in labels],
            x = values,
            orientation = 'h',
            width = width,
            hovertext = text if show_values else [],
            text = text if show_values else [],
            textposition = 'auto',
        ))
    if xrange is not None:
        if not isinstance(xrange, tuple) or len(xrange) != 2:
            raise ValueError('xrange must be a tuple of 2 elements')
        fig.update_xaxes(range = xrange)
    if yrange is not None:
        if not isinstance(yrange, tuple) or len(yrange) != 2:
            raise ValueError('yrange must be a tuple of 2 elements')
        fig.update_yaxes(range = yrange)
    if title is not None:
        fig.update_layout(title = {"text": title, "x": 0.5, "xanchor":  "center"})
    if xlabel is not None:
        fig.update_xaxes(title_text = xlabel)
    if ylabel is not None:
        fig.update_yaxes(title_text = ylabel)
    fig.update_xaxes(showgrid = show_grid)
    fig.update_yaxes(showgrid = False)
    # This is literally the dumbest thing I've seen in years...
    # This puts space between the ticks and tick labels. SMFH.
    fig.update_yaxes(ticksuffix = "  ")
    return fig