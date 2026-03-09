"""
Lead Magnet PDF Generator - 5 Emergency Calm Techniques
A free mini-PDF given in exchange for email signup
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "pdfs"


def draw_rounded_rect(c, x, y, w, h, r, fill_color=None, stroke_color=None, stroke_width=1):
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


def draw_circle_pattern(c, page_w, page_h, color, count=15):
    import random
    random.seed(99)
    c.saveState()
    for _ in range(count):
        x = random.uniform(0, page_w)
        y = random.uniform(0, page_h)
        r = random.uniform(3, 20)
        opacity = random.uniform(0.03, 0.08)
        c.setFillColor(Color(color.red, color.green, color.blue, opacity))
        c.circle(x, y, r, fill=1, stroke=0)
    c.restoreState()


def generate_lead_magnet():
    """Generate the free 5 Emergency Calm Techniques mini-PDF."""
    filepath = str(OUTPUT_DIR / "5_emergency_calm_techniques.pdf")
    page_w, page_h = letter
    primary = HexColor("#3A5A40")
    accent = HexColor("#E76F51")
    secondary = HexColor("#E9C46A")
    bg = HexColor("#FDFCF8")
    text_color = HexColor("#1A1A1A")
    muted = HexColor("#5C5C5C")

    c = canvas.Canvas(filepath, pagesize=letter)

    # === COVER PAGE ===
    c.setFillColor(primary)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_circle_pattern(c, page_w, page_h, HexColor("#FFFFFF"), 30)

    card_w, card_h = 420, 520
    card_x = (page_w - card_w) / 2
    card_y = (page_h - card_h) / 2
    draw_rounded_rect(c, card_x, card_y, card_w, card_h, 24, fill_color=HexColor("#FFFFFF"))

    # Free badge
    draw_rounded_rect(c, page_w / 2 - 30, card_y + card_h - 45, 60, 24, 12, fill_color=accent)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(page_w / 2, card_y + card_h - 38, "FREE")

    c.setFillColor(primary)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(page_w / 2, card_y + card_h - 75, "THE CALM MIND COLLECTION")

    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(page_w / 2, card_y + card_h - 120, "5 Emergency")
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(page_w / 2, card_y + card_h - 160, "Calm Techniques")

    c.setStrokeColor(secondary)
    c.setLineWidth(2)
    c.line(card_x + 80, card_y + card_h - 180, card_x + card_w - 80, card_y + card_h - 180)

    c.setFillColor(muted)
    c.setFont("Helvetica", 13)
    c.drawCentredString(page_w / 2, card_y + card_h - 210, "Instant Relief When You Need It Most")
    c.drawCentredString(page_w / 2, card_y + card_h - 230, "Science-Backed Methods That Work in Under 2 Minutes")

    # Decorative dots
    c.setFillColor(secondary)
    for i in range(5):
        c.circle(page_w / 2 - 40 + i * 20, card_y + 90, 4 + (i == 2) * 2, fill=1, stroke=0)

    c.setFillColor(muted)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w / 2, card_y + 50, "Your Quick-Reference Guide to Calm")
    c.drawCentredString(page_w / 2, card_y + 35, "thecalmmindcollection.com")

    c.showPage()

    # === INTRO PAGE ===
    c.setFillColor(bg)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Header bar
    c.setFillColor(primary)
    c.rect(0, page_h - 55, page_w, 55, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w / 2, page_h - 38, "When Anxiety Hits, Use These 5 Techniques")

    y = page_h - 95
    c.setFillColor(text_color)
    c.setFont("Helvetica", 11)
    intro_lines = [
        "You know that feeling. Your heart races. Your thoughts spiral.",
        "You can't focus. Everything feels overwhelming.",
        "",
        "These 5 techniques are your emergency toolkit. Each one takes",
        "less than 2 minutes and is backed by neuroscience research.",
        "",
        "Keep this guide on your phone, print it for your desk, or",
        "save it wherever you'll need it most.",
        "",
        "The goal isn't to eliminate anxiety. It's to have tools ready",
        "so anxiety doesn't control your next moment.",
    ]
    for line in intro_lines:
        if not line:
            y -= 8
            continue
        c.drawString(60, y, line)
        y -= 20

    # Quick reference box
    y -= 20
    draw_rounded_rect(c, 50, y - 130, page_w - 100, 140, 12, fill_color=HexColor("#F0F7F0"), stroke_color=primary, stroke_width=1)
    c.setFillColor(primary)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(70, y - 10, "Quick Reference - Which Technique When?")
    c.setFont("Helvetica", 10)
    c.setFillColor(text_color)
    situations = [
        ("Panic attack or sudden overwhelm", "Technique 1: Physiological Sigh"),
        ("Racing, spiraling thoughts", "Technique 2: 5-4-3-2-1 Grounding"),
        ("Physical tension and tightness", "Technique 3: Butterfly Hug"),
        ("Pre-meeting or social anxiety", "Technique 4: Box Breathing"),
        ("Nighttime anxiety or insomnia", "Technique 5: 4-7-8 Sleep Breath"),
    ]
    sy = y - 35
    for situation, technique in situations:
        c.setFillColor(muted)
        c.setFont("Helvetica", 9)
        c.drawString(70, sy, situation)
        c.setFillColor(primary)
        c.setFont("Helvetica-Bold", 9)
        c.drawRightString(page_w - 70, sy, technique)
        sy -= 18

    # Footer
    c.setFillColor(Color(primary.red, primary.green, primary.blue, 0.15))
    c.rect(0, 0, page_w, 30, fill=1, stroke=0)
    c.setFillColor(primary)
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w / 2, 12, "5 Emergency Calm Techniques  |  The Calm Mind Collection  |  Page 1")

    c.showPage()

    # === 5 TECHNIQUE PAGES ===
    techniques = [
        {
            "number": 1,
            "title": "The Physiological Sigh",
            "time": "30 seconds",
            "when": "Panic attacks, sudden overwhelm, acute stress",
            "science": "Discovered by Stanford neuroscientist Dr. Andrew Huberman. This is the fastest known way to activate your parasympathetic nervous system. The double inhale reinflates collapsed lung sacs (alveoli), maximizing CO2 offloading on the exhale.",
            "steps": [
                "Take a quick, sharp inhale through your nose",
                "Immediately take a second, smaller inhale on top of the first (don't exhale yet)",
                "Now release a long, slow, extended exhale through your mouth",
                "Repeat 2-3 times. That's it.",
            ],
            "pro_tips": [
                "You can do this with your eyes open, in public, without anyone noticing",
                "The exhale should be at least twice as long as both inhales combined",
                "Your body does this naturally when you sob - you're just doing it on purpose",
            ],
            "color": primary,
        },
        {
            "number": 2,
            "title": "5-4-3-2-1 Grounding",
            "time": "60-90 seconds",
            "when": "Dissociation, racing thoughts, feeling 'unreal'",
            "science": "This technique works by forcing your brain to shift from the amygdala (threat center) to the sensory cortex (present-moment processing). By naming sensory experiences, you literally redirect neural activity away from the anxiety loop.",
            "steps": [
                "Name 5 things you can SEE (look for small details: a shadow, a texture)",
                "Name 4 things you can physically TOUCH (feel the texture, temperature)",
                "Name 3 things you can HEAR (even subtle sounds: air conditioning, birds)",
                "Name 2 things you can SMELL (or recall a scent you love)",
                "Name 1 thing you can TASTE (or take a sip of water mindfully)",
            ],
            "pro_tips": [
                "Say each item out loud if possible - engaging your voice adds a grounding layer",
                "Try to notice things you wouldn't normally pay attention to",
                "If you can't smell anything, touch your lip - the tactile sensation helps",
            ],
            "color": HexColor("#2A9D8F"),
        },
        {
            "number": 3,
            "title": "The Butterfly Hug",
            "time": "60 seconds",
            "when": "Emotional overwhelm, feeling unsafe, PTSD triggers",
            "science": "Originally developed for EMDR (Eye Movement Desensitization and Reprocessing) therapy. The bilateral stimulation from alternating taps activates both brain hemispheres, which helps process emotional distress and creates a sense of safety.",
            "steps": [
                "Cross your arms over your chest, placing each hand on the opposite shoulder",
                "Begin alternating taps: left hand taps right shoulder, then right hand taps left",
                "Tap at a slow, steady rhythm (about 1 tap per second per side)",
                "Breathe slowly and naturally as you tap. Close your eyes if comfortable.",
                "Continue for 25-30 taps (about 1 minute). Notice how your body calms.",
            ],
            "pro_tips": [
                "The rhythm matters more than the force - keep it gentle and steady",
                "You can do this sitting at your desk, in bed, or even standing",
                "Pair with a calming phrase: 'I am safe. This will pass.'",
            ],
            "color": HexColor("#6366F1"),
        },
        {
            "number": 4,
            "title": "Box Breathing",
            "time": "90 seconds",
            "when": "Pre-meeting anxiety, performance stress, need to focus",
            "science": "Used by Navy SEALs and first responders. The equal timing of each phase (inhale, hold, exhale, hold) activates the vagus nerve and signals safety to your brain. The hold phases prevent hyperventilation and normalize CO2 levels.",
            "steps": [
                "Inhale slowly through your nose for 4 counts",
                "Hold your breath gently for 4 counts (no straining)",
                "Exhale slowly through your mouth for 4 counts",
                "Hold empty for 4 counts",
                "Repeat for 4 rounds (about 90 seconds total)",
            ],
            "pro_tips": [
                "Visualize tracing a square: up (inhale), across (hold), down (exhale), across (hold)",
                "If 4 counts feels too long, start with 3. The equal timing is what matters.",
                "Can be done with eyes open during a stressful meeting without anyone knowing",
            ],
            "color": secondary,
        },
        {
            "number": 5,
            "title": "The 4-7-8 Sleep Breath",
            "time": "90 seconds",
            "when": "Nighttime anxiety, insomnia, can't stop thinking",
            "science": "Developed by Dr. Andrew Weil based on ancient pranayama breathing. The extended hold and extra-long exhale maximally activate the parasympathetic nervous system. Called 'a natural tranquilizer for the nervous system.' Regular practice makes it more powerful over time.",
            "steps": [
                "Place the tip of your tongue behind your upper front teeth",
                "Exhale completely through your mouth (making a whoosh sound)",
                "Close your mouth and inhale through your nose for 4 counts",
                "Hold your breath for 7 counts",
                "Exhale completely through your mouth for 8 counts (whoosh)",
                "Repeat for 3-4 cycles. Do not exceed 4 cycles when starting.",
            ],
            "pro_tips": [
                "The exhale 'whoosh' is important - let your lips vibrate slightly",
                "Don't worry about exact seconds - the RATIO (4:7:8) matters more",
                "Practice this every night for 2 weeks and it becomes dramatically more effective",
            ],
            "color": accent,
        },
    ]

    for tech in techniques:
        c.setFillColor(bg)
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

        # Header
        c.setFillColor(tech["color"])
        c.rect(0, page_h - 70, page_w, 70, fill=1, stroke=0)

        # Number circle
        c.setFillColor(HexColor("#FFFFFF"))
        c.circle(55, page_h - 35, 20, fill=1, stroke=0)
        c.setFillColor(tech["color"])
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(55, page_h - 42, str(tech["number"]))

        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 20)
        c.drawString(85, page_h - 35, tech["title"])
        c.setFont("Helvetica", 10)
        c.drawString(85, page_h - 55, f"Time: {tech['time']}  |  Best for: {tech['when']}")

        y = page_h - 100

        # Science section
        draw_rounded_rect(c, 40, y - 70, page_w - 80, 75, 10, fill_color=HexColor("#F0F7F0"))
        c.setFillColor(primary)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(55, y - 5, "THE SCIENCE")
        c.setFont("Helvetica", 9)
        c.setFillColor(text_color)

        # Word wrap science text
        words = tech["science"].split()
        line = ""
        sy = y - 22
        for word in words:
            test = line + " " + word if line else word
            if c.stringWidth(test, "Helvetica", 9) > page_w - 120:
                c.drawString(55, sy, line)
                line = word
                sy -= 14
            else:
                line = test
        if line:
            c.drawString(55, sy, line)

        y -= 95

        # Steps
        draw_rounded_rect(c, 40, y - 15 - len(tech["steps"]) * 45, page_w - 80, 25 + len(tech["steps"]) * 45, 10, fill_color=HexColor("#FFFFFF"), stroke_color=tech["color"], stroke_width=1.5)
        c.setFillColor(tech["color"])
        c.setFont("Helvetica-Bold", 12)
        c.drawString(55, y - 5, "STEPS")

        sy = y - 30
        for i, step in enumerate(tech["steps"]):
            # Step number
            c.setFillColor(tech["color"])
            c.circle(65, sy + 3, 10, fill=1, stroke=0)
            c.setFillColor(HexColor("#FFFFFF"))
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(65, sy, str(i + 1))

            c.setFillColor(text_color)
            c.setFont("Helvetica", 10)

            # Word wrap step
            words = step.split()
            line = ""
            for word in words:
                test = line + " " + word if line else word
                if c.stringWidth(test, "Helvetica", 10) > page_w - 160:
                    c.drawString(85, sy, line)
                    line = word
                    sy -= 16
                else:
                    line = test
            if line:
                c.drawString(85, sy, line)
            sy -= 30

        y = sy - 10

        # Pro Tips
        draw_rounded_rect(c, 40, y - 15 - len(tech["pro_tips"]) * 28, page_w - 80, 25 + len(tech["pro_tips"]) * 28, 10, fill_color=HexColor("#FFFBF0"))
        c.setFillColor(HexColor("#854d0e"))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(55, y - 5, "PRO TIPS")

        sy = y - 25
        c.setFont("Helvetica", 9)
        c.setFillColor(muted)
        for tip in tech["pro_tips"]:
            c.setFillColor(secondary)
            c.circle(60, sy + 2, 3, fill=1, stroke=0)
            c.setFillColor(muted)
            words = tip.split()
            line = ""
            for word in words:
                test = line + " " + word if line else word
                if c.stringWidth(test, "Helvetica", 9) > page_w - 140:
                    c.drawString(72, sy, line)
                    line = word
                    sy -= 14
                else:
                    line = test
            if line:
                c.drawString(72, sy, line)
            sy -= 18

        # Footer
        c.setFillColor(Color(tech["color"].red, tech["color"].green, tech["color"].blue, 0.15))
        c.rect(0, 0, page_w, 30, fill=1, stroke=0)
        c.setFillColor(tech["color"])
        c.setFont("Helvetica", 8)
        c.drawCentredString(page_w / 2, 12, f"Technique {tech['number']}: {tech['title']}  |  The Calm Mind Collection  |  Page {tech['number'] + 1}")

        c.showPage()

    # === FINAL PAGE - CTA ===
    c.setFillColor(primary)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_circle_pattern(c, page_w, page_h, HexColor("#FFFFFF"), 25)

    card_w, card_h = 420, 400
    card_x = (page_w - card_w) / 2
    card_y = (page_h - card_h) / 2
    draw_rounded_rect(c, card_x, card_y, card_w, card_h, 24, fill_color=HexColor("#FFFFFF"))

    c.setFillColor(primary)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(page_w / 2, card_y + card_h - 55, "Want to Go Deeper?")

    c.setFillColor(muted)
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w / 2, card_y + card_h - 85, "These 5 techniques are just the beginning.")
    c.drawCentredString(page_w / 2, card_y + card_h - 105, "The full Calm Mind Collection includes:")

    items = [
        "90-Day Anxiety Relief Journal (90 daily prompts)",
        "Morning & Evening Routine Planner (30 days)",
        "The Calm Mind Ebook (complete anxiety guide)",
        "Weekly Reflection Workbook (12 weeks)",
        "20 Mindfulness & Breathing Exercise Cards",
    ]
    y = card_y + card_h - 140
    for item in items:
        c.setFillColor(primary)
        c.circle(card_x + 40, y + 2, 4, fill=1, stroke=0)
        c.setFillColor(text_color)
        c.setFont("Helvetica", 11)
        c.drawString(card_x + 55, y - 2, item)
        y -= 22

    y -= 15
    draw_rounded_rect(c, card_x + 30, y - 30, card_w - 60, 35, 8, fill_color=accent)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w / 2, y - 18, "Get the Full Bundle - Save 46%")

    c.setFillColor(muted)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w / 2, card_y + 40, "Visit thecalmmindcollection.com")

    c.showPage()
    c.save()
    return filepath
