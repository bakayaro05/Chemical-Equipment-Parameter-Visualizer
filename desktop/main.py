import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QListWidget
)
from api import upload_csv, get_history, get_dataset
from charts import BarChart

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.resize(900, 700)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload)

        self.summary_label = QLabel("Summary")
        self.history = QListWidget()
        self.history.itemClicked.connect(self.load_from_history)

        self.layout.addWidget(self.upload_btn)
        self.layout.addWidget(self.summary_label)
        self.layout.addWidget(QLabel("Upload History (Last 5)"))
        self.layout.addWidget(self.history)

        self.chart = None
        self.load_history()

    def upload(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        data = upload_csv(file_path)
        self.render_summary(data)
        self.load_history()

    def load_history(self):
        self.history.clear()
        datasets = get_history()
        for d in datasets:
            self.history.addItem(f"{d['id']} — {d['summary']['total_equipment']} equipments")

    def load_from_history(self, item):
        dataset_id = item.text().split(" — ")[0]
        data = get_dataset(dataset_id)
        self.render_summary(data["summary"])

    def render_summary(self, data):
        s = data
        self.summary_label.setText(
            f"""
Total Equipment: {s['total_equipment']}
Avg Flowrate: {s['avg_flowrate']}
Avg Pressure: {s['avg_pressure']}
Avg Temperature: {s['avg_temperature']}
"""
        )

        if self.chart:
            self.layout.removeWidget(self.chart)
            self.chart.deleteLater()

        self.chart = BarChart(s)
        self.layout.addWidget(self.chart)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
