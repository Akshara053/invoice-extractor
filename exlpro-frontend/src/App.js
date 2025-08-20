import React, { useState, useEffect, useRef } from "react";
import "./App.css";
import logo from "./logo.png";
import { FaUser, FaUpload, FaHistory, FaInfoCircle, FaSignOutAlt, FaMoon, FaSun, FaChartBar, FaBell, FaPlus, FaRocket, FaShieldAlt, FaBolt, FaSearch, FaFilter, FaCloudUploadAlt, FaDownload, FaTrash, FaEye, FaEdit } from "react-icons/fa";
import { API_BASE } from "./config";
import Header from "./components/Header.jsx";

const defaultProfile = {
  username: "",
  email: "",
  full_name: "",
  phone: "",
  company: "",
  address: "",
  city: "",
  state: "",
  country: "",
  zip: "",
  bio: "",
};

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [file, setFile] = useState(null);
  const [invoiceType, setInvoiceType] = useState("printed");
  const [uploading, setUploading] = useState(false);
  const [excelUrl, setExcelUrl] = useState("");
  const [wordUrl, setWordUrl] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState([]);
  const [activeTab, setActiveTab] = useState("profile");
  const [profile, setProfile] = useState(defaultProfile);
  const [editingProfile, setEditingProfile] = useState(false);
  const [darkMode, setDarkMode] = useState(localStorage.getItem("darkMode") === "true");
  const [notifications, setNotifications] = useState([]);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("all");
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [draftProfile, setDraftProfile] = useState(defaultProfile);

  // Only send fields the backend supports
  const buildProfilePayload = (p) => ({
    email: p.email || "",
    full_name: p.full_name || "",
    phone: p.phone || "",
    company: p.company || "",
    address: p.address || "",
    city: p.city || "",
    state: p.state || "",
    country: p.country || "",
    zip: p.zip || "",
    bio: p.bio || "",
  });

  const saveProfile = async (partial = {}) => {
    if (!token || token.trim() === "") {
      addNotification('error', 'Please log in again.');
      return;
    }
    try {
      const payload = buildProfilePayload({ ...profile, ...partial });
      const response = await fetch(`${API_BASE}/api/profile`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (data.message) {
        setEditingProfile(false);
        await fetchProfile(token);
        setMessage("Profile updated successfully!");
        addNotification('success', 'Profile saved');
      } else if (data.error) {
        setError(data.error);
        addNotification('error', data.error);
      }
    } catch (err) {
      setError("Failed to update profile. Please try again.");
      addNotification('error', 'Failed to update profile');
    }
  };

  // Apply dark mode on mount and when it changes
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    localStorage.setItem("darkMode", darkMode.toString());
  }, [darkMode]);

  // Fetch history and profile after login
  useEffect(() => {
    if (token && token.trim() !== "") {
      fetchHistory(token);
      fetchProfile(token);
    }
  }, [token]);

  // Add floating particles
  useEffect(() => {
    const particles = [];
    for (let i = 0; i < 9; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = `${Math.random() * 100}%`;
      particle.style.animationDelay = `${Math.random() * 6}s`;
      document.body.appendChild(particle);
      particles.push(particle);
    }

    return () => {
      particles.forEach(particle => particle.remove());
    };
  }, []);

  const addNotification = (type, message) => {
    const id = Date.now();
    const notification = { id, type, message };
    setNotifications(prev => [...prev, notification]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== id));
    }, 5000);
  };

  const fetchHistory = async (token) => {
    if (!token || token.trim() === "") return;
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/api/history`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (data.history) {
        setHistory(data.history);
      }
    } catch (err) {
      addNotification('error', 'Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const fetchProfile = async (token) => {
    if (!token || token.trim() === "") return;
    try {
      const response = await fetch(`${API_BASE}/api/profile`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (data.username) {
        setProfile({
          ...defaultProfile,
          ...data,
        });
        setUsername(data.username);
      } else if (data.error) {
        addNotification('error', data.error);
      }
    } catch (err) {
      addNotification('error', 'Failed to load profile');
    }
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    if (!username || !password) {
      setError("Please enter username and password.");
      return;
    }
    try {
      const response = await fetch(
        `${API_BASE}/api/${isLogin ? "login" : "register"}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        }
      );
      const data = await response.json();
      if (data.error) {
        setError(data.error);
        addNotification('error', data.error);
      } else if (isLogin) {
        setToken(data.token);
        localStorage.setItem("token", data.token);
        setMessage("Login successful!");
        addNotification('success', 'Login successful!');
        setActiveTab("profile");
      } else {
        setMessage("Registration successful! Please log in.");
        addNotification('success', 'Registration successful! Please log in.');
        setIsLogin(true);
      }
    } catch (err) {
      setError("Server error. Please try again.");
      addNotification('error', 'Server error. Please try again.');
    }
  };

  const handleLogout = () => {
    setToken("");
    localStorage.removeItem("token");
    setExcelUrl("");
    setWordUrl("");
    setMessage("Logged out.");
    addNotification('success', 'Logged out successfully');
    setHistory([]);
    setProfile(defaultProfile);
    setActiveTab("profile");
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setExcelUrl("");
    setWordUrl("");
    setError("");
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && (droppedFile.type === 'application/pdf' || droppedFile.type.startsWith('image/'))) {
      setFile(droppedFile);
      setExcelUrl("");
      setWordUrl("");
      setError("");
      addNotification('success', 'File dropped successfully!');
    } else {
      addNotification('error', 'Please drop a PDF or image file');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a PDF or image file.");
      addNotification('error', 'Please select a PDF or image file');
      return;
    }
    if (!token || token.trim() === "") {
      setError("Please log in again (missing token).");
      addNotification('error', 'Please log in again.');
      return;
    }
    setUploading(true);
    setError("");
    setExcelUrl("");
    setWordUrl("");
    setUploadProgress(0);
    
    const formData = new FormData();
    formData.append("file", file);
    formData.append("invoice_type", invoiceType);

    // Simulate upload progress
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 10;
      });
    }, 200);

    try {
      const response = await fetch(`${API_BASE}/api/upload`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });
      const data = await response.json();
      if (data.error) {
        setError(data.error);
        addNotification('error', data.error);
      } else {
        setExcelUrl(data.excel_url);
        setWordUrl(data.word_url);
        setUploadProgress(100);
        addNotification('success', 'File uploaded and processed successfully!');
        fetchHistory(token);
      }
    } catch (err) {
      setError("Upload failed. Is the backend running?");
      addNotification('error', 'Upload failed. Please try again.');
    }
    setUploading(false);
    clearInterval(progressInterval);
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    if (!darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    localStorage.setItem("darkMode", (!darkMode).toString());
  };

  // Apply dark mode on mount
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [darkMode]);

  const filteredHistory = history.filter(item => {
    const matchesSearch = item.original_filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.invoice_type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === "all" || item.invoice_type === filterType;
    return matchesSearch && matchesFilter;
  });

  // Sidebar navigation
  const Sidebar = () => (
    <nav className="sidebar">
      <div className="sidebar-logo">
        <img src={logo} alt="EXLPRO Logo" />
      </div>
      <ul>
        <li
          className={activeTab === "profile" ? "active" : ""}
          onClick={() => setActiveTab("profile")}
        >
          <FaUser /> Profile
        </li>
        <li
          className={activeTab === "upload" ? "active" : ""}
          onClick={() => setActiveTab("upload")}
        >
          <FaUpload /> Upload Invoice
        </li>
        <li
          className={activeTab === "history" ? "active" : ""}
          onClick={() => setActiveTab("history")}
        >
          <FaHistory /> History
        </li>
        <li
          className={activeTab === "about" ? "active" : ""}
          onClick={() => setActiveTab("about")}
        >
          <FaInfoCircle /> About
        </li>
        <li onClick={handleLogout} className="logout-link">
          <FaSignOutAlt /> Logout
        </li>
      </ul>
    </nav>
  );

  // Stats Dashboard Component
  const StatsDashboard = () => (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-number">{history.length}</div>
        <div className="stat-label">Total Uploads</div>
      </div>
      <div className="stat-card">
        <div className="stat-number">{history.filter(h => h.excel_filename).length}</div>
        <div className="stat-label">Excel Files</div>
      </div>
      <div className="stat-card">
        <div className="stat-number">{history.filter(h => h.word_filename).length}</div>
        <div className="stat-label">Word Files</div>
      </div>
      <div className="stat-card">
        <div className="stat-number">{history.filter(h => h.invoice_type === 'printed').length}</div>
        <div className="stat-label">Printed Invoices</div>
      </div>
    </div>
  );

  // Notification Center
  const NotificationCenter = () => (
    <div className="notification-center">
      {notifications.map(notification => (
        <div key={notification.id} className={`notification ${notification.type}`}>
          {notification.message}
        </div>
      ))}
    </div>
  );

  // Main content for each tab
  const ProfileTab = () => {
    const formRef = useRef(null);
    const handleSaveClick = async () => {
      if (!formRef.current) return;
      const fd = new FormData(formRef.current);
      const payload = {
        email: (fd.get('email') || '').toString(),
        full_name: (fd.get('full_name') || '').toString(),
        phone: (fd.get('phone') || '').toString(),
        company: (fd.get('company') || '').toString(),
        address: (fd.get('address') || '').toString(),
        city: (fd.get('city') || '').toString(),
        state: (fd.get('state') || '').toString(),
        country: (fd.get('country') || '').toString(),
        zip: (fd.get('zip') || '').toString(),
        bio: (fd.get('bio') || '').toString(),
      };
      await saveProfile(payload);
    };
    return (
    <div className="tab-content profile-card">
      <div className="profile-header">
        <div className="avatar-edit">
          <div className="avatar-circle">
            {profile.full_name
              ? profile.full_name
                  .split(" ")
                  .map((n) => n[0])
                  .join("")
                  .toUpperCase()
              : profile.username
              ? profile.username[0].toUpperCase()
              : "U"}
          </div>
        </div>
        <h2>Profile</h2>
        <div style={{ marginLeft: "auto", display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <button type="button" className="edit-profile-btn" onClick={() => fetchProfile(token)} title="Refresh profile">
            Refresh
          </button>
        </div>
      </div>
      
      <StatsDashboard />
      
      {loading ? (
        <div className="skeleton">
          <div className="skeleton-text"></div>
          <div className="skeleton-text"></div>
          <div className="skeleton-text"></div>
        </div>
      ) : (
        <>
          {!editingProfile ? (
            <div className="profile-fields-grid">
              <div>
                <label>Username:</label>
                <span className="profile-value">{profile.username}</span>
              </div>
              <div>
                <label>Email:</label>
                <span className="profile-value">{profile.email || <span style={{ color: "#888" }}>(not set)</span>}</span>
              </div>
              <div>
                <label>Full Name:</label>
                <span className="profile-value">{profile.full_name || <span style={{ color: "#888" }}>(not set)</span>}</span>
              </div>
              <div>
                <label>Phone:</label>
                <span className="profile-value">{profile.phone || <span style={{ color: "#888" }}>(not set)</span>}</span>
              </div>
              <div>
                <label>Company:</label>
                <span className="profile-value">{profile.company || <span style={{ color: "#888" }}>(not set)</span>}</span>
              </div>
              <div>
                <label>Address:</label>
                <span className="profile-value">{profile.address || <span style={{ color: "#888" }}>(not set)</span>}</span>
              </div>
              <div>
                <label>City:</label>
                <span className="profile-value">{profile.city || <span style={{ color: "#888" }}>(not set)</span>}</span>
              </div>
              <div>
                <label>State:</label>
                <span className="profile-value">{profile.state || <span style={{ color: "#888" }}>(not set)</span>}</span>
              </div>
              <div>
                <label>Country:</label>
                <span className="profile-value">{profile.country || <span style={{ color: "#888" }}>(not set)</span>}</span>
              </div>
              <div>
                <label>Zip:</label>
                <span className="profile-value">{profile.zip || <span style={{ color: "#888" }}>(not set)</span>}</span>
              </div>
              <div style={{ gridColumn: "1 / -1" }}>
                <label>Bio:</label>
                <span className="profile-value">{profile.bio || <span style={{ color: "#888" }}>(not set)</span>}</span>
              </div>
            </div>
          ) : (
            <form
              ref={formRef}
              className="profile-edit-form profile-fields-grid"
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); } }}
            >
              <div>
                <label>Username:</label>
                <input
                  type="text"
                  defaultValue={profile.username}
                  disabled
                  style={{ background: "#f5f7fa", color: "#888" }}
                />
              </div>
              <div>
                <label>Email:</label>
                <input
                  type="email"
                  name="email"
                  defaultValue={profile.email || ""}
                  placeholder="Enter your email"
                  style={{ marginLeft: 0 }}
                />
              </div>
              <div>
                <label>Full Name:</label>
                <input
                  type="text"
                  name="full_name"
                  defaultValue={profile.full_name || ""}
                  placeholder="Enter your full name"
                />
              </div>
              <div>
                <label>Phone:</label>
                <input
                  type="text"
                  name="phone"
                  defaultValue={profile.phone || ""}
                  placeholder="Enter your phone number"
                />
              </div>
              <div>
                <label>Company:</label>
                <input
                  type="text"
                  name="company"
                  defaultValue={profile.company || ""}
                  placeholder="Enter your company name"
                />
              </div>
              <div>
                <label>Address:</label>
                <input
                  type="text"
                  name="address"
                  defaultValue={profile.address || ""}
                  placeholder="Enter your address"
                />
              </div>
              <div>
                <label>City:</label>
                <input
                  type="text"
                  name="city"
                  defaultValue={profile.city || ""}
                  placeholder="Enter your city"
                />
              </div>
              <div>
                <label>State:</label>
                <input
                  type="text"
                  name="state"
                  defaultValue={profile.state || ""}
                  placeholder="Enter your state"
                />
              </div>
              <div>
                <label>Country:</label>
                <input
                  type="text"
                  name="country"
                  defaultValue={profile.country || ""}
                  placeholder="Enter your country"
                />
              </div>
              <div>
                <label>Zip:</label>
                <input
                  type="text"
                  name="zip"
                  defaultValue={profile.zip || ""}
                  placeholder="Enter your zip code"
                />
              </div>
              <div style={{ gridColumn: "1 / -1" }}>
                <label>Bio:</label>
                <input
                  type="text"
                  name="bio"
                  defaultValue={profile.bio || ""}
                  placeholder="Enter your bio"
                />
              </div>
              <div style={{ gridColumn: "1 / -1", textAlign: "center" }}>
                <button type="button" onClick={handleSaveClick} style={{ marginTop: "1rem" }}>
                  Save Changes
                </button>
                <button
                  type="button"
                  onClick={() => { setEditingProfile(false); setDraftProfile(profile); }}
                  style={{ marginLeft: "1rem", background: "#b0b8c1", color: "#205081" }}
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
          {!editingProfile && (
            <div style={{ textAlign: "center", marginTop: "1.5rem" }}>
              <button type="button" onClick={() => { setDraftProfile(profile); setEditingProfile(true); }} className="edit-profile-btn">
                <FaEdit /> Edit Profile
              </button>
            </div>
          )}
        </>
      )}
    </div>
  ); };

  const UploadTab = () => (
    <div className="tab-content">
      <h2>Extract Invoice Data</h2>
      
      <div className="feature-card">
        <div className="feature-icon">
          <FaRocket />
        </div>
        <h3>Smart Invoice Processing</h3>
        <p>Upload your invoices and let our AI extract all the important data automatically. Supports both printed and handwritten invoices.</p>
      </div>
      
      <form className="upload-form" onSubmit={handleUpload}>
        <label className="type-label">
          Invoice Type:
          <select
            value={invoiceType}
            onChange={(e) => setInvoiceType(e.target.value)}
          >
            <option value="printed">Printed</option>
            <option value="handwritten">Handwritten</option>
          </select>
        </label>
        
        <div 
          className={`file-upload-area ${isDragging ? 'dragover' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-input').click()}
        >
          <div className="file-upload-icon">
            <FaCloudUploadAlt />
          </div>
          <div className="file-upload-text">
            {file ? file.name : "Click to select or drag & drop your file"}
          </div>
          <div className="file-upload-hint">
            Supports PDF, PNG, JPG, JPEG files
          </div>
          <input
            id="file-input"
            type="file"
            accept="application/pdf,image/png,image/jpeg,image/jpg"
            onChange={handleFileChange}
            disabled={uploading}
            style={{ display: 'none' }}
          />
        </div>
        
        {uploading && (
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${uploadProgress}%` }}></div>
          </div>
        )}
        
        <button type="submit" disabled={uploading || !file}>
          {uploading ? <span className="spinner"></span> : "Upload & Extract"}
        </button>
      </form>
      
      {error && <div className="alert error">{error}</div>}
      {(excelUrl || wordUrl) && (
        <div className="results">
          <h3>Download Results:</h3>
          {excelUrl && (
            <a
              href={`${API_BASE}${excelUrl}`}
              target="_blank"
              rel="noopener noreferrer"
              className="download-link"
            >
              <FaDownload /> Download Excel
            </a>
          )}
          {wordUrl && (
            <a
              href={`${API_BASE}${wordUrl}`}
              target="_blank"
              rel="noopener noreferrer"
              className="download-link"
            >
              <FaDownload /> Download Word
            </a>
          )}
        </div>
      )}
      {message && <div className="alert success">{message}</div>}
    </div>
  );

  const HistoryTab = () => (
    <div className="tab-content">
      <h2>Your Invoice History</h2>
      
      <StatsDashboard />
      
      <div className="search-filter-bar">
        <div style={{ position: 'relative', flex: 1 }}>
          <FaSearch style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-light)' }} />
          <input
            type="text"
            placeholder="Search by filename or type..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
            style={{ paddingLeft: '40px' }}
          />
        </div>
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="filter-select"
        >
          <option value="all">All Types</option>
          <option value="printed">Printed</option>
          <option value="handwritten">Handwritten</option>
        </select>
      </div>
      
      {loading ? (
        <div className="skeleton">
          <div className="skeleton-text"></div>
          <div className="skeleton-text"></div>
          <div className="skeleton-text"></div>
        </div>
      ) : filteredHistory.length === 0 ? (
        <div className="feature-card">
          <div className="feature-icon">
            <FaChartBar />
          </div>
          <h3>No uploads found</h3>
          <p>{searchTerm || filterType !== 'all' ? 'Try adjusting your search or filter criteria.' : 'Start by uploading your first invoice to see your processing history here.'}</p>
        </div>
      ) : (
        <table className="history-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Type</th>
              <th>Original File</th>
              <th>Excel</th>
              <th>Word</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredHistory.map((item) => (
              <tr key={item.id}>
                <td>{new Date(item.upload_time).toLocaleString()}</td>
                <td>
                  <span className={`badge ${item.invoice_type}`}>
                    {item.invoice_type}
                  </span>
                </td>
                <td>{item.original_filename}</td>
                <td>
                  {item.excel_filename ? (
                    <a
                      href={`${API_BASE}/api/download/${item.excel_filename}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="download-link"
                    >
                      <FaDownload /> Download
                    </a>
                  ) : (
                    "-"
                  )}
                </td>
                <td>
                  {item.word_filename ? (
                    <a
                      href={`${API_BASE}/api/download/${item.word_filename}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="download-link"
                    >
                      <FaDownload /> Download
                    </a>
                  ) : (
                    "-"
                  )}
                </td>
                <td>
                  <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
                    <button className="tooltip" title="View Details">
                      <FaEye />
                    </button>
                    <button className="tooltip" title="Delete">
                      <FaTrash />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );

  const AboutTab = () => (
    <div className="tab-content">
      <h2>About EXLPRO Invoice Extractor</h2>
      
      <div className="feature-card">
        <div className="feature-icon">
          <FaBolt />
        </div>
        <h3>Lightning Fast Processing</h3>
        <p>Our advanced OCR technology processes invoices in seconds, not minutes. Get your data instantly.</p>
      </div>
      
      <div className="feature-card">
        <div className="feature-icon">
          <FaShieldAlt />
        </div>
        <h3>Secure & Private</h3>
        <p>Your data is encrypted and secure. We never store your sensitive information longer than necessary.</p>
      </div>
      
      <div className="chart-container">
        <div className="chart-title">Processing Statistics</div>
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <div style={{ fontSize: '3rem', color: 'var(--primary-blue)', marginBottom: '1rem' }}>
            {history.length}
          </div>
          <div style={{ color: 'var(--text-light)' }}>
            Invoices Processed Successfully
          </div>
        </div>
      </div>
      
      <p>
        <b>EXLPRO Invoice Extractor</b> is a cutting-edge web application designed for accountants, businesses, and professionals to automate the extraction of data from invoices. Upload your PDF or image invoices, select the type, and instantly get structured data in Excel or Word format. Save time, reduce errors, and streamline your workflow with our easy-to-use platform.
      </p>
      <ul>
        <li>Supports both printed and handwritten invoices</li>
        <li>Download results in Excel and Word formats</li>
        <li>Secure, user-friendly dashboard</li>
        <li>Profile management and upload history</li>
        <li>Modern, responsive design</li>
        <li>Real-time processing with progress tracking</li>
        <li>Advanced AI-powered data extraction</li>
        <li>Dark mode support for better user experience</li>
        <li>Search and filter functionality</li>
        <li>Drag & drop file upload</li>
      </ul>
    </div>
  );

  return (
    <div className="DashboardApp">
      {/* Top Navigation */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onLogout={handleLogout}
        profile={profile}
        darkMode={darkMode}
        onToggleDark={toggleDarkMode}
      />

      {/* Notification Center */}
      <NotificationCenter />
      
      {/* Floating Action Button */}
      <button className="fab tooltip" onClick={() => setActiveTab("upload")}>
        <FaPlus />
        <span className="tooltiptext">Quick Upload</span>
      </button>
      
      {!token ? (
        <div className="center-card">
          <div className="auth-form">
            <img src={logo} alt="EXLPRO Logo" className="logo" />
            <h2>{isLogin ? "Login" : "Sign Up"}</h2>
            <form onSubmit={handleAuth}>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoComplete="username"
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete={isLogin ? "current-password" : "new-password"}
              />
              <button type="submit">{isLogin ? "Login" : "Sign Up"}</button>
            </form>
            <button
              className="switch-btn"
              onClick={() => {
                setIsLogin(!isLogin);
                setError("");
                setMessage("");
              }}
            >
              {isLogin
                ? "Don't have an account? Sign Up"
                : "Already have an account? Login"}
            </button>
            {error && <div className="alert error">{error}</div>}
            {message && <div className="alert success">{message}</div>}
          </div>
        </div>
      ) : (
        <div className="dashboard-layout">
          <Sidebar />
          <main className="dashboard-main">
            {activeTab === "profile" && <ProfileTab />}
            {activeTab === "upload" && <UploadTab />}
            {activeTab === "history" && <HistoryTab />}
            {activeTab === "about" && <AboutTab />}
          </main>
        </div>
      )}
      <footer>
        &copy; {new Date().getFullYear()} EXLPRO Invoice Extractor | Smart Invoice Data Automation
      </footer>
    </div>
  );
}

export default App;
    