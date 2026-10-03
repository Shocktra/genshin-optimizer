# Teyvat Optimizer

Genshin Impact UID'nizi girin; Enka.Network Showcase verisinden karakterlerinizin stat'larını ideal yapıyla karşılaştırın, önerilen silah, yadigâr ve yetenek önceliklerini görün.

## Geliştirme

```bash
npm install
npm run dev     # geliştirme sunucusu
npm test        # birim testleri (vitest)
npm run lint    # oxlint
npm run build   # üretim derlemesi
```

> **Not:** Enka API isteklerini tarayıcı CORS kısıtından kaçınmak için `vite.config.js` içindeki geliştirme proxy'si (`/api/enka`) karşılıyor. Bu proxy yalnızca `npm run dev` sırasında çalışır; derlenmiş sürümü statik olarak yayınlarken aynı yolu Enka'ya yönlendiren bir sunucu/reverse proxy gerekir.

## İdeal stat veritabanı

`src/data/guides.json`, `build_db.py` ile `chars.json` ve `loc.json` dosyalarından üretilir (bu iki dosya repoda yok; oyun verisi dump'larından sağlanmalıdır). İdeal değerler elle yazılmış tahminlerdir, resmî veri değildir.

Teknolojiler: React, Vite.
