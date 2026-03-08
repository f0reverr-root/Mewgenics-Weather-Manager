

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re, os
import sys
import json

if os.name == 'nt':
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            'Mewgenics.WeatherTool'
        )
    except Exception:
        pass


def _resolve_icon_path():
    candidates = []
    if getattr(sys, 'frozen', False):
        candidates.append(os.path.join(os.path.dirname(sys.executable), 'icon.ico'))
        meipass = getattr(sys, '_MEIPASS', '')
        if meipass:
            candidates.append(os.path.join(meipass, 'icon.ico'))
    else:
        candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico'))
        candidates.append(os.path.join(os.getcwd(), 'icon.ico'))

    for path in candidates:
        if path and os.path.exists(path):
            return path
    return None


def _apply_app_icon(root):
    icon_path = _resolve_icon_path()
    if not icon_path:
        return

    try:
        root.iconbitmap(icon_path)
    except Exception:
        pass

    if os.name != 'nt':
        return

    try:
        import ctypes
        user32 = ctypes.windll.user32
        LR_LOADFROMFILE = 0x0010
        IMAGE_ICON = 1
        WM_SETICON = 0x0080
        ICON_SMALL = 0
        ICON_BIG = 1
        GCLP_HICON = -14
        GCLP_HICONSM = -34

        root.update_idletasks()
        hwnd = root.winfo_id()

        hicon_small = user32.LoadImageW(None, icon_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE)
        hicon_big = user32.LoadImageW(None, icon_path, IMAGE_ICON, 32, 32, LR_LOADFROMFILE)

        if hicon_small:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small)
        if hicon_big:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon_big)

        set_class_icon = getattr(user32, 'SetClassLongPtrW', None)
        if set_class_icon is not None:
            if hicon_big:
                set_class_icon(hwnd, GCLP_HICON, hicon_big)
            if hicon_small:
                set_class_icon(hwnd, GCLP_HICONSM, hicon_small)
        else:
            if hicon_big:
                user32.SetClassLongW(hwnd, GCLP_HICON, hicon_big)
            if hicon_small:
                user32.SetClassLongW(hwnd, GCLP_HICONSM, hicon_small)
    except Exception:
        pass

# ── Bundled weather.gon ───────────────────────────────────────────────────────

