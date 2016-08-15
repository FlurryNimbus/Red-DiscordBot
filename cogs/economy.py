import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO, fileIO
from collections import namedtuple, defaultdict
from datetime import datetime
from random import randint
from copy import deepcopy
from .utils import checks
from __main__ import send_cmd_help
import os
import time
import logging
import random

default_settings = {"PAYDAY_TIME": 300, "PAYDAY_CREDITS": 120, "SLOT_MIN": 5, "SLOT_MAX": 100, "SLOT_TIME": 0}

slot_payouts = """Loot box item values:
    :green_heart:Common
            5:gem:
    :blue_heart:Rare
            15:gem:
    :purple_heart:Epic
            50:gem:
    :yellow_heart:Legendary
            200:gem:
    """

# Yup.
commonloot = {
    "sprays": ["...Punch", "Catcher", "Caution", "Dance", "Dark Logo", "Dark Overwatch", "Dark Title",
               "Fighters of the Storm 2", "Fuji", "Goldshire Pictures", "Leek", "Lumérico", "Numbani Statue",
               "Omnic Rights", "Overwatch", "Overwatch Title", "Rhino", "Rikimaru", "Sarcophagus", "Scooter", "Scroll",
               "Siege Mode", "Six-Gun Killer", "Sol", "Soulstone", "Vivi's Adventure", "Action (Ana)", "Ana (Ana)",
               "Bearer", "Cheer", "Cracked", "Cute (Ana)", "Eyepatch", "Fareeha", "Gaze (Ana)", "Grenade",
               "Guardian (Ana)", "Hesitation", "Icon (Ana)", "Letter", "Old Soldier (Ana)", "Overhead", "Photograph",
               "Pixel (Ana)", "Rifle (Ana)", "Shadow (Ana)", "Shhh" "Sidearm", "Wedjat (Ana)", "Wrist Launcher (Ana)",
               "ZZZ", "Action (Bastion)", "Bird" "Birdwatchers", "Black", "Blocks", "Cannon (Bastion)", "Crisis",
               "Curious", "Cute (Bastion)", "ES4", "Fire at Will", "Flight", "Flower Power", "Ganymede", "Giant",
               "Icon (Bastion)", "In Repairs", "Nest", "Omnic", "Overgrown", "Pixel (Bastion)", "Recovery", "Retro",
               "Sprout", "Wood and Stone", "Bang (D.Va)", "Bubble Gum", "Bunny", "Bunny (2)", "Bunny Hop",
               "Cute (D.Va)", "Diva", "GG", "Hana", "Headset", "Heart", "Icon (D.Va)", "Light Gun", "Love DVa", "Meka",
               "Nano Cola", "Photo", "Pixel (D.Va)", "Pixel Bunny", "Power Up!", "Salt", "Star", "Unload",
               "Walk of Fame (D.Va)", "Watching", "Assassin", "Cute (Genji)", "Dragon (Genji)", "Dragonblade",
               "Draw (Genji)", "God of War", "Green Ninja", "Icon (Genji)", "Kaze No Gotoku", "Lunge", "Nin (Genji)",
               "Onmyodo", "Pixel (Genji)", "Prepared", "Ryugekiken", "Shimada", "Shuriken", "Shuriken (2)",
               "Signature (Genji)", "Soul", "Stance", "Stoic (Genji)", "Swords", "Target Practice", "Warrior", "Archer",
               "Challenge", "Cloud", "Cute (Hanzo)", "Dragon (Hanzo)", "Dragons (Hanzo)", "Dragonstrike", "Drawn",
               "Duty", "Haori", "Icon (Hanzo)", "Kneeling", "Kumo", "Moon", "Nin (Hanzo)", "Pixel (Hanzo)", "Sake",
               "Scarf", "Seal", "Spray (Hanzo)", "Stoic (Hanzo)", "Successor", "Tea", "Wanderer", "Yellow", "Ahhhh!",
               "Bang Bang", "Crazy", "Cute (Junkrat)", "Fireball", "Firework", "For You", "Frag", "Fuse",
               "Grin (Junkrat)", "Icon (Junkrat)", "Junk", "Kaboom!", "Mad", "Mayhem", "Mine", "Minefield",
               "Pixel (Junkrat)", "Rolling", "Smile (Junkrat)", "Smoke", "Spin (Junkrat)", "Trapper",
               "Wanted (Junkrat)", "Vroom!!", "Acelerar", "Baixo", "Bass", "Break It Down", "Cereal",
               "Confident (Lúcio)", "Cute (Lúcio)", "Deck", "Frog", "Grin (Lúcio)", "Hero", "Icon (Lúcio)",
               "In Concert", "Kambô", "Pixel (Lúcio)", "Scratch", "Signature (Lúcio)", "Signature (2) (Lúcio)",
               "Spin (Lúcio)", "Tag", "Triplo", "Under Control", "Vinyl", "Walk of Fame (Lúcio)", "Wave", "Badge",
               "BAMF", "Bang! (McCree)", "Buckle", "Bullet", "Cute (McCree)", "Deadeye", "Draw (McCree)", "Enigma",
               "Gunslinger", "High Noon", "Icon (McCree)", "Jesse", "Noose", "Outlaw", "Pixel (McCree)", "Skull",
               "Spin (McCree)", "Take It Easy", "Target", "The Name's", "Thumbs Up", "Tumbleweed", "Wanted (McCree)",
               "Your Face Here", "^_^", ">_<", "Beat The Heat", "Blaster (Mei)", "Carefree", "Casual",
               "Confident (Mei)", "Cute (Mei)", "Dizzy", "Explorer (Mei)", "Eyes (Mei)", "Hairpin", "Icon (Mei)",
               "Mei's Journal", "Pixel (Mei)", "Popsicle", "Print", "Reading", "Sketch", "Smile (Mei)", "Snow Art",
               "Snowball", "Snowman", "Soft Serve", "Walled", "Arrow", "Bandage", "Battle Ready", "Blaster (Mercy)",
               "Cute (Mercy)", "Emblem (Mercy)", "Gauze", "Halo", "Heroes Never Die", "Huge Rez!!", "Icon (Mercy)",
               "Light (Mercy)", "Medic", "On Call", "Patched Up", "Pixel (Mercy)", "Resurrect", "Smile (Mercy)",
               "Stethoscope", "Sting", "Support", "Swiss", "Valkyrie", "Wings (Mercy)", "Ziegler", "Aerial Superiority",
               "Amari", "Ana (Pharah)", "Cobra", "Concussive Blast", "Cute (Pharah)", "Guardian (Pharah)", "Hieroglyph",
               "Icon (Pharah)", "Incoming", "Justice...", "On Guard", "Pixel (Pharah)", "Play Pharah", "Raptora",
               "Rocket Jump", "Rocket Launcher", "Salute (Pharah)", "Scarab", "Statue", "Stone", "Tattoo",
               "Wedjat (Pharah)", "Wings (Pharah)", "Wrist Launcher (Pharah)", "Blackwatch", "Blossom", "Cloaked",
               "Cute (Reaper)", "Death Blossom", "Death Comes", "Die Die Die", "Everywhere", "Grave (Reaper)",
               "Hellfire", "Hooded", "Horns", "Icon (Reaper)", "Oops (Reaper)", "Pixel (Reaper)", "Psst", "Reap On",
               "Reaping", "Revenge", "Scythes", "Shadow Step", "Shadow (Reaper)", "Silent", "Soul Globe",
               "Time To Kill", "Barrier (Reinhardt)", "Charge", "Cracks", "Crusader", "Cute (Reinhardt)",
               "Earthshatter",
               "Emblem (Reinhardt)", "Firestrike", "Glorious", "Hammer Down", "Helm", "Honor", "Icon (Reinhardt)",
               "Knight", "Lion", "Pixel (Reinhardt)", "Roar (Reinhardt)", "Royal", "Shield Up", "Stein",
               "Swing (Reinhardt)", "Vigilant", "White (Reinhardt)", "Wilhelm", "Wrestle (Reinhardt)", "Breathin'",
               "Cute (Roadhog)", "Deep Thoughts", "Emblem (Roadhog)", "Eyes (Roadhog)", "Free Pig", "Fresh Meat",
               "Gotcha", "Grand Theft" "Helmet", "Here Piggy", "Hogpower", "Hooked", "Icon (Roadhog)", "Left",
               "License", "Mako", "No Pork", "Piggy", "Pixel (Roadhog)", "Popper", "Tails", "Toxic",
               "Wanted (Roadhog)", "Wild Hog", "76", "All Soldiers", "American Hero", "Coin", "Cute (Solider 76)",
               "Grave (Soldier 76)", "Grizzled", "Heal Up", "Helix", "Hooah", "Icon (Soldier 76)", "Jacket:76",
               "Move!", "Old Soldier (Soldier 76)", "Pixel (Soldier 76)", "Pulse Rifle", "Rifle: 76 (Soldier 76)",
               "Rockets", "Salute (Soldier 76)", "Strike Commander", "Vigilante", "Vigilante (2)",
               "Visor (Soldier 76)", "Wanted (Soldier 76)", "Agent", "Architect", "Behold", "Blueprint", "Builder",
               "Car Wash", "Caution (Symmetra)", "Cute (Symmetra)", "Design", "Glove", "Icon (Symmetra)",
               "Light (Symmetra)", "Lines", "Lotus", "Pixel (Symmetra)", "Pose", "Projector", "Sayta", "Superior",
               "The Path", "Vawani", "Vishkar", "Visor (Symmetra)", "Weaver", "Will", "Armor", "Beard",
               "Catch A Ride", "Chef", "Claw", "Cute (Torbjörn)", "Fix It Up", "Forged", "Gears", "Get Ready",
               "Hammer", "Hot", "Icon (Torbjörn)", "Ironclad", "Kanon", "Mask", "Molten Core", "Pixel (Torbjörn)",
               "Ready to Work", "Run!", "Smält", "Stoic (Torbjörn)", "Turret", "Turrets", "Upgradera", "Blink",
               "Bombs Away!", "Cavalry's Here", "Cheers", "Cheers, Love", "Clock's Tickin'", "Confident (Tracer)",
               "Cute (Tracer)", "Fighter", "Icon (Tracer)", "Kneeling (Tracer)", "Lena", "Orange", "Pew! Pew! Pew!",
               "Pistols!", "Pixel (Tracer)", "Portrait (Tracer)", "Poster", "Pulse Bomb", "Ready for Action",
               "Salute (Tracer)", "Shaded", "Tagged", "Watcha' Lookin' At?", "Wings (Tracer)", "Baiser",
               "Black Widow", "Blood", "Crouch", "Cute (Widowmaker)", "Detected", "Emblem (Widowmaker)",
               "Gaze (Widowmaker)", "Hourglass", "Icon (Widowmaker)", "In My Sights", "Je Te Vois",
               "Kneeling (Widowmaker)", "No One Escapes", "Noire", "Pixel (Widowmaker)", "Portrait (Widowmaker)",
               "Scope", "Sniper", "Spider", "Swing (Widowmaker)", "Une Balle", "Veuve", "Widow", "Widow's Kiss",
               "Angry", "Ape Crossing", "Baby", "Banana", "Cute (Winston)", "Explorer (Winston)", "Fastball",
               "Harold", "Horizon", "Icon (Winston)", "Lexigrams", "Lightning", "Mine!", "PB", "Pixel (Winston)",
               "Primal Rage", "Q.E.D.", "Rage", "Research", "Roar (Winston)", "Science!", "Serious",
               "Swing (Winston)", "White (Winston)", "Wow", "512", "Alexandra", "Avenger", "Avenger (2)",
               "Barrier (Zarya)", "Bear", "Cannon (Zarya)", "Champion", "Cute (Zarya)", "Defender", "Focused",
               "Gun Show", "Icon (Zarya)", "Lift", "Pink", "Pixel (Zarya)", "Pumped", "Shield", "Smile (Zarya)",
               "Strength", "Surge", "Tobelstein", "We Are Strong", "Weights", "Wrestle (Zarya)", "Adorable", "Aura",
               "Balance", "Contemplative", "Cute (Zenyatta)", "Discord", "Enlightened", "Fist Bump", "Flow", "Foot",
               "Graphic", "Guru", "Hand", "Harmony", "Icon (Zenyatta)", "Inner Fire", "Nine", "Orb", "Orbs",
               "Peace", "Pixel (Zenyatta)", "Taunt", "Tekhartha", "Throw", "Together"],
    "voicelines": ["(Ana) Justice Delivered", "(Ana) Children, Behave", "(Ana) Everyone Dies",
                   "(Ana) It Takes A Woman To Know It", "(Ana) Justice Rains From Above", "(Ana) Mother Knows Best",
                   "(Ana) No Scope Needed", "(Ana) Someone To Tuck You In?", "(Ana) What Are You Thinking?",
                   "(Ana) Witness Me", "(Ana) You Know Nothing", "(Bastion) Doo-Woo", "(Bastion) Beeple",
                   "(Bastion) Boo Boo Doo De Doo", "(Bastion) Bweeeeeeeeeee", "(Bastion) Chirr Chirr Chirr",
                   "(Bastion) Dah-Dah Weeeee!", "(Bastion) Dun Dun Boop Boop", "(Bastion) Dweet Dweet Dweet!",
                   "(Bastion) Hee Hoo Hoo", "(Bastion) Sh-Sh-Sh", "(Bastion) Zwee?", "(D.Va) Aw, Yeah!",
                   "(D.Va) Love, D.Va", "(D.Va) ;)", "(D.Va) A New Challenger!", "(D.Va) AFK",
                   "(D.Va) D.Va: 1, Bad Guys: 0", "(D.Va) GG!", "(D.Va) I Play To Win", "(D.Va) Is This Easy Mode?",
                   "(D.Va) LOL", "(D.Va) No Hacks Required", "(Genji) A Steady Blade", "(Genji) Come On!",
                   "(Genji) Damn!", "(Genji) I Am Prepared!", "(Genji) Let's Fight!", "(Genji) Measure Twice, Cut Once",
                   "(Genji) My Soul Seeks Balance", "(Genji) Not Good Enough", "(Genji) Simple", "(Genji) Yeah!",
                   "(Genji) You Are Only Human", "(Hanzo) Expect Nothing Less", "(Hanzo) Flow Like Water",
                   "(Hanzo) From One Thing...", "(Hanzo) Hm...", "(Hanzo) I Do What I Must", "(Hanzo) Never In Doubt",
                   "(Hanzo) Remember This Moment", "(Hanzo) Sake!", "(Hanzo) Spirit Dragon",
                   "(Hanzo) Step Into The Dojo", "(Junkrat) Tick-Tock-Tick-Tock", "(Junkrat) ...Blow It Up Again",
                   "(Junkrat) Anyone Want Some BBQ?", "(Junkrat) Brrring!", "(Junkrat) Coming Up Explodey!",
                   "(Junkrat) Happy Birthday", "(Junkrat) Have A Nice Day!", "(Junkrat) It's The Little Things",
                   "(Junkrat) Kaboom", "(Junkrat) Ooh, Shiny", "(Junkrat) Smile!", "(Lúcio) To The Rhythm",
                   "(Lúcio) Tinnitus", "(Lúcio) Can't Stop, Won't Stop", "(Lúcio) Hit Me!",
                   "(Lúcio) I'm On Top Of The World", "(Lúcio) I Could Do This All Day", "(Lúcio) Jackpot!",
                   "(Lúcio) Not Hearing That Noise", "(Lúcio) Oh, Yeah!",
                   "(Lúcio) Why Are You So Angry?" "(Lúcio) You Gotta Believe!", "(McCree) Watch And Learn",
                   "(McCree) Ain't I Killed You Before", "(McCree) Happens To The Best Of Us",
                   "(McCree) I'm The Quick...", "(McCree) I'm Your Huckleberry", "(McCree) I've Got A Bullet...",
                   "(McCree) I Tried Being Reasonable", "(McCree) Reach For The Sky",
                   "(McCree) Sure As Hell Ain't Ugly", "(McCree) Wanted: Dead Or Alive", "(McCree) You Done?",
                   "(Mei) Hang In There", "(Mei) Learned Your Lesson", "(Mei) Yay!", "(Mei) A-Mei-Zing!",
                   "(Mei) Chill Out!", "(Mei) Fight For Our World", "(Mei) Okay!", "(Mei) Ouch, Are You Okay?",
                   "(Mei) Sorry Sorry Sorry Sorry", "(Mei) That Was Great", "(Mei) You Have To Let It Go",
                   "(Mercy) I Have My Eye On You", "(Mercy) Consultation Fee", "(Mercy) Doctor's Orders",
                   "(Mercy) How Barbaric", "(Mercy) Miracle Worker", "(Mercy) Need A Second Opinion?",
                   "(Mercy) On A Scale Of 1-10", "(Mercy) Super!", "(Mercy) Take Two", "(Mercy) The Doctor Is In",
                   "(Mercy) The Doctor Will See You", "(Pharah) Security In My Hands",
                   "(Pharah) Aerial Superiority Achieved", "(Pharah) Fly Like An Egyptian",
                   "(Pharah) Flying The Friendly Skies", "(Pharah) Got You On My Radar",
                   "(Pharah) Leave This To A Professional", "(Pharah) Not A Chance", "(Pharah) Play Nice, Play Pharah",
                   "(Pharah) Rocket Jump?", "(Pharah) Shot Down", "(Pharah) Sorry, But I Need To Jet",
                   "(Reaper) What Are You Looking At", "(Reaper) Seen A Ghost?", "(Reaper) Dead Man Walking",
                   "(Reaper) Give Me A Break", "(Reaper) Haven't I Killed You", "(Reaper) I'm Back In Black",
                   "(Reaper) If It Lives, I Can Kill It", "(Reaper) Next", "(Reaper) Psychopath", "(Reaper) Too Easy",
                   "(Reaper) Was That All?", "(Reinhardt) I Salute You", "(Reinhardt) Bring Me Another",
                   "(Reinhardt) Honor And Glory", "(Reinhardt) This Old Dog", "(Reinhardt) Are You Afraid?",
                   "(Reinhardt) Catch Phrase!", "(Reinhardt) Crusader Online", "(Reinhardt) Crushing Machine",
                   "(Reinhardt) German Engineering", "(Reinhardt) Respect Your Elders",
                   "(Reinhardt) Show You How It's Done", "(Roadhog) The Apocalypse", "(Roadhog) Candy From A Baby",
                   "(Roadhog) Got Something To Say?", "(Roadhog) Hahaha!", "(Roadhog) Hook, Line, And Sinker",
                   "(Roadhog) Life Is Pain, So Is Death", "(Roadhog) Piece Of Cake", "(Roadhog) Push Off",
                   "(Roadhog) Say Bacon...", "(Roadhog) Violence Is The Answer", "(Roadhog) We're All Animals",
                   "(Soldier: 76) I've Still Got It", "(Soldier: 76) Not On My Watch", "(Soldier: 76) Get Off My Lawn",
                   "(Soldier: 76) I'm An Army Of One", "(Soldier: 76) I Didn't Start This War...",
                   "(Soldier: 76) Old Soldiers", "(Soldier: 76) Smells Like Victory",
                   "(Soldier: 76) That's \"Sir\" To You", "(Soldier: 76) What Are You Lookin' At?",
                   "(Soldier: 76) You're The Other One", "(Soldier: 76) You Didn't Make The Cut",
                   "(Symmetra) Such A Lack Of Imagination", "(Symmetra) Everything By Design", "(Symmetra) Exquisite",
                   "(Symmetra) How Unsightly", "(Symmetra) I Don't Think So", "(Symmetra) Impressive",
                   "(Symmetra) Perfect Harmony", "(Symmetra) Precisely", "(Symmetra) Put You In Your Place",
                   "(Symmetra) Welcome To My Reality", "(Symmetra) Why Do You Struggle?",
                   "(Torbjörn) Hard Work Pays Off", "(Torbjörn) Let's Not Buy The Pig",
                   "(Torbjörn) A Chicken Out Of A Feather", "(Torbjörn) Completion Date?",
                   "(Torbjörn) Don't Get Caught", "(Torbjörn) Engineers", "(Torbjörn) I'm Giving It All I've Got!",
                   "(Torbjörn) I'm Swedish!", "(Torbjörn) Leave This To An Expert", "(Torbjörn) Some Assembly Required",
                   "(Torbjörn) Working As Intended", "(Tracer) You Got It", "(Tracer) Aw, Rubbish",
                   "(Tracer) Be Right Back!", "(Tracer) Check Me Out", "(Tracer) Cheers, Love!", "(Tracer) Déjà Vu",
                   "(Tracer) Keep Calm", "(Tracer) She Shoots, She Scores", "(Tracer) The World Needs Heroes",
                   "(Tracer) Under Control", "(Tracer) You Need A Time Out", "(Widowmaker) A Single Death",
                   "(Widowmaker) Encore?", "(Widowmaker) Let Them Eat Cake", "(Widowmaker) Look For The Woman",
                   "(Widowmaker) Magnifique", "(Widowmaker) One Shot, One Kill", "(Widowmaker) Ouh Là Là",
                   "(Widowmaker) Step Into My Parlor...", "(Widowmaker) That's How It Is",
                   "(Widowmaker) To Life, To Death", "(Widowmaker) What's An Aimbot?", "(Winston) Curious",
                   "(Winston) ...Excuse Me", "(Winston) Don't Get Me Angry", "(Winston) How Embarrassing!",
                   "(Winston) I Do Not Want A Banana", "(Winston) Natural Selection", "(Winston) No Monkey Business",
                   "(Winston) Peanut Butter?", "(Winston) Sorry About That!", "(Winston) The Power Of Science!",
                   "(Winston) We Have A Problem", "(Zarya) Need Personal Training?", "(Zarya) Strong As The Mountain",
                   "(Zarya) Get Down, Give Me 20", "(Zarya) I Am Mother Russia", "(Zarya) I Can Bench More Than You",
                   "(Zarya) I Will Break You", "(Zarya) In Russia, Game Plays You", "(Zarya) No Mercy",
                   "(Zarya) Siberian Bear", "(Zarya) Together We Are Strong", "(Zarya) Welcome To The Gun Show",
                   "(Zenyatta) I Dreamt I Was A Butterfly", "(Zenyatta) We Are In Harmony",
                   "(Zenyatta) Death Is Whimsical Today", "(Zenyatta) Do I Think?", "(Zenyatta) Free Your Mind",
                   "(Zenyatta) Hello, World!", "(Zenyatta) I Think, Therefore I Am", "(Zenyatta) I Will Not Juggle",
                   "(Zenyatta) Ones And Zeroes", "(Zenyatta) Peace And Blessings", "(Zenyatta) The Iris Embraces You"]
}

