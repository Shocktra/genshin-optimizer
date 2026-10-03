import React, { useRef, useState } from 'react';
import guides from './data/guides.json';
import { fetchPlayer, parseStats } from './lib/enka';
import './index.css';

const LABEL_MAP = {
  hp: 'HP (Can)',
  atk: 'ATK (Saldırı)',
  def: 'DEF (Savunma)',
  critRate: 'CRIT Rate (%)',
  critDamage: 'CRIT DMG (%)',
  energyRecharge: 'Energy Recharge (%)',
  elementalMastery: 'Elemental Mastery'
};

function StatBar({ label, current, optimal }) {
  const percentage = Math.min(100, Math.max(0, (current / optimal) * 100));
  const isComplete = percentage >= 100;
  
  return (
    <div className="stat-container">
      <div className="stat-header">
        <span className="stat-label">{LABEL_MAP[label] || label}</span>
        <span className={`stat-value ${isComplete ? 'perfect' : 'needs-work'}`}>
          {current.toFixed(1)} / {optimal}
        </span>
      </div>
      <div className="progress-bar-bg">
        <div 
          className={`progress-bar-fill ${isComplete ? 'glow-green' : 'glow-yellow'}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
      {!isComplete && (
        <div className="stat-advice">
          Daha fazla <strong>{LABEL_MAP[label]}</strong> bulmalısın! (Eksik: {(optimal - current).toFixed(1)})
        </div>
      )}
      {isComplete && (
        <div className="stat-advice success">
          Mükemmel! Bu stat ideal seviyede. ✨
        </div>
      )}
    </div>
  );
}

function App() {
  const [uid, setUid] = useState('700000000'); 
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [playerData, setPlayerData] = useState(null);

  const abortRef = useRef(null);

  const fetchEnkaData = async (e) => {
    e.preventDefault();
    // Önceki istek bitmeden yenisi başlarsa eskisini iptal et.
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setLoading(true);
    setError(null);
    setPlayerData(null);

    try {
      setPlayerData(await fetchPlayer(uid, { signal: controller.signal }));
    } catch (err) {
      if (err.name === 'AbortError') return;
      setError(err.message);
    } finally {
      if (abortRef.current === controller) setLoading(false);
    }
  };

  return (
    <div className="app-wrapper">
      <div className="background-overlay"></div>
      
      <main className="glass-panel main-container">
        <header className="header">
          <h1 className="title">✧ Teyvat Optimizer ✧</h1>
          <p className="subtitle">Karakterlerinizin eksiklerini bulun ve ideal yapıya (build) ulaşın.</p>
        </header>

        <form onSubmit={fetchEnkaData} className="search-bar">
          <input 
            type="text" 
            placeholder="Genshin UID Giriniz..." 
            value={uid}
            onChange={(e) => setUid(e.target.value)}
            inputMode="numeric"
            aria-label="Genshin UID"
            className="uid-input"
          />
          <button type="submit" className="search-btn animate-pulse-btn" disabled={loading}>
            {loading ? 'Sorgulanıyor...' : 'Analiz Et'}
          </button>
        </form>

        {error && <div className="error-box">⚠️ {error}</div>}

        {playerData && (
          <div className="results-container animate-fade-in">
            <h2 className="player-name">Oyuncu: {playerData.playerInfo?.nickname}</h2>
            
            <div className="character-grid">
              {playerData.avatarInfoList.map((avatar, idx) => {
                const charId = avatar.avatarId.toString();
                const guide = guides[charId] || guides[`${charId}-502`] || guides[`${charId}-701`]; // Fallback for Traveler variants
                const currentStats = parseStats(avatar.fightPropMap);

                return (
                  <div key={idx} className="character-card glass-panel" style={{ animationDelay: `${idx * 0.15}s` }}>
                    <div className={`card-header element-${guide ? guide.element.toLowerCase() : 'unknown'}`}>
                      {guide && guide.icon && (
                        <div className="portrait-wrapper">
                          <img 
                            src={`https://enka.network/ui/${guide.icon}.png`} 
                            alt={guide.name} 
                            className="character-portrait"
                            onError={(e) => e.target.style.display = 'none'}
                          />
                        </div>
                      )}
                      <h3>{guide ? guide.name : `Karakter ID: ${charId}`}</h3>
                    </div>

                    {guide ? (
                      <div className="card-body">
                        <div className="stats-list">
                          <h4 className="section-title">İdeal Stat Analizi</h4>
                          {Object.keys(guide.optimal_stats).map(statKey => (
                            <StatBar 
                              key={statKey}
                              label={statKey} 
                              current={currentStats[statKey] || 0} 
                              optimal={guide.optimal_stats[statKey]} 
                            />
                          ))}
                        </div>

                        <div className="equipment-section">
                          <div className="eq-box">
                            <h4 className="section-title">⚔️ Önerilen Silahlar</h4>
                            <ul>
                              {guide.weapons.map((w, i) => <li key={i}>{w}</li>)}
                            </ul>
                          </div>
                          
                          <div className="eq-box">
                            <h4 className="section-title">🌸 Önerilen Yadigarlar</h4>
                            <ul>
                              {guide.artifacts.map((a, i) => <li key={i}>{a}</li>)}
                            </ul>
                          </div>
                        </div>
                        
                        <div className="talents-section">
                          <h4 className="section-title">👑 Yetenek Önceliği</h4>
                          <ul>
                            {guide.talent_priority.map((talent, tIdx) => (
                              <li key={tIdx}>
                                <span>{tIdx + 1}. {talent.name}</span>
                                <span className="target-lvl">Hedef: Lv.{talent.recommendedLevel}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    ) : (
                      <div className="no-guide">
                        <p>Bilinmeyen Karakter (Veritabanında bulunamadı).</p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
