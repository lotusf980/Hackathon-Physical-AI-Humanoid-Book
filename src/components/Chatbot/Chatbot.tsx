import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  sources?: string[];
}

const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [useSelectedTextOnly, setUseSelectedTextOnly] = useState(false);
  const [isProcessingSelection, setIsProcessingSelection] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Check for selected text on page load and selection changes
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection()?.toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
        setUseSelectedTextOnly(true);
      } else {
        setSelectedText(null);
        setUseSelectedTextOnly(false);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('selectionchange', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('selectionchange', handleSelection);
    };
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && textareaRef.current) {
      setTimeout(() => {
        textareaRef.current?.focus();
      }, 100);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Prepare the request payload
      const requestBody = {
        question: inputText,
        selected_text: useSelectedTextOnly && selectedText ? selectedText : null,
        context: null, // Additional context can be added here if needed
        max_tokens: 1000,
        temperature: 0.3,
      };

      // Get API URL from environment or use default
      const apiUrl = process.env.REACT_APP_CHATBOT_API_URL ||
                    document.querySelector('meta[name="chatbot-api-url"]')?.getAttribute('content') ||
                    'http://localhost:8000/api/v1/chat';

      // Call the FastAPI backend
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add bot response
      const botMessage: Message = {
        id: Date.now().toString(),
        text: data.response,
        sender: 'bot',
        timestamp: new Date(),
        sources: data.sources || [],
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  const formatSources = (sources: string[] | undefined) => {
    if (!sources || sources.length === 0) return null;

    return (
      <div className="chatbot-message-sources">
        <strong>Sources:</strong>
        <ul>
          {sources.slice(0, 3).map((source, index) => (
            <li key={index}>{source}</li>
          ))}
        </ul>
      </div>
    );
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        className={`chatbot-float-button ${isOpen ? 'open' : ''}`}
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 12H8.01M12 12H12.01M16 12H16.01M21 12C21 16.4183 16.9706 20 12 20C9.44426 20 7.15828 18.9117 5.59288 17.157L3 20V13C3 8.58172 7.02944 4 12 4C16.9706 4 21 8.58172 21 13Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        )}
      </button>

      {/* Chat Container */}
      {isOpen && (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <h3>Physical AI & Humanoid Robotics Assistant</h3>
            <div className="chatbot-header-controls">
              <label className="chatbot-checkbox">
                <input
                  type="checkbox"
                  checked={useSelectedTextOnly}
                  onChange={(e) => setUseSelectedTextOnly(e.target.checked)}
                  disabled={!selectedText || isProcessingSelection}
                />
                <span className="chatbot-checkbox-label">
                  Answer from selected text only
                </span>
              </label>
              {selectedText && (
                <button
                  className="chatbot-clear-selection"
                  onClick={() => {
                    setSelectedText(null);
                    setUseSelectedTextOnly(false);
                  }}
                  title="Clear selection"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6 18L18 6M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
              )}
            </div>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your Physical AI & Humanoid Robotics assistant.</p>
                <p>Ask me anything about the book, or select text on the page to get answers specifically from that content.</p>
                {selectedText && (
                  <div className="chatbot-selected-text-preview">
                    <p><strong>Selected text:</strong> {selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}</p>
                  </div>
                )}
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`chatbot-message ${message.sender}`}
                >
                  <div className="chatbot-message-content">
                    {message.text.split('\n').map((line, i) => (
                      <p key={i}>{line}</p>
                    ))}
                    {message.sources && formatSources(message.sources)}
                  </div>
                  <div className="chatbot-message-timestamp">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="chatbot-message bot">
                <div className="chatbot-message-content">
                  <div className="chatbot-typing-indicator">
                    <div className="chatbot-typing-dot"></div>
                    <div className="chatbot-typing-dot"></div>
                    <div className="chatbot-typing-dot"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chatbot-input-form" onSubmit={handleSubmit}>
            <textarea
              ref={textareaRef}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={selectedText
                ? "Ask a question about the selected text..."
                : "Ask a question about the book..."}
              rows={1}
              disabled={isLoading}
              className="chatbot-input-textarea"
            />
            <button
              type="submit"
              disabled={!inputText.trim() || isLoading}
              className="chatbot-send-button"
            >
              {isLoading ? (
                <svg className="chatbot-spinner" width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <circle className="chatbot-spinner-path" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              )}
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default Chatbot;