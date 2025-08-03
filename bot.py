import discord
from discord.ext import commands
import random
import os
from typing import List, Dict

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Tarot card data with upright and reversed meanings
MAJOR_ARCANA = [
    {
        "name": "The Fool", 
        "upright": "New beginnings, innocence, spontaneity, free spirit, leap of faith",
        "reversed": "Recklessness, foolishness, lack of direction, poor judgment, naivety"
    },
    {
        "name": "The Magician", 
        "upright": "Manifestation, resourcefulness, power, inspired action, willpower",
        "reversed": "Manipulation, poor planning, untapped talents, lack of focus"
    },
    {
        "name": "The High Priestess", 
        "upright": "Intuition, sacred knowledge, divine feminine, subconscious mind, inner wisdom",
        "reversed": "Secrets, disconnected from intuition, withdrawal, silence, repressed feelings"
    },
    {
        "name": "The Empress", 
        "upright": "Femininity, beauty, nature, nurturing, abundance, creativity",
        "reversed": "Creative block, dependence on others, smothering, lack of growth"
    },
    {
        "name": "The Emperor", 
        "upright": "Authority, establishment, structure, father figure, control, leadership",
        "reversed": "Tyranny, rigidity, coldness, domination, lack of discipline"
    },
    {
        "name": "The Hierophant", 
        "upright": "Spiritual wisdom, religious beliefs, conformity, tradition, institutions",
        "reversed": "Personal beliefs, freedom, challenging the status quo, inner guidance"
    },
    {
        "name": "The Lovers", 
        "upright": "Love, harmony, relationships, values alignment, choices, union",
        "reversed": "Disharmony, imbalance, misalignment of values, relationship struggles"
    },
    {
        "name": "The Chariot", 
        "upright": "Control, willpower, success, determination, direction, focus",
        "reversed": "Lack of control, lack of direction, aggression, scattered energy"
    },
    {
        "name": "Strength", 
        "upright": "Strength, courage, persuasion, influence, compassion, inner power",
        "reversed": "Self-doubt, lack of confidence, abuse of power, weakness"
    },
    {
        "name": "The Hermit", 
        "upright": "Soul searching, introspection, inner guidance, wisdom, seeking truth",
        "reversed": "Isolation, loneliness, withdrawal, lost your way, paranoia"
    },
    {
        "name": "Wheel of Fortune", 
        "upright": "Good luck, karma, life cycles, destiny, turning point, change",
        "reversed": "Bad luck, lack of control, clinging to control, unwelcome changes"
    },
    {
        "name": "Justice", 
        "upright": "Justice, fairness, truth, cause and effect, law, balance",
        "reversed": "Unfairness, lack of accountability, dishonesty, bias, avoiding consequences"
    },
    {
        "name": "The Hanged Man", 
        "upright": "Suspension, restriction, letting go, sacrifice, martyrdom, surrender",
        "reversed": "Delays, resistance, stalling, indecision, lack of sacrifice"
    },
    {
        "name": "Death", 
        "upright": "Endings, beginnings, change, transformation, transition, rebirth",
        "reversed": "Resistance to change, personal transformation, inner purging, stagnation"
    },
    {
        "name": "Temperance", 
        "upright": "Balance, moderation, patience, purpose, meaning, harmony",
        "reversed": "Imbalance, excess, self-healing, re-alignment, hasty decisions"
    },
    {
        "name": "The Devil", 
        "upright": "Bondage, addiction, sexuality, materialism, temptation, restriction",
        "reversed": "Releasing limiting beliefs, exploring dark thoughts, detachment, breaking free"
    },
    {
        "name": "The Tower", 
        "upright": "Sudden change, upheaval, chaos, revelation, awakening, destruction",
        "reversed": "Personal transformation, fear of change, averting disaster, delayed catastrophe"
    },
    {
        "name": "The Star", 
        "upright": "Hope, faith, purpose, renewal, spirituality, healing, inspiration",
        "reversed": "Lack of faith, despair, self-trust, disconnection, discouragement"
    },
    {
        "name": "The Moon", 
        "upright": "Illusion, fear, anxiety, subconscious, intuition, dreams, uncertainty",
        "reversed": "Release of fear, repressed emotion, inner confusion, unveiling secrets"
    },
    {
        "name": "The Sun", 
        "upright": "Positivity, fun, warmth, success, vitality, joy, enlightenment",
        "reversed": "Inner child, feeling down, overly optimistic, lack of success, delayed happiness"
    },
    {
        "name": "Judgement", 
        "upright": "Judgement, rebirth, inner calling, absolution, second chances, awakening",
        "reversed": "Self-doubt, harsh self-judgement, lack of self-awareness, avoiding calling"
    },
    {
        "name": "The World", 
        "upright": "Completion, accomplishment, travel, fulfillment, success, unity",
        "reversed": "Incomplete goals, lack of closure, stagnation, failed plans, delays"
    }
]

