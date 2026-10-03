const PROP_MAP = {
  2000: 'hp',
  2001: 'atk',
  2002: 'def',
  20: 'critRate',
  22: 'critDamage',
  23: 'energyRecharge',
  28: 'elementalMastery',
};

// Enka bu stat'ları 0-1 arası oran olarak verir; arayüz yüzde gösterir.
const PERCENT_PROPS = new Set(['20', '22', '23']);

/** Genshin UID'leri 9 haneli rakamdır (bazı sunucularda 10 hane). */
export const isValidUid = (uid) => /^\d{9,10}$/.test(uid);

export function parseStats(fightPropMap = {}) {
  const stats = {};
  for (const [key, value] of Object.entries(fightPropMap)) {
    const name = PROP_MAP[key];
    if (!name || typeof value !== 'number') continue;
    stats[name] = PERCENT_PROPS.has(key) ? value * 100 : value;
  }
  return stats;
}

const ERROR_MESSAGES = {
  400: 'Geçersiz UID biçimi.',
  404: 'Bu UID ile oyuncu bulunamadı.',
  424: 'Oyun sunucuları bakımda, daha sonra tekrar deneyin.',
  429: 'Çok fazla istek gönderildi, biraz bekleyip tekrar deneyin.',
  500: 'Enka sunucusunda bir hata oluştu.',
  503: 'Enka servisi şu anda kullanılamıyor.',
};

export async function fetchPlayer(uid, { signal } = {}) {
  const id = uid.trim();
  if (!isValidUid(id)) throw new Error('UID 9 veya 10 haneli bir sayı olmalı.');

  const response = await fetch(`/api/enka/api/uid/${id}`, { signal });
  if (!response.ok) {
    throw new Error(ERROR_MESSAGES[response.status] || `İstek başarısız oldu (HTTP ${response.status}).`);
  }

  const data = await response.json();
  if (!data.avatarInfoList || data.avatarInfoList.length === 0) {
    throw new Error('Karakter Vitrini (Showcase) boş veya gizli! Oyun içinden karakterlerinizi sergileyin.');
  }
  return data;
}