WEATHER_GON = r"""None {
    name "WEATHER_NONE_NAME"
    desc "WEATHER_NONE_DESC"
}

Fog {
    name "WEATHER_FOG_NAME"
    desc "WEATHER_FOG_DESC"
    effects {
        Fog 1
    }
}

Rain {
    name "WEATHER_RAIN_NAME"
    desc "WEATHER_RAIN_DESC"
    ambient_sound amb_rain.ogg
    hint_persistent_elements [Water]
    effects {
        Rain 1
    }
}

HeavyRain {
    name "WEATHER_HEAVYRAIN_NAME"
    desc "WEATHER_HEAVYRAIN_DESC"
    ambient_sound amb_heavyrain.ogg
    hint_persistent_elements [Water]
    effects {
        Rain 2
        SpawnExtraThingsOnBattleStart {
            tile WaterTile
            number [12 20]
        }
    }
}

Windy {
    name "WEATHER_WINDY_NAME"
    desc "WEATHER_WINDY_DESC"
    ambient_sound amb_windy.ogg
    hint_persistent_elements [Wind]
    effects {
        Windy 1
    }
}

Sandstorm {
    name "WEATHER_SANDSTORM_NAME"
    desc "WEATHER_SANDSTORM_DESC"
    ambient_sound amb_sandstorm.ogg
    effects {
        Sandstorm 1
    }
}

Overgrowth {
    name "WEATHER_OVERGROWTH_NAME"
    desc "WEATHER_OVERGROWTH_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            tile BrambleTile
            number [2 5]
        }
        SpawnExtraThingsOnBattleStart {
            tile TallGrassTile
            number [2 5]
        }
    }
}

Earthquake {
    name "WEATHER_EARTHQUAKE_NAME"
    desc "WEATHER_EARTHQUAKE_DESC"
    effects {
        DeleteInanimateObjectsChance 25%
        SpawnExtraThingsOnBattleStart {
            object SmallRock
            number [3 5]
        }
        SpawnExtraThingsOnBattleStart {
            object Boulder
            number [0 2]
        }
    }
}

Wildfire {
    name "WEATHER_WILDFIRE_NAME"
    desc "WEATHER_WILDFIRE_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            tile FireTile
            number [3 8]
        }
    }
}

HeatWave {
    name "WEATHER_HEATWAVE_NAME"
    desc "WEATHER_HEATWAVE_DESC"
    hint_persistent_elements [Heat]
    effects {
        HeatWave 1
    }
}

Snow {
    name "WEATHER_SNOW_NAME"
    desc "WEATHER_SNOW_DESC"
    ambient_sound amb_snow.ogg
    hint_persistent_elements [Ice]
    effects {
        Snow 1
    }
}

AcidRain {
    name "WEATHER_ACIDRAIN_NAME"
    desc "WEATHER_ACIDRAIN_DESC"
    ambient_sound amb_acidrain.ogg
    effects {
        AcidRain 2
    }
}

MeteorShower {
    name "WEATHER_METEORS_NAME"
    desc "WEATHER_METEORS_DESC"
    effects {
        MeteorShower 25%
    }
}

Thunderstorm {
    name "WEATHER_THUNDERSTORM_NAME"
    desc "WEATHER_THUNDERSTORM_DESC"
    ambient_sound amb_thunderstorm.ogg
    hint_persistent_elements [Water Wind]
    effects {
        Rain 1
        RandomLightning 50%
        Windy 1
    }
}

FlashFlood {
    name "WEATHER_FLASHFLOOD_NAME"
    desc "WEATHER_FLASHFLOOD_DESC"
    ambient_sound amb_rain.ogg
    hint_persistent_elements [Water]
    effects {
        Rain 4
        SpawnExtraThingsOnBattleStart {
            tile WaterTile
            number [40 60]
        }
    }
}

TrashDay {
    name "WEATHER_TRASHDAY_NAME"
    desc "WEATHER_TRASHDAY_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            object [Junk Junk TrashBag]
            number [3 6]
        }
    }
}

RainingFrogs {
    name "WEATHER_FROGS_NAME"
    desc "WEATHER_FROGS_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            object NeutralToad
            number [2 4]
        }
    }
}

PipeBlockage {
    name "WEATHER_BLOCKAGE_NAME"
    desc "WEATHER_BLOCKAGE_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            object Poop
            number [1 3]
        }
        SpawnExtraThingsOnBattleStart {
            tile CreepTile
            number [3 5]
        }
    }
}

PayDay {
    name "WEATHER_PAYDAY_NAME"
    desc "WEATHER_PAYDAY_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            object Coin
            number [5 10]
        }
    }
}

HuntingSeason {
    name "WEATHER_HUNTING_NAME"
    desc "WEATHER_HUNTING_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            trap BearTrap
            number [2 4]
        }
    }
}

RestlessDead {
    name "WEATHER_RESTLESS_NAME"
    desc "WEATHER_RESTLESS_DESC"
    effects {
        GlobalSpawnOnRoundEnd {
            object NeutralZombieKitten
        }
    }
}

FireflySwarm {
    name "WEATHER_FIREFLY_NAME"
    desc "WEATHER_FIREFLY_DESC"
    effects {
        FireflySwarm 2
    }
}

ButterflySwarm {
    name "WEATHER_BUTTERFLY_NAME"
    desc "WEATHER_BUTTERFLY_DESC"
    ambient_sound amb_butterflyswarm.ogg
    effects {
        ButterflySwarm 2
    }
}

FlySwarm {
    name "WEATHER_FLYSWARM_NAME"
    desc "WEATHER_FLYSWARM_DESC"
    ambient_sound amb_flyswarm.ogg
    effects {
        FlySwarm 50%
    }
}

VisualFlySwarm {
    name "WEATHER_TORFLIES_NAME"
    desc "WEATHER_TORFLIES_DESC"
    ambient_sound amb_flyswarm.ogg
    effects {
        VisualFlySwarm 1
    }
}

LowGravity {
    name "WEATHER_LOWGRAV_NAME"
    desc "WEATHER_LOWGRAV_DESC"
    effects {
        LowGravityRangeBoost 2
        LowGravityKnockbackBoost 1
        ClearDefaultDebris 1
        AddTilesetObjects {
            FloatingDebris {
                count 20
            }
        }
    }
}

Firestorm {
    name "WEATHER_FIRESTORM_NAME"
    desc "WEATHER_FIRESTORM_DESC"
    hint_persistent_elements [Fire]
    effects {
        FireStorm 0%
        SpawnExtraThingsOnBattleStart {
            tile FireTile
            number [2 5]
        }
    }
}

KaijuFirestorm {
    name "WEATHER_KAIJUFIRE_NAME"
    desc "WEATHER_KAIJUFIRE_DESC"
    hint_persistent_elements [Fire]
    effects {
        FireStorm 33%
        LowerAmbientLight 50%
    }
}

Meteornado {
    name "WEATHER_METEORNADO_NAME"
    desc "WEATHER_METEORNADO_DESC"
    effects {
        Meteornado 1
    }
}

KaijuMeteornado {
    name "WEATHER_KAIJUMETEORNADO_NAME"
    desc "WEATHER_KAIJUMETEORNADO_DESC"
    effects {
        Meteornado 1
        LowerAmbientLight 33%
        SpecialGodRays {
            Big {
                position [4.5 4.5]
                follow_character_tag zaratana
            }
        }
    }
}

KaijuMeteornadoSolo {
    name "WEATHER_KAIJUMETEORSOLO_NAME"
    desc "WEATHER_KAIJUMETEORSOLO_DESC"
    effects {
        Meteornado 1
        LowerAmbientLight 50%
        SpecialGodRays {
            Big {
                position [4.5 4.5]
                follow_character_tag zaratana
            }
        }
    }
}

RobotUprising {
    name "WEATHER_ROBOTS_NAME"
    desc "WEATHER_ROBOTS_DESC"
    effects {
        FactionUprising robot
        SpawnExtraThingsOnBattleStart {
            object [SecurityBot CopBot_Uprising Rover RoboTom]
            number 1
        }
        SpawnExtraThingsOnBattleStart {
            object [Bombchu Deathbot RoboVacuum TinkererTurret]
            number [1 3]
        }
    }
}

HauntedNight {
    name "WEATHER_HAUNTED_NAME"
    desc "WEATHER_HAUNTED_DESC"
    effects {
        FactionUprising ghost
        LowerAmbientLight 33%
        SpawnExtraThingsOnBattleStart {
            object [Spookie Scary Tatters Wisp Wisp Wisp]
            number [2 4]
        }
    }
}

BirdMigration {
    name "WEATHER_MIGRATION_NAME"
    desc "WEATHER_MIGRATION_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            object [Bird]
            number [1 2]
        }
    }
}

CockroachSwarm {
    name "WEATHER_COCKROACHES_NAME"
    desc "WEATHER_COCKROACHES_DESC"
    effects {
        CockroachSwarm 1
        CharacterTypeGainsStatusAtBattleStart {
            tag any
            Conditional_Flying {
            } Else {
                Fear [1 .25]
                Poison [1 .25]
            }
        }
    }
}

JudgementDay {
    name "WEATHER_JUDGEMENT_NAME"
    desc "WEATHER_JUDGEMENT_DESC"
    effects {
        JudgementDay 25
    }
}

Pandemonium {
    name "WEATHER_PANDEMONIUM_NAME"
    desc "WEATHER_PANDEMONIUM_DESC"
    effects {
        StatusCharactersOnRoundStart {
            Madness [1 .25]
        }
    }
}

TheHollowing {
    name "WEATHER_HOLLOWING_NAME"
    desc "WEATHER_HOLLOWING_DESC"
    effects {
        StatusCharactersOnRoundEnd {
            Conditional_GoodRoll {
                odds 25%
                Conditional_Corpse {
                    Revive 50%
                    Madness 5
                }
            }
        }
    }
}

OilSpill {
    name "WEATHER_OILSPILL_NAME"
    desc "WEATHER_OILSPILL_DESC"
    effects {
        SpawnTilePuddleOnBattleStart {
            tile OilTile
            min_radius 1.5
            max_radius 3.5
        }
    }
}

Blizzard {
    name "WEATHER_BLIZZARD_NAME"
    desc "WEATHER_BLIZZARD_DESC"
    ambient_sound amb_blizzard.ogg
    hint_persistent_elements [Ice Wind]
    effects {
        Snow 1
        RandomLightning 50%
        Windy 1
    }
}

Hurricane {
    name "WEATHER_HURRICANE_NAME"
    desc "WEATHER_HURRICANE_DESC"
    ambient_sound amb_windy.ogg
    hint_persistent_elements [Wind]
    effects {
        Windy 10
    }
}

StrangeSpikes {
    name "WEATHER_STRANGESPIKES_NAME"
    desc "WEATHER_STRANGESPIKES_DESC"
    effects {
        StatusCharactersOnRoundEnd {
            Thorns 1
        }
    }
}

BlessedDay {
    name "WEATHER_BLESSED_NAME"
    desc "WEATHER_BLESSED_DESC"
    hint_persistent_elements [Holy]
    effects {
        PersistentElement Holy
        GlobalHealthRegenAura 3
    }
}

StealthMission {
    name "WEATHER_STEALTH_NAME"
    desc "WEATHER_STEALTH_DESC"
    effects {
        CharacterTypeGainsStatusAtBattleStart {
            tag any
            Stealth 1
        }
    }
}

Infestation {
    name "WEATHER_INFESTATION_NAME"
    desc "WEATHER_INFESTATION_DESC"
    effects {
        StatusAllCharactersOnSpawn {
            Conditional_Tiny {
            } Else {
                AllyInfested {
                    object ["Maggot", "Fly"]
                }
            }
        }
    }
}

Eruption {
    name "WEATHER_ERUPTION_NAME"
    desc "WEATHER_ERUPTION_DESC"
    effects {
        SpawnVolcanoOnBattleStart {
            object MiniVolcano
            puddle_tile LavaTile
            min_radius .2
            max_radius 2.2
        }
    }
}

Drugs {
    name "WEATHER_DRUGS_NAME"
    desc "WEATHER_DRUGS_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            object RandomCatnipPickup
            number [4 6]
        }
        FindExtraItemFromPoolOnBattleEnd pills
    }
}

TrainingDay {
    name "WEATHER_TRAININGDAY_NAME"
    desc "WEATHER_TRAININGDAY_DESC"
    effects {
        SpawnVolcanoOnBattleStart {
            object PunchingBag
        }
    }
}

Tornado {
    name "WEATHER_TORNADOES_NAME"
    desc "WEATHER_TORNADOES_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            object NeutralTwister
            number [1 2]
        }
        GlobalSpawnOnRoundEnd {
            object NeutralTwister
            number [1 2]
        }
    }
}

CrazyWeather {
    name "WEATHER_CRAZY_NAME"
    desc "WEATHER_CRAZY_DESC"
    effects {
        RandomWeatherEachFight [Fog Rain Windy Sandstorm HeatWave Snow Thunderstorm Blizzard Tornado]
    }
}

BountyHunting {
    name "WEATHER_BOUNTY_NAME"
    desc "WEATHER_BOUNTY_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            object EventBountyHunter
        }
    }
}

Minesweeper {
    name "WEATHER_MINESWEEPER_NAME"
    desc "WEATHER_MINESWEEPER_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            trap LandMine
            number [2 4]
        }
    }
}

AlienInvasion {
    name "WEATHER_ALIENS_NAME"
    desc "WEATHER_ALIENS_DESC"
    effects {
        FactionUprising alien
        SpawnExtraThingsOnBattleStart {
            object [SmallUFO SmallUFO SmallUFO YellowBlaster GreyAlien GreenProber]
            number [2 3]
        }
        SpawnExtraThingsOnBattleStart {
            object [BigUFO]
            number [-2 1]
        }
    }
}

Birdemic {
    name "WEATHER_BIRDEMIC_NAME"
    desc "WEATHER_BIRDEMIC_DESC"
    effects {
        FactionUprising {
            tag bird
            extra_statuses {
                Conditional_HasTag {
                    tag bonusbird
                    ApplyPassives {
                        AddInitiative 999
                    }
                    AddExtraTurnsBeforeRun 2
                }
                AllStatsUp 2
                HealthGain 8
            }
        }
        SpawnExtraThingsOnBattleStart {
            object [Bird]
            number [2 4]
        }
    }
}

SolarFlare {
    name "WEATHER_SOLARFLARE_NAME"
    desc "WEATHER_SOLARFLARE_DESC"
    effects {
        SolarFlare {
            damage 5
            effects {
                Burn 3
                Blind 3
            }
            elements [
                Fire
            ]
        }
    }
}

GeomagneticStorm {
    name "WEATHER_GEOMAGSTORM_NAME"
    desc "WEATHER_GEOMAGSTORM_DESC"
    effects {
        StatusCharactersOnRoundEnd {
            tag_filter rock
            FloatingRockTrap 1
        }
        SpawnExtraThingsOnBattleStart {
            object SmallRock
            number [1 3]
        }
        SpawnExtraThingsOnBattleStart {
            object Boulder
            number [0 2]
        }
    }
}

TheShimmer {
    name "WEATHER_SHIMMER_NAME"
    desc "WEATHER_SHIMMER_DESC"
    effects {
        AddPostProcessEffect {
            shader shimmervignette
            requires_framebuffer false
        }
        StatusCharactersOnRoundStart {
            Conditional_GoodRoll {
                odds .5
                RandomStatusFromPool {
                    RandomStatUp 1
                    RandomStatUp 1
                    RandomStatUp 1
                    RandomStatUp 1
                    Brace 1
                    Shield 1
                    DivineShield 1
                    SpellDamageUp 1
                    DamageUp 1
                    Thorns 1
                    KineticSpikes 1
                }
            } Else {
                RandomStatusFromPool {
                    RandomStatDown 1
                    RandomStatDown 1
                    RandomStatDown 1
                    RandomStatDown 1
                    Poison 1
                    Bruise 1
                    Bleed 1
                    Weakness 1
                    Blind 1
                    Drowsy 1
                    Slow 1
                }
            }
        }
        StatusAllCharactersOnSpawn {
            Conditional_PartyMember {
                ApplyPassives {
                    StatusOnBattleEnd {
                        RandomMutation 1
                    }
                }
            }
        }
    }
}

StrangeEggs {
    name "WEATHER_STRANGEEGGS_NAME"
    desc "WEATHER_STRANGEEGGS_DESC"
    effects {
        SpawnExtraThingsOnBattleStart {
            object AlienEgg
            number [3 6]
        }
    }
}

AlienOvergrowth {
    name "WEATHER_ALIENOVERGROWTH_NAME"
    desc "WEATHER_ALIENOVERGROWTH_DESC"
    effects {
        SpawnVolcanoOnBattleStart {
            object Sprout
            puddle_tile [BrambleTile TallBrambleTile]
            min_radius 1
            max_radius 2.2
            number [3 5]
        }
    }
}
"""

