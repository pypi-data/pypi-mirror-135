import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


@pd.api.extensions.register_series_accessor("weekly_returns")
class WeeklyReturns:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj.fillna(method="pad").resample("W").last().pct_change()

    @staticmethod
    def _validate(obj):
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    @property
    def srri(self):
        return self._obj.srri

    @property
    def positive_weekly_returns_percentage(self):
        return round(self._obj[self._obj > 0].shape[0] / self._obj.shape[0] * 100, 2)

    @property
    def annualized(self):
        """Returns the annualized return."""
        comp_growth = (1 + self._obj).prod()
        return comp_growth ** (52 / self._obj.shape[0]) - 1

    @property
    def volatility_annualized(self):
        """Returns the annualized volatility."""
        return self._obj.std() * (52 ** 0.5)

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        series_to_plot = self._obj * 100
        series_to_plot.plot(lw=2, alpha=0.7, ax=ax, kind="bar", **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)
        if 'label' in kwargs:
            ax.legend(loc="best")

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        weekly_dates = [i for i in self._obj.index.strftime("%W")]
        ax.set_xticklabels(weekly_dates, fontsize="small")
        ax.tick_params(axis='x', labelrotation=45)

        ax.set_title("Weekly Returns", fontweight="bold")
        return ax