MINOR_ARCANA_SUITS = {
    "Cups": {
        "upright": "Emotions, love, relationships, spirituality, intuition, healing",
        "reversed": "Emotional imbalance, blocked creativity, unrequited love, moodiness"
    },
    "Pentacles": {
        "upright": "Material world, career, money, physical manifestation, resources, prosperity",
        "reversed": "Financial loss, lack of planning, greed, materialistic focus, scarcity mindset"
    },
    "Swords": {
        "upright": "Thought, communication, conflict, mental activity, intellect, clarity",
        "reversed": "Confusion, harsh self-criticism, mental fog, miscommunication, inner conflict"
    },
    "Wands": {
        "upright": "Energy, creativity, passion, growth, inspiration, adventure",
        "reversed": "Lack of energy, creative blocks, delays, frustration, burnout"
    }
}

COURT_CARDS = ["Page", "Knight", "Queen", "King"]
NUMBER_CARDS = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]

def create_full_deck() -> List[Dict]:
    """Create a full 78-card tarot deck with upright and reversed meanings"""
    deck = []
    
    # Add Major Arcana
    deck.extend(MAJOR_ARCANA)
    
    # Add Minor Arcana
    for suit, suit_meanings in MINOR_ARCANA_SUITS.items():
        # Number cards
        for number in NUMBER_CARDS:
            deck.append({
                "name": f"{number} of {suit}",
                "upright": f"{suit_meanings['upright']} - {number} energy in {suit.lower()}",
                "reversed": f"{suit_meanings['reversed']} - {number} challenges in {suit.lower()}"
            })
        
        # Court cards
        for court in COURT_CARDS:
            deck.append({
                "name": f"{court} of {suit}",
                "upright": f"{suit_meanings['upright']} - {court} personality embodying {suit.lower()}",
                "reversed": f"{suit_meanings['reversed']} - {court} shadow aspects in {suit.lower()}"
            })
    
    return deck

def draw_card_with_orientation(card_data: Dict) -> Dict:
    """Draw a card and determine if it's upright or reversed (50% chance each)"""
    is_reversed = random.choice([True, False])
    
    card_result = {
        "name": card_data["name"],
        "is_reversed": is_reversed,
        "meaning": card_data["reversed"] if is_reversed else card_data["upright"]
    }
    
    return card_result

def format_card_name(card: Dict) -> str:
    """Format card name with reversed indicator"""
    if card["is_reversed"]:
        return f"{card['name']} (Reversed)"
    return card["name"]

def get_card_emoji(card: Dict) -> str:
    """Get appropriate emoji based on card orientation"""
    return "🔄" if card["is_reversed"] else "✨"

FULL_DECK = create_full_deck()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

@bot.command(name='card', help='Draw a single tarot card')
async def single_card(ctx):
    """Draw a single random tarot card"""
    card_data = random.choice(FULL_DECK)
    card = draw_card_with_orientation(card_data)
    
    embed = discord.Embed(
        title="🔮 Single Card Draw",
        color=0x800080 if not card["is_reversed"] else 0x4B0082
    )
    embed.add_field(
        name=f"**{get_card_emoji(card)} {format_card_name(card)}**",
        value=card['meaning'],
        inline=False
    )
    
    if card["is_reversed"]:
        embed.set_footer(text="🔄 This card appeared reversed - consider its shadow aspects and internal challenges")
    else:
        embed.set_footer(text="✨ Trust your intuition")
    
    await ctx.send(embed=embed)

@bot.command(name='threecards', help='Draw a three-card spread (Past, Present, Future)')
async def three_card_spread(ctx):
    """Draw a three-card spread"""
    card_data_list = random.sample(FULL_DECK, 3)
    cards = [draw_card_with_orientation(card_data) for card_data in card_data_list]
    positions = ["Past", "Present", "Future"]
    
    # Determine embed color based on majority orientation
    reversed_count = sum(1 for card in cards if card["is_reversed"])
    embed_color = 0x4B0082 if reversed_count >= 2 else 0x800080
    
    embed = discord.Embed(
        title="🔮 Three Card Spread",
        description="Past • Present • Future",
        color=embed_color
    )
    
    for card, position in zip(cards, positions):
        embed.add_field(
            name=f"**{position}: {get_card_emoji(card)} {format_card_name(card)}**",
            value=card['meaning'],
            inline=False
        )
    
    reversed_cards = [card for card in cards if card["is_reversed"]]
    if reversed_cards:
        embed.set_footer(text=f"🔄 {len(reversed_cards)} card(s) appeared reversed - pay attention to internal challenges and shadow work")
    else:
        embed.set_footer(text="✨ Reflect on the connections between these cards")
    
    await ctx.send(embed=embed)

