import React, { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async () => {
    const res = await fetch(`http://localhost:8000/chat?query=${encodeURIComponent(query)}`);
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="p-8">
      <h1 className="text-xl font-bold mb-4">RAG Chatbot</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="border p-2 w-full mb-2"
        placeholder="質問を入力してください"
      />
      <button
        onClick={handleSubmit}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        質問する
      </button>
      <div className="mt-4">
        <p>回答: {response}</p>
      </div>
    </div>
  );
}
