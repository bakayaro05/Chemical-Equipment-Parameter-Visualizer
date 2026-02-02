from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class BarChart(FigureCanvasQTAgg):
    def __init__(self, data):
        fig = Figure(figsize=(5, 4))
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.plot(data)

    def plot(self, summary):
        self.ax.clear()

        types = summary["type_distribution"]
        names = list(types.keys())
        values = list(types.values())

        self.ax.bar(names, values)
        self.ax.set_title("Equipment Type Distribution")
        self.ax.set_ylabel("Count")
        self.ax.tick_params(axis='x', rotation=30)

        self.draw()