@bot.command(name='celtic', help='Draw a Celtic Cross spread (10 cards)')
async def celtic_cross(ctx):
    """Draw a Celtic Cross spread"""
    card_data_list = random.sample(FULL_DECK, 10)
    cards = [draw_card_with_orientation(card_data) for card_data in card_data_list]
    positions = [
        "Present Situation",
        "Challenge/Cross",
        "Distant Past/Foundation", 
        "Recent Past",
        "Possible Outcome",
        "Near Future",
        "Your Approach",
        "External Influences",
        "Hopes and Fears",
        "Final Outcome"
    ]
    
    # Determine embed color based on majority orientation
    reversed_count = sum(1 for card in cards if card["is_reversed"])
    embed_color = 0x4B0082 if reversed_count >= 5 else 0x800080
    
    embed = discord.Embed(
        title="🔮 Celtic Cross Spread",
        description="A comprehensive 10-card reading",
        color=embed_color
    )
    
    # Split into two embeds if too long
    for i in range(5):
        embed.add_field(
            name=f"**{i+1}. {positions[i]}: {get_card_emoji(cards[i])} {format_card_name(cards[i])}**",
            value=cards[i]['meaning'],
            inline=False
        )
    
    await ctx.send(embed=embed)
    
    # Second embed for remaining cards
    embed2 = discord.Embed(
        title="🔮 Celtic Cross Spread (continued)",
        color=embed_color
    )
    
    for i in range(5, 10):
        embed2.add_field(
            name=f"**{i+1}. {positions[i]}: {get_card_emoji(cards[i])} {format_card_name(cards[i])}**",
            value=cards[i]['meaning'],
            inline=False
        )
    
    reversed_cards = [card for card in cards if card["is_reversed"]]
    if reversed_cards:
        embed2.set_footer(text=f"🔄 {len(reversed_cards)} card(s) appeared reversed - deep inner work and shadow integration needed")
    else:
        embed2.set_footer(text="✨ Take time to meditate on this reading")
    
    await ctx.send(embed=embed2)

@bot.command(name='love', help='Draw a love/relationship reading')
async def love_reading(ctx):
    """Draw a relationship-focused reading"""
    card_data_list = random.sample(FULL_DECK, 3)
    cards = [draw_card_with_orientation(card_data) for card_data in card_data_list]
    positions = ["You", "Your Partner/Potential Partner", "The Relationship"]
    
    # Determine embed color based on majority orientation
    reversed_count = sum(1 for card in cards if card["is_reversed"])
    embed_color = 0xFF1493 if reversed_count >= 2 else 0xFF69B4  # Darker pink for mostly reversed
    
    embed = discord.Embed(
        title="💕 Love & Relationship Reading",
        description="Understanding your romantic energy",
        color=embed_color
    )
    
    for card, position in zip(cards, positions):
        embed.add_field(
            name=f"**{position}: {get_card_emoji(card)} {format_card_name(card)}**",
            value=card['meaning'],
            inline=False
        )
    
    reversed_cards = [card for card in cards if card["is_reversed"]]
    if reversed_cards:
        embed.set_footer(text=f"💔 {len(reversed_cards)} card(s) reversed - focus on healing and inner work in love")
    else:
        embed.set_footer(text="💖 Love grows through understanding")
    
    await ctx.send(embed=embed)

@bot.command(name='daily', help='Draw your daily guidance card')
async def daily_reading(ctx):
    """Draw a daily guidance card"""
    card_data = random.choice(FULL_DECK)
    card = draw_card_with_orientation(card_data)
    
    embed = discord.Embed(
        title="🌅 Daily Guidance",
        description="Your card for today",
        color=0xFFD700 if not card["is_reversed"] else 0xDAA520  # Gold or darker gold
    )
    
    guidance_text = f"{card['meaning']}\n\n*How can this energy guide you today?*"
    if card["is_reversed"]:
        guidance_text += f"\n\n🔄 *This card appeared reversed - what inner work needs attention?*"
    
    embed.add_field(
        name=f"**{get_card_emoji(card)} {format_card_name(card)}**",
        value=guidance_text,
        inline=False
    )
    
    if card["is_reversed"]:
        embed.set_footer(text="🔄 Today calls for introspection and shadow work")
    else:
        embed.set_footer(text="🌟 Carry this wisdom with you")
    
    await ctx.send(embed=embed)

@bot.command(name='help_tarot', help='Show all tarot bot commands')
async def help_tarot(ctx):
    """Show help for tarot commands"""
    embed = discord.Embed(
        title="🔮 Tarot Bot Commands",
        description="Available tarot readings\n\n🔄 **Note:** All cards have a 50% chance of appearing reversed, offering deeper shadow work insights!",
        color=0x9932CC
    )
    
    commands_list = [
        ("!card", "Draw a single tarot card"),
        ("!daily", "Daily guidance card"),
        ("!threecards", "Past, Present, Future spread"),
        ("!love", "Love & relationship reading"),
        ("!celtic", "Celtic Cross spread (10 cards)"),
        ("!help_tarot", "Show this help message")
    ]
    
    for cmd, desc in commands_list:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    embed.add_field(
        name="🔄 **Understanding Reversed Cards**",
        value="Reversed cards aren't 'bad' - they represent:\n• Internal challenges\n• Shadow aspects to explore\n• Blocked energy needing attention\n• Opportunities for inner growth",
        inline=False
    )
    
    embed.set_footer(text="✨ May the cards guide your path - both light and shadow")
    
    await ctx.send(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("🔮 Command not found. Use `!help_tarot` to see available commands.")
    else:
        print(f"Error: {error}")
        await ctx.send("🔮 Something went wrong. Please try again.")

# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: DISCORD_TOKEN environment variable not found!")
        exit(1)
    
    bot.run(token)
