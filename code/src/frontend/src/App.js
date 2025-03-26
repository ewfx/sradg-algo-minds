import { useState, useEffect, useRef } from "react";
import "./App.css";
import { anomalyOptions, addAnomalyType } from "./anomalyTypes";


function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [tableData, setTableData] = useState([]);
  const [columnOrder, setColumnOrder] = useState([]);
  const [isProcessed, setIsProcessed] = useState(false);
  const [editingRow, setEditingRow] = useState(null);
  const [newAnomaly, setNewAnomaly] = useState(""); // State for new anomaly input
  const [showModal, setShowModal] = useState(false); // State to show modal
  const [message, setMessage] = useState('');

  const tableWrapperRef = useRef(null);
  const scrollContainerRef = useRef(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  
    const handleSendMail = async (index) => {
        try {
            const response = await fetch("http://127.0.0.1:5000/send-mail", {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            });
            const data = await response.json();
            setMessage(data.message);
        } catch (error) {
            setMessage("Error sending email.");
        }
    };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);

    //Upload API
    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (response.ok) {
      setFilename(data.filename);
      fetchData(data.filename);
      setIsProcessed(true);
    } else {
      alert(data.error);
    }
  };

  //Update Row Data
  const handleRowEdit = async (index) => {
    if (editingRow === index) {
        // Save the row to the backend
        await saveRowData(index, tableData[index]);

        // Show success popup
        alert("Row data saved successfully!");

        setEditingRow(null); // Exit edit mode
    } else {
        setEditingRow(index); // Enter edit mode
    }
  };

  const saveRowData = async (index, rowData) => {
    if (!filename) return;

    const response = await fetch("http://127.0.0.1:5000/update-row", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ filename, rowIndex: index, rowData }),
        mode: "cors",  // Ensure cross-origin request handling
        // credentials: "include",  // Allow cookies if needed
    });

    const data = await response.json();
    if (!response.ok) {
        alert("Error updating row: " + data.error);
    }
  };




  //Fetch Data API
  const fetchData = async (file) => {
    const response = await fetch(`http://127.0.0.1:5000/data/${file}`);
    const data = await response.json();

    //Add 2 new columns in table
    if (data.length > 0) {
      const orderedColumns = Object.keys(data[0]).filter(
        (col) => col !== "Match Status" && col !== "Anomaly Type" && col!="Comments"
      );
      setColumnOrder([...orderedColumns, "Match Status", "Anomaly Type", "Comments"]);
    }
    setTableData(data);
  };

  const handleEdit = (index, key, value) => {
    const newData = [...tableData];
    newData[index][key] = value;
    if (key === "Match Status" && value === "Match") {
      newData[index]["Anomaly Type"] = ""; // Clear dropdown value
    }
    setTableData(newData);
  };

  //Synchronize horizontal scrolling between table and fixed scrollbar
  useEffect(() => {
    const syncScroll = () => {
      if (scrollContainerRef.current && tableWrapperRef.current) {
        scrollContainerRef.current.scrollLeft = tableWrapperRef.current.scrollLeft;
      }
    };

    const syncScrollContainer = () => {
      if (scrollContainerRef.current && tableWrapperRef.current) {
        tableWrapperRef.current.scrollLeft = scrollContainerRef.current.scrollLeft;
      }
    };

    if (tableWrapperRef.current && scrollContainerRef.current) {
      tableWrapperRef.current.addEventListener("scroll", syncScroll);
      scrollContainerRef.current.addEventListener("scroll", syncScrollContainer);
    }

    return () => {
      if (tableWrapperRef.current && scrollContainerRef.current) {
        tableWrapperRef.current.removeEventListener("scroll", syncScroll);
        scrollContainerRef.current.removeEventListener("scroll", syncScrollContainer);
      }
    };
  }, []);

  const handleDownload = () => {
    if (!filename) return alert("No file available for download");
    window.location.href = `http://127.0.0.1:5000/download/${filename}`;
  };


  //Handle add new anomaly
  const handleAddAnomaly = () => {
    if (newAnomaly.trim() === "") {
      alert("Anomaly type cannot be empty.");
      return;
    }
    addAnomalyType(newAnomaly);
    setNewAnomaly("");
    setShowModal(false); // Close modal after adding
  };


  return (
    <div>
       <header>Anomaly Detector
        <div className="logo_container"  >
        <img src={ require('./logo.png') } />
        </div>
      </header>

      <div className="container">
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload & Process File</button>

        {isProcessed && (
          <div className="button-container">
            <button onClick={handleDownload}>Download File</button>
            <button onClick={() => setShowModal(true)}>Add New Anomaly Type</button>
          </div>
        )}
      </div>

        {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Add New Anomaly Type</h3>
            <input
              type="text"
              value={newAnomaly}
              onChange={(e) => setNewAnomaly(e.target.value)}
              placeholder="Enter anomaly type"
            />
            <button onClick={handleAddAnomaly}>Add</button>
            <button onClick={() => setShowModal(false)}>Cancel</button>
          </div>
        </div>
      )}

      {tableData.length > 0 && (
        <>
          <div className="table-wrapper" ref={tableWrapperRef}>
            <table>
              <thead>
                <tr>
                  {columnOrder.map((col, index) => (
                    <th key={index}>{col}</th>
                  ))}
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {tableData.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {columnOrder.map((key, colIndex) => (
                      <td key={colIndex}>
                      {key === "Match Status" ? (
                        <select value={row[key]} onChange={(e) => handleEdit(rowIndex, key, e.target.value)}>
                          <option value="Match">Match</option>
                          <option value="Break">Break</option>
                        </select>
                      ) : key === "Anomaly Type" ? (
                        <select value={row[key]} onChange={(e) => {
                          handleEdit(rowIndex, key,  e.target.value)}}
                          disabled={row["Match Status"] == "Match"} 
                        >
                         {anomalyOptions.map((option, idx) => (
                            <option key={idx} value={option}>{option}</option>
                          ))}
                        </select>
                      ) : key === "Comments" ? (
                        <input
                          type="text"
                          value={row[key] || ""}
                          onChange={(e) => handleEdit(rowIndex, key, e.target.value)}
                        />
                      ) : (
                        row[key]
                      )}
                    </td>
                    ))}
                    <td>
                      <button className="edit-btn" onClick={() => handleRowEdit(rowIndex)}>
                      {editingRow === rowIndex ? "Save" : "Edit"}
                      </button >
                      <button className="edit-btn-email" onClick={() => handleSendMail(rowIndex)} >
                        Send Mail
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Fixed Scrollbar */}
          <div className="scroll-container" ref={scrollContainerRef}>
            <div className="scroll-content" style={{ width: tableWrapperRef.current?.scrollWidth || "100%" }}></div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
