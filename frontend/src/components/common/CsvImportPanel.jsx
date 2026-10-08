import { useState } from "react";
import api from "../../api/client";

export default function CsvImportPanel({ dataset, onImported }) {
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  async function upload(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    setBusy(true);
    setMessage("");
    const form = new FormData();
    form.append("file", file);
    try {
      const response = await api.post(`/imports/${dataset}`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage(`${response.data.count} records imported.`);
      onImported?.();
    } catch (error) {
      setMessage(error.response?.data?.detail || "CSV import failed.");
    } finally {
      setBusy(false);
      event.target.value = "";
    }
  }

  return (
    <div className="flex flex-wrap items-center gap-3 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-4">
      <label className="cursor-pointer rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700">
        <span>{busy ? "Importing..." : "Import CSV"}</span>
        <input
          type="file"
          accept=".csv,text/csv"
          onChange={upload}
          disabled={busy}
          className="sr-only"
        />
      </label>
      {message && <span className="text-sm text-slate-600">{message}</span>}
    </div>
  );
}
