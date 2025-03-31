import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.animation import FFMpegWriter


class CommonChart:
    def __init__(self, filename, fig_kwargs, title):
        self.filename = filename
        self.extension = self.filename.split(".")[-1]
        self.fig_kwargs = self.get_fig_kwargs(fig_kwargs)
        self.title = self.get_title(title)

    def get_tick_template(self, tick_template):
        if isinstance(tick_template, str):
            return ticker.StrMethodFormatter(tick_template)
        elif callable(tick_template):
            return ticker.FuncFormatter(tick_template)

    def get_title(self, title):
        if isinstance(title, str):
            return {"label": title}
        elif isinstance(title, dict):
            if "label" not in title:
                raise ValueError(
                    'You must use the key "label" in the `title` dictionary '
                    "to supply the name of the title"
                )
        elif title is not None:
            raise TypeError("`title` must be either a string or dictionary")
        else:
            return {"label": None}
        return title

    def set_shared_fontdict(self, shared_fontdict):
        orig_rcParams = plt.rcParams.copy()
        if shared_fontdict is None:
            return orig_rcParams
        for k, v in shared_fontdict.items():
            if k not in ["fontsize", "size"]:
                if k in [
                    "cursive",
                    "family",
                    "fantasy",
                    "monospace",
                    "sans-serif",
                    "serif",
                ]:
                    if isinstance(v, str):
                        v = [v]
                if k == "color":
                    plt.rcParams["text.color"] = v
                    plt.rcParams["xtick.color"] = v
                    plt.rcParams["ytick.color"] = v
                    continue
                try:
                    plt.rcParams[f"font.{k}"] = v
                except KeyError as exc:
                    raise KeyError(
                        f"{k} is not a valid key in `sharedfont_dict`"
                        "It must be one of "
                        "'cursive', 'family', 'fantasy', 'monospace', 'sans-serif',"
                        "'serif', 'stretch','style', 'variant', 'weight'"
                    ) from exc
        return orig_rcParams

    def get_writer(self, metadata, fps):
        if self.extension == "gif":
            writer = "imagemagick"
        else:
            writer = FFMpegWriter(
                fps=fps, metadata=metadata, extra_args=["-pix_fmt", "yuv420p"]
            )
        return writer

    def get_fig_kwargs(self, fig_kwargs):
        default_fig_kwargs = {"figsize": (6, 3.5), "dpi": 144}
        if fig_kwargs is None:
            return default_fig_kwargs
        if isinstance(fig_kwargs, dict):
            fig_kwargs = {**default_fig_kwargs, **fig_kwargs}
        else:
            raise TypeError("fig_kwargs must be a dict or None")
        return fig_kwargs

    def get_fig(self, fig):
        if fig is not None and not isinstance(fig, plt.Figure):
            raise TypeError("`fig` must be a matplotlib Figure instance")
        if fig is not None:
            if not fig.axes:
                raise ValueError("The figure passed to `fig` must have an axes")
        else:
            fig = self.create_figure()
        return fig
