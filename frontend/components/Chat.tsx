"use client"
import { useState } from "react"

export default function Chat() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (file.type === 'application/pdf' || file.type === 'text/csv') {
        setSelectedFile(file)
      } else {
        alert('PDFまたはCSVファイルのみアップロード可能です')
      }
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return
    setLoading(true)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      })

      if (res.ok) {
        alert('ファイルが正常にアップロードされました')
      } else {
        alert('アップロードに失敗しました')
      }
    } catch (error) {
      alert('エラーが発生しました')
    } finally {
      setLoading(false)
      setSelectedFile(null)
    }
  }

  const handleSend = async () => {
    if (!question.trim()) return
    setLoading(true)

    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    })

    const data = await res.json()
    setAnswer(data.answer)
    setLoading(false)
  }

  return (
    <div className="max-w-xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold">Chat with Document</h1>

      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          ファイルをアップロード
        </label>
        <div className="flex items-center space-x-2">
          <input
            type="file"
            accept=".pdf,.csv"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100"
          />
          <button
            onClick={handleUpload}
            disabled={!selectedFile || loading}
            className="bg-green-600 text-white px-4 py-2 rounded disabled:opacity-50"
          >
            {loading ? "アップロード中..." : "アップロード"}
          </button>
        </div>
      </div>

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="質問を入力..."
        rows={3}
        className="w-full border rounded p-2"
      />

      <button
        onClick={handleSend}
        className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
        disabled={loading}
      >
        {loading ? "送信中..." : "送信"}
      </button>

      {answer && (
        <div className="p-4 border rounded bg-gray-50">
          <p className="font-semibold text-gray-700">回答：</p>
          <p>{answer}</p>
        </div>
      )}
    </div>
  )
}