rareloot = {
    "rareskins": ["Citrine Ana", "Garnet Ana", "Peridot Ana", "Turquoise", "Dawn Bastion", "Meadow Bastion",
                  "Sky Bastion", "Soot Bastion", "Blueberry D.Va", "Lemon-Lime D.Va", "Tangerine D.Va",
                  "Watermelon D.Va", "Azurite Genji", "Malachite Genji", "Ochre Genji", "Cinnabar Genji", "Azuki Hanzo",
                  "Kinoko Hanzo", "Midori Hanzo", "Sora Hanzo", "Bleached Junkrat", "Drowned Junkrat",
                  "Irradiated Junkrat", "Rusted Junkrat", "Azul Lúcio", "Laranja Lúcio", "Vermelho Lúcio", "Roxo Lúcio",
                  "Ebony McCree", "Sage McCree", "Lake McCree", "Wheat McCree", "Jade Mei", "Persimmon Mei",
                  "Heliotrope Mei", "Chrysanthemum Mei", "Celestial Mercy", "Mist Mercy", "Orchid Mercy",
                  "Vendant Mercy", "Amethyst Pharah", "Copper Pharah", "Emerald Pharah", "Titanium Pharah",
                  "Blood Reaper", "Midnight Reaper", "Moss Reaper", "Royal Reaper", "Brass Reinhardt",
                  "Cobalt Reinhardt", "Copper Reinhardt", "Viridian Reinhardt", "Kiwi Roadhog", "Mud Roadhog",
                  "Thistle Roadhog", "Sand Roadhog", "Olive Soldier: 76", "Russet Soldier:76", "Jet Soldier: 76",
                  "Smoke Soldier: 76", "Hyacinth Symmetra", "Cardamom Symmetra", "Saffron Symmetra",
                  "Technomancer Symmetra", "Blå Torbjörn", "Citron Torbjörn", "Grön Torbjörn", "Plommon Torbjörn",
                  "Royal Blue Tracer", "Neon Green Tracer", "Hot Pink Tracer", "Electric Purple Tracer",
                  "Ciel Widowmaker", "Nuit Widowmaker", "Vert Widowmaker", "Rose Widowmaker", "Banana Winston",
                  "Forest Winston", "Red Planet Winston", "Atmosphere Winston", "Brick Zarya", "Taiga Zarya",
                  "Violet Zarya", "Golden Rod Zarya", "Air Zenyatta", "Leaf Zenyatta", "Water Zenyatta"],
    "playericons": ["Bastion", "Ganymede", "Tank Crossing", "D.Va", "Bunny", "Charm", "Genji", "God of War", "Nin",
                    "Hanzo", "Shimada", "Storm", "Junkrat", "Ahhhh!", "Bomb", "Lúcio", "Frog", "Kambô", "McCree",
                    "Badge", "Deadeye", "Mei", "Hairpin", "Snowball", "Mercy", "Guardian Angel", "Valkyrie", "Pharah",
                    "Raptora", "Wadjet", "Reaper", "Emblem", "Soul", "Reinhardt", "Lionhardt", "Scar", "Roadhog",
                    "Hook", "Piggy", "Soldier: 76", "Strike-Commander", "76", "Symmetra", "Sentry", "Vishkar",
                    "Torbjörn", "Forge", "Gears", "Tracer", "Patch", "Pulse Bomb", "Widowmaker", "Baiser",
                    "Grappling Hook", "Winston", "Lunar Ops", "Peanut Butter", "Zarya", "Particle Barrier", "512",
                    "Zenyatta", "Harmony", "Meditation", "16-Bit Hero", "Anubis", "Bao", "Capsule", "Cheers",
                    "Colossus", "Credit", "Demolition", "Elephant", "Happy Squid", "Kofi Aromo", "Loot Box",
                    "Los Muertos", "Mama Pig's", "Mariachi", "Mech", "Pachimari", "Pharaoh", "Pinata", "Ramen", "Rhino",
                    "Route 66", "Sakura", "Scooter", "Six-Gun Killer", "Syvatogor", "They Came From Beyond The Moon",
                    "Totem", "Training Bot", "Vivi", "Alliance", "Barbarian", "Crusader", "Dark Lady", "Diablo",
                    "Dominion", "For The Horde", "Garrosh", "Hearthstone", "Hierarch", "Jaina", "Jim", "Lich King",
                    "Monk", "Murloc", "Nexus", "Protoss", "Queen of Blades", "Terran", "Witch Doctor", "Wizard", "Zerg",
                    "Demon Hunter", "Varian Wrynn", "Siege Mode"],
    "victoryposes": ["(Ana) Mission Complete", "(Ana) Protector", "(Ana) Seated", "(Bastion) Birdwatching",
                     "(Bastion) Pop Up", "(Bastion) Tank", "(D.Va) I Heart You", "(D.Va) Peace", "(D.Va) Sitting",
                     "(Genji) Sword Stance", "(Genji) Kneeling", "(Genji) Shuriken", "(Hanzo) Confident",
                     "(Hanzo) Kneeling", "(Hanzo) Over The Shoulder", "(Junkrat) It'll Freeze That Way",
                     "(Junkrat) Kneeling", "(Junkrat) Nyah Nyah", "(Lúcio) Confident", "(Lúcio) Grooving",
                     "(Lúcio) Ready For Action", "(McCree) Over The Shoulder", "(McCree) Contemplative",
                     "(McCree) Take It Easy", "(Mei) Casual", "(Mei) Hands On Hips", "(Mei) Kneeling",
                     "(Mercy) Angelic", "(Mercy) Carefree", "(Mercy) Ready For Battle", "(Pharah) Guardian",
                     "(Pharah) Jump Jet", "(Pharah) Kneeling", "(Reaper) Casual", "(Reaper) Enigmatic",
                     "(Reaper) Menacing", "(Reinhardt) Legendary", "(Reinhardt) Confident", "(Reinhardt) Flex",
                     "(Roadhog) Pointing To The Sky", "(Roadhog) Thumbs Up", "(Roadhog) Tuckered Out",
                     "(Soldier: 76) Fist Pump", "(Soldier: 76) Locked And Loaded", "(Soldier: 76) Soldier",
                     "(Symmetra) Balance", "(Symmetra) Creation", "(Symmetra) Dance", "(Torbjörn) Take Five",
                     "(Torbjörn) Hammer", "(Torbjörn) Sitting Pretty", "(Tracer) Over The Shoulder", "(Tracer) Salute",
                     "(Tracer) Sitting", "(Widowmaker) Activating Visor", "(Widowmaker) Gaze",
                     "(Widowmaker) Over The Shoulder", "(Winston) Beast", "(Winston) Glasses", "(Winston) The Thinker",
                     "(Zarya) Casual", "(Zarya) Check Out This Gun", "(Zarya) Flexing", "(Zenyatta) Balance",
                     "(Zenyatta) Harmony", "(Zenyatta) Peace"]
}

epicloot = {
    "epicskins": ["Merciful Ana", "Shrike Ana", "Defense Matrix Bastion", "Omnic Crisis Bastion", "Carbon Fiber D.Va",
                  "White Rabbit D.Va", "Carbon Fiber Genji", "Chrome Genji", "Cloud Hanzo", "Dragon Hanzo",
                  "Jailbird Junkrat", "Toasted Junkrat", "Auditva Lúcio", "Synaesthesia Lúcio", "On The Range McCree",
                  "White Hat McCree", "Earthen Mei", "Snow Plum Mei", "Amber Mercy", "Cobalt Mercy", "Jackal Pharah",
                  "Anubis Pharah", "Desert Reaper", "Wight Reaper", "Bundeswehr Reinhardt", "Paragon Reinhardt",
                  "Pigpen Roadhog", "Stiched Roadhog", "Bone Soldier: 76", "Golden Soldier: 76", "Regal Symmetra",
                  "Utopaea Symmetra", "Plommon Torbjörn", "Cathode Torbjörn", "Posh Tracer", "Sporty Tracer",
                  "Winter Widowmaker", "Patina Widowmaker", "Desert Winston", "Horizon Winston", "Dawn Zarya",
                  "Midnight Zarya", "Ascendant Zenyatta", "Harmonious Zenyatta"],
    "emotes": ["(Ana) Disapproving", "(Ana) Protector", "(Ana) Tea Time", "(Bastion) Alert! Alert!", "(Bastion) Dizzy",
               "(Bastion) Robot", "(D.Va) Bunny Hop", "(D.Va) Heartbreaker", "(D.Va) Party Time", "(Genji) Challenge",
               "(Genji) Cutting Edge", "(Genji) Salute", "(Hanzo) Victory", "(Hanzo) Beckon", "(Hanzo) Brush Shoulder",
               "(Junkrat) Juggling", "(Junkrat) Puppet", "(Junkrat) Vaudeville", "(Lúcio) Capoeira",
               "(Lúcio) In The Groove", "(Lúcio) Nah!", "(McCree) Gunspinning", "(McCree) Hat Tip", "(McCree) Spit",
               "(Mei) Companion", "(Mei) Spray", "(Mei) Yaaaaaaaaay!", "(Mercy) Applause", "(Mercy) Caduceus",
               "(Mercy) No Pulse", "(Pharah) Cheer", "(Pharah) Flourish", "(Pharah) Knuckles", "(Reaper) Not Impressed",
               "(Reaper) Slice", "(Reaper) Slow Clap", "(Reinhardt) Flex", "(Reinhardt) Taunt",
               "(Reinhardt) Warrior's Salute", "(Roadhog) Boo!", "(Roadhog) Can Crusher", "(Roadhog) Headbanging",
               "(Soldier: 76) Fist", "(Soldier: 76) I See You", "(Soldier: 76) Locked And Loaded", "(Symmetra) Clap",
               "(Symmetra) Flow", "(Symmetra) Insignificant", "(Torbjörn) Clicking Heels", "(Torbjörn) Fisticuffs",
               "(Torbjörn) Overload", "(Tracer) Cheer", "(Tracer) Laughing", "(Tracer) Spin",
               "(Widowmaker) Curtain Call", "(Widowmaker) Shot Dead", "(Widowmaker) Widow's Kiss",
               "(Winston) Peanut Butter?", "(Winston) Monkey Business", "(Winston) Roar", "(Zarya) Bring It On",
               "(Zarya) Crush You", "(Zarya) Pumping Iron", "(Zenyatta) Focusing", "(Zenyatta) Round of Applause",
               "(Zenyatta) Taunt"],
    "highlightintros": ["(Ana) Guardian", "(Ana) Locked On", "(Ana) Shh...", "(Bastion) Bullet Rain",
                        "(Bastion) Ganymede", "(Bastion) On Guard", "(D.Va) Eject", "(D.Va) Lying Around",
                        "(D.Va) Meka Activated", "(Genji) Shuriken", "(Genji) Unsheathing The Sword",
                        "(Genji) Warrior's Salute", "(Hanzo) Backflip", "(Hanzo) Superior", "(Hanzo) My Aim Is True",
                        "(Junkrat) I'm Flying!", "(Junkrat) RIP-Tire", "(Junkrat) Unfortunate", "(Lúcio) Drop The Beat",
                        "(Lúcio) Freestyle", "(Lúcio) In The Groove", "(McCree) Rolling Into Action",
                        "(McCree) The Duel", "(McCree) The Name's McCree", "(Mei) Frosty :)", "(Mei) Going Up!",
                        "(Mei) Skating Around", "(Mercy) Battle Angel", "(Mercy) Guardian Angel",
                        "(Mercy) Heroes Never Die", "(Pharah) Barrage", "(Pharah) Mission Complete",
                        "(Pharah) Touchdown", "(Reaper) Death Blossom", "(Reaper) Executioner", "(Reaper) Shadow Step",
                        "(Reinhardt) Charge", "(Reinhardt) Hammer Down", "(Reinhardt) More Stretching Required",
                        "(Roadhog) Little Piggy", "(Roadhog) Say \"Cheese\"", "(Roadhog) Whole Hog",
                        "(Soldier: 76) Helix", "(Soldier: 76) Looking At You", "(Soldier: 76) Target Rich Environment",
                        "(Symmetra) Askew", "(Symmetra) Dance", "(Symmetra) My Reality", "(Torbjörn) In Your Face",
                        "(Torbjörn) Refreshing", "(Torbjörn) Ride 'Em", "(Tracer) Backflip", "(Tracer) Just In Time",
                        "(Tracer) Serious Business", "(Widowmaker) Hanging Around", "(Widowmaker) I See You...",
                        "(Widowmaker) Swinging Into Action", "(Winston) Excuse Me", "(Winston) Glasses",
                        "(Winston) Primal Rage", "(Zarya) Deadlift", "(Zarya) Maximum Charge",
                        "(Zarya) This Is Strength", "(Zenyatta) Focused", "(Zenyatta) Harmony And Discord",
                        "(Zenyatta) Transcendence"]
}

legendaryloot = {
    "legendaryskins": ["Wadjet Ana", "Wasteland Ana", "Captain Amari Ana", "Horus Ana", "Gearbot Bastion",
                       "Woodbot Bastion", "Antique Bastion", "Steambot Bastion", "Junker D.Va", "B.Va",
                       "Scavenger D.Va", "Junebug D.Va", "Sparrow Genji", "Young Genji", "Bedouin Genji", "Nomad Genji",
                       "Young Hanzo", "Young Master Hanzo", "Lone Wolf Hanzo", "Okami Hanzo", "Jester Junkrat",
                       "Fool Junkrat", "Hayseed Junkrat", "Scarecrow Junkrat", "Hippityhop Lúcio", "Ribbit Lúcio",
                       "Breakaway Lúcio", "Slapshot Lúcio", "Gambler McCree", "Mystery Man McCree", "Riverboat McCree",
                       "Vigilante McCree", "Firefighter Mei", "Rescue Mei", "Abominable Mei", "Yeti Hunter Mei",
                       "Sigrún Mercy", "Valkyrie Mercy", "Devil Mercy", "Imp Mercy", "Mechaqueen Pharah",
                       "Raptorian Pharah", "Raindancer Pharah", "Thunderbird Pharah", "Plague Doctor Reaper",
                       "El Blanco Reaper" "Mariachi Reaper", "Nevermore Reaper", "Blackhardt", "Bloodhardt",
                       "Lionhardt", "Stonehardt", "Mako Roadhog", "Toa Roadhog", "Islander Roadhog",
                       "Sharkbait Roadhog", "Commando: 76", "Night Ops: 76", "Daredevil: 76", "Stunt Rider: 76",
                       "Architech Symmetra", "Devi Symmetra", "Goddess Symmetra", "Vishkar Symmetra",
                       "Barbarossa Torbjörn", "Blackbeard Torbjörn", "Chopper Torbjörn", "Deadlock Torbjörn",
                       "Mach T Tracer", "Punk Tracer", "T. Racer", "Ultraviolet", "Odette Widowmaker",
                       "Odile Widowmaker", "Comtesse Widowmaker", "Huntress Widowmaker", "Explorer Winston", "Frogston",
                       "Undersea Winston", "Safari Winston", "Arctic Zarya", "Siberian Front Zarya", "Cybergoth Zarya",
                       "Industrial Zarya", "Djinyatta", "Ifrit Zenyatta", "Ra Zenyatta", "Sunyatta"]
}


class BankError(Exception):
    pass


class AccountAlreadyExists(BankError):
    pass


class NoAccount(BankError):
    pass


class InsufficientBalance(BankError):
    pass


class NegativeValue(BankError):
    pass


class SameSenderAndReceiver(BankError):
    pass


class Bank:
    def __init__(self, bot, file_path):
        self.accounts = dataIO.load_json(file_path)
        self.bot = bot

    def create_account(self, user):
        server = user.server
        if not self.account_exists(user):
            if server.id not in self.accounts:
                self.accounts[server.id] = {}
            if user.id in self.accounts:  # Legacy account
                balance = self.accounts[user.id]["balance"]
            else:
                balance = 0
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            account = {"name": user.name, "balance": balance,
                       "created_at": timestamp}
            self.accounts[server.id][user.id] = account
            self._save_bank()
            return self.get_account(user)
        else:
            raise AccountAlreadyExists()

    def account_exists(self, user):
        try:
            self._get_account(user)
        except NoAccount:
            return False
        return True

    def withdraw_credits(self, user, amount):
        server = user.server

        if amount < 0:
            raise NegativeValue()

        account = self._get_account(user)
        if account["balance"] >= amount:
            account["balance"] -= amount
            self.accounts[server.id][user.id] = account
            self._save_bank()
        else:
            raise InsufficientBalance()

    def deposit_credits(self, user, amount):
        server = user.server
        if amount < 0:
            raise NegativeValue()
        account = self._get_account(user)
        account["balance"] += amount
        self.accounts[server.id][user.id] = account
        self._save_bank()

    def set_credits(self, user, amount):
        server = user.server
        if amount < 0:
            raise NegativeValue()
        account = self._get_account(user)
        account["balance"] = amount
        self.accounts[server.id][user.id] = account
        self._save_bank()

    def transfer_credits(self, sender, receiver, amount):
        server = sender.server
        if amount < 0:
            raise NegativeValue()
        if sender is receiver:
            raise SameSenderAndReceiver()
        if self.account_exists(sender) and self.account_exists(receiver):
            sender_acc = self._get_account(sender)
            if sender_acc["balance"] < amount:
                raise InsufficientBalance()
            self.withdraw_credits(sender, amount)
            self.deposit_credits(receiver, amount)
        else:
            raise NoAccount()

    def update_name(self, user):
        server = user.server
        account = self._get_account(user)
        account["name"] = user.display_name
        self.accounts[server.id][user.id] = account
        self._save_bank()

    def can_spend(self, user, amount):
        account = self._get_account(user)
        if account["balance"] >= amount:
            return True
        else:
            return False

    def wipe_bank(self, server):
        self.accounts[server.id] = {}
        self._save_bank()

    def get_server_accounts(self, server):
        if server.id in self.accounts:
            raw_server_accounts = deepcopy(self.accounts[server.id])
            accounts = []
            for k, v in raw_server_accounts.items():
                v["id"] = k
                v["server"] = server
                acc = self._create_account_obj(v)
                accounts.append(acc)
            return accounts
        else:
            return []

    def get_all_accounts(self):
        accounts = []
        for server_id, v in self.accounts.items():
            server = self.bot.get_server(server_id)
            if server is None:  # Servers that have since been left will be ignored
                continue  # Same for users_id from the old bank format
            raw_server_accounts = deepcopy(self.accounts[server.id])
            for k, v in raw_server_accounts.items():
                v["id"] = k
                v["server"] = server
                acc = self._create_account_obj(v)
                accounts.append(acc)
        return accounts

    def get_balance(self, user):
        account = self._get_account(user)
        return account["balance"]

    def get_account(self, user):
        acc = self._get_account(user)
        acc["id"] = user.id
        acc["server"] = user.server
        return self._create_account_obj(acc)

    def _create_account_obj(self, account):
        account["member"] = account["server"].get_member(account["id"])
        account["created_at"] = datetime.strptime(account["created_at"],
                                                  "%Y-%m-%d %H:%M:%S")
        Account = namedtuple("Account", "id name balance "
                                        "created_at server member")
        return Account(**account)

    def _save_bank(self):
        dataIO.save_json("data/economy/bank.json", self.accounts)

    def _get_account(self, user):
        server = user.server
        try:
            return deepcopy(self.accounts[server.id][user.id])
        except KeyError:
            raise NoAccount()


class Economy:
    """Economy - Overwatch Loot Box Simulator Edition

    Open lootboxes. Get 4 commons!"""

    def __init__(self, bot):
        global default_settings
        self.bot = bot
        self.bank = Bank(bot, "data/economy/bank.json")
        self.settings = fileIO("data/economy/settings.json", "load")
        if "PAYDAY_TIME" in self.settings:  # old format
            default_settings = self.settings
            self.settings = {}
        self.settings = defaultdict(lambda: default_settings, self.settings)
        self.payday_register = defaultdict(dict)
        self.slot_register = defaultdict(dict)

    @commands.group(name="bank", pass_context=True)
    async def _bank(self, ctx):
        """Bank operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_bank.command(pass_context=True, no_pm=True)
    async def register(self, ctx):
        """Gives the invoker a copy of Fake Overwatch and registers their data in the server's files."""
        user = ctx.message.author
        try:
            account = self.bank.create_account(user)
            await self.bot.say("{} You purchased Fake Overwatch for 0:gem:. You receive a pouch for your Fake Gems. "
                               "Current balance: {}:gem:".format(user.display_name,
                                                                 account.balance))
        except AccountAlreadyExists:
            await self.bot.say("{} You already have Fake Overwatch!".format(user.display_name))

    @_bank.command(pass_context=True, no_pm=True)
    async def updatename(self, ctx):
        """Updates a user's name in the leaderboards to their current display name"""
        author = ctx.message.author
        try:
            self.bank.update_name(author)
            await self.bot.say("Done.")
        except NoAccount:
            await self.bot.say("You don't have an account.")

    @_bank.command(pass_context=True)
    async def balance(self, ctx, user: discord.Member = None):
        """Shows balance of user.

        Defaults to yours."""
        if not user:
            user = ctx.message.author
            try:
                await self.bot.say("{} You have {}:gem:.".format(user.display_name, self.bank.get_balance(user)))
            except NoAccount:
                await self.bot.say("{} You don't have Fake Overwatch."
                                   " Type {}buyfakeoverwatch to buy Fake Overwatch for 0:gem:.".format(
                    user.display_name,
                    ctx.prefix))
        else:
            try:
                await self.bot.say("{} has {}:gem:.".format(user.display_name, self.bank.get_balance(user)))
            except NoAccount:
                await self.bot.say("That user doesn't have Fake Overwatch.")

    @_bank.command(pass_context=True)
    async def transfer(self, ctx, user: discord.Member, sum: int):
        """Transfer credits to other users"""
        author = ctx.message.author
        try:
            self.bank.transfer_credits(author, user, sum)
            logger.info("{}({}) transferred {}:gem: to {}({})".format(
                author.name, author.id, sum, user.name, user.id))
            await self.bot.say("{} sent {}:gem: to {}.".format(author.mention, sum, user.mention))
        except NegativeValue:
            await self.bot.say("You need to transfer at least 1:gem:.")
        except SameSenderAndReceiver:
            await self.bot.say("You throw {}:gem: up in the air. Luckily, you manage to catch it before it gets "
                               "Board Game Online'd.".format(sum))
        except InsufficientBalance:
            await self.bot.say("You don't have that many Fake Gems.")
        except NoAccount:
            await self.bot.say("That user doesn't have Fake Overwatch.")

    @_bank.command(name="set", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _set(self, ctx, user: discord.Member, sum: int):
        """Sets credits of user's bank account

        Admin/owner restricted."""
        author = ctx.message.author
        try:
            self.bank.set_credits(user, sum)
            logger.info("{}({}) set {} credits to {} ({})".format(author.name, author.id, str(sum), user.name, user.id))
            await self.bot.say(
                "An admin abused their power to set {}'s inventory to {}:gem:.".format(user.mention, str(sum)))
        except NoAccount:
            await self.bot.say("User doesn't have Fake Overwatch.")

    @commands.command(pass_context=True, no_pm=True)
    async def payday(self, ctx):  # TODO
        """Open your daily lootbox"""
        author = ctx.message.author
        server = author.server
        id = author.id
        rolls = ["", "", "", ""]
        lootmessage = ""
        payout = 0

        if self.bank.account_exists(author):
            if id in self.payday_register[server.id]:
                seconds = abs(self.payday_register[server.id][id] - int(time.perf_counter()))
                if seconds >= self.settings[server.id]["PAYDAY_TIME"]:
                    rolls = []
                    lootmessage = ""
                    payout = 0
                    for i in range(4):
                        lootnumber = randint(0, 10000)
                        if lootnumber <= 5866:
                            rolls.append("Common")
                        elif lootnumber <= 9035:
                            rolls.append("Rare")
                        elif lootnumber <= 9757:
                            rolls.append("Epic")
                        else:
                            rolls.append("Legendary")
                    if rolls[0] == rolls[1] == rolls[2] == rolls[3] == "Common":
                        rolls[
                            2] = "Rare"  # Force a rare roll if all 4 rolls were common. Do this before payout is calculated.
                    for i in range(4):
                        lootmessageline = ""
                        if rolls[i] == "Common":
                            payout += 5
                            lootmessageline = generatelootmessageline("Common")
                            lootmessageline += "+5:gem:"
                        elif rolls[i] == "Rare":
                            payout += 15
                            lootmessageline = generatelootmessageline("Rare")
                            lootmessageline += "+15:gem:"
                        elif rolls[i] == "Epic":
                            payout += 50
                            lootmessageline = generatelootmessageline("Epic")
                            lootmessageline += "+50:gem:"
                        elif rolls[i] == "Legendary":
                            payout += 200
                            lootmessageline = generatelootmessageline("Legendary")
                            lootmessageline += "+200:gem:"
                        lootmessage += lootmessageline + "\n"
                    self.bank.deposit_credits(author, payout)
                    self.payday_register[server.id][id] = int(time.perf_counter())
                    await self.bot.say(
                        "{} levelled up and opened a Fake Lootbox!\n".format(author.display_name) + lootmessage +
                        "\n\n{} now has {}:gem:.".format(author.display_name, self.bank.get_balance(author)))

                else:
                    await self.bot.say(
                        "{} Too soon. For your next free Fake Lootbox you have to wait {}.".format(author.mention,
                                                                                                   self.display_time(
                                                                                                       self.settings[
                                                                                                           server.id][
                                                                                                           "PAYDAY_TIME"] - seconds)))
            else:
                rolls = []
                lootmessage = ""
                payout = 0
                for i in range(4):
                    lootnumber = randint(0, 10000)
                    if lootnumber <= 5866:
                        rolls.append("Common")
                    elif lootnumber <= 9035:
                        rolls.append("Rare")
                    elif lootnumber <= 9757:
                        rolls.append("Epic")
                    else:
                        rolls.append("Legendary")
                if rolls[0] == rolls[1] == rolls[2] == rolls[3] == "Common":
                    rolls[
                        2] = "Rare"  # Force a rare roll if all 4 rolls were common. Do this before payout is calculated.
                for i in range(4):
                    lootmessageline = ""
                    if rolls[i] == "Common":
                        payout += 5
                        lootmessageline = generatelootmessageline("Common")
                        lootmessageline += "+5:gem:"
                    elif rolls[i] == "Rare":
                        payout += 15
                        lootmessageline = generatelootmessageline("Rare")
                        lootmessageline += "+15:gem:"
                    elif rolls[i] == "Epic":
                        payout += 50
                        lootmessageline = generatelootmessageline("Epic")
                        lootmessageline += "+50:gem:"
                    elif rolls[i] == "Legendary":
                        payout += 200
                        lootmessageline = generatelootmessageline("Legendary")
                        lootmessageline += "+200:gem:"
                    lootmessage += lootmessageline + "\n"
                self.bank.deposit_credits(author, payout)
                self.payday_register[server.id][id] = int(time.perf_counter())
                await self.bot.say(
                    "{} levelled up and opened a Fake Lootbox!\n".format(author.display_name) + lootmessage +
                    "\n\n{} now has {}:gem:.".format(author.display_name, self.bank.get_balance(author)))
        else:
            await self.bot.say(
                "{} You need Fake Overwatch to open a lootbox. Type {}buyfakeoverwatch to buy Fake Overwatch for 0:gem:.".format(
                    author.mention, ctx.prefix))

    @commands.group(pass_context=True)
    async def leaderboard(self, ctx):
        """Server / global leaderboard

        Defaults to server"""
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self._server_leaderboard)

    @leaderboard.command(name="server", pass_context=True)
    async def _server_leaderboard(self, ctx, top: int = 10):
        """Prints out the server's leaderboard

        Defaults to top 10"""  # Originally coded by Airenkun - edited by irdumb
        server = ctx.message.server
        if top < 1:
            top = 10
        bank_sorted = sorted(self.bank.get_server_accounts(server),
                             key=lambda x: x.balance, reverse=True)
        if len(bank_sorted) < top:
            top = len(bank_sorted)
        topten = bank_sorted[:top]
        highscore = ""
        place = 1
        for acc in topten:
            highscore += str(place).ljust(len(str(top)) + 1)
            highscore += (acc.name + " ").ljust(23 - len(str(acc.balance)))
            highscore += str(acc.balance) + "\n"
            place += 1
        if highscore:
            if len(highscore) < 1985:
                await self.bot.say("```py\n" + highscore + "```")
            else:
                await self.bot.say("The leaderboard is too big to be displayed. Try with a lower <top> parameter.")
        else:
            await self.bot.say("No one is playing Fake Overwatch.")

    @leaderboard.command(name="global")
    async def _global_leaderboard(self, top: int = 10):
        """Prints out the global leaderboard

        Defaults to top 10"""
        if top < 1:
            top = 10
        bank_sorted = sorted(self.bank.get_all_accounts(),
                             key=lambda x: x.balance, reverse=True)
        unique_accounts = []
        for acc in bank_sorted:
            if not self.already_in_list(unique_accounts, acc):
                unique_accounts.append(acc)
        if len(unique_accounts) < top:
            top = len(unique_accounts)
        topten = unique_accounts[:top]
        highscore = ""
        place = 1
        for acc in topten:
            highscore += str(place).ljust(len(str(top)) + 1)
            highscore += ("{} |{}| ".format(acc.name, acc.server.name)).ljust(23 - len(str(acc.balance)))
            highscore += str(acc.balance) + "\n"
            place += 1
        if highscore:
            if len(highscore) < 1985:
                await self.bot.say("```py\n" + highscore + "```")
            else:
                await self.bot.say("The leaderboard is too big to be displayed. Try with a lower <top> parameter.")
        else:
            await self.bot.say("No one is playing Fake Overwatch.")

    def already_in_list(self, accounts, user):
        for acc in accounts:
            if user.id == acc.id:
                return True
        return False

    @commands.command()
    async def payouts(self):
        """Shows how many Fake Gems each item of Fake Loot is worth."""
        await self.bot.whisper(slot_payouts)

    @commands.command(pass_context=True, no_pm=True)
    async def slot(self, ctx):
        """Buy a Fake Lootbox with Fake Gems."""
        author = ctx.message.author
        server = author.server
        bid = self.settings[server.id]["BOX_COST"]
        if not self.bank.account_exists(author):
            await self.bot.say(
                "{} You don't have Fake Overwatch. Type {}buyfakeoverwatch to buy Fake Overwatch.".format(
                    author.mention, ctx.prefix))
            return
        if self.bank.can_spend(author, bid):
            if True:  # remove deprecated feature
                if author.id in self.slot_register:
                    seconds = abs(self.slot_register[author.id] - int(time.perf_counter()))
                    if abs(self.slot_register[author.id] - int(time.perf_counter())) >= self.settings[server.id][
                        "SLOT_TIME"]:
                        self.slot_register[author.id] = int(time.perf_counter())
                        await self.slot_machine(ctx.message, bid, author)
                    else:
                        await self.bot.say(
                            "You can't open Fake Lootboxes that fast! You need to wait for the cool Fake Animation! {} seconds left.".format(
                                self.settings[server.id]["SLOT_TIME"] - seconds))
                else:
                    self.slot_register[author.id] = int(time.perf_counter())
                    await self.slot_machine(ctx.message, bid, author)
            else:
                await self.bot.say("Admin goofed. Tell them about it.")
        else:
            await self.bot.say(
                "{} You don't have enough Fake Gems to buy a Fake Lootbox."
                "Fake Lootboxes cost {}:gem:.".format(author.mention, bid))

    async def slot_machine(self, message, bid, author):
        rolls = []
        lootmessage = ""
        payout = 0
        for i in range(4):
            lootnumber = randint(0, 10000)
            if lootnumber <= 5866:
                rolls.append("Common")
            elif lootnumber <= 9035:
                rolls.append("Rare")
            elif lootnumber <= 9757:
                rolls.append("Epic")
            else:
                rolls.append("Legendary")
        if rolls[0] == rolls[1] == rolls[2] == rolls[3] == "Common":
            rolls[
                2] = "Rare"  # Force a rare roll if all 4 rolls were common. Do this before payout is calculated.
        for i in range(4):
            lootmessageline = ""
            if rolls[i] == "Common":
                payout += 5
                lootmessageline = generatelootmessageline("Common")
                lootmessageline += "+5:gem:"
            elif rolls[i] == "Rare":
                payout += 15
                lootmessageline = generatelootmessageline("Rare")
                lootmessageline += "+15:gem:"
            elif rolls[i] == "Epic":
                payout += 50
                lootmessageline = generatelootmessageline("Epic")
                lootmessageline += "+50:gem:"
            elif rolls[i] == "Legendary":
                payout += 200
                lootmessageline = generatelootmessageline("Legendary")
                lootmessageline += "+200:gem:"
            lootmessage += lootmessageline + "\n"

        self.bank.withdraw_credits(message.author, bid)
        self.bank.deposit_credits(message.author, payout)
        await self.bot.say(
            "{} purchased and opened a Fake Lootbox for {}:gem:!\n".format(author.display_name, bid) + lootmessage +
            "\n\n{} now has {}:gem:.".format(author.display_name, self.bank.get_balance(message.author)))

    @commands.group(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def economyset(self, ctx):
        """Changes economy module settings"""
        server = ctx.message.server
        settings = self.settings[server.id]
        if ctx.invoked_subcommand is None:
            msg = "```"
            for k, v in settings.items():
                msg += "{}: {}\n".format(k, v)
            msg += "```"
            await send_cmd_help(ctx)
            await self.bot.say(msg)

    @economyset.command(pass_context=True)
    async def slotmin(self, ctx, bid: int):
        """Minimum slot machine bid"""
        server = ctx.message.server
        self.settings[server.id]["SLOT_MIN"] = bid
        await self.bot.say("Minimum bid is now " + str(bid) + " credits.")
        fileIO("data/economy/settings.json", "save", self.settings)

    @economyset.command(pass_context=True)
    async def slotmax(self, ctx, bid: int):
        """Maximum slot machine bid"""
        server = ctx.message.server
        self.settings[server.id]["SLOT_MAX"] = bid
        await self.bot.say("Maximum bid is now " + str(bid) + " credits.")
        fileIO("data/economy/settings.json", "save", self.settings)

    @economyset.command(pass_context=True)
    async def boxcost(self, ctx, cost: int):
        """Lootbox cost"""
        server = ctx.message.server
        self.settings[server.id]["BOX_COST"] = cost
        await self.bot.say("Boxes now cost {}:gem:.".format(cost))
        fileIO("data/economy/settings.json", "save", self.settings)

    @economyset.command(pass_context=True)
    async def slottime(self, ctx, seconds: int):
        """Seconds between each slots use"""
        server = ctx.message.server
        self.settings[server.id]["SLOT_TIME"] = seconds
        await self.bot.say("Cooldown is now " + str(seconds) + " seconds.")
        fileIO("data/economy/settings.json", "save", self.settings)

    @economyset.command(pass_context=True)
    async def paydaytime(self, ctx, seconds: int):
        """Seconds between each payday"""
        server = ctx.message.server
        self.settings[server.id]["PAYDAY_TIME"] = seconds
        await self.bot.say("Value modified. At least " + str(seconds) + " seconds must pass between each payday.")
        fileIO("data/economy/settings.json", "save", self.settings)

    @economyset.command(pass_context=True)
    async def paydaycredits(self, ctx, credits: int):
        """Credits earned each payday"""
        server = ctx.message.server
        self.settings[server.id]["PAYDAY_CREDITS"] = credits
        await self.bot.say("Every payday will now give " + str(credits) + " credits.")
        fileIO("data/economy/settings.json", "save", self.settings)

    def display_time(self, seconds, granularity=2):  # What would I ever do without stackoverflow?
        intervals = (  # Source: http://stackoverflow.com/a/24542445
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),  # 60 * 60 * 24
            ('hours', 3600),  # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
        )

        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])


def generatelootmessageline(quality: str):
    # 324 sprays
    # 488 voicelines
    # ---
    # 812 common loot

    # 87  rareskins
    # 118 playericons
    # 66  victoryposes
    # ---
    # 271 rare loot

    # 43  epicskins
    # 66  emotes
    # 66  highlightintros
    # ---
    # 175 epic loot

    # 87  legendaryskins
    line = ""
    loottype = ""
    lootname = ""
    if quality == "Common":
        lootroll = randint(1, 812)
        if lootroll <= 324:
            loottype = "Spray"
            lootname = random.choice(commonloot["sprays"])
        else:
            loottype = "Voice Line"
            lootname = random.choice(commonloot["voicelines"])
    if quality == "Rare":
        lootroll = randint(1, 271)
        if lootroll <= 87:
            loottype = "Skin"
            lootname = random.choice(rareloot["rareskins"])
        elif lootroll <= 205:
            loottype = "Player Icon"
            lootname = random.choice(rareloot["playericons"])
        else:
            loottype = "Victory Pose"
            lootname = random.choice(rareloot["victoryposes"])
    if quality == "Epic":
        lootroll = randint(1, 175)
        if lootroll <= 43:
            loottype = "Skin"
            lootname = random.choice(epicloot["epicskins"])
        elif lootroll <= 109:
            loottype = "Emote"
            lootname = random.choice(epicloot["emotes"])
        else:
            loottype = "Highlight Intro"
            lootname = random.choice(epicloot["highlightintros"])
    if quality == "Legendary":
        loottype = "Skin"
        lootname = random.choice(legendaryloot["legendaryskins"])
    emoji = {"Common": ":green_heart:", "Rare": ":blue_heart:", "Epic": ":purple_heart:",
             "Legendary": ":yellow_heart:"}
    line = line + emoji[quality] + " " + loottype + " | " + lootname + " "
    return line
    # Remember to append the value!


def check_folders():
    if not os.path.exists("data/economy"):
        print("Creating data/economy folder...")
        os.makedirs("data/economy")


def check_files():
    f = "data/economy/settings.json"
    if not fileIO(f, "check"):
        print("Creating default economy's settings.json...")
        fileIO(f, "save", {})

    f = "data/economy/bank.json"
    if not fileIO(f, "check"):
        print("Creating empty bank.json...")
        fileIO(f, "save", {})


def setup(bot):
    global logger
    check_folders()
    check_files()
    logger = logging.getLogger("red.economy")
    if logger.level == 0:  # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='data/economy/economy.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    bot.add_cog(Economy(bot))
