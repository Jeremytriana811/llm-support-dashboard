/**
 * App.jsx — The main React component for the dashboard.
 *
 * WHAT IS REACT?
 * React is a JavaScript library for building user interfaces. You define
 * "components" (reusable pieces of UI) and React handles updating the
 * page when your data changes.
 *
 * KEY CONCEPTS USED HERE:
 * - useState: stores data that can change (like the list of tickets)
 * - useEffect: runs code when the component first appears (like fetching data)
 * - fetch(): built-in browser function to call APIs
 */

import { useState, useEffect } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

// Register Chart.js components (required by Chart.js v4)
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

// ---------------------------------------------------------------------------
// API base URL — change this when deploying to a cloud server
// ---------------------------------------------------------------------------
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";


// ===========================================================================
// Main App Component
// ===========================================================================
export default function App() {
  // --- State variables (data that changes over time) ---
  const [tickets, setTickets] = useState([]);
  const [metrics, setMetrics] = useState({ total: 0, by_category: {} });
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // --- Fetch data when the page first loads ---
  useEffect(() => {
    fetchTickets();
    fetchMetrics();
  }, []);

  // --- API call functions ---
  async function fetchTickets() {
    try {
      const res = await fetch(`${API_URL}/tickets`);
      const data = await res.json();
      setTickets(data);
    } catch (err) {
      console.error("Failed to fetch tickets:", err);
    }
  }

  async function fetchMetrics() {
    try {
      const res = await fetch(`${API_URL}/metrics/tickets`);
      const data = await res.json();
      setMetrics(data);
    } catch (err) {
      console.error("Failed to fetch metrics:", err);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault(); // Prevent page reload
    if (!title.trim() || !description.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_URL}/tickets`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description }),
      });

      if (!res.ok) throw new Error("Failed to create ticket");

      // Clear the form and refresh data
      setTitle("");
      setDescription("");
      await fetchTickets();
      await fetchMetrics();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // --- Chart data ---
  const chartData = {
    labels: Object.keys(metrics.by_category),
    datasets: [
      {
        label: "Tickets by Category",
        data: Object.values(metrics.by_category),
        backgroundColor: [
          "#ef4444", // red (bug)
          "#3b82f6", // blue (feature)
          "#f59e0b", // amber (question)
          "#10b981", // green (documentation)
          "#8b5cf6", // purple (other)
        ],
        borderRadius: 6,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: true, text: "Tickets by Category", font: { size: 16 } },
    },
    scales: {
      y: { beginAtZero: true, ticks: { stepSize: 1 } },
    },
  };

  // --- Category badge colors ---
  const categoryColors = {
    bug: "#fecaca",
    feature: "#bfdbfe",
    question: "#fde68a",
    documentation: "#a7f3d0",
  };

  // ===========================================================================
  // Render the UI
  // ===========================================================================
  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <h1 style={styles.headerTitle}>🤖 LLM Support Dashboard</h1>
        <p style={styles.headerSub}>
          AI-powered ticket classification & summarization
        </p>
      </header>

      {/* Stats Cards */}
      <div style={styles.statsRow}>
        <div style={styles.statCard}>
          <div style={styles.statNumber}>{metrics.total}</div>
          <div style={styles.statLabel}>Total Tickets</div>
        </div>
        {Object.entries(metrics.by_category).map(([cat, count]) => (
          <div key={cat} style={styles.statCard}>
            <div style={styles.statNumber}>{count}</div>
            <div style={styles.statLabel}>{cat}</div>
          </div>
        ))}
      </div>

      {/* Two-column layout: Form + Chart */}
      <div style={styles.twoCol}>
        {/* New Ticket Form */}
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Create New Ticket</h2>
          <div>
            <input
              type="text"
              placeholder="Ticket title..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              style={styles.input}
            />
            <textarea
              placeholder="Describe the issue in detail..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={4}
              style={{ ...styles.input, resize: "vertical" }}
            />
            <button
              onClick={handleSubmit}
              disabled={loading || !title.trim() || !description.trim()}
              style={{
                ...styles.button,
                opacity: loading ? 0.6 : 1,
              }}
            >
              {loading ? "⏳ AI is classifying..." : "Submit Ticket"}
            </button>
            {error && <p style={{ color: "#ef4444", marginTop: 8 }}>{error}</p>}
          </div>
        </div>

        {/* Chart */}
        <div style={styles.card}>
          <Bar data={chartData} options={chartOptions} />
        </div>
      </div>

      {/* Tickets Table */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>All Tickets</h2>
        {tickets.length === 0 ? (
          <p style={{ color: "#6b7280", textAlign: "center", padding: 32 }}>
            No tickets yet. Create one above!
          </p>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>ID</th>
                  <th style={styles.th}>Title</th>
                  <th style={styles.th}>Category</th>
                  <th style={styles.th}>AI Summary</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map((t) => (
                  <tr key={t.id}>
                    <td style={styles.td}>{t.id}</td>
                    <td style={{ ...styles.td, fontWeight: 500 }}>{t.title}</td>
                    <td style={styles.td}>
                      <span
                        style={{
                          ...styles.badge,
                          backgroundColor:
                            categoryColors[t.category] || "#e5e7eb",
                        }}
                      >
                        {t.category}
                      </span>
                    </td>
                    <td style={{ ...styles.td, color: "#4b5563", fontSize: 13 }}>
                      {t.summary}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer style={styles.footer}>
        Built with FastAPI, React, Hugging Face Transformers, PostgreSQL & Docker
      </footer>
    </div>
  );
}


// ===========================================================================
// Inline Styles (keeps everything in one file for simplicity)
// ===========================================================================
const styles = {
  container: {
    fontFamily: "'Inter', -apple-system, sans-serif",
    maxWidth: 1100,
    margin: "0 auto",
    padding: "24px 16px",
    backgroundColor: "#f9fafb",
    minHeight: "100vh",
  },
  header: {
    textAlign: "center",
    marginBottom: 32,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 700,
    color: "#111827",
    margin: 0,
  },
  headerSub: {
    fontSize: 14,
    color: "#6b7280",
    marginTop: 4,
  },
  statsRow: {
    display: "flex",
    gap: 16,
    marginBottom: 24,
    flexWrap: "wrap",
  },
  statCard: {
    flex: "1 1 120px",
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: "20px 16px",
    textAlign: "center",
    boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 700,
    color: "#111827",
  },
  statLabel: {
    fontSize: 13,
    color: "#6b7280",
    textTransform: "capitalize",
    marginTop: 4,
  },
  twoCol: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 24,
    marginBottom: 24,
  },
  card: {
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 24,
    boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
    marginBottom: 0,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 600,
    color: "#111827",
    marginTop: 0,
    marginBottom: 16,
  },
  input: {
    width: "100%",
    padding: "10px 12px",
    border: "1px solid #d1d5db",
    borderRadius: 8,
    fontSize: 14,
    marginBottom: 12,
    boxSizing: "border-box",
    fontFamily: "inherit",
  },
  button: {
    width: "100%",
    padding: "12px",
    backgroundColor: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: 8,
    fontSize: 15,
    fontWeight: 600,
    cursor: "pointer",
    fontFamily: "inherit",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: 14,
  },
  th: {
    textAlign: "left",
    padding: "12px 16px",
    borderBottom: "2px solid #e5e7eb",
    color: "#374151",
    fontWeight: 600,
    fontSize: 13,
    textTransform: "uppercase",
    letterSpacing: "0.05em",
  },
  td: {
    padding: "12px 16px",
    borderBottom: "1px solid #f3f4f6",
  },
  badge: {
    display: "inline-block",
    padding: "4px 12px",
    borderRadius: 20,
    fontSize: 12,
    fontWeight: 600,
    textTransform: "capitalize",
  },
  footer: {
    textAlign: "center",
    color: "#9ca3af",
    fontSize: 12,
    marginTop: 48,
    paddingTop: 24,
    borderTop: "1px solid #e5e7eb",
  },
};
