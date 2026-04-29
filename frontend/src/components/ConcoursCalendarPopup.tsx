import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Calendar, X, Bell, ArrowRight, Clock } from 'lucide-react';
import { getConcoursCatalog } from '../services/api';

/**
 * Floating popup that surfaces upcoming concours dates on the landing page.
 * - Auto-opens on the first visit (localStorage flag)
 * - Re-openable via a floating button at the bottom-right
 * - Pulls live data from /concours/catalog (calendar_2025 + per-concours
 *   registration periods)
 */
export default function ConcoursCalendarPopup() {
  const [open, setOpen] = useState(false);
  const [catalog, setCatalog] = useState<any>(null);

  useEffect(() => {
    getConcoursCatalog()
      .then((res) => setCatalog(res.data))
      .catch(() => null);

    const seen = localStorage.getItem('moalim_calendar_seen');
    if (!seen) {
      const t = setTimeout(() => setOpen(true), 1500);
      return () => clearTimeout(t);
    }
  }, []);

  const close = () => {
    setOpen(false);
    localStorage.setItem('moalim_calendar_seen', '1');
  };

  const cal = catalog?.calendar_2025;
  const concours: any[] = catalog?.concours || [];

  return (
    <>
      {/* Floating trigger button */}
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-5 right-5 z-40 bg-gradient-to-r from-amber-500 to-pink-600 hover:from-amber-600 hover:to-pink-700 text-white rounded-full shadow-2xl px-4 py-3 flex items-center gap-2 text-sm font-semibold transition transform hover:scale-105"
        aria-label="Calendrier des concours"
      >
        <Calendar className="w-4 h-4" />
        <span className="hidden sm:inline">Calendrier des concours</span>
      </button>

      {/* Modal overlay */}
      {open && (
        <div
          className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto"
          onClick={close}
        >
          <div
            className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="relative bg-gradient-to-br from-indigo-700 via-purple-700 to-pink-700 text-white px-6 py-5">
              <button
                onClick={close}
                className="absolute top-3 right-3 p-1.5 hover:bg-white/20 rounded-lg"
                aria-label="Fermer"
              >
                <X className="w-5 h-5" />
              </button>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-white/20 rounded-2xl flex items-center justify-center">
                  <Calendar className="w-6 h-6" />
                </div>
                <div>
                  <div className="text-[11px] uppercase tracking-widest opacity-80">À ne pas manquer</div>
                  <h3 className="text-xl font-bold">Calendrier des concours {catalog?.year || '2026'}</h3>
                </div>
              </div>
            </div>

            {/* Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-5">
              {/* Key milestones */}
              {cal && (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {[
                    { label: 'Ouverture des inscriptions', value: cal.registration_open, cls: 'bg-emerald-50 border-emerald-200', icon: 'text-emerald-600', text: 'text-emerald-700' },
                    { label: 'Clôture des inscriptions', value: cal.registration_close, cls: 'bg-red-50 border-red-200', icon: 'text-red-600', text: 'text-red-700' },
                    { label: 'Listes de présélection', value: cal.preselection_lists, cls: 'bg-amber-50 border-amber-200', icon: 'text-amber-600', text: 'text-amber-700' },
                    { label: 'Épreuves écrites', value: cal.written_exams, cls: 'bg-indigo-50 border-indigo-200', icon: 'text-indigo-600', text: 'text-indigo-700' },
                    { label: 'Résultats finaux', value: cal.final_results, cls: 'bg-purple-50 border-purple-200', icon: 'text-purple-600', text: 'text-purple-700' },
                    { label: 'Rentrée académique', value: cal.academic_start, cls: 'bg-blue-50 border-blue-200', icon: 'text-blue-600', text: 'text-blue-700' },
                  ].map((m) => (
                    <div
                      key={m.label}
                      className={`${m.cls} border rounded-xl p-3 flex items-start gap-2`}
                    >
                      <Clock className={`w-4 h-4 ${m.icon} mt-0.5 flex-shrink-0`} />
                      <div className="min-w-0">
                        <div className={`text-[10px] uppercase tracking-wide font-bold ${m.text}`}>
                          {m.label}
                        </div>
                        <div className="text-sm font-semibold text-gray-900 truncate">{m.value}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Per-concours summary */}
              {concours.length > 0 && (
                <div className="border-t pt-4">
                  <div className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-2">
                    Concours communs ({concours.length})
                  </div>
                  <div className="space-y-2">
                    {concours.map((c: any) => (
                      <div
                        key={c.id}
                        className="flex items-center justify-between gap-3 bg-gray-50 hover:bg-gray-100 rounded-lg px-3 py-2 text-sm"
                      >
                        <div className="min-w-0">
                          <div className="font-semibold text-gray-900 truncate">{c.name}</div>
                          <div className="text-xs text-gray-500 truncate">
                            Inscription : {c.registration?.period || '—'}
                          </div>
                        </div>
                        <a
                          href={c.registration?.site || '#'}
                          target="_blank"
                          rel="noreferrer"
                          className="text-xs text-indigo-700 hover:text-indigo-900 font-medium whitespace-nowrap"
                        >
                          Voir →
                        </a>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Footer CTA */}
            <div className="border-t bg-gradient-to-r from-amber-50 to-pink-50 px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-sm text-gray-700">
                <Bell className="w-4 h-4 text-pink-600" />
                <span>
                  Reçois les <b>dates clés</b> et nouveautés directement par email.
                </span>
              </div>
              <Link
                to="/signup"
                onClick={close}
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-pink-600 to-orange-500 hover:from-pink-700 hover:to-orange-600 text-white font-semibold rounded-xl shadow-md text-sm whitespace-nowrap"
              >
                Recevoir les nouveautés <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
