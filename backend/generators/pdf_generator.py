"""
PDF Generator for The Calm Mind Collection
Generates 5 colorful, professional PDF products
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String
from reportlab.graphics import renderPDF
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "pdfs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Color palettes for each product
COLORS = {
    "journal": {
        "primary": HexColor("#3A5A40"),
        "secondary": HexColor("#A3B18A"),
        "accent": HexColor("#DAD7CD"),
        "bg": HexColor("#F0F7F0"),
        "dark": HexColor("#1B2E1B"),
        "text": HexColor("#2D3D2D"),
        "light": HexColor("#E8F0E8"),
    },
    "planner": {
        "primary": HexColor("#E9C46A"),
        "secondary": HexColor("#F4A261"),
        "accent": HexColor("#264653"),
        "bg": HexColor("#FFFBF0"),
        "dark": HexColor("#5C4A1E"),
        "text": HexColor("#3D3520"),
        "light": HexColor("#FFF8E8"),
    },
    "ebook": {
        "primary": HexColor("#2A9D8F"),
        "secondary": HexColor("#76C7B7"),
        "accent": HexColor("#264653"),
        "bg": HexColor("#F0FAF8"),
        "dark": HexColor("#1A4A44"),
        "text": HexColor("#1A3A36"),
        "light": HexColor("#E0F5F2"),
    },
    "workbook": {
        "primary": HexColor("#6366F1"),
        "secondary": HexColor("#A5B4FC"),
        "accent": HexColor("#312E81"),
        "bg": HexColor("#F0F0FF"),
        "dark": HexColor("#2D2A6E"),
        "text": HexColor("#2D2B5E"),
        "light": HexColor("#E8E8FF"),
    },
    "cards": {
        "primary": HexColor("#E76F51"),
        "secondary": HexColor("#F4A261"),
        "accent": HexColor("#264653"),
        "bg": HexColor("#FFF5F2"),
        "dark": HexColor("#8B3A28"),
        "text": HexColor("#4A2518"),
        "light": HexColor("#FFE8E2"),
    },
}


def draw_rounded_rect(c, x, y, w, h, r, fill_color=None, stroke_color=None, stroke_width=1):
    """Draw a rounded rectangle on the canvas."""
    c.saveState()
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
    else:
        c.setStrokeColor(fill_color if fill_color else HexColor("#000000"))
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    if fill_color and stroke_color:
        c.drawPath(p, fill=1, stroke=1)
    elif fill_color:
        c.drawPath(p, fill=1, stroke=0)
    else:
        c.drawPath(p, fill=0, stroke=1)
    c.restoreState()


def draw_circle_pattern(c, page_width, page_height, color, count=15):
    """Draw decorative circle pattern."""
    import random
    random.seed(42)
    c.saveState()
    for _ in range(count):
        x = random.uniform(0, page_width)
        y = random.uniform(0, page_height)
        r = random.uniform(3, 20)
        opacity = random.uniform(0.03, 0.08)
        c.setFillColor(Color(color.red, color.green, color.blue, opacity))
        c.circle(x, y, r, fill=1, stroke=0)
    c.restoreState()


def draw_header_bar(c, page_width, page_height, color, height=60):
    """Draw a colored header bar at top of page."""
    c.saveState()
    c.setFillColor(color)
    c.rect(0, page_height - height, page_width, height, fill=1, stroke=0)
    c.restoreState()


def draw_footer(c, page_width, color, text, page_num):
    """Draw footer with page number."""
    c.saveState()
    c.setFillColor(Color(color.red, color.green, color.blue, 0.15))
    c.rect(0, 0, page_width, 35, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_width / 2, 14, f"{text}  |  Page {page_num}")
    c.restoreState()


def generate_journal():
    """Generate the 90-Day Anxiety Relief Journal."""
    filepath = str(OUTPUT_DIR / "90_day_anxiety_relief_journal.pdf")
    colors = COLORS["journal"]
    page_w, page_h = letter

    c = canvas.Canvas(filepath, pagesize=letter)

    # === COVER PAGE ===
    c.setFillColor(colors["primary"])
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Decorative circles
    draw_circle_pattern(c, page_w, page_h, HexColor("#FFFFFF"), 25)

    # Central white card
    card_w, card_h = 400, 500
    card_x = (page_w - card_w) / 2
    card_y = (page_h - card_h) / 2
    draw_rounded_rect(c, card_x, card_y, card_w, card_h, 20, fill_color=HexColor("#FFFFFF"))

    # Title
    c.setFillColor(colors["primary"])
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w / 2, card_y + card_h - 60, "THE")
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(page_w / 2, card_y + card_h - 100, "90-Day")
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(page_w / 2, card_y + card_h - 140, "Anxiety Relief")
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(page_w / 2, card_y + card_h - 180, "Journal")

    # Decorative line
    c.setStrokeColor(colors["secondary"])
    c.setLineWidth(2)
    c.line(card_x + 80, card_y + card_h - 200, card_x + card_w - 80, card_y + card_h - 200)

    # Subtitle
    c.setFillColor(colors["text"])
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w / 2, card_y + card_h - 230, "Daily Prompts, Mood Tracking")
    c.drawCentredString(page_w / 2, card_y + card_h - 248, "& Gratitude Practice")

    # Leaf decorative element
    c.setFillColor(colors["secondary"])
    c.circle(page_w / 2 - 30, card_y + 100, 8, fill=1, stroke=0)
    c.circle(page_w / 2, card_y + 100, 10, fill=1, stroke=0)
    c.circle(page_w / 2 + 30, card_y + 100, 8, fill=1, stroke=0)

    c.setFillColor(colors["text"])
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w / 2, card_y + 60, "The Calm Mind Collection")
    c.drawCentredString(page_w / 2, card_y + 45, "www.thecalmmindcollection.com")

    c.showPage()

    # === INTRO PAGE ===
    c.setFillColor(colors["bg"])
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_header_bar(c, page_w, page_h, colors["primary"])
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_w / 2, page_h - 40, "Welcome to Your Journey")

    y = page_h - 110
    c.setFillColor(colors["text"])
    c.setFont("Helvetica-Bold", 16)
    c.drawString(60, y, "Dear Friend,")
    y -= 30

    intro_lines = [
        "Welcome to your 90-Day Anxiety Relief Journal. This journal is designed",
        "to be your daily companion on the path to calm and clarity.",
        "",
        "Each day, you will find:",
        "",
        "  A morning intention to set your focus",
        "  A mood tracker to understand your patterns",
        "  Guided journaling prompts to process your thoughts",
        "  A gratitude section to shift your perspective",
        "  An evening reflection to close your day peacefully",
        "",
        "Remember: There are no wrong answers here. This is your safe space.",
        "Write freely, honestly, and without judgment.",
        "",
        "The journey of a thousand miles begins with a single step.",
        "Today, you are taking that step.",
        "",
        "With warmth and compassion,",
        "The Calm Mind Collection",
    ]

    c.setFont("Helvetica", 11)
    for line in intro_lines:
        c.drawString(60, y, line)
        y -= 20

    draw_footer(c, page_w, colors["primary"], "90-Day Anxiety Relief Journal", 1)
    c.showPage()

    # === HOW TO USE PAGE ===
    c.setFillColor(colors["bg"])
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_header_bar(c, page_w, page_h, colors["primary"])
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_w / 2, page_h - 40, "How to Use This Journal")

    y = page_h - 100
    instructions = [
        ("Morning (5 minutes)", [
            "Set your intention for the day",
            "Rate your morning mood on a scale of 1-10",
            "Write what you are grateful for",
        ]),
        ("Midday Check-in (2 minutes)", [
            "Pause and breathe for 30 seconds",
            "Note your current emotional state",
            "Adjust your intention if needed",
        ]),
        ("Evening Reflection (5 minutes)", [
            "Answer the daily journaling prompt",
            "Record 3 things that went well",
            "Rate your evening mood",
            "Write one kind thing you did for yourself",
        ]),
    ]

    for title, items in instructions:
        draw_rounded_rect(c, 50, y - 20 - len(items) * 22, page_w - 100, 30 + len(items) * 22, 10, fill_color=colors["light"])
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 13)
        c.drawString(70, y, title)
        y -= 25
        c.setFillColor(colors["text"])
        c.setFont("Helvetica", 10)
        for item in items:
            c.drawString(90, y, f"  {item}")
            y -= 22
        y -= 20

    draw_footer(c, page_w, colors["primary"], "90-Day Anxiety Relief Journal", 2)
    c.showPage()

    # === DAILY JOURNAL PAGES (90 days) ===
    prompts = [
        "What is weighing on your mind today? Write it all out.",
        "Describe a time you felt completely at peace. What made it special?",
        "What would you say to a friend feeling the way you feel right now?",
        "List 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.",
        "What is one small thing you can do today to be kind to yourself?",
        "Write about a challenge you have overcome. What strength did it reveal?",
        "If your anxiety could speak, what would it say? What would you respond?",
        "Describe your ideal morning. How can you move closer to it?",
        "What boundaries do you need to set or maintain this week?",
        "Write a letter of forgiveness to yourself.",
        "What are three things that always make you smile?",
        "Describe the last time you laughed really hard. How did it feel?",
        "What does 'calm' look like for you? Paint it with words.",
        "List everything you are worried about. Now circle what you can control.",
        "What is one habit you would like to build? Why does it matter?",
        "Write about someone who makes you feel safe and supported.",
        "What song, book, or movie always makes you feel better?",
        "Describe a place where you feel most yourself.",
        "What would you do today if you weren't afraid?",
        "Write three affirmations that feel true and powerful to you.",
        "What lesson has your anxiety taught you about yourself?",
        "Describe a perfect evening of self-care in detail.",
        "What are you holding onto that you need to let go of?",
        "Write about a time when things turned out better than you expected.",
        "What does your inner critic say most often? Now rewrite it with compassion.",
        "List 10 things you are grateful for right now.",
        "What activity makes you lose track of time in the best way?",
        "Write about your relationship with rest. Do you allow yourself to rest?",
        "What would your life look like if anxiety didn't hold you back?",
        "Describe three wins from this past week, no matter how small.",
    ]

    moods = ["Anxious", "Worried", "Neutral", "Calm", "Hopeful", "Peaceful", "Joyful"]

    for day in range(1, 91):
        prompt = prompts[(day - 1) % len(prompts)]

        # Background
        c.setFillColor(colors["bg"])
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

        # Header bar
        draw_header_bar(c, page_w, page_h, colors["primary"], 50)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, page_h - 35, f"Day {day} of 90")
        c.setFont("Helvetica", 10)
        c.drawRightString(page_w - 30, page_h - 35, "Date: ____/____/________")

        y = page_h - 80

        # Morning Intention Box
        draw_rounded_rect(c, 30, y - 60, page_w - 60, 65, 8, fill_color=colors["light"], stroke_color=colors["secondary"], stroke_width=1)
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(45, y - 5, "Morning Intention")
        c.setStrokeColor(colors["accent"])
        c.setLineWidth(0.5)
        for i in range(2):
            c.line(45, y - 25 - i * 18, page_w - 45, y - 25 - i * 18)
        y -= 80

        # Mood Tracker
        draw_rounded_rect(c, 30, y - 45, page_w - 60, 50, 8, fill_color=HexColor("#FFFFFF"), stroke_color=colors["secondary"], stroke_width=1)
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(45, y - 5, "Mood Check-in:")
        spacing = (page_w - 200) / len(moods)
        for i, mood in enumerate(moods):
            cx = 170 + i * spacing
            c.setStrokeColor(colors["secondary"])
            c.setLineWidth(1)
            c.circle(cx, y - 20, 8, fill=0, stroke=1)
            c.setFillColor(colors["text"])
            c.setFont("Helvetica", 7)
            c.drawCentredString(cx, y - 38, mood)
        y -= 65

        # Gratitude Section
        draw_rounded_rect(c, 30, y - 75, (page_w - 70) / 2, 80, 8, fill_color=colors["light"])
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 10)
        c.drawString(45, y - 5, "I am grateful for...")
        c.setFont("Helvetica", 9)
        c.setFillColor(colors["text"])
        for i in range(3):
            c.drawString(45, y - 25 - i * 18, f"{i + 1}. _________________________________")

        # Self-Care Box
        right_x = 30 + (page_w - 70) / 2 + 10
        draw_rounded_rect(c, right_x, y - 75, (page_w - 70) / 2, 80, 8, fill_color=colors["light"])
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 10)
        c.drawString(right_x + 15, y - 5, "Today I will care for myself by...")
        c.setFont("Helvetica", 9)
        c.setStrokeColor(colors["accent"])
        for i in range(3):
            c.line(right_x + 15, y - 25 - i * 18, right_x + (page_w - 70) / 2 - 15, y - 25 - i * 18)
        y -= 95

        # Journaling Prompt
        draw_rounded_rect(c, 30, y - 200, page_w - 60, 205, 8, fill_color=HexColor("#FFFFFF"), stroke_color=colors["primary"], stroke_width=1.5)
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(45, y - 5, "Today's Prompt:")
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(colors["text"])

        # Word wrap the prompt
        words = prompt.split()
        line = ""
        prompt_y = y - 25
        for word in words:
            test = line + " " + word if line else word
            if c.stringWidth(test, "Helvetica-Oblique", 10) > page_w - 120:
                c.drawString(45, prompt_y, line)
                line = word
                prompt_y -= 15
            else:
                line = test
        if line:
            c.drawString(45, prompt_y, line)

        # Lines for writing
        c.setStrokeColor(colors["accent"])
        c.setLineWidth(0.3)
        for i in range(8):
            line_y = prompt_y - 20 - i * 18
            if line_y > y - 195:
                c.line(45, line_y, page_w - 45, line_y)
        y -= 220

        # Evening Reflection
        draw_rounded_rect(c, 30, y - 130, page_w - 60, 135, 8, fill_color=colors["light"])
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(45, y - 5, "Evening Reflection")

        c.setFont("Helvetica", 9)
        c.setFillColor(colors["text"])
        c.drawString(45, y - 25, "Three things that went well today:")
        for i in range(3):
            c.drawString(45, y - 42 - i * 16, f"{i + 1}. _______________________________________________")

        c.drawString(45, y - 95, "Evening mood (1-10): _____")
        c.drawString(250, y - 95, "One kind thing I did for myself: _____________________")
        c.drawString(45, y - 115, "Tomorrow I look forward to: _________________________________________________")

        draw_footer(c, page_w, colors["primary"], "90-Day Anxiety Relief Journal", day + 2)
        c.showPage()

    # === FINAL REFLECTION PAGE ===
    c.setFillColor(colors["primary"])
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_circle_pattern(c, page_w, page_h, HexColor("#FFFFFF"), 20)

    draw_rounded_rect(c, 60, 150, page_w - 120, page_h - 300, 20, fill_color=HexColor("#FFFFFF"))

    c.setFillColor(colors["primary"])
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(page_w / 2, page_h - 200, "Congratulations!")
    c.setFont("Helvetica", 14)
    c.drawCentredString(page_w / 2, page_h - 230, "You completed 90 days of journaling.")

    y = page_h - 280
    reflection_prompts = [
        "How has your relationship with anxiety changed?",
        "What surprised you most about this journey?",
        "What daily habit will you continue?",
        "What would you tell someone starting this journal?",
        "Describe yourself in 3 words now vs. 90 days ago.",
    ]
    c.setFont("Helvetica-Bold", 11)
    c.drawString(90, y, "Final Reflection Questions:")
    y -= 25
    c.setFont("Helvetica", 10)
    for q in reflection_prompts:
        c.drawString(90, y, f"  {q}")
        y -= 18
        for _ in range(2):
            c.line(90, y, page_w - 90, y)
            y -= 18
        y -= 10

    c.showPage()
    c.save()
    return filepath


def generate_planner():
    """Generate the Morning & Evening Routine Planner."""
    filepath = str(OUTPUT_DIR / "morning_evening_routine_planner.pdf")
    colors = COLORS["planner"]
    page_w, page_h = letter
    c = canvas.Canvas(filepath, pagesize=letter)

    # === COVER ===
    c.setFillColor(colors["primary"])
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_circle_pattern(c, page_w, page_h, HexColor("#FFFFFF"), 20)

    card_w, card_h = 400, 480
    card_x = (page_w - card_w) / 2
    card_y = (page_h - card_h) / 2
    draw_rounded_rect(c, card_x, card_y, card_w, card_h, 20, fill_color=HexColor("#FFFFFF"))

    c.setFillColor(colors["accent"])
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(page_w / 2, card_y + card_h - 55, "THE CALM MIND COLLECTION")
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(page_w / 2, card_y + card_h - 95, "Morning & Evening")
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(page_w / 2, card_y + card_h - 135, "Routine Planner")

    c.setStrokeColor(colors["secondary"])
    c.setLineWidth(2)
    c.line(card_x + 80, card_y + card_h - 155, card_x + card_w - 80, card_y + card_h - 155)

    c.setFillColor(colors["text"])
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w / 2, card_y + card_h - 185, "Build Calm Habits That Stick")
    c.drawCentredString(page_w / 2, card_y + card_h - 205, "One Morning, One Evening at a Time")

    c.setFillColor(colors["primary"])
    c.circle(page_w / 2 - 20, card_y + 80, 6, fill=1, stroke=0)
    c.circle(page_w / 2, card_y + 80, 8, fill=1, stroke=0)
    c.circle(page_w / 2 + 20, card_y + 80, 6, fill=1, stroke=0)

    c.showPage()

    # === INTRO PAGE ===
    c.setFillColor(colors["bg"])
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_header_bar(c, page_w, page_h, colors["accent"], 50)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w / 2, page_h - 35, "Your Routine is Your Anchor")

    y = page_h - 90
    c.setFillColor(colors["text"])
    c.setFont("Helvetica", 11)
    intro = [
        "A calm morning sets the tone for your entire day.",
        "A peaceful evening restores your energy for tomorrow.",
        "",
        "This planner gives you the framework to design routines that reduce",
        "anxiety and build resilience. Use it daily, weekly, or however works for you.",
        "",
        "Inside you'll find:",
        "  Morning routine templates with time blocks",
        "  Evening wind-down checklists",
        "  Weekly habit tracking grids",
        "  Space for reflection and adjustment",
        "  Inspirational quotes to keep you motivated",
    ]
    for line in intro:
        c.drawString(60, y, line)
        y -= 20
    draw_footer(c, page_w, colors["accent"], "Morning & Evening Routine Planner", 1)
    c.showPage()

    # === DAILY ROUTINE PAGES (30 days) ===
    morning_tasks = [
        "Wake up at consistent time", "Drink a glass of water",
        "5-minute stretching", "Mindful breathing (3 min)",
        "Set daily intention", "Healthy breakfast",
        "Review today's priorities", "Gratitude moment",
    ]
    evening_tasks = [
        "Screen-free 30 min before bed", "Prepare tomorrow's essentials",
        "Gentle stretching or yoga", "Journal 3 good things",
        "Read for 15 minutes", "Relaxation breathing",
        "Set consistent bedtime", "Body scan meditation",
    ]

    quotes = [
        "The secret of your future is hidden in your daily routine.",
        "How you start your day is how you live your day.",
        "Evening is a time for reflection, morning for intention.",
        "Small daily improvements lead to stunning results.",
        "The calm you seek is within the habits you build.",
        "Be patient with yourself. Growth is not linear.",
        "Rest is not laziness. It is preparation for greatness.",
    ]

    for day in range(1, 31):
        c.setFillColor(colors["bg"])
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

        # Header
        draw_header_bar(c, page_w, page_h, colors["accent"], 50)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, page_h - 35, f"Day {day}")
        c.drawRightString(page_w - 30, page_h - 35, "Date: ____/____/________")

        y = page_h - 80

        # Quote
        quote = quotes[(day - 1) % len(quotes)]
        draw_rounded_rect(c, 30, y - 30, page_w - 60, 35, 6, fill_color=colors["light"])
        c.setFillColor(colors["accent"])
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(page_w / 2, y - 18, f'"{quote}"')
        y -= 50

        # MORNING SECTION
        draw_rounded_rect(c, 30, y - 250, (page_w - 70) / 2, 255, 10, fill_color=HexColor("#FFFFFF"), stroke_color=colors["primary"], stroke_width=1)
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 13)
        c.drawString(45, y - 5, "Morning Routine")
        c.setFont("Helvetica", 9)
        c.drawString(45, y - 22, "Wake time: ________  Target: ________")

        task_y = y - 45
        c.setFont("Helvetica", 9)
        for task in morning_tasks:
            c.setStrokeColor(colors["primary"])
            c.rect(48, task_y - 3, 10, 10, fill=0, stroke=1)
            c.setFillColor(colors["text"])
            c.drawString(65, task_y, task)
            task_y -= 18

        c.setFillColor(colors["text"])
        c.setFont("Helvetica-Bold", 9)
        c.drawString(45, task_y - 10, "Morning energy (1-10): _____")

        # EVENING SECTION
        right_x = 30 + (page_w - 70) / 2 + 10
        draw_rounded_rect(c, right_x, y - 250, (page_w - 70) / 2, 255, 10, fill_color=HexColor("#FFFFFF"), stroke_color=colors["secondary"], stroke_width=1)
        c.setFillColor(colors["accent"])
        c.setFont("Helvetica-Bold", 13)
        c.drawString(right_x + 15, y - 5, "Evening Routine")
        c.setFont("Helvetica", 9)
        c.drawString(right_x + 15, y - 22, "Wind-down start: ________  Bed: ________")

        task_y = y - 45
        for task in evening_tasks:
            c.setStrokeColor(colors["secondary"])
            c.rect(right_x + 18, task_y - 3, 10, 10, fill=0, stroke=1)
            c.setFillColor(colors["text"])
            c.drawString(right_x + 35, task_y, task)
            task_y -= 18

        c.setFillColor(colors["text"])
        c.setFont("Helvetica-Bold", 9)
        c.drawString(right_x + 15, task_y - 10, "Sleep quality (1-10): _____")
        y -= 270

        # Notes section
        draw_rounded_rect(c, 30, y - 120, page_w - 60, 125, 10, fill_color=colors["light"])
        c.setFillColor(colors["accent"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(45, y - 5, "Daily Reflection & Notes")
        c.setStrokeColor(colors["accent"])
        c.setLineWidth(0.3)
        for i in range(5):
            c.line(45, y - 28 - i * 18, page_w - 45, y - 28 - i * 18)

        draw_footer(c, page_w, colors["accent"], "Morning & Evening Routine Planner", day + 1)
        c.showPage()

    # === WEEKLY TRACKER (4 weeks) ===
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for week in range(1, 5):
        c.setFillColor(colors["bg"])
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
        draw_header_bar(c, page_w, page_h, colors["accent"], 50)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(page_w / 2, page_h - 35, f"Week {week} Habit Tracker")

        y = page_h - 90
        habits = ["Wake on time", "Morning routine", "Hydration", "Exercise", "Evening routine", "Bedtime goal", "Journaling", "Gratitude"]

        # Table header
        col_w = (page_w - 180) / 7
        c.setFillColor(colors["accent"])
        c.setFont("Helvetica-Bold", 9)
        c.drawString(45, y, "Habit")
        for i, d in enumerate(days_of_week):
            c.drawCentredString(170 + i * col_w, y, d)

        y -= 5
        c.setStrokeColor(colors["accent"])
        c.setLineWidth(1)
        c.line(30, y, page_w - 30, y)
        y -= 20

        for habit in habits:
            draw_rounded_rect(c, 30, y - 8, page_w - 60, 22, 4, fill_color=colors["light"])
            c.setFillColor(colors["text"])
            c.setFont("Helvetica", 9)
            c.drawString(45, y - 2, habit)
            for i in range(7):
                cx = 170 + i * col_w
                c.setStrokeColor(colors["primary"])
                c.circle(cx, y, 6, fill=0, stroke=1)
            y -= 28

        draw_footer(c, page_w, colors["accent"], "Morning & Evening Routine Planner", 32 + week)
        c.showPage()

    c.save()
    return filepath


def generate_ebook():
    """Generate The Calm Mind Ebook."""
    filepath = str(OUTPUT_DIR / "the_calm_mind_ebook.pdf")
    colors = COLORS["ebook"]
    page_w, page_h = letter
    c = canvas.Canvas(filepath, pagesize=letter)

    # === COVER ===
    c.setFillColor(colors["primary"])
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_circle_pattern(c, page_w, page_h, HexColor("#FFFFFF"), 25)

    card_w, card_h = 400, 500
    card_x = (page_w - card_w) / 2
    card_y = (page_h - card_h) / 2
    draw_rounded_rect(c, card_x, card_y, card_w, card_h, 20, fill_color=HexColor("#FFFFFF"))

    c.setFillColor(colors["primary"])
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(page_w / 2, card_y + card_h - 55, "THE CALM MIND COLLECTION PRESENTS")

    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(page_w / 2, card_y + card_h - 100, "The Calm")
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(page_w / 2, card_y + card_h - 140, "Mind")

    c.setStrokeColor(colors["secondary"])
    c.setLineWidth(2)
    c.line(card_x + 100, card_y + card_h - 160, card_x + card_w - 100, card_y + card_h - 160)

    c.setFillColor(colors["text"])
    c.setFont("Helvetica", 13)
    c.drawCentredString(page_w / 2, card_y + card_h - 190, "A Complete Guide to Understanding")
    c.drawCentredString(page_w / 2, card_y + card_h - 210, "and Managing Everyday Anxiety")

    c.setFillColor(colors["accent"])
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_w / 2, card_y + 60, "Evidence-Based Strategies for Lasting Calm")

    c.showPage()

    # === TABLE OF CONTENTS ===
    c.setFillColor(colors["bg"])
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_header_bar(c, page_w, page_h, colors["primary"], 50)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_w / 2, page_h - 35, "Table of Contents")

    chapters = [
        ("Chapter 1", "Understanding Anxiety: Your Brain's Alarm System", 3),
        ("Chapter 2", "The Science of Calm: How Relaxation Works", 8),
        ("Chapter 3", "Breathing Techniques That Actually Work", 13),
        ("Chapter 4", "Cognitive Reframing: Changing Your Thought Patterns", 18),
        ("Chapter 5", "The Power of Routine & Ritual", 23),
        ("Chapter 6", "Mindfulness for the Overwhelmed", 28),
        ("Chapter 7", "Building Your Personal Calm Toolkit", 33),
        ("Chapter 8", "When to Seek Professional Help", 38),
        ("Chapter 9", "Your 30-Day Calm Action Plan", 42),
        ("Appendix", "Quick Reference: Emergency Calm Techniques", 47),
    ]

    y = page_h - 100
    for ch_num, ch_title, pg in chapters:
        draw_rounded_rect(c, 50, y - 10, page_w - 100, 28, 6, fill_color=colors["light"])
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 10)
        c.drawString(65, y - 2, ch_num)
        c.setFillColor(colors["text"])
        c.setFont("Helvetica", 10)
        c.drawString(150, y - 2, ch_title)
        c.drawRightString(page_w - 65, y - 2, str(pg))
        y -= 35

    draw_footer(c, page_w, colors["primary"], "The Calm Mind Ebook", 1)
    c.showPage()

    # === CHAPTER PAGES ===
    chapter_content = {
        "Understanding Anxiety": [
            "Anxiety is not your enemy. It is your brain's built-in alarm system,",
            "designed to keep you safe. The problem arises when this alarm becomes",
            "too sensitive, triggering at perceived threats rather than real ones.",
            "",
            "What Happens in Your Brain:",
            "",
            "When you feel anxious, your amygdala (the brain's fear center) activates",
            "your fight-or-flight response. This releases cortisol and adrenaline,",
            "causing physical symptoms like rapid heartbeat, sweating, and tension.",
            "",
            "The good news? Your prefrontal cortex (the rational brain) can learn",
            "to regulate this response. That's exactly what this book teaches you.",
            "",
            "Types of Everyday Anxiety:",
            "",
            "  Generalized worry about the future",
            "  Social anxiety in interactions",
            "  Performance anxiety at work or school",
            "  Health-related anxiety",
            "  Decision-making paralysis",
            "",
            "Key Insight: Anxiety is a signal, not a sentence. Learning to interpret",
            "it rather than fear it is the first step to calm.",
        ],
        "The Science of Calm": [
            "Your nervous system has two modes: sympathetic (fight-or-flight) and",
            "parasympathetic (rest-and-digest). Chronic anxiety keeps you locked",
            "in sympathetic mode. The techniques in this book activate your",
            "parasympathetic system.",
            "",
            "The Vagus Nerve: Your Calm Superhighway",
            "",
            "The vagus nerve runs from your brain to your gut and controls your",
            "relaxation response. You can directly stimulate it through:",
            "",
            "  Deep, slow breathing (especially extended exhales)",
            "  Cold water on your face or neck",
            "  Humming or chanting",
            "  Gentle movement like yoga",
            "",
            "Neuroplasticity: Rewiring Your Brain",
            "",
            "Every time you practice a calming technique, you strengthen the neural",
            "pathways associated with calm. Over time, calm becomes your default",
            "state rather than something you have to work to achieve.",
            "",
            "Research shows that consistent mindfulness practice for just 8 weeks",
            "can physically shrink the amygdala and thicken the prefrontal cortex.",
        ],
        "Breathing Techniques": [
            "Breathing is the single most powerful tool you have for instant",
            "anxiety relief. Here are five evidence-based techniques:",
            "",
            "1. Box Breathing (4-4-4-4)",
            "   Inhale for 4 counts, hold for 4, exhale for 4, hold for 4.",
            "   Used by Navy SEALs for stress management.",
            "",
            "2. 4-7-8 Breathing",
            "   Inhale for 4 counts, hold for 7, exhale slowly for 8.",
            "   Activates the parasympathetic nervous system.",
            "",
            "3. Diaphragmatic Breathing",
            "   Place one hand on chest, one on belly. Breathe so only the",
            "   belly hand moves. Practice for 5-10 minutes.",
            "",
            "4. Alternate Nostril Breathing",
            "   Close right nostril, inhale left. Close left, exhale right.",
            "   Repeat alternating. Balances both brain hemispheres.",
            "",
            "5. Physiological Sigh",
            "   Double inhale through nose, long exhale through mouth.",
            "   Fastest known way to calm down (researched at Stanford).",
        ],
        "Cognitive Reframing": [
            "Your thoughts create your feelings. Cognitive reframing is the skill",
            "of identifying unhelpful thought patterns and replacing them with",
            "more balanced, realistic ones.",
            "",
            "Common Thinking Traps:",
            "",
            "  Catastrophizing: 'This will definitely go wrong'",
            "  Mind Reading: 'Everyone thinks I'm incompetent'",
            "  All-or-Nothing: 'If it's not perfect, it's a failure'",
            "  Fortune Telling: 'I know this will end badly'",
            "  Emotional Reasoning: 'I feel anxious, so danger must be real'",
            "",
            "The ABCDE Method:",
            "",
            "  A - Activating Event: What happened?",
            "  B - Belief: What did you tell yourself?",
            "  C - Consequence: How did you feel/act?",
            "  D - Dispute: Is this belief accurate?",
            "  E - Effective New Belief: What's more realistic?",
            "",
            "Practice this daily and watch your anxiety patterns shift.",
            "It typically takes 3-4 weeks of consistent practice to notice change.",
        ],
        "Power of Routine": [
            "When life feels chaotic, routine provides an anchor. A predictable",
            "morning and evening routine reduces decision fatigue and creates",
            "a sense of safety that directly counters anxiety.",
            "",
            "Why Routines Reduce Anxiety:",
            "",
            "  They reduce the number of decisions you make daily",
            "  They give you a sense of control",
            "  They build positive momentum",
            "  They create neural pathways for automatic calm behaviors",
            "",
            "Building Your Ideal Morning Routine:",
            "",
            "  Start with just 3 elements (e.g., hydrate, breathe, set intention)",
            "  Keep it under 30 minutes initially",
            "  Do it before checking your phone",
            "  Track your consistency, not perfection",
            "",
            "Building Your Ideal Evening Routine:",
            "",
            "  Begin your wind-down 60-90 minutes before bed",
            "  Include a 'brain dump' to transfer worries to paper",
            "  Add gentle movement or stretching",
            "  Practice gratitude reflection",
            "  Keep screens out of the bedroom",
        ],
        "Mindfulness for the Overwhelmed": [
            "Mindfulness doesn't mean sitting in silence for an hour. For anxious",
            "minds, that can feel impossible. Here's mindfulness that actually works",
            "for people who feel overwhelmed.",
            "",
            "Micro-Mindfulness (30 seconds each):",
            "",
            "  Feel your feet on the ground. Wiggle your toes.",
            "  Notice 3 colors in your environment.",
            "  Take one deep breath and really feel it.",
            "  Touch something textured and focus on the sensation.",
            "  Listen for the farthest sound you can hear.",
            "",
            "The 5-4-3-2-1 Grounding Technique:",
            "",
            "  Name 5 things you can see",
            "  Name 4 things you can touch",
            "  Name 3 things you can hear",
            "  Name 2 things you can smell",
            "  Name 1 thing you can taste",
            "",
            "Walking Meditation:",
            "  Walk slowly, feeling each foot contact the ground.",
            "  Match your breathing to your steps.",
            "  When your mind wanders, gently bring it back.",
            "  Even 5 minutes can shift your state.",
        ],
    }

    page_num = 2
    for ch_title, ch_lines in chapter_content.items():
        # Chapter title page
        c.setFillColor(colors["primary"])
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
        draw_circle_pattern(c, page_w, page_h, HexColor("#FFFFFF"), 10)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(page_w / 2, page_h / 2 + 20, ch_title)
        c.setStrokeColor(HexColor("#FFFFFF"))
        c.setLineWidth(1)
        c.line(page_w / 2 - 80, page_h / 2 - 5, page_w / 2 + 80, page_h / 2 - 5)
        c.showPage()
        page_num += 1

        # Content page
        c.setFillColor(colors["bg"])
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
        draw_header_bar(c, page_w, page_h, colors["primary"], 45)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(page_w / 2, page_h - 32, ch_title)

        y = page_h - 75
        for line in ch_lines:
            if not line:
                y -= 10
                continue
            if line.startswith("  "):
                c.setFont("Helvetica", 10)
                c.setFillColor(colors["text"])
            elif any(line.startswith(x) for x in ["1.", "2.", "3.", "4.", "5."]):
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(colors["primary"])
            elif ":" in line and len(line) < 50:
                c.setFont("Helvetica-Bold", 11)
                c.setFillColor(colors["primary"])
            else:
                c.setFont("Helvetica", 10)
                c.setFillColor(colors["text"])
            c.drawString(60, y, line)
            y -= 16

        draw_footer(c, page_w, colors["primary"], "The Calm Mind Ebook", page_num)
        c.showPage()
        page_num += 1

    c.save()
    return filepath


def generate_workbook():
    """Generate the Weekly Reflection Workbook."""
    filepath = str(OUTPUT_DIR / "weekly_reflection_workbook.pdf")
    colors = COLORS["workbook"]
    page_w, page_h = letter
    c = canvas.Canvas(filepath, pagesize=letter)

    # === COVER ===
    c.setFillColor(colors["primary"])
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_circle_pattern(c, page_w, page_h, HexColor("#FFFFFF"), 25)

    card_w, card_h = 400, 480
    card_x = (page_w - card_w) / 2
    card_y = (page_h - card_h) / 2
    draw_rounded_rect(c, card_x, card_y, card_w, card_h, 20, fill_color=HexColor("#FFFFFF"))

    c.setFillColor(colors["primary"])
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(page_w / 2, card_y + card_h - 55, "THE CALM MIND COLLECTION")
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(page_w / 2, card_y + card_h - 100, "Weekly Reflection")
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(page_w / 2, card_y + card_h - 140, "Workbook")

    c.setStrokeColor(colors["secondary"])
    c.setLineWidth(2)
    c.line(card_x + 80, card_y + card_h - 160, card_x + card_w - 80, card_y + card_h - 160)

    c.setFillColor(colors["text"])
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w / 2, card_y + card_h - 190, "Check In, Reflect, Grow")
    c.drawCentredString(page_w / 2, card_y + card_h - 210, "12 Weeks of Guided Self-Discovery")

    c.showPage()

    # === WEEKLY PAGES (12 weeks) ===
    weekly_themes = [
        "Awareness", "Acceptance", "Gratitude", "Boundaries",
        "Self-Compassion", "Letting Go", "Connection", "Purpose",
        "Resilience", "Joy", "Growth", "Integration",
    ]

    for week in range(1, 13):
        theme = weekly_themes[week - 1]

        # Page 1: Review
        c.setFillColor(colors["bg"])
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

        draw_header_bar(c, page_w, page_h, colors["primary"], 55)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, page_h - 25, f"Week {week}: {theme}")
        c.setFont("Helvetica", 10)
        c.drawRightString(page_w - 30, page_h - 25, "Dates: ____/____ to ____/____")
        c.drawRightString(page_w - 30, page_h - 42, f"Theme: {theme}")

        y = page_h - 85

        # Weekly Wins
        draw_rounded_rect(c, 30, y - 90, (page_w - 70) / 2, 95, 10, fill_color=colors["light"])
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(45, y - 5, "This Week's Wins")
        c.setFont("Helvetica", 9)
        c.setFillColor(colors["text"])
        for i in range(4):
            c.drawString(45, y - 25 - i * 16, f"{i + 1}. _______________________________________")

        # Challenges
        right_x = 30 + (page_w - 70) / 2 + 10
        draw_rounded_rect(c, right_x, y - 90, (page_w - 70) / 2, 95, 10, fill_color=colors["light"])
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(right_x + 15, y - 5, "Challenges I Faced")
        c.setFont("Helvetica", 9)
        c.setFillColor(colors["text"])
        for i in range(4):
            c.drawString(right_x + 15, y - 25 - i * 16, f"{i + 1}. _______________________________________")
        y -= 110

        # Mood Overview
        draw_rounded_rect(c, 30, y - 55, page_w - 60, 60, 10, fill_color=HexColor("#FFFFFF"), stroke_color=colors["secondary"])
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(45, y - 5, "Weekly Mood Overview")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_w = (page_w - 140) / 7
        for i, d in enumerate(days):
            cx = 80 + i * day_w
            c.setFont("Helvetica", 8)
            c.setFillColor(colors["text"])
            c.drawCentredString(cx, y - 25, d)
            c.setStrokeColor(colors["secondary"])
            c.circle(cx, y - 40, 8, fill=0, stroke=1)
        y -= 75

        # Reflection Questions
        draw_rounded_rect(c, 30, y - 200, page_w - 60, 205, 10, fill_color=HexColor("#FFFFFF"), stroke_color=colors["primary"], stroke_width=1.5)
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(45, y - 5, f"Reflection: {theme}")

        questions = [
            f"How did the theme of '{theme.lower()}' show up in your week?",
            "What did you learn about yourself?",
            "What would you do differently?",
            "What are you carrying into next week?",
        ]
        q_y = y - 30
        for q in questions:
            c.setFont("Helvetica-Oblique", 9)
            c.setFillColor(colors["primary"])
            c.drawString(45, q_y, q)
            q_y -= 15
            c.setStrokeColor(colors["accent"])
            c.setLineWidth(0.3)
            for _ in range(2):
                c.line(45, q_y, page_w - 45, q_y)
                q_y -= 14
            q_y -= 5
        y -= 220

        # Next Week Intentions
        draw_rounded_rect(c, 30, y - 80, page_w - 60, 85, 10, fill_color=colors["light"])
        c.setFillColor(colors["primary"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(45, y - 5, "Next Week's Intentions")
        c.setFillColor(colors["text"])
        c.setFont("Helvetica", 9)
        c.drawString(45, y - 25, "Focus area: ________________________________________________")
        c.drawString(45, y - 43, "One thing to start: _________________________________________")
        c.drawString(45, y - 61, "One thing to stop: __________________________________________")

        draw_footer(c, page_w, colors["primary"], "Weekly Reflection Workbook", week)
        c.showPage()

    c.save()
    return filepath


def generate_exercise_cards():
    """Generate the Mindfulness & Breathing Exercise Cards."""
    filepath = str(OUTPUT_DIR / "mindfulness_breathing_cards.pdf")
    colors = COLORS["cards"]
    page_w, page_h = letter
    c = canvas.Canvas(filepath, pagesize=letter)

    # === COVER ===
    c.setFillColor(colors["primary"])
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_circle_pattern(c, page_w, page_h, HexColor("#FFFFFF"), 25)

    card_w, card_h = 400, 480
    card_x = (page_w - card_w) / 2
    card_y = (page_h - card_h) / 2
    draw_rounded_rect(c, card_x, card_y, card_w, card_h, 20, fill_color=HexColor("#FFFFFF"))

    c.setFillColor(colors["primary"])
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(page_w / 2, card_y + card_h - 55, "THE CALM MIND COLLECTION")
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(page_w / 2, card_y + card_h - 95, "Mindfulness &")
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(page_w / 2, card_y + card_h - 130, "Breathing Exercise")
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(page_w / 2, card_y + card_h - 165, "Cards")

    c.setStrokeColor(colors["secondary"])
    c.setLineWidth(2)
    c.line(card_x + 80, card_y + card_h - 185, card_x + card_w - 80, card_y + card_h - 185)

    c.setFillColor(colors["text"])
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w / 2, card_y + card_h - 215, "20 Printable Cards for Instant Calm")
    c.drawCentredString(page_w / 2, card_y + card_h - 235, "Cut, Keep & Practice Anywhere")

    c.showPage()

    # === EXERCISE CARDS (2 per page, 10 pages = 20 cards) ===
    exercises = [
        {
            "title": "Box Breathing",
            "duration": "4 minutes",
            "difficulty": "Beginner",
            "steps": ["Inhale slowly for 4 counts", "Hold your breath for 4 counts", "Exhale slowly for 4 counts", "Hold empty for 4 counts", "Repeat 4 times"],
            "tip": "Visualize tracing a square with each phase.",
        },
        {
            "title": "4-7-8 Relaxation",
            "duration": "3 minutes",
            "difficulty": "Beginner",
            "steps": ["Inhale through nose for 4 counts", "Hold your breath for 7 counts", "Exhale through mouth for 8 counts", "Repeat 3-4 times"],
            "tip": "Best used before sleep or during high stress.",
        },
        {
            "title": "Body Scan",
            "duration": "10 minutes",
            "difficulty": "Intermediate",
            "steps": ["Lie down comfortably", "Focus attention on your toes", "Slowly move focus up through body", "Notice tension without judging", "Release each area as you move up"],
            "tip": "If you fall asleep, that's perfectly okay!",
        },
        {
            "title": "5-4-3-2-1 Grounding",
            "duration": "5 minutes",
            "difficulty": "Beginner",
            "steps": ["Name 5 things you can SEE", "Name 4 things you can TOUCH", "Name 3 things you can HEAR", "Name 2 things you can SMELL", "Name 1 thing you can TASTE"],
            "tip": "Perfect for panic attacks or dissociation.",
        },
        {
            "title": "Physiological Sigh",
            "duration": "30 seconds",
            "difficulty": "Beginner",
            "steps": ["Take a quick inhale through nose", "Take a second smaller inhale on top", "Let out a long, slow exhale through mouth", "Repeat 2-3 times"],
            "tip": "Fastest evidence-based calming technique.",
        },
        {
            "title": "Alternate Nostril",
            "duration": "5 minutes",
            "difficulty": "Intermediate",
            "steps": ["Close right nostril with thumb", "Inhale through left nostril", "Close left nostril with ring finger", "Exhale through right nostril", "Inhale right, exhale left. Repeat."],
            "tip": "Balances both hemispheres of the brain.",
        },
        {
            "title": "Loving Kindness",
            "duration": "10 minutes",
            "difficulty": "Intermediate",
            "steps": ["Sit comfortably, close eyes", "Say: 'May I be happy, may I be safe'", "Extend to a loved one", "Extend to a neutral person", "Extend to all beings"],
            "tip": "Research shows it increases positive emotions.",
        },
        {
            "title": "Mindful Walking",
            "duration": "10 minutes",
            "difficulty": "Beginner",
            "steps": ["Walk slowly and deliberately", "Feel each foot contact the ground", "Notice heel, arch, toes", "Match breathing to steps", "When mind wanders, return to feet"],
            "tip": "Great for restless anxiety when sitting is hard.",
        },
        {
            "title": "Progressive Relaxation",
            "duration": "15 minutes",
            "difficulty": "Intermediate",
            "steps": ["Start with feet: tense for 5 sec", "Release and notice the difference", "Move to calves, thighs, abdomen", "Continue to shoulders, arms, face", "End with full body release"],
            "tip": "Perfect for physical tension from anxiety.",
        },
        {
            "title": "Counting Meditation",
            "duration": "5 minutes",
            "difficulty": "Beginner",
            "steps": ["Close eyes, breathe naturally", "Count '1' on your first exhale", "Count '2' on your second exhale", "Continue to 10, then restart", "If you lose count, begin at 1"],
            "tip": "Simple but powerful focus training.",
        },
        {
            "title": "Diaphragmatic Breathing",
            "duration": "5 minutes",
            "difficulty": "Beginner",
            "steps": ["Place one hand on chest", "Place other hand on belly", "Breathe so only belly hand moves", "Inhale for 4, exhale for 6", "Practice for 10 breaths"],
            "tip": "Activates your vagus nerve directly.",
        },
        {
            "title": "Thought Clouds",
            "duration": "5 minutes",
            "difficulty": "Intermediate",
            "steps": ["Close eyes and breathe", "Notice each thought as it arises", "Imagine placing it on a cloud", "Watch it drift away gently", "Return focus to breath"],
            "tip": "Builds skill of non-attachment to thoughts.",
        },
        {
            "title": "Gratitude Pause",
            "duration": "3 minutes",
            "difficulty": "Beginner",
            "steps": ["Stop whatever you're doing", "Take 3 deep breaths", "Name 3 things you're grateful for", "Feel each one in your body", "Carry that feeling forward"],
            "tip": "Shifts your nervous system from threat to safety.",
        },
        {
            "title": "Cold Exposure Reset",
            "duration": "1 minute",
            "difficulty": "Beginner",
            "steps": ["Splash cold water on face", "Or hold ice cubes in hands", "Focus on the sensation", "Breathe slowly through it", "Notice your heart rate slow down"],
            "tip": "Triggers the mammalian dive reflex for instant calm.",
        },
        {
            "title": "Sound Bath",
            "duration": "5 minutes",
            "difficulty": "Beginner",
            "steps": ["Sit or lie comfortably", "Close your eyes", "Listen for the farthest sound", "Layer in closer sounds", "Let sounds wash over you"],
            "tip": "Works anywhere: nature, office, even traffic.",
        },
        {
            "title": "Butterfly Hug",
            "duration": "2 minutes",
            "difficulty": "Beginner",
            "steps": ["Cross arms over chest", "Hands on opposite shoulders", "Alternately tap left, right", "Breathe slowly as you tap", "Continue for 25+ taps"],
            "tip": "Used in EMDR therapy for emotional regulation.",
        },
        {
            "title": "Humming Breath",
            "duration": "3 minutes",
            "difficulty": "Beginner",
            "steps": ["Inhale deeply through nose", "Exhale making 'hmmm' sound", "Feel the vibration in your chest", "Continue for 6-8 breaths", "Sit in the silence after"],
            "tip": "Stimulates the vagus nerve through vibration.",
        },
        {
            "title": "Mindful Eating",
            "duration": "5 minutes",
            "difficulty": "Beginner",
            "steps": ["Choose one small food item", "Look at it: color, shape, texture", "Smell it. Notice what happens", "Take one small bite, chew 20x", "Notice flavor, texture changes"],
            "tip": "Try with a raisin, piece of chocolate, or nut.",
        },
        {
            "title": "Safe Place Visualization",
            "duration": "5 minutes",
            "difficulty": "Intermediate",
            "steps": ["Close eyes, breathe deeply", "Imagine your safest, calmest place", "Add sensory details: sounds, smells", "Feel the safety in your body", "Return here whenever you need"],
            "tip": "Build this 'mental room' strong with practice.",
        },
        {
            "title": "Morning Intention Set",
            "duration": "2 minutes",
            "difficulty": "Beginner",
            "steps": ["Before getting out of bed", "Take 3 conscious breaths", "Set one intention for the day", "Visualize acting on that intention", "Rise with purpose"],
            "tip": "How you start your day shapes everything after.",
        },
    ]

    for i in range(0, len(exercises), 2):
        c.setFillColor(colors["bg"])
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

        # Two cards per page
        for j, card_idx in enumerate([i, i + 1]):
            if card_idx >= len(exercises):
                break
            ex = exercises[card_idx]

            card_y_start = page_h - 30 - j * (page_h / 2 - 15)
            card_height = page_h / 2 - 30

            # Card background
            draw_rounded_rect(c, 30, card_y_start - card_height, page_w - 60, card_height, 12, fill_color=HexColor("#FFFFFF"), stroke_color=colors["primary"], stroke_width=1.5)

            # Card number badge
            badge_x = 50
            badge_y = card_y_start - 25
            c.setFillColor(colors["primary"])
            c.circle(badge_x, badge_y, 15, fill=1, stroke=0)
            c.setFillColor(HexColor("#FFFFFF"))
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(badge_x, badge_y - 4, str(card_idx + 1))

            # Title
            c.setFillColor(colors["primary"])
            c.setFont("Helvetica-Bold", 16)
            c.drawString(75, badge_y - 5, ex["title"])

            # Duration & difficulty badges
            c.setFillColor(colors["light"])
            draw_rounded_rect(c, 75, badge_y - 28, 80, 18, 8, fill_color=colors["light"])
            c.setFillColor(colors["primary"])
            c.setFont("Helvetica", 8)
            c.drawCentredString(115, badge_y - 23, ex["duration"])

            draw_rounded_rect(c, 165, badge_y - 28, 80, 18, 8, fill_color=colors["light"])
            c.setFillColor(colors["secondary"])
            c.setFont("Helvetica", 8)
            c.drawCentredString(205, badge_y - 23, ex["difficulty"])

            # Steps
            step_y = badge_y - 50
            c.setFont("Helvetica", 9)
            for si, step in enumerate(ex["steps"]):
                c.setFillColor(colors["primary"])
                c.circle(55, step_y + 2, 3, fill=1, stroke=0)
                c.setFillColor(colors["text"])
                c.drawString(65, step_y - 2, step)
                step_y -= 16

            # Tip box
            tip_y = card_y_start - card_height + 20
            draw_rounded_rect(c, 45, tip_y, page_w - 90, 22, 6, fill_color=colors["light"])
            c.setFillColor(colors["primary"])
            c.setFont("Helvetica-Bold", 8)
            c.drawString(55, tip_y + 7, f"TIP: {ex['tip']}")

        # Cut line
        c.setStrokeColor(colors["accent"])
        c.setDash(6, 3)
        c.setLineWidth(0.5)
        c.line(30, page_h / 2, page_w - 30, page_h / 2)
        c.setDash()

        draw_footer(c, page_w, colors["primary"], "Mindfulness & Breathing Exercise Cards", i // 2 + 1)
        c.showPage()

    c.save()
    return filepath


def generate_all_pdfs():
    """Generate all PDFs and return file paths."""
    paths = {}
    paths["journal"] = generate_journal()
    paths["planner"] = generate_planner()
    paths["ebook"] = generate_ebook()
    paths["workbook"] = generate_workbook()
    paths["cards"] = generate_exercise_cards()
    return paths
