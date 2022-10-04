""" Snake-Spiel aus dem Kurs "Programmieren lernen mit Python" von openHPI
    https://open.hpi.de/courses/pythonjunior2020
"""

import turtle
import random
import time




def erstelle_turtle(x, y, rotationswinkel, shape="triangle", color="green"):
    element = turtle.Turtle()
    element.speed(0)  # Keine Animation, Turtle "springt" zum Zielpunkt
    element.shape(shape)
    element.color(color)
    element.right(rotationswinkel)  # Nur für grüne Steuerungsdreiecke relevant
    element.penup()
    element.goto(x, y)

   
    element.direction = "stop"

    return element


def nach_unten_ausrichten():
    if kopf.direction != "up":
        kopf.direction = "down"


def nach_rechts_ausrichten():
    if kopf.direction != "left":
        kopf.direction = "right"


def nach_links_ausrichten():
    if kopf.direction != "right":
        kopf.direction = "left"


def nach_oben_ausrichten():
    if kopf.direction != "down":
        kopf.direction = "up"


def interpretiere_eingabe(x, y):
    if x >= 150 and x <= 170 and y >= -190 and y <= -170:
        # Kürzer: 150 <= x <= 170 and -190 <= y <= -170
        nach_unten_ausrichten()
    elif x >= 170 and x <= 190 and y >= -170 and y <= -150:
        # Kürzer: 170 <= x <= 190 and -170 <= y <= -150
        nach_rechts_ausrichten()
    elif (x >= 130 and x <= 150 and y >= -170 and y <= -150):
        nach_links_ausrichten()
    elif (x >= 150 and x <= 170 and y >= -150 and y <= -130):
        nach_oben_ausrichten()


def kopf_bewegen():
    if kopf.direction == "down":
        y = kopf.ycor()
        kopf.sety(y - 20)

    if kopf.direction == "right":
        x = kopf.xcor()
        kopf.setx(x + 20)

    if kopf.direction == "up":
        y = kopf.ycor()
        kopf.sety(y + 20)
		
    if kopf.direction == "left":
        x = kopf.xcor()
        kopf.setx(x - 20)



def koerper_bewegen():
    # Alternativ kann auch nur das letzte Element auf die Position des
    # Kopfes bewegt werden und die restlichen Segmente bleiben unverändert.
    for index in range(len(segmente) - 1, 0, -1):
        x = segmente[index-1].xcor()
        y = segmente[index-1].ycor()
        segmente[index].goto(x, y)
    if len(segmente) > 0:
        x = kopf.xcor()
        y = kopf.ycor()
        segmente[0].goto(x, y)


def segmente_entfernen():
    # Verstecke und entferne Segmente
    for segment in segmente:
        segment.hideturtle()
        del segment
    segmente.clear()


def spiel_neustarten():
    kopf.goto(0, 0)
    kopf.direction = "stop"
    segmente_entfernen()
    print("Spiel ist vorbei")


def checke_kollision_mit_fensterrand():
    if kopf.xcor() > 200 or kopf.xcor() < -200 or kopf.ycor() > 200 or kopf.ycor() < -200:
        spiel_neustarten()


def checke_kollision_mit_segmenten():
    for segment in segmente:
        if segment.distance(kopf) < 20:
            spiel_neustarten()


def checke_kollision_mit_essen():
    if kopf.distance(essen) < 20:
        newy = -140
        newx = 150
        while(newx >= 140 and newy <= -140):
            newx = random.randint(-9, 9)
            newy = random.randint(-9, 9)
            newy = newy * 20
            newx = newx * 20
			
        essen.goto(newx, newy)
        
        neues_segment = turtle.Turtle()
        neues_segment.shape("square")
        neues_segment.color("blue")
        neues_segment.speed(0)
        neues_segment.penup()
        segmente.append(neues_segment)


def wiederhole_spiellogik():
    # Damit das Spiel bis zu einer Niederlage läuft, wird der folgende
    # Code von wiederhole_spiellogik() in einer Endlosschleife aufgerufen
    while True:
        checke_kollision_mit_essen()
        checke_kollision_mit_fensterrand()

        koerper_bewegen()
        kopf_bewegen()
        checke_kollision_mit_segmenten()

        # Position der verschiedenen Turtle-Elemente aktualisieren
        turtle.update()

        # time.sleep() unterbricht die Ausführung des weiteren
        # Codes für die angegebene Anzahl an Sekunden
        # An dieser Stelle verlangsamt sleep() das Spiel, damit die Schlange
        # nicht aus dem Bildschirm laufen kann, bevor man sie sehen kann.
        time.sleep(0.15)


# Auf dem Spielfeld sichtbare Elemente definieren
rechts = erstelle_turtle(180, -160, 0)
unten = erstelle_turtle(160, -180, 90)
links = erstelle_turtle(140, -160, 180)
oben = erstelle_turtle(160, -140, -90)
essen = erstelle_turtle(0, 100, 0, "circle", "red")
kopf = erstelle_turtle(0, 0, 0, "square", "black")
segmente = []

# Spielbereich (das sich öffnende Fenster beim Ausführen dieser Datei) definieren
spielbereich = turtle.Screen()
spielbereich.title("Mein Snake-Spiel")
spielbereich.setup(width=440, height=440)
turtle.bgpic("image.png")

# Drücken der Pfeiltasten zur Richtungssteuerung registrieren
spielbereich.onkeypress(nach_oben_ausrichten, "Up")
spielbereich.onkeypress(nach_links_ausrichten, "Left")
spielbereich.onkeypress(nach_unten_ausrichten, "Down")
spielbereich.onkeypress(nach_rechts_ausrichten, "Right")
spielbereich.listen(0)

# Registrierung der Richtungssteuerung über das Anklicken der grünen Dreiecke
turtle.onscreenclick(interpretiere_eingabe)

# Turtle in der Mitte verbergen
turtle.hideturtle()

# Automatisches Aktualisieren der Turtle-Elemente ausschalten
turtle.tracer(False)

# Try-Except-Block fängt Beenden des Spiels ab
try:
    wiederhole_spiellogik()
except turtle.Terminator:
    print("Das Spiel wurde beendet.")
    # exit(0) beendet das Program sauber
    exit(0)
