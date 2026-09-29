import { Link } from 'react-router-dom';

export default function WelcomePage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col justify-center px-6 py-16 lg:px-8">
        <div className="max-w-3xl">
          <p className="mb-4 inline-flex rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-blue-700">
            LOGIMIND
          </p>
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 md:text-6xl">
            AI-Powered Distributor Operations Intelligence
          </h1>
          <p className="mt-6 max-w-2xl text-lg text-slate-600">
            LOGIMIND helps distributors understand today&apos;s delivery operations, find hotspots,
            analyze performance, and learn from historical experience so the next recommendation is wiser.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link
              to="/login"
              className="inline-flex items-center justify-center rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-500"
            >
              Get Started
            </Link>
            <Link
              to="/login"
              className="inline-flex items-center justify-center rounded-lg border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-slate-100"
            >
              Login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
