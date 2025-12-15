// frontend/src/App.jsx

import React, { useState, useRef, useEffect } from 'react';
// --- NEW: Import the FaPlus icon ---
import { FaPaperPlane, FaFilePdf, FaGithub, FaPlus } from 'react-icons/fa';
import ChatMessage from './ChatMessage';
import './App.css';

const API_URL = 'http://127.0.0.1:8000';

function App() {
  const [file, setFile] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatBoxRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  // --- NEW: Function to reset the state and go back to the upload screen ---
  const handleNewChat = () => {
    setSessionId(null);
    setMessages([]);
    setFile(null);
  };

  const handleFileChangeAndUpload = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      handleUpload(selectedFile);
    }
  };
  
  const handleUpload = async (fileToUpload) => {
    // ... same handleUpload function as before ...
    if (!fileToUpload) return;
    setIsLoading(true);
    setSessionId(null);
    setMessages([]);
    
    const formData = new FormData();
    formData.append('file', fileToUpload);

    try {
      const response = await fetch(`${API_URL}/upload`, { method: 'POST', body: formData });
      const data = await response.json();
      if (response.ok) {
        setSessionId(data.session_id);
        setMessages([{ sender: 'bot', text: data.summary }]);
      } else { throw new Error(data.detail || 'File upload failed'); }
    } catch (error) {
      setMessages([{ sender: 'bot', text: `Error: ${error.message}` }]);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleQuery = async (event) => {
    // ... same handleQuery function as before ...
    event.preventDefault();
    if (!query || !sessionId || isLoading) return;
    
    const userMessage = { sender: 'user', text: query };
    const thinkingMessage = { sender: 'bot', text: 'Thinking...', thinking: true };
    setMessages(prev => [...prev, userMessage, thinkingMessage]);
    setIsLoading(true);
    setQuery('');

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, query: query }),
      });
      const data = await response.json();
      if (response.ok) {
        setMessages(prev => [...prev.slice(0, -1), { sender: 'bot', text: data.answer }]);
      } else { throw new Error(data.detail || 'Query failed'); }
    } catch (error) {
        setMessages(prev => [...prev.slice(0, -1), { sender: 'bot', text: `Error: ${error.message}` }]);
    } finally {
        setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <aside className="sidebar">
        {/* ... same sidebar code as before ... */}
        <header className="sidebar-header">
          AskPDF<span>.ai</span>
        </header>
        <div className="sidebar-info">
          <p>Built with FastAPI & React</p>
          <p>
            <a href="https://github.com" target="_blank" rel="noopener noreferrer">
              <FaGithub /> View on GitHub
            </a>
          </p>
        </div>
      </aside>

      <main className="main-content">
        {!sessionId ? (
          // ... same hero section code as before ...
          <div className="hero-section">
            <h1>Unlock Insights from your <span>Documents</span></h1>
            <p>Upload a PDF and start a conversation. Get summaries, find key information, and ask complex questions instantly.</p>
            <label className="hero-upload-btn">
              <FaFilePdf />
              <span>{isLoading ? 'Processing...' : 'Upload PDF & Start Chat'}</span>
              <input type="file" ref={fileInputRef} onChange={handleFileChangeAndUpload} accept=".pdf" disabled={isLoading} />
            </label>
          </div>
        ) : (
          <div className="chat-container">
            {/* --- NEW: Button added to the chat header --- */}
            <header className="chat-header">
              <div className="file-info">
                <span className="icon"><FaFilePdf/></span>
                {file.name}
              </div>
              <button onClick={handleNewChat} className="new-chat-btn" title="Start New Chat">
                <FaPlus />
              </button>
            </header>
            <div className="chat-box" ref={chatBoxRef}>
              {messages.map((msg, index) => <ChatMessage key={index} message={msg} />)}
            </div>
            <form onSubmit={handleQuery} className="chat-input-form">
              {/* ... same form code as before ... */}
              <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ask your document anything..." disabled={isLoading}/>
              <button type="submit" disabled={isLoading}><FaPaperPlane /></button>
            </form>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;