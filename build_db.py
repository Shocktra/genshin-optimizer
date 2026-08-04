import json
import os

# Dosya yolları
GUIDES_PATH = 'src/data/guides.json'
CHARS_PATH = 'chars.json'
LOC_PATH = 'loc.json'

# Mevcut veritabanını yükle (El ile özenle girilen Raiden, Hu Tao vb. bozulmasın diye)
with open(GUIDES_PATH, 'r', encoding='utf-8') as f:
    guides = json.load(f)

# Enka raw datalarını yükle
with open(CHARS_PATH, 'r', encoding='utf-8') as f:
    chars = json.load(f)

with open(LOC_PATH, 'r', encoding='utf-8') as f:
    loc = json.load(f)
    loc_en = loc.get('en', {})

new_count = 0

for char_id, char_data in chars.items():
    # Zaten eklenmiş olanları atla
    if char_id in guides:
        continue
        
    # Karakterin ismini bul
    name_hash = str(char_data.get('NameTextMapHash', ''))
    name = loc_en.get(name_hash, "Bilinmeyen Karakter")
    
    # NPC veya test karakterlerini filtrele (Genelde isimleri boş veya kalitesiz olur)
    if name == "Bilinmeyen Karakter" or "QualityType" not in char_data:
        continue

    # Traveler (Gezgin) versiyonlarını isimlendir
    element = char_data.get('Element', 'Unknown')
    if "-" in char_id:
        name = f"Traveler ({element})"

    # Varsayılan Stat Şablonu Belirleme (Elemente göre)
    optimal_stats = {
        "critRate": 60,
        "critDamage": 120,
        "energyRecharge": 130
    }
    
    # Elemente göre özel kural (Anemo genelde EM, Hydro genelde HP, Geo genelde DEF)
    if element == 'Wind':  # Anemo
        optimal_stats['elementalMastery'] = 800
        optimal_stats['energyRecharge'] = 160
    elif element == 'Water':  # Hydro
        optimal_stats['hp'] = 30000
    elif element == 'Rock':  # Geo
        optimal_stats['def'] = 2000
        optimal_stats['atk'] = 1500
    else:  # Pyro, Electro, Cryo, Dendro
        optimal_stats['atk'] = 2000
        
    # Eğer Dendro ise EM de lazım
    if element == 'Grass':
        optimal_stats['elementalMastery'] = 250

    # Yetenek önceliği (Jenerik)
    talent_priority = [
        { "name": "Elemental Burst", "recommendedLevel": 8 },
        { "name": "Elemental Skill", "recommendedLevel": 8 },
        { "name": "Normal Attack", "recommendedLevel": 6 }
    ]

    # Sisteme ekle
    guides[char_id] = {
        "name": name,
        "element": element,
        "optimal_stats": optimal_stats,
        "talent_priority": talent_priority
    }
    new_count += 1

# Güncel JSON'u kaydet
with open(GUIDES_PATH, 'w', encoding='utf-8') as f:
    json.dump(guides, f, indent=2, ensure_ascii=False)

print(f"Veritabanı güncellendi! {new_count} adet yeni karakter eklendi.")
