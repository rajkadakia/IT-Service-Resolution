import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';

const ChatInterface = ({ messages, isTyping }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  return (
    <div className="flex-grow-1 overflow-auto p-4 bg-light" style={{ scrollBehavior: 'smooth' }}>
      {messages.length === 0 && (
        <div className="d-flex flex-column align-items-center justify-content-center h-100 text-muted">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="mb-3 opacity-50" style={{ width: '64px', height: '64px' }}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.159 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
          </svg>
          <p className="lead">Select a category and start describing your issue.</p>
        </div>
      )}

      <div className="container" style={{ maxWidth: '900px' }}>
        {messages.map((msg, index) => (
            <div
            key={index}
            className={`d-flex w-100 mb-3 ${msg.sender === 'user' ? 'justify-content-end' : 'justify-content-start'}`}
            >
            <div
                className={`
                p-3 shadow-sm
                ${
                    msg.sender === 'user'
                    ? 'bg-primary text-white rounded-start-top-3'
                    : 'bg-white text-dark border rounded-end-top-3'
                }
                `}
                style={{ 
                    maxWidth: '85%', 
                    borderRadius: '1rem',
                    borderBottomRightRadius: msg.sender === 'user' ? '0' : '1rem',
                    borderBottomLeftRadius: msg.sender !== 'user' ? '0' : '1rem'
                }}
            >
                {msg.sender === 'system' ? (
                    <div>
                        <ReactMarkdown>{msg.text}</ReactMarkdown>
                        {msg.context && msg.context.length > 0 && (
                            <div className="mt-3 pt-3 border-top">
                                <p className="small fw-bold text-muted mb-2 text-uppercase">Relevant Incidents:</p>
                                <div className="d-flex flex-column gap-2">
                                    {msg.context.map((ctx, i) => (
                                        <div key={i} className="bg-light p-2 rounded small text-secondary">
                                            <span className="badge bg-secondary me-2">#{ctx.incident_id}</span>
                                            {ctx.text.substring(0, 100)}...
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                ) : (
                    <p className="mb-0" style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</p>
                )}
            </div>
            </div>
        ))}

        {isTyping && (
            <div className="d-flex w-100 justify-content-start mb-3">
            <div className="bg-white border rounded p-3 shadow-sm" style={{ borderBottomLeftRadius: '0', borderRadius: '1rem' }}>
                <div className="d-flex gap-1">
                <div className="spinner-grow spinner-grow-sm text-secondary" role="status" style={{ animationDuration: '1s' }}></div>
                <div className="spinner-grow spinner-grow-sm text-secondary" role="status" style={{ animationDelay: '0.2s', animationDuration: '1s' }}></div>
                <div className="spinner-grow spinner-grow-sm text-secondary" role="status" style={{ animationDelay: '0.4s', animationDuration: '1s' }}></div>
                </div>
            </div>
            </div>
        )}
      </div>
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatInterface;