# ── GON helpers ───────────────────────────────────────────────────────────────

def parse_blocks(text):
    blocks, i, n = [], 0, len(text)
    while i < n:
        while i < n and text[i] in ' \t\r\n': i += 1
        if i >= n: break
        if text[i:i+2] == '//':
            e = text.find('\n', i); i = e+1 if e != -1 else n; continue
        if text[i:i+2] == '/*':
            e = text.find('*/', i); i = e+2 if e != -1 else n; continue
        if text[i].isalpha() or text[i] == '_':
            j = i
            while j < n and (text[j].isalnum() or text[j] == '_'): j += 1
            name = text[i:j]; i = j
            while i < n and text[i] in ' \t\r\n': i += 1
            if i < n and text[i] == '{':
                start = i; depth = 0
                while i < n:
                    if text[i] == '{': depth += 1
                    elif text[i] == '}':
                        depth -= 1
                        if depth == 0: i += 1; break
                    i += 1
                blocks.append((name, text[start:i]))
        else:
            i += 1
    return blocks

def has_effects(block):
    m = re.search(r'\beffects\s*\{', block)
    if not m: return True
    s = block.find('{', m.start()); depth = 0
    for ch in block[s:]:
        if ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0: break
    return bool(block[s+1:block.find('}', s)].strip())

def strip_effects(block):
    m = re.search(r'\beffects\s*\{', block)
    if not m: return block
    s = block.find('{', m.start()); depth = 0; i = s
    while i < len(block):
        if block[i] == '{': depth += 1
        elif block[i] == '}':
            depth -= 1
            if depth == 0: i += 1; break
        i += 1
    return block[:m.start()] + 'effects {}\n' + block[i:]

# ── Metadata ──────────────────────────────────────────────────────────────────

NAMES = {
    'None':'None (Clear)','Fog':'Fog','Rain':'Rain','HeavyRain':'Heavy Rain',
    'Windy':'Windy','Sandstorm':'Sandstorm','Overgrowth':'Overgrowth',
    'Earthquake':'Earthquake','Wildfire':'Wildfire','HeatWave':'Heat Wave',
    'Snow':'Snow','AcidRain':'Acid Rain','MeteorShower':'Meteor Shower',
    'Thunderstorm':'Thunderstorm','FlashFlood':'Flash Flood','TrashDay':'Trash Day',
    'RainingFrogs':'Raining Frogs','PipeBlockage':'Pipe Blockage','PayDay':'Pay Day',
    'HuntingSeason':'Hunting Season','RestlessDead':'Restless Dead',
    'FireflySwarm':'Firefly Swarm','ButterflySwarm':'Butterfly Swarm',
    'FlySwarm':'Fly Swarm','VisualFlySwarm':'Visual Fly Swarm',
    'LowGravity':'Low Gravity','Firestorm':'Firestorm',
    'KaijuFirestorm':'Kaiju Firestorm','Meteornado':'Meteornado',
    'KaijuMeteornado':'Kaiju Meteornado','KaijuMeteornadoSolo':'Kaiju Meteornado Solo',
    'RobotUprising':'Robot Uprising','HauntedNight':'Haunted Night',
    'BirdMigration':'Bird Migration','CockroachSwarm':'Cockroach Swarm',
    'JudgementDay':'Judgement Day','Pandemonium':'Pandemonium',
    'TheHollowing':'The Hollowing','OilSpill':'Oil Spill','Blizzard':'Blizzard',
    'Hurricane':'Hurricane','StrangeSpikes':'Strange Spikes','BlessedDay':'Blessed Day',
    'StealthMission':'Stealth Mission','Infestation':'Infestation','Eruption':'Eruption',
    'Drugs':'Drugs','TrainingDay':'Training Day','Tornado':'Tornado',
    'CrazyWeather':'Crazy Weather','BountyHunting':'Bounty Hunting',
    'Minesweeper':'Minesweeper','AlienInvasion':'Alien Invasion','Birdemic':'Birdemic',
    'SolarFlare':'Solar Flare','GeomagneticStorm':'Geomagnetic Storm',
    'TheShimmer':'The Shimmer','StrangeEggs':'Strange Eggs',
    'AlienOvergrowth':'Alien Overgrowth',
}

