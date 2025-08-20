import React from "react";

export default function Header({ activeTab, setActiveTab, onLogout, profile, darkMode, onToggleDark }) {
  const tabs = [
    { key: "profile", label: "Profile" },
    { key: "upload", label: "Upload" },
    { key: "history", label: "History" },
    { key: "about", label: "About" },
  ];

  return (
    <header className="topbar">
      <div className="topbar-left">
        <div className="brand">EXLPRO</div>
        <nav className="topnav">
          {tabs.map((t) => (
            <button
              key={t.key}
              className={`topnav-link ${activeTab === t.key ? "active" : ""}`}
              onClick={() => setActiveTab(t.key)}
              type="button"
            >
              {t.label}
            </button>
          ))}
        </nav>
      </div>
      <div className="topbar-right">
        <button type="button" className="topbar-toggle" onClick={onToggleDark} aria-label="Toggle dark mode">
          {darkMode ? "☀️" : "🌙"}
        </button>
        <div className="user-chip" title={profile?.email || ""}>
          <div className="user-avatar">{(profile?.full_name || profile?.username || "U").charAt(0).toUpperCase()}</div>
          <div className="user-name">{profile?.full_name || profile?.username || "User"}</div>
        </div>
        <button type="button" className="topbar-logout" onClick={onLogout}>Logout</button>
      </div>
    </header>
  );
}


