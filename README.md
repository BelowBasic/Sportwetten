# Sportwetten

Erstellung einer Microservices-Architektur, die basierend auf einer einfach
gestalteten Webseite (Front-End) Sportwetten entgegennimmt. Eine
Sportwette besteht dabei aus einem Ereignis, einer Eintreffwahrscheinlichkeit,
einem Preis sowie einem Gewinn. Eine separater Preis-Server berechnet
aufgrund dieser Parameter unter Zuziehung von weiteren Werten (Historie von
diesen und ähnlichen Ereignissen, etc.) für jedes Ereignis einen
entsprechenden Preis, der dann via Webseite dargestellt wird. Beide
Komponenten kommunizieren über eine skalierbare Middleware, um
entsprechende Vervielfachung des Webseiten-Verkehrs abbilden zu können.


### Details:
 - Einfaches Frontend. bwin.de und tipico.de sind nicht über Nacht
entstanden. Falls ihr Live-Ereignisse modellieren wollt: Pluspunkt!
Andernfalls genügt eine einfach Modellierung wie z.B. Fußball-Toto.
 - Da Frontend und Preis-Server nur lose gekoppelt sind, um entsprechend
des Verkehrs “mitzuwachsen”: Welche Middleware skaliert am besten
und warum?
 - Wichtig: Welche geschäftlichen Anforderungen könnt ihr hier zugrunde
legen (z. B. Skalierung => die einzelnen Microservices laufen auf
unterschiedlichen Rechnern => ebenfalls höhere Ausfallsicherheit).
• Paketierung aller Komponenten in Containern, die auf einer OCI-
konformen Container-Runtime ausgeführt werden.

# Running the Application

Go to the Project directory and execute these two commands.

```
docker compose build
docker compose up -d
```

