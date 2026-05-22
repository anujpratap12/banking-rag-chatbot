import { useEffect, useRef, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [query, setQuery] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text:
        "Hello 👋 I'm your AI Banking Assistant powered by RAG. Upload banking documents and ask me questions about loans, credit cards, KYC, interest rates, banking policies, or financial procedures.",
      time: getCurrentTime(),
      sources: ["banking_policy.pdf", "loan_faqs.pdf"]
    }
  ]);

  const [loading, setLoading] = useState(false);

  const [file, setFile] = useState(null);

  const [uploadedFileName, setUploadedFileName] = useState("");

  const chatEndRef = useRef(null);

  // AUTO SCROLL

  useEffect(() => {

    chatEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });

  }, [messages, loading]);

  // CURRENT TIME

  function getCurrentTime() {

    return new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit"
    });
  }

  // COMMON FUNCTION FOR API CALL

  const sendQueryToBackend = async (text) => {

    const userMessage = {
      sender: "user",
      text: text,
      time: getCurrentTime()
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {

      const response = await axios.post(
  "https://banking-rag-chatbot-production.up.railway.app/chat",
        {},
        {
          params: {
            query: text
          }
        }
      );

      const aiMessage = {
        sender: "ai",
        text: response.data.answer,
        time: getCurrentTime(),
        sources: [
          "retrieved_context.txt",
          "vector_search"
        ]
      };

      setMessages((prev) => [...prev, aiMessage]);

    } catch (error) {

      const errorMessage = {
        sender: "ai",
        text: "Error connecting to backend server.",
        time: getCurrentTime()
      };

      setMessages((prev) => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  // SEND MESSAGE

  const sendMessage = async () => {

    if (!query.trim()) return;

    const currentQuery = query;

    setQuery("");

    sendQueryToBackend(currentQuery);
  };

  // ENTER KEY SEND

  const handleKeyPress = (e) => {

    if (e.key === "Enter") {
      sendMessage();
    }
  };

  // QUICK PROMPTS

  const handleQuickPrompt = async (text) => {

    sendQueryToBackend(text);
  };

  // FILE UPLOAD

  const uploadFile = async () => {

    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      await axios.post(
  "https://banking-rag-chatbot-production.up.railway.app/upload",
        formData
      );

      setUploadedFileName(file.name);

      alert("File uploaded successfully!");

    } catch (error) {

      alert("File upload failed.");
    }
  };

  // QUICK PROMPTS LIST

  const quickPrompts = [
  
    "Summarize the uploaded document",
    "What are the key points in this document?",
    "Explain the important policies mentioned",
    "What are the requirements discussed?",
    "Give a short overview of the uploaded file"

  ];

  return (

    <div className="app-container">

      {/* SIDEBAR */}

      <div className="sidebar">

        <div className="sidebar-header">

          <button className="hamburger-btn">
            ☰
          </button>

          <div className="logo-text">

            <div className="logo-title">
              FinAssist AI
            </div>

            <div className="logo-sub">
              BANKING SUPPORT AGENT
            </div>

          </div>

        </div>

        {/* NEW SESSION */}

        <button
          className="new-session-btn"
          onClick={() => setMessages([])}
        >

          <span className="plus-icon">+</span>

          New Session

        </button>

        {/* RECENT */}

        <div className="recent-label">
          RECENT SESSIONS
        </div>

        {/* SESSION LIST */}
        <div className="session-list">

  <div
    className="session-item session-active"
    onClick={() =>
      handleQuickPrompt(
        "Summarize the uploaded document"
      )
    }
  >

    <div className="session-dot dot-active"></div>

    <div className="session-title">
      Document Summary
    </div>

  </div>

  <div
    className="session-item"
    onClick={() =>
      handleQuickPrompt(
        "What are the key points in this document?"
      )
    }
  >

    <div className="session-dot"></div>

    <div className="session-title">
      Key Points
    </div>

  </div>

  <div
    className="session-item"
    onClick={() =>
      handleQuickPrompt(
        "Explain the important policies mentioned"
      )
    }
  >

    <div className="session-dot"></div>

    <div className="session-title">
      Policy Details
    </div>

  </div>

  <div
    className="session-item"
    onClick={() =>
      handleQuickPrompt(
        "What are the requirements discussed?"
      )
    }
  >

    <div className="session-dot"></div>

    <div className="session-title">
      Requirements
    </div>

  </div>

</div>

        

      {/* MAIN CONTENT */}

      <div className="main-content">

        {/* TOP BAR */}

        <div className="top-bar">

          <div className="top-bar-left">

            <div className="live-badge">

              <div className="live-dot"></div>

              LIVE RAG

            </div>

            <div className="top-bar-titles">

              <div className="chat-title">
                AI Banking Support Chatbot
              </div>

              <div className="chat-subtitle">
                Production-ready Retrieval-Augmented Generation Assistant
              </div>

            </div>

          </div>

          <div className="top-bar-right">

            {uploadedFileName && (

              <div className="uploaded-file-chip">

                📄

                <span>
                  {uploadedFileName}
                </span>

              </div>
            )}

            <label className="upload-btn-top">

              + Upload

              <input
                type="file"
                hidden
                onChange={(e) => setFile(e.target.files[0])}
              />

            </label>

          </div>

        </div>

        {/* QUICK CHIPS */}

        <div className="quick-chips-row">

          <div className="quick-label">
            QUICK PROMPTS
          </div>

          {quickPrompts.map((prompt, index) => (

            <button
              key={index}
              className="quick-chip"
              onClick={() => handleQuickPrompt(prompt)}
            >
              {prompt}
            </button>

          ))}

        </div>

        {/* CHAT BOX */}

        <div className="chat-box">

          {messages.map((msg, index) => (

            <div
              key={index}
              className={
                msg.sender === "ai"
                  ? "message-row ai-row"
                  : "message-row user-row"
              }
            >

              {/* AVATAR */}

              <div
                className={
                  msg.sender === "ai"
                    ? "avatar ai-avatar"
                    : "avatar user-avatar"
                }
              >

                {msg.sender === "ai" ? "AI" : "YOU"}

              </div>

              {/* MESSAGE */}

              <div className="message-col">

                <div
                  className={
                    msg.sender === "ai"
                      ? "bubble ai-bubble"
                      : "bubble user-bubble"
                  }
                >

                  <p>
                    {msg.text}
                  </p>

                </div>

                {/* SOURCES */}

                {msg.sources && (

                  <div className="sources-area">

                    <div className="source-chips">

                      {msg.sources.map((source, idx) => (

                        <div
                          key={idx}
                          className="source-chip"
                        >

                          📄 {source}

                        </div>

                      ))}

                    </div>

                  </div>
                )}

                {/* TIMESTAMP */}

                <div
                  className={
                    msg.sender === "ai"
                      ? "msg-time"
                      : "msg-time user-time"
                  }
                >

                  {msg.time}

                </div>

              </div>

            </div>
          ))}

          {/* TYPING */}

          {loading && (

            <div className="message-row ai-row">

              <div className="avatar ai-avatar">
                AI
              </div>

              <div className="message-col">

                <div className="bubble ai-bubble typing-bubble">

                  <div className="typing-dots">

                    <span></span>
                    <span></span>
                    <span></span>

                  </div>

                </div>

              </div>

            </div>
          )}

          <div ref={chatEndRef}></div>

        </div>

        {/* INPUT BAR */}

        <div className="input-bar">

          <button
            className="attach-btn"
            onClick={uploadFile}
          >
            📎
          </button>

          <input
            type="text"
            className="chat-input"
            placeholder="Ask banking questions..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyPress}
          />

          <button
            className="send-btn"
            onClick={sendMessage}
            disabled={loading}
          >
            ➤
          </button>

        </div>

        {/* FOOTER */}

        <div className="footer-note">

          AI Banking Support Assistant • Hybrid Search • ChromaDB • FastAPI • React • OpenRouter

        </div>

      </div>

    </div>
  );
}

export default App;