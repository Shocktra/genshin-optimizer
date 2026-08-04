import React, { useState } from 'react';
import guides from './data/guides.json';
import './index.css';

// Enka.Network fightPropMap keys
const PROP_MAP = {
  2000: 'hp',
  2001: 'atk',
  2002: 'def',
  20: 'critRate',
  22: 'critDamage',
  23: 'energyRecharge',
  28: 'elementalMastery'
};

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
  const [uid, setUid] = useState('700000000'); // Örnek UID
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [playerData, setPlayerData] = useState(null);

  const fetchEnkaData = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPlayerData(null);

    try {
      // API call to Enka.Network (Sondaki slash kaldırıldı, Redirect CORS hatasını önlemek için)
      const response = await fetch(`https://enka.network/api/uid/${uid}`);
      if (!response.ok) throw new Error('Hesap bulunamadı veya Showcase gizli!');
      
      const data = await response.json();
      if (!data.avatarInfoList || data.avatarInfoList.length === 0) {
        throw new Error('Karakter Vitrini (Showcase) boş! Oyun içinden karakterlerinizi sergileyin.');
      }
      setPlayerData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const parseStats = (fightPropMap) => {
    const stats = {};
    for (const [key, value] of Object.entries(fightPropMap)) {
      if (PROP_MAP[key]) {
        let val = value;
        // Yüzdelik değerleri 100 ile çarp (CRIT, ER)
        if (['20', '22', '23'].includes(key)) val *= 100;
        stats[PROP_MAP[key]] = val;
      }
    }
    return stats;
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
            className="uid-input"
          />
          <button type="submit" className="search-btn" disabled={loading}>
            {loading ? 'Sorgulanıyor...' : 'Analiz Et'}
          </button>
        </form>

        {error && <div className="error-box">⚠️ {error}</div>}

        {playerData && (
          <div className="results-container">
            <h2 className="player-name">Oyuncu: {playerData.playerInfo?.nickname}</h2>
            
            <div className="character-grid">
              {playerData.avatarInfoList.map((avatar, idx) => {
                const charId = avatar.avatarId.toString();
                const guide = guides[charId];
                const currentStats = parseStats(avatar.fightPropMap);

                return (
                  <div key={idx} className="character-card glass-panel">
                    <div className="card-header">
                      <h3>{guide ? guide.name : `Karakter ID: ${charId}`}</h3>
                      {!guide && <span className="badge warning">Rehber Eksik</span>}
                    </div>

                    {guide ? (
                      <div className="stats-list">
                        <h4>İdeal Stat Analizi</h4>
                        {Object.keys(guide.optimal_stats).map(statKey => (
                          <StatBar 
                            key={statKey}
                            label={statKey} 
                            current={currentStats[statKey] || 0} 
                            optimal={guide.optimal_stats[statKey]} 
                          />
                        ))}
                        
                        <div className="talents-section">
                          <h4>Yetenek (Talent) Önceliği</h4>
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
                        <p>Bu karakter için henüz KQM (KeqingMains) ideal veritabanı eklenmedi. Sadece Raiden, Hu Tao, Neuvillette ve Alhaitham desteklenmektedir.</p>
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
