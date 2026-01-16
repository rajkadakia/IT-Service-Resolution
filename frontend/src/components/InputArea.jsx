import React, { useState } from 'react';

const InputArea = ({ onSendMessage, disabled, placeholder }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="container-fluid p-3 border-top bg-white">
        <form onSubmit={handleSubmit} className="w-100 mx-auto" style={{ maxWidth: '900px' }}>
        <div className="input-group input-group-lg shadow-sm rounded-pill overflow-hidden border">
            <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={placeholder || "Describe your issue..."}
            disabled={disabled}
            className="form-control border-0 px-4"
            style={{ boxShadow: 'none' }}
            />
            <button
            type="submit"
            disabled={!input.trim() || disabled}
            className="btn btn-primary px-4 d-flex align-items-center"
            >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="currentColor"
                style={{ width: '24px', height: '24px' }}
            >
                <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
            </svg>
            </button>
        </div>
        </form>
    </div>
  );
};

export default InputArea;
