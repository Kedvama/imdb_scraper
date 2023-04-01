import plotly.express as px


class FigureMaker:
    def __init__(self, serie):
        self.serie = serie
        self.df = serie.get_dict()
        self.refactor()
        self.figure1 = self.fig1()
        self.figure2 = self.fig2()
        self.figure3 = self.fig3()

    def refactor(self):
        self.df.rename(index=lambda x: f"Episode {x + 1}", inplace=True)

    def fig1(self):
        # Figure1 is a linechart with the mean per season
        figure1 = px.line(self.df.astype(float).mean().round(1), x=self.df.astype(float).mean().round(1).index,
                          y=self.df.astype(float).mean().round(1).values,
                          title=f"{self.serie.get_showname()}: Season mean",
                          markers=True).update_layout(xaxis_title="Season",
                                                      yaxis_title="Mean rating")

        return figure1

    def fig2(self):
        # Figure2 is a linechart with all episode rating per season
        figure2 = px.line(self.df.melt(ignore_index=False),
                          x=self.df.melt(ignore_index=False).index.values,
                          y=self.df.melt(ignore_index=False)["value"].astype(float),
                          color=self.df.melt(ignore_index=False)["variable"],
                          title=self.serie.get_showname(),
                          markers=True).update_layout(xaxis_title="Season",
                                                      yaxis_title="Rating")

        return figure2

    def fig3(self):
        # name with the figure
        figure3 = px.imshow(self.df.T, color_continuous_scale='RdBu_r', text_auto=True)
        return figure3