CATS = {
    'Natural':     ['Fog','Rain','HeavyRain','Windy','Sandstorm','Snow','Blizzard',
                    'Hurricane','Thunderstorm','FlashFlood','HeatWave','Tornado','Firestorm'],
    'Disasters':   ['Earthquake','Wildfire','MeteorShower','Meteornado','Eruption',
                    'SolarFlare','GeomagneticStorm','KaijuFirestorm',
                    'KaijuMeteornado','KaijuMeteornadoSolo'],
    'Creatures':   ['Overgrowth','RainingFrogs','RestlessDead','FireflySwarm',
                    'ButterflySwarm','FlySwarm','VisualFlySwarm','CockroachSwarm',
                    'BirdMigration','Birdemic','Infestation','AlienOvergrowth','StrangeEggs'],

}

EXCLUDED = {
    'Pandemonium','TheHollowing','JudgementDay','HauntedNight',
    'RobotUprising','AlienInvasion','TheShimmer','LowGravity',
    'CrazyWeather','StrangeSpikes','AcidRain',
    'TrashDay','PayDay','HuntingSeason','PipeBlockage','OilSpill',
    'BountyHunting','Minesweeper','TrainingDay','Drugs',
    'BlessedDay','StealthMission','None',
}

# ── App ───────────────────────────────────────────────────────────────────────

