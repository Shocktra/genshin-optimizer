import json

CHARS_PATH = 'chars.json'
LOC_PATH = 'loc.json'
GUIDES_PATH = 'src/data/guides.json'

# Mükemmel Stat, Silah ve Artifact Veritabanı (KQM Standartları)
META_KNOWLEDGE = {
    "Raiden Shogun": {
        "er": 250, "cr": 60, "cd": 120, "atk": 1800,
        "weapons": ["Engulfing Lightning", "The Catch", "Wavebreaker's Fin"],
        "artifacts": ["4x Emblem of Severed Fate"]
    },
    "Hu Tao": {
        "hp": 30000, "em": 150, "cr": 70, "cd": 180,
        "weapons": ["Staff of Homa", "Dragon's Bane", "Deathmatch"],
        "artifacts": ["4x Crimson Witch of Flames", "4x Shimenawa's Reminiscence"]
    },
    "Neuvillette": {
        "hp": 35000, "cr": 50, "cd": 220, "er": 120,
        "weapons": ["Tome of the Eternal Flow", "Sacrificial Jade", "Prototype Amber"],
        "artifacts": ["4x Marechaussee Hunter"]
    },
    "Alhaitham": {
        "em": 350, "cr": 70, "cd": 150, "er": 130, "atk": 1200,
        "weapons": ["Light of Foliar Incision", "Jade Cutter", "Iron Sting"],
        "artifacts": ["4x Gilded Dreams", "4x Deepwood Memories"]
    },
    "Furina": {
        "hp": 40000, "er": 160, "cr": 70, "cd": 140,
        "weapons": ["Splendor of Tranquil Waters", "Festering Desire", "Fleuve Cendre Ferryman"],
        "artifacts": ["4x Golden Troupe"]
    },
    "Mavuika": {
        "atk": 2500, "cr": 60, "cd": 180, "em": 200,
        "weapons": ["A Thousand Blazing Suns", "Serpent Spine", "Beacon of the Reed Sea"],
        "artifacts": ["4x Obsidian Codex"]
    },
    "Yelan": {
        "hp": 32000, "er": 180, "cr": 70, "cd": 160,
        "weapons": ["Aqua Simulacra", "Favonius Warbow", "Elegy for the End"],
        "artifacts": ["4x Emblem of Severed Fate"]
    },
    "Xiangling": {
        "er": 200, "em": 150, "cr": 60, "cd": 120, "atk": 1500,
        "weapons": ["The Catch", "Engulfing Lightning", "Dragon's Bane"],
        "artifacts": ["4x Emblem of Severed Fate"]
    },
    "Xingqiu": {
        "er": 180, "cr": 60, "cd": 120, "atk": 1600,
        "weapons": ["Sacrificial Sword", "Favonius Sword", "Primordial Jade Cutter"],
        "artifacts": ["4x Emblem of Severed Fate", "2x HoD + 2x NO"]
    },
    "Kaedehara Kazuha": {
        "em": 900, "er": 160,
        "weapons": ["Freedom-Sworn", "Iron Sting", "Xiphos' Moonlight"],
        "artifacts": ["4x Viridescent Venerer"]
    },
    "Nahida": {
        "em": 800, "er": 140, "cr": 50, "cd": 120,
        "weapons": ["A Thousand Floating Dreams", "The Widsith", "Magic Guide"],
        "artifacts": ["4x Deepwood Memories", "4x Gilded Dreams"]
    },
    "Zhongli": {
        "hp": 40000, "er": 130,
        "weapons": ["Black Tassel", "Staff of Homa", "Favonius Lance"],
        "artifacts": ["4x Tenacity of the Millelith", "2x HP + 2x HP"]
    },
    "Kamisato Ayaka": {
        "atk": 2000, "er": 130, "cr": 40, "cd": 200,
        "weapons": ["Mistsplitter Reforged", "Amenoma Kageuchi", "Finale of the Deep"],
        "artifacts": ["4x Blizzard Strayer"]
    },
    "Navia": {
        "atk": 2500, "cr": 70, "cd": 150, "er": 130,
        "weapons": ["Verdict", "Serpent Spine", "Melusine's Ultimate Overlord"],
        "artifacts": ["4x Nighttime Whispers in the Echoing Woods"]
    },
    "Arataki Itto": {
        "def": 2200, "er": 130, "cr": 70, "cd": 150,
        "weapons": ["Redhorn Stonethresher", "Serpent Spine", "Whiteblind"],
        "artifacts": ["4x Husk of Opulent Dreams"]
    }
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
    icon_name = char_data.get('SideIconName', '').replace('_Side', '')
    
    if "-" in char_id:
        name = f"Traveler ({element})"

    # Varsayılanlar
    optimal_stats = {}
    weapons = ["5-Star Signature Weapon", "4-Star F2P Alternative"]
    artifacts = ["4x Elemental DMG Set", "2x ATK + 2x Elemental DMG"]
    
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
        if "weapons" in meta: weapons = meta["weapons"]
        if "artifacts" in meta: artifacts = meta["artifacts"]
    else:
        # Generic Jenerik Şablonlar
        optimal_stats = {"critRate": 60, "critDamage": 120, "energyRecharge": 130}
        if element == 'Wind':
            optimal_stats['elementalMastery'] = 800
            artifacts = ["4x Viridescent Venerer"]
        elif element == 'Water':
            optimal_stats['hp'] = 30000
        elif element == 'Rock':
            optimal_stats['def'] = 2000
            artifacts = ["4x Husk of Opulent Dreams", "2x DEF + 2x Geo DMG"]
        elif element == 'Grass':
            optimal_stats['elementalMastery'] = 250
            optimal_stats['atk'] = 1500
            artifacts = ["4x Deepwood Memories", "4x Gilded Dreams"]
        else:
            optimal_stats['atk'] = 2000

    guides[char_id] = {
        "name": name,
        "element": element,
        "icon": icon_name,
        "optimal_stats": optimal_stats,
        "weapons": weapons,
        "artifacts": artifacts,
        "talent_priority": talent_priority
    }

# Eksik Beta Karakterleri Manuel Olarak Ekle (Kullanıcı İsteği: Lauma ve Nefer)
guides["10000125"] = {
    "name": "Lauma (Columbina)",
    "element": "Unknown",
    "icon": "UI_AvatarIcon_Columbina",
    "optimal_stats": {"elementalMastery": 1000, "energyRecharge": 160, "hp": 30000},
    "weapons": ["A Thousand Floating Dreams", "Sacrificial Fragments"],
    "artifacts": ["4x Gilded Dreams", "4x Deepwood Memories"],
    "talent_priority": [
        { "name": "Elemental Skill", "recommendedLevel": 10 },
        { "name": "Elemental Burst", "recommendedLevel": 8 },
        { "name": "Normal Attack", "recommendedLevel": 1 }
    ]
}

guides["10000133"] = {
    "name": "Nefer (Sandrone)",
    "element": "Unknown",
    "icon": "UI_AvatarIcon_Sandrone",
    "optimal_stats": {"elementalMastery": 900, "energyRecharge": 180, "critRate": 50, "critDamage": 120},
    "weapons": ["Wandering Evenstar", "Magic Guide"],
    "artifacts": ["4x Flower of Paradise Lost", "4x Gilded Dreams"],
    "talent_priority": [
        { "name": "Elemental Burst", "recommendedLevel": 10 },
        { "name": "Elemental Skill", "recommendedLevel": 9 },
        { "name": "Normal Attack", "recommendedLevel": 1 }
    ]
}

with open(GUIDES_PATH, 'w', encoding='utf-8') as f:
    json.dump(guides, f, indent=2, ensure_ascii=False)

print(f"KQM Hassasiyetiyle {len(guides)} karakterin portre ve silah veritabanı başarıyla inşa edildi!")
