import React, { useState, useEffect } from "react";
import API from "./api";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

function App() {
  const [summary, setSummary] = useState(null);
  const [file, setFile] = useState(null);

  const [history, setHistory] = useState([]);

const loadHistory = async () => {
  const res = await API.get("history/");
  setHistory(res.data);
};

useEffect(() => {
  loadHistory();
}, []);


const loadDataset = async (id) => {
  const res = await fetch(`http://127.0.0.1:8000/api/dataset/${id}/`);
  const data = await res.json();

  setSummary(data.summary);
};


const uploadCSV = async () => {
  if (!file) {
    alert("Please select a CSV file first");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const res = await API.post("upload/", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });

  setSummary(res.data);
  loadHistory(); // refresh history after upload
};


  return (
    <div style={{ padding: "20px" }}>
      <h2>Chemical Equipment Parameter Visualizer</h2>

      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={uploadCSV}>Upload CSV</button>

      {summary && (
        <>
          <h3>Summary</h3>
          <p>Total Equipment: {summary.total_equipment}</p>
          <p>Avg Flowrate: {summary.avg_flowrate}</p>
          <p>Avg Pressure: {summary.avg_pressure}</p>
          <p>Avg Temperature: {summary.avg_temperature}</p>

          <Bar
            data={{
              labels: Object.keys(summary.type_distribution),
              datasets: [
                {
                  label: "Equipment Count",
                  data: Object.values(summary.type_distribution),
                  backgroundColor: "rgba(54, 162, 235, 0.6)"
                }
              ]
            }}
          />
        </>
      )}

      <br />
      <a href="http://127.0.0.1:8000/api/pdf/" target="_blank" rel="noreferrer">
        Download PDF Report
      </a>

      <h3>Upload History (Last 5)</h3>
<ul>
 {history.map(item => (
  <div
    key={item.id}
    onClick={() => loadDataset(item.id)}
    style={{ cursor: "pointer", padding: "8px", borderBottom: "1px solid #ccc" }}
  >
    Dataset #{item.id} – Total Equipment: {item.summary.total_equipment}
  </div>
))}

</ul>

    </div>
    
  );
}

export default App;
