import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, signup } from "../api/auth";
import { Activity, ArrowLeft, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";

export default function LoginPage({ onLogin = null, signupMode = false }) {
  const [email, setEmail] = useState("owner@logimind.ai");
  const [password, setPassword] = useState("demo1234");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const response = await (signupMode ? signup : login)(
        email.trim(),
        password,
      );
      localStorage.setItem("logimind-user", JSON.stringify(response.data));
      localStorage.removeItem("logimind-profile");
      if (onLogin) onLogin(response.data);
      navigate(signupMode ? "/profile-setup" : "/dashboard");
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
          "Login service unavailable. Start the backend and try again.",
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="surface-grid flex min-h-screen items-center justify-center bg-[#f4f7fb] px-4 py-12">
      <div className="w-full max-w-[440px] rounded-3xl border border-slate-200 bg-white p-8 shadow-2xl shadow-slate-900/10 md:p-10">
        <Link to="/" className="mb-10 inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-blue-700"><ArrowLeft size={16} /> Back to home</Link>
        <div className="mb-6">
          <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-xl bg-[#0b1220] text-white"><Activity size={21} /></div>
          <p className="text-xs font-bold uppercase tracking-[0.2em] text-blue-700">LOGIMIND workspace</p>
          <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-900">
            {signupMode ? "Create your workspace" : "Welcome back"}
          </h1>
        </div>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-3 text-slate-900 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
              placeholder="distributor@logimind.ai"
              required
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-3 text-slate-900 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
              placeholder="••••••••"
              required
            />
          </div>

          {error && (
            <p className="rounded-lg bg-amber-50 p-3 text-sm text-amber-800">
              {error}
            </p>
          )}
          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-xl bg-blue-600 px-4 py-3.5 text-sm font-bold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-700"
          >
            {submitting ? "Connecting..." : signupMode ? "Sign up" : "Sign in"}
          </button>
        </form>
        <p className="mt-6 flex items-center justify-center gap-2 text-center text-xs text-slate-500"><ShieldCheck size={14} className="text-emerald-600" /> Your workspace data remains tenant-isolated.</p>
      </div>
    </div>
  );
}
