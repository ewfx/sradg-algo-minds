import { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [tableData, setTableData] = useState([]);
  const [columnOrder, setColumnOrder] = useState([]);
  const [isProcessed, setIsProcessed] = useState(false);

  const tableWrapperRef = useRef(null);
  const scrollContainerRef = useRef(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);

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

  const fetchData = async (file) => {
    const response = await fetch(`http://127.0.0.1:5000/data/${file}`);
    const data = await response.json();

    if (data.length > 0) {
      const orderedColumns = Object.keys(data[0]).filter(
        (col) => col !== "anomaly_exists" && col !== "anomaly_type"
      );
      setColumnOrder([...orderedColumns, "anomaly_exists", "anomaly_type"]);
    }
    setTableData(data);
  };

  const handleEdit = (index, key, value) => {
    const newData = [...tableData];
    newData[index][key] = value;
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

  return (
    <div>
      <header>Anomaly Detector</header>

      <div className="container">
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload & Process File</button>

        {isProcessed && <button onClick={handleDownload}>Download File</button>}
      </div>

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
                        {key === "anomaly_exists" || key === "anomaly_type" ? (
                          <input
                            type="text"
                            value={row[key]}
                            onChange={(e) => handleEdit(rowIndex, key, e.target.value)}
                          />
                        ) : (
                          row[key]
                        )}
                      </td>
                    ))}
                    <td>
                      <button className="edit-btn">Edit</button>
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