class App(tk.Tk):
    BG    = '#2b2b2b'
    PANEL = '#242424'
    CARD  = '#333333'
    ACC   = '#8b3a3a'
    TEXT  = '#d4cfc9'
    SUB   = '#7a7570'
    ON    = '#6a9e6a'
    OFF   = '#5a5550'
    FN    = ('Georgia', 10)
    FS    = ('Georgia', 9)
    FT    = ('Georgia', 13, 'bold')
    FC    = ('Georgia', 9, 'bold')

    def __init__(self):
        super().__init__()
        self.title('Mewgenics — Weather Tool')
        self.configure(bg=self.BG)
        self.geometry('920x700')
        _apply_app_icon(self)
        self.resizable(False, False)
        # rounded
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Round.TButton',
            relief='flat', borderwidth=0,
            padding=(10, 5),
            background='#3d3d3d', foreground='#d4cfc9',
            font=('Georgia', 9))
        style.map('Round.TButton',
            background=[('active', '#4a4545')])
        style.configure('RoundAcc.TButton',
            relief='flat', borderwidth=0,
            padding=(10, 5),
            background='#8b3a3a', foreground='#d4cfc9',
            font=('Georgia', 9))
        style.map('RoundAcc.TButton',
            background=[('active', '#a04444')])

        self.originals = {}
        self.states    = {}
        self.refs      = {}
        self._settings_filename = 'weather_tool_settings.json'
        self._settings_write_warning_shown = False
        self._load()
        self._ui()
        self._populate()
        self.protocol('WM_DELETE_WINDOW', self._on_close)
        self.after(50, lambda: _apply_app_icon(self))

    def _primary_settings_path(self):
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, self._settings_filename)

    def _fallback_settings_path(self):
        appdata = os.getenv('APPDATA')
        if not appdata:
            appdata = os.path.expanduser('~')
        return os.path.join(appdata, 'MewgenicsWeatherTool', self._settings_filename)

    def _load_settings(self):
        for path in (self._primary_settings_path(), self._fallback_settings_path()):
            if not os.path.exists(path):
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data
            except Exception:
                continue
        return {}

    def _save_settings(self):
        data = {name: bool(var.get()) for name, var in self.states.items()}

        primary_path = self._primary_settings_path()
        try:
            with open(primary_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            pass

        fallback_path = self._fallback_settings_path()
        try:
            os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
            with open(fallback_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            if not self._settings_write_warning_shown:
                self._settings_write_warning_shown = True
                self._sv.set('Warning: could not save toggle settings.')
            return False

    def _on_close(self):
        self._save_settings()
        self.destroy()

    def _load(self):
        saved = self._load_settings()
        self.blocks = parse_blocks(WEATHER_GON)
        for name, text in self.blocks:
            self.originals[name] = text
            default_state = has_effects(text)
            if name in saved:
                default_state = bool(saved[name])
            self.states[name] = tk.BooleanVar(value=default_state)

    def _ui(self):
        # header
        h = tk.Frame(self, bg=self.BG, padx=20, pady=14)
        h.pack(fill='x')
        tk.Label(h, text='⛈  MEWGENICS  WEATHER  MANAGER',
                 font=self.FT, bg=self.BG, fg=self.ACC).pack(side='left')
        bf = tk.Frame(h, bg=self.BG)
        bf.pack(side='right')
        for label, cmd, ac in [
                ('Enable All',         self._all_on,    False),
                ('Disable All',        self._all_off,   False),
                ('Install to Game ▶',  self._build,     True)]:
            ttk.Button(bf, text=label, command=cmd,
                       style='RoundAcc.TButton' if ac else 'Round.TButton',
                       cursor='hand2').pack(side='left', padx=3)

        # instruction bar
        ib = tk.Frame(self, bg=self.PANEL, padx=20, pady=7)
        ib.pack(fill='x')
        tk.Label(ib,
            text='Toggle weather effects on or off  →  click  Install to Game  '
                 '→  point to your Mewgenics game folder. Launch game normally.',
            font=self.FS, bg=self.PANEL, fg=self.SUB).pack(anchor='w')

        # scroll canvas
        outer = tk.Frame(self, bg=self.BG)
        outer.pack(fill='both', expand=True, padx=14, pady=10)
        self._cv = tk.Canvas(outer, bg=self.BG, bd=0, highlightthickness=0)
        sb = ttk.Scrollbar(outer, orient='vertical', command=self._cv.yview)
        self._cv.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')
        self._cv.pack(side='left', fill='both', expand=True)
        self._inner = tk.Frame(self._cv, bg=self.BG)
        win = self._cv.create_window((0,0), window=self._inner, anchor='nw')
        self._inner.bind('<Configure>',
            lambda e: self._cv.configure(scrollregion=self._cv.bbox('all')))
        self._cv.bind('<Configure>',
            lambda e: self._cv.itemconfig(win, width=e.width))
        self._cv.bind_all('<MouseWheel>',
            lambda e: self._cv.yview_scroll(-1*(e.delta//120), 'units'))

        # status
        self._sv = tk.StringVar(value='Ready. Toggle weather above then click Install to Game.')
        tk.Label(self, textvariable=self._sv, font=self.FS,
                 bg=self.PANEL, fg=self.SUB, anchor='w',
                 padx=16, pady=6).pack(fill='x', side='bottom')

    def _populate(self):
        for w in self._inner.winfo_children():
            w.destroy()
        self.refs.clear()

        assigned = set()
        all_cats = list(CATS.items())
        leftover = [n for n,_ in self.blocks
                    if not any(n in m for _,m in all_cats)
                    and n not in EXCLUDED]
        if leftover:
            all_cats.append(('Other', leftover))

        for col, (cat, members) in enumerate(all_cats):
            present = [m for m in members if m in self.originals and m not in EXCLUDED]
            if not present: continue
            cf = tk.Frame(self._inner, bg=self.BG)
            cf.grid(row=0, column=col, sticky='n', padx=5, pady=2)
            hf = tk.Frame(cf, bg=self.ACC)
            hf.pack(fill='x', pady=(0,5))
            tk.Label(hf, text=f'  {cat.upper()}  ',
                     font=self.FC, bg=self.ACC, fg=self.BG,
                     pady=3).pack(anchor='w')
            for name in present:
                self._row(cf, name)

    def _row(self, parent, name):
        var  = self.states[name]
        en   = var.get()
        disp = NAMES.get(name, name)
        row  = tk.Frame(parent, bg=self.CARD, pady=3, padx=8)
        row.pack(fill='x', pady=2)
        dot = tk.Label(row, text='●', font=self.FN,
                       bg=self.CARD, fg=self.ON if en else self.OFF)
        dot.pack(side='left', padx=(0,5))
        tk.Label(row, text=disp, font=self.FN,
                 bg=self.CARD, fg=self.TEXT, anchor='w', width=21).pack(side='left')
        tv = tk.StringVar(value='ON' if en else 'OFF')
        btn = tk.Button(row, textvariable=tv, font=self.FS, width=4,
                        bg=self.ON if en else '#3a3535',
                        fg=self.BG if en else self.SUB,
                        relief='flat', cursor='hand2')
        btn.configure(command=lambda n=name,v=var,d=dot,t=tv,b=btn:
                      self._tog(n,v,d,t,b))
        btn.pack(side='right', padx=2)
        self.refs[name] = (dot, btn, tv)

    def _tog(self, name, var, dot, tv, btn):
        new = not var.get(); var.set(new)
        dot.configure(fg=self.ON if new else self.OFF)
        tv.set('ON' if new else 'OFF')
        btn.configure(bg=self.ON if new else '#3a3535',
                      fg=self.BG if new else self.SUB)
        en  = sum(v.get() for v in self.states.values())
        self._sv.set(f'{en} enabled · {len(self.states)-en} disabled')
        self._save_settings()

    def _all_on(self):
        for n,(d,b,t) in self.refs.items():
            self.states[n].set(True)
            d.configure(fg=self.ON); t.set('ON')
            b.configure(bg=self.ON, fg=self.BG)
        self._sv.set(f'All {len(self.states)} weather effects enabled.')
        self._save_settings()

    def _all_off(self):
        for n,(d,b,t) in self.refs.items():
            self.states[n].set(False)
            d.configure(fg=self.OFF); t.set('OFF')
            b.configure(bg='#3a3535', fg=self.SUB)
        self._sv.set(f'All {len(self.states)} weather effects disabled.')
        self._save_settings()

    def _build(self):
        game_dir = filedialog.askdirectory(title='Select your Mewgenics game folder')
        if not game_dir: return

        data_dir = os.path.join(game_dir, 'data')

        try:
            os.makedirs(data_dir, exist_ok=True)
        except PermissionError:
            messagebox.showerror('Permission Denied',
                'Could not write to the game folder.\n\n'
                'Fix: Right-click the weather tool and select\n'
                '"Run as administrator", then try again.')
            self._sv.set('Error: permission denied. Run as administrator.')
            return

        parts = []
        for name, orig in self.originals.items():
            block = orig if self.states[name].get() else strip_effects(orig)
            parts.append(f'{name} {block}')

        gon_path = os.path.join(data_dir, 'weather.gon')
        try:
            with open(gon_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(parts) + '\n')
        except PermissionError:
            messagebox.showerror('Permission Denied',
                'Could not write to the game folder.\n\n'
                'Fix: Right-click the weather tool and select\n'
                '"Run as administrator", then try again.')
            self._sv.set('Error: permission denied. Run as administrator.')
            return

        en  = sum(v.get() for v in self.states.values())
        dis = len(self.states) - en

        self._sv.set(f'✔  Installed!  {en} enabled · {dis} disabled  →  {gon_path}')
        messagebox.showinfo('Installed!',
            f'weather.gon written to:\n{gon_path}\n\n'
            f'{en} enabled  ·  {dis} disabled\n\n'
            f'Launch Mewgenics and your settings will be active.\n'
            f'To uninstall, delete:  data/weather.gon  from your game folder.')


if __name__ == '__main__':
    App().mainloop()
