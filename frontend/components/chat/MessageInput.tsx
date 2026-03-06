"use client";

import { Send } from "lucide-react";
import { type KeyboardEvent, useRef, useState } from "react";

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function MessageInput({ onSend, disabled = false }: MessageInputProps) {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (!input.trim() || disabled) return;
    onSend(input.trim());
    setInput("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  const suggestions = [
    "Show me my recent activities",
    "What's my average heart rate?",
    "How far did I run this month?",
  ];

  return (
    <div className="p-4">
      {/* Quick suggestions */}
      <div className="flex gap-2 mb-3 flex-wrap">
        {suggestions.map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => onSend(suggestion)}
            disabled={disabled}
            className="text-xs bg-gray-100 text-gray-600 px-3 py-1.5 rounded-full hover:bg-gray-200 transition-colors disabled:opacity-50"
          >
            {suggestion}
          </button>
        ))}
      </div>

      {/* Input area */}
      <div className="flex items-end gap-2 bg-gray-100 rounded-2xl p-2">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          onInput={handleInput}
          placeholder="Ask about your fitness data..."
          disabled={disabled}
          rows={1}
          className="flex-1 bg-transparent resize-none outline-none text-sm px-2 py-1 max-h-32 text-gray-900 placeholder-gray-400 disabled:opacity-50"
        />
        <button
          onClick={handleSend}
          disabled={disabled || !input.trim()}
          className="flex-shrink-0 bg-blue-600 text-white p-2 rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Send message"
        >
          <Send className="h-4 w-4" />
        </button>
      </div>
      <p className="text-xs text-gray-400 mt-2 text-center">
        Press Enter to send, Shift+Enter for new line
      </p>
    </div>
  );
}
