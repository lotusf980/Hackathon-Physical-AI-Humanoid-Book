import React, { useState, useEffect, useRef } from 'react';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  sources?: string[];
}

const BookChatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && inputRef.current) {
      setTimeout(() => {
        inputRef.current?.focus();
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
      // Get API URL from meta tag or fallback
      const metaTag = document.querySelector('meta[name="chatbot-api-url"]');
      const apiUrl = metaTag
        ? (metaTag as HTMLElement).getAttribute('content') || 'http://localhost:8000/api/v1/chat'
        : 'http://localhost:8000/api/v1/chat';

      console.log('Sending request to:', apiUrl);
      console.log('Request body:', {
        question: inputText,
        selected_text: null,
        context: null,
        max_tokens: 1000,
        temperature: 0.3,
      });

      // Try to reach the backend API
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          question: inputText,
          selected_text: null,
          context: null,
          max_tokens: 1000,
          temperature: 0.3,
        }),
      });

      console.log('Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('HTTP error details:', response.status, errorText);
        throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`);
      }

      const data = await response.json();
      console.log('Received response data:', data);

      // Validate response format
      if (!data || typeof data !== 'object') {
        throw new Error('Invalid response format received from server');
      }

      // Handle both direct response and ChatResponse model format
      let responseText = '';
      let responseSources = [];

      if (typeof data === 'string') {
        responseText = data;
      } else if (typeof data === 'object') {
        // Check if it's the ChatResponse format
        if ('response' in data) {
          responseText = data.response;
          responseSources = Array.isArray(data.sources) ? data.sources : [];
        } else if ('answer' in data) {
          // Fallback to 'answer' field if present
          responseText = data.answer;
          responseSources = Array.isArray(data.sources) ? data.sources : [];
        } else {
          // Try to find any text field in the response
          const textFields = ['response', 'answer', 'text', 'message'];
          for (const field of textFields) {
            if (field in data && typeof data[field] === 'string') {
              responseText = data[field];
              break;
            }
          }

          if (!responseText) {
            throw new Error('No valid response text found in server response');
          }
        }
      } else {
        throw new Error('Unexpected response format from server');
      }

      // Add bot response
      const botMessage: Message = {
        id: Date.now().toString(),
        text: responseText,
        sender: 'bot',
        timestamp: new Date(),
        sources: responseSources,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      let errorMessageText = 'Sorry, I encountered an error processing your request. Please try again.';

      if (error instanceof TypeError) {
        if (error.message.includes('fetch')) {
          errorMessageText = 'Unable to connect to the chatbot server. Please make sure the backend is running on http://localhost:8000.';
        } else if (error.message.includes('network')) {
          errorMessageText = 'Network error occurred. Please check your connection and ensure the backend is running.';
        } else {
          errorMessageText = `Network error: ${error.message}`;
        }
      } else if (error instanceof Error) {
        if (error.message.includes('HTTP error')) {
          errorMessageText = `Server responded with error: ${error.message}`;
        } else {
          errorMessageText = `Error: ${error.message}`;
        }
      } else {
        errorMessageText = 'An unexpected error occurred. Please try again.';
      }

      const errorMessage: Message = {
        id: Date.now().toString(),
        text: errorMessageText,
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
      <div className="book-chatbot-message-sources">
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
        className={`book-chatbot-float-button ${isOpen ? 'open' : ''}`}
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
        <div className="book-chatbot-container">
          <div className="book-chatbot-header">
            <h3>Physical AI & Humanoid Robotics Assistant</h3>
            <button
              className="book-chatbot-close-button"
              onClick={toggleChat}
              aria-label="Close chat"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>

          <div className="book-chatbot-messages">
            {messages.length === 0 ? (
              <div className="book-chatbot-welcome">
                <p>Hello! I'm your Physical AI & Humanoid Robotics assistant.</p>
                <p>Ask me anything about the book content, and I'll provide answers based on the textbook.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`book-chatbot-message ${message.sender}`}
                >
                  <div className="book-chatbot-message-content">
                    {message.text.split('\n').map((line, i) => (
                      <p key={i}>{line}</p>
                    ))}
                    {message.sources && formatSources(message.sources)}
                  </div>
                  <div className="book-chatbot-message-timestamp">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="book-chatbot-message bot">
                <div className="book-chatbot-message-content">
                  <div className="book-chatbot-typing-indicator">
                    <div className="book-chatbot-typing-dot"></div>
                    <div className="book-chatbot-typing-dot"></div>
                    <div className="book-chatbot-typing-dot"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="book-chatbot-input-form" onSubmit={handleSubmit}>
            <textarea
              ref={inputRef}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about the book..."
              rows={1}
              disabled={isLoading}
              className="book-chatbot-input-textarea"
            />
            <button
              type="submit"
              disabled={!inputText.trim() || isLoading}
              className="book-chatbot-send-button"
            >
              {isLoading ? (
                <svg className="book-chatbot-spinner" width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <circle className="book-chatbot-spinner-path" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
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

export default BookChatbot;