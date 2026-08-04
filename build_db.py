import json

CHARS_PATH = 'chars.json'
LOC_PATH = 'loc.json'
GUIDES_PATH = 'src/data/guides.json'

# Mükemmel Stat Veritabanı (KQM Standartları)
META_KNOWLEDGE = {
    "Raiden Shogun": {"er": 250, "cr": 60, "cd": 120, "atk": 1800},
    "Hu Tao": {"hp": 30000, "em": 150, "cr": 70, "cd": 180},
    "Neuvillette": {"hp": 35000, "cr": 50, "cd": 220, "er": 120},
    "Alhaitham": {"em": 350, "cr": 70, "cd": 150, "er": 130, "atk": 1200},
    "Furina": {"hp": 40000, "er": 160, "cr": 70, "cd": 140},
    "Mavuika": {"atk": 2500, "cr": 60, "cd": 180, "em": 200},
    "Yelan": {"hp": 32000, "er": 180, "cr": 70, "cd": 160},
    "Xiangling": {"er": 200, "em": 150, "cr": 60, "cd": 120, "atk": 1500},
    "Xingqiu": {"er": 180, "cr": 60, "cd": 120, "atk": 1600},
    "Kaedehara Kazuha": {"em": 900, "er": 160},
    "Nahida": {"em": 800, "er": 140, "cr": 50, "cd": 120},
    "Nilou": {"hp": 70000, "em": 300, "er": 130},
    "Zhongli": {"hp": 40000, "er": 130},
    "Kamisato Ayaka": {"atk": 2000, "er": 130, "cr": 40, "cd": 200}, # Blizzard Strayer
    "Ganyu": {"atk": 2200, "cr": 60, "cd": 180, "em": 150},
    "Arataki Itto": {"def": 2200, "er": 130, "cr": 70, "cd": 150},
    "Navia": {"atk": 2500, "cr": 70, "cd": 150, "er": 130},
    "Tartaglia": {"atk": 2000, "cr": 70, "cd": 140, "em": 100},
    "Wanderer": {"atk": 2000, "cr": 70, "cd": 150},
    "Sangonomiya Kokomi": {"hp": 35000, "er": 160},
    "Bennett": {"er": 220, "hp": 25000},
    "Kuki Shinobu": {"em": 900, "hp": 25000},
    "Thoma": {"er": 200, "em": 600}, # Burgeon
    "Sucrose": {"em": 800, "er": 150},
    "Venti": {"em": 800, "er": 160},
    "Kamisato Ayato": {"atk": 2000, "cr": 70, "cd": 150, "er": 130},
    "Albedo": {"def": 2500, "cr": 60, "cd": 120},
    "Arlecchino": {"atk": 2200, "cr": 70, "cd": 150, "em": 100},
    "Clorinde": {"atk": 2000, "cr": 70, "cd": 150, "em": 100},
    "Xiao": {"atk": 2100, "cr": 75, "cd": 160, "er": 120},
    "Yae Miko": {"atk": 1800, "cr": 70, "cd": 150, "em": 100},
    "Baizhu": {"hp": 45000, "er": 180},
    "Tighnari": {"em": 350, "cr": 70, "cd": 140, "atk": 1300},
    "Cyno": {"em": 300, "cr": 70, "cd": 140, "er": 130, "atk": 1500},
    "Dehya": {"hp": 30000, "er": 180},
    "Yoimiya": {"atk": 2000, "cr": 75, "cd": 150, "em": 100},
    "Eula": {"atk": 2000, "cr": 70, "cd": 150, "er": 130},
    "Shenhe": {"atk": 3000, "er": 160},
}

with open(CHARS_PATH, 'r', encoding='utf-8') as f:
    chars = json.load(f)

with open(LOC_PATH, 'r', encoding='utf-8') as f:
    loc = json.load(f)
    loc_en = loc.get('en', {})

guides = {}

for char_id, char_data in chars.items():
    name_hash = str(char_data.get('NameTextMapHash', ''))
    name = loc_en.get(name_hash, "Unknown Character")
    
    if name == "Unknown Character" or "QualityType" not in char_data:
        continue

    element = char_data.get('Element', 'Unknown')
    if "-" in char_id:
        name = f"Traveler ({element})"

    # Varsayılanlar
    optimal_stats = {}
    talent_priority = [
        { "name": "Elemental Burst", "recommendedLevel": 8 },
        { "name": "Elemental Skill", "recommendedLevel": 8 },
        { "name": "Normal Attack", "recommendedLevel": 6 }
    ]

    # Meta eşleşmesi varsa oradan al
    if name in META_KNOWLEDGE:
        meta = META_KNOWLEDGE[name]
        if "hp" in meta: optimal_stats["hp"] = meta["hp"]
        if "atk" in meta: optimal_stats["atk"] = meta["atk"]
        if "def" in meta: optimal_stats["def"] = meta["def"]
        if "em" in meta: optimal_stats["elementalMastery"] = meta["em"]
        if "er" in meta: optimal_stats["energyRecharge"] = meta["er"]
        if "cr" in meta: optimal_stats["critRate"] = meta["cr"]
        if "cd" in meta: optimal_stats["critDamage"] = meta["cd"]
    else:
        # Generic Jenerik Şablonlar
        optimal_stats = {"critRate": 60, "critDamage": 120, "energyRecharge": 130}
        if element == 'Wind':
            optimal_stats['elementalMastery'] = 800
        elif element == 'Water':
            optimal_stats['hp'] = 30000
        elif element == 'Rock':
            optimal_stats['def'] = 2000
        elif element == 'Grass':
            optimal_stats['elementalMastery'] = 250
            optimal_stats['atk'] = 1500
        else:
            optimal_stats['atk'] = 2000

    guides[char_id] = {
        "name": name,
        "element": element,
        "optimal_stats": optimal_stats,
        "talent_priority": talent_priority
    }

with open(GUIDES_PATH, 'w', encoding='utf-8') as f:
    json.dump(guides, f, indent=2, ensure_ascii=False)

print(f"KQM Hassasiyetiyle {len(guides)} karakterin veritabanı başarıyla inşa edildi!")
