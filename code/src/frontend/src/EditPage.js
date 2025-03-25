import React, { useState } from "react";
import { anomalyOptions, addAnomalyType } from "./anomalyTypes";
import { useLocation, useNavigate } from "react-router-dom";
import "./App.css"; // Reuse CSS styles

const EditPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const rowData = location.state?.rowData || {};
  const rowIndex = location.state?.rowIndex;

  const [anomalyExists, setAnomalyExists] = useState(rowData.anomaly_exists);
  const [anomalyType, setAnomalyType] = useState(rowData.anomaly_type);
  const [newAnomalyType, setNewAnomalyType] = useState("");
  const [comment, setComment] = useState(rowData.comment || "");

  const handleSave = () => {
    const updatedRow = {
      ...rowData,
      anomaly_exists: anomalyExists,
      anomaly_type: anomalyType,
      comment,
    };

    // Redirect to main page with updated data
    navigate("/", { state: { updatedData: updatedRow, rowIndex } });
  };

  const handleAddAnomalyType = () => {
    if (newAnomalyType.trim() !== "") {
      addAnomalyType(newAnomalyType);
      setAnomalyType(newAnomalyType);
      setNewAnomalyType("");
    }
  };

  return (
    <div className="edit-container">
      <h2>Edit Row Data</h2>
      <div className="edit-form">
        {Object.entries(rowData).map(([key, value]) => (
          key !== "anomaly_exists" && key !== "anomaly_type" && key !== "comment" ? (
            <div key={key} className="edit-row">
              <strong>{key}:</strong> <span>{value}</span>
            </div>
          ) : null
        ))}

        <div className="edit-row">
          <strong>Anomaly Exists:</strong>
          <select value={anomalyExists} onChange={(e) => setAnomalyExists(e.target.value)}>
            <option value="Break">Break</option>
            <option value="Match">Match</option>
          </select>
        </div>

        <div className="edit-row">
          <strong>Anomaly Type:</strong>
          <select value={anomalyType} onChange={(e) => setAnomalyType(e.target.value)}>
            {anomalyOptions.map((option, i) => (
              <option key={i} value={option}>{option}</option>
            ))}
          </select>
        </div>

        <div className="edit-row">
          <strong>Add New Anomaly Type:</strong>
          <input type="text" value={newAnomalyType} onChange={(e) => setNewAnomalyType(e.target.value)} />
          <button onClick={handleAddAnomalyType}>Add</button>
        </div>

        <div className="edit-row">
          <strong>Comment:</strong>
          <textarea value={comment} onChange={(e) => setComment(e.target.value)} />
        </div>

        <button onClick={handleSave}>Save</button>
      </div>
    </div>
  );
};

export default EditPage;
