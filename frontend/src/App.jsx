import { useState } from "react";
import CategorySelector from "./components/CategorySelector";
import ChatInterface from "./components/ChatInterface";
import InputArea from "./components/InputArea";
import { api } from "./api/client";

function App() {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [conversationState, setConversationState] = useState({
    mode: "idle",
    turn: 0,
    previousQuery: "",
  });

  const handleCategorySelect = (categoryId) => {
    setSelectedCategory(categoryId);
    setMessages([
      {
        sender: "system",
        text: `Category **${categoryId.toUpperCase()}** selected. How can the system assist with this service?`,
      },
    ]);
    setConversationState({ mode: "idle", turn: 0, previousQuery: "" });
  };

  const handleSendMessage = async (text) => {
    const userMsg = { sender: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    try {
      let response;

      if (conversationState.mode === "clarification") {
        response = await api.followup(
          selectedCategory,
          conversationState.previousQuery,
          text,
          conversationState.turn
        );
      } else {
        response = await api.search(selectedCategory, text);

        setConversationState((prev) => ({ ...prev, previousQuery: text }));
      }

      if (response.type === "answer") {
        setMessages((prev) => [
          ...prev,
          {
            sender: "system",
            text: response.answer,
            context: response.context,
          },
        ]);
        setConversationState((prev) => ({ ...prev, mode: "idle", turn: 0 }));
      } else if (response.type === "clarification") {
        setMessages((prev) => [
          ...prev,
          {
            sender: "system",
            text: response.question,
            context: [],
          },
        ]);
        setConversationState((prev) => ({
          ...prev,
          mode: "clarification",
          turn: response.turn,
        }));
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "system",
          text: "The system encountered an error communicating with the server. Please check your connection and try again.",
        },
      ]);
      console.error(error);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="d-flex vh-100 overflow-hidden bg-light">
      {}
      <div
        className="d-flex flex-column bg-white border-end shadow-sm"
        style={{ width: "300px", zIndex: 10 }}
      >
        <div className="p-4 border-bottom">
          <h1 className="h4 fw-bold text-primary mb-1">IT Resolution</h1>
          <p className="small text-muted mb-0">Intelligent Support Agent</p>
        </div>

        <div className="flex-grow-1 overflow-auto py-3">
          <p
            className="px-4 text-uppercase small fw-bold text-muted mb-3"
            style={{ fontSize: "0.75rem", letterSpacing: "0.05em" }}
          >
            Select Service
          </p>
          <CategorySelector
            selectedCategory={selectedCategory}
            onSelectCategory={handleCategorySelect}
          />
        </div>
      </div>

      {}
      <div className="flex-grow-1 d-flex flex-column position-relative">
        {}
        <div
          className="position-absolute top-0 start-0 w-100 bg-gradient opacity-25"
          style={{
            height: "200px",
            background: "linear-gradient(to bottom, #e9ecef, transparent)",
            zIndex: 0,
          }}
        ></div>

        {!selectedCategory ? (
          <div
            className="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center p-4"
            style={{ zIndex: 1 }}
          >
            <h2 className="display-6 fw-bold text-dark mb-3">
              Welcome to IT Support
            </h2>
            <p className="lead text-muted" style={{ maxWidth: "400px" }}>
              Please select a service category from the sidebar to begin
              troubleshooting your issue.
            </p>
          </div>
        ) : (
          <>
            <div
              className="px-4 py-3 bg-white border-bottom shadow-sm d-flex align-items-center sticky-top"
              style={{ zIndex: 5, height: "70px" }}
            >
              <h2 className="h5 mb-0 fw-semibold d-flex align-items-center gap-2">
                <span
                  className="rounded-pill bg-primary"
                  style={{ width: "6px", height: "24px" }}
                ></span>
                {selectedCategory.toUpperCase()} Support
              </h2>
            </div>

            <ChatInterface messages={messages} isTyping={isTyping} />

            <InputArea
              onSendMessage={handleSendMessage}
              disabled={isTyping}
              placeholder={
                conversationState.mode === "clarification"
                  ? "Type your clarification..."
                  : "Describe your issue..."
              }
            />
          </>
        )}
      </div>
    </div>
  );
}

export default App;
