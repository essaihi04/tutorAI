import { Link } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

export default function Landing() {
  const { isAuthenticated } = useAuthStore();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Nav */}
      <nav className="flex items-center justify-between px-8 py-4">
        <Link to="/" className="flex items-center gap-3">
          <img src="/media/logo.png" alt="معلم" className="h-10 w-auto" />
          <h1 className="text-2xl font-bold text-blue-700 font-brand hidden sm:block">معلم</h1>
        </Link>
        <div className="flex gap-3">
          {isAuthenticated ? (
            <Link
              to="/dashboard"
              className="px-5 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition"
            >
              Dashboard
            </Link>
          ) : (
            <>
              <Link
                to="/login"
                className="px-5 py-2 border border-blue-600 text-blue-600 rounded-lg font-medium hover:bg-blue-50 transition"
              >
                Connexion
              </Link>
              <Link
                to="/inscription"
                className="px-5 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition"
              >
                S'inscrire
              </Link>
            </>
          )}
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-5xl mx-auto px-8 py-20 text-center">
        <h2 className="text-5xl font-extrabold text-gray-900 leading-tight">
          Ton tuteur IA pour le
          <span className="text-blue-600"> Baccalaureat</span>
        </h2>
        <p className="mt-6 text-xl text-gray-500 max-w-2xl mx-auto">
          Un professeur intelligent qui t'enseigne la Physique, la Chimie et les SVT
          en francais et en arabe, avec la voix et en temps reel.
        </p>
        <div className="mt-10 flex justify-center gap-4">
          <Link
            to="/inscription"
            className="px-8 py-4 bg-blue-600 text-white rounded-xl text-lg font-semibold hover:bg-blue-700 transition shadow-lg shadow-blue-200"
          >
            Commencer gratuitement
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-8 py-16">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white rounded-2xl p-8 shadow-sm border">
            <div className="text-4xl mb-4">&#127891;</div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Enseignement adaptatif</h3>
            <p className="text-gray-500">
              L'IA s'adapte a ton niveau et ta vitesse d'apprentissage. Elle detecte tes
              difficultes et ajuste ses explications.
            </p>
          </div>
          <div className="bg-white rounded-2xl p-8 shadow-sm border">
            <div className="text-4xl mb-4">&#127908;</div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Interaction vocale</h3>
            <p className="text-gray-500">
              Parle avec ton tuteur comme avec un vrai professeur. Il t'ecoute, te repond
              et t'explique avec patience.
            </p>
          </div>
          <div className="bg-white rounded-2xl p-8 shadow-sm border">
            <div className="text-4xl mb-4">&#128202;</div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Suivi de progression</h3>
            <p className="text-gray-500">
              Revision espacee, exercices adaptes, et statistiques detaillees pour suivre
              ta progression vers le BAC.
            </p>
          </div>
        </div>
      </section>

      {/* Subjects */}
      <section className="max-w-6xl mx-auto px-8 py-16">
        <h3 className="text-3xl font-bold text-center text-gray-800 mb-10">
          Programme complet du BAC Marocain
        </h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-blue-50 border border-blue-200 rounded-2xl p-6">
            <h4 className="text-xl font-bold text-blue-700 mb-3">Physique</h4>
            <p className="text-blue-600 text-sm">15 chapitres</p>
            <ul className="mt-3 text-sm text-gray-600 space-y-1">
              <li>Ondes mecaniques</li>
              <li>Electricite (RC, RL, RLC)</li>
              <li>Mecanique de Newton</li>
              <li>Oscillateurs mecaniques</li>
            </ul>
          </div>
          <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-6">
            <h4 className="text-xl font-bold text-emerald-700 mb-3">Chimie</h4>
            <p className="text-emerald-600 text-sm">14 chapitres</p>
            <ul className="mt-3 text-sm text-gray-600 space-y-1">
              <li>Cinetique chimique</li>
              <li>Equilibres chimiques</li>
              <li>Acides-bases et dosages</li>
              <li>Electrochimie</li>
            </ul>
          </div>
          <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6">
            <h4 className="text-xl font-bold text-amber-700 mb-3">SVT</h4>
            <p className="text-amber-600 text-sm">6 unites</p>
            <ul className="mt-3 text-sm text-gray-600 space-y-1">
              <li>Genetique et ADN</li>
              <li>Immunologie</li>
              <li>Geologie et tectonique</li>
              <li>Energie cellulaire</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="text-center py-8 text-gray-400 text-sm">
        معلم — 2ème BAC Sciences Physiques BIOF
      </footer>
    </div>
  );
}
