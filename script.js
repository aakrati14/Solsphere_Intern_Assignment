// Fetch all reports and apply optional OS filter
async function fetchAllReports() {
  const allReportsDiv = document.getElementById("all-reports");
  const osFilter = document.getElementById("os-filter").value;
  allReportsDiv.innerHTML = "Loading...";

  try {
    const response = await fetch("http://127.0.0.1:5000/reports");
    if (!response.ok) throw new Error("API error: " + response.status);
    const data = await response.json();

    if (!Array.isArray(data) || data.length === 0) {
      allReportsDiv.innerHTML = "<p>No reports found.</p>";
      return;
    }

    const filtered = osFilter
      ? data.filter((r) => r.os_update === osFilter)
      : data;

    allReportsDiv.innerHTML = "";
    filtered.forEach((report) => {
      const reportCard = document.createElement("div");
      reportCard.className = "report-card";

      // Add issue class if there's a problem
      const hasIssue =
        report.disk_encryption === "False" ||
        report.os_update === "Might be outdated" ||
        report.antivirus === "Antivirus not active" ||
        report.sleep_settings !== "Enabled (≤10min)";

      if (hasIssue) {
        reportCard.classList.add("issue");
      }

      reportCard.innerHTML = `
        <h4>Device: ${report.device_id}</h4>
        <ul>
          <li><strong>Timestamp:</strong> ${report.timestamp}</li>
          <li><strong>Disk Encryption:</strong> ${report.disk_encryption}</li>
          <li><strong>OS Update:</strong> ${report.os_update}</li>
          <li><strong>Antivirus:</strong> ${report.antivirus}</li>
          <li><strong>Sleep Settings:</strong> ${report.sleep_settings}</li>
        </ul>
      `;
      allReportsDiv.appendChild(reportCard);
    });
  } catch (error) {
    console.error("Error fetching all reports:", error);
    allReportsDiv.innerHTML = `<span style="color:red;">Error loading all reports</span>`;
  }
}

// Export current data to CSV
async function exportToCSV() {
  try {
    const response = await fetch("http://127.0.0.1:5000/reports");
    const data = await response.json();

    if (!Array.isArray(data)) return;

    const headers = [
      "Device ID",
      "Timestamp",
      "Disk Encryption",
      "OS Update",
      "Antivirus",
      "Sleep Settings",
    ];

    const rows = data.map((r) => [
      r.device_id,
      r.timestamp,
      r.disk_encryption,
      r.os_update,
      r.antivirus,
      r.sleep_settings,
    ]);

    const csvContent =
      "data:text/csv;charset=utf-8," +
      [headers.join(","), ...rows.map((row) => row.join(","))].join("\n");

    const link = document.createElement("a");
    link.setAttribute("href", encodeURI(csvContent));
    link.setAttribute("download", "system_reports.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (err) {
    alert("Failed to export CSV");
    console.error(err);
  }
}

// Fetch specific device
document.getElementById("fetch-button").addEventListener("click", async () => {
  const deviceId = document.getElementById("device-id").value;
  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "Fetching...";

  try {
    const response = await fetch(`http://127.0.0.1:5000/latest/${deviceId}`);
    const data = await response.json();

    if (data.error) {
      resultDiv.innerHTML = `<span style="color:red;">Error: ${data.error}</span>`;
    } else {
      resultDiv.innerHTML = `
        <h3>Latest Report for ${data.device_id}</h3>
        <ul>
            <li><strong>Timestamp:</strong> ${data.timestamp}</li>
            <li><strong>Disk Encryption:</strong> ${data.disk_encryption}</li>
            <li><strong>OS Update:</strong> ${data.os_update}</li>
            <li><strong>Antivirus:</strong> ${data.antivirus}</li>
            <li><strong>Sleep Settings:</strong> ${data.sleep_settings}</li>
        </ul>
      `;
    }
  } catch (error) {
    resultDiv.innerHTML = `<span style="color:red;">Error fetching data</span>`;
    console.error("Fetch error:", error);
  }
});

// Trigger fetch and export
document
  .getElementById("os-filter")
  .addEventListener("change", fetchAllReports);
document.getElementById("export-btn").addEventListener("click", exportToCSV);

// Initial load
fetchAllReports();
