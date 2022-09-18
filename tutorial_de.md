# openHAB statische Beispiele

## Motivation

In openHAB werden Items in der Regel gebunden erstellt. Dies bedeutet, dass es meist ein physikalisch existierendes Gerät gibt. Über ein entsprechendes Binding wird zu diesem Gerät (manchmal sind es aber auch irgendwelche Online-Konten), dann ein Thing erstellt. Dieses Thing ermöglicht es über Channels dann entsprechende Items zu erstellen, die in openHAB zur Bedienung des Geräts genutzt werden können.

Lösgelöst von irgendwelchen Geräte, Bindings, Things oder Channels ist es möglich sogenannte [ungebundene Items](https://community.openhab.org/t/design-pattern-unbound-item-aka-virtual-item/15993) zu erstellen, welche man auch als virtuelle Items bezeichnen kann. Anwendungsbeispiele gibt es hierfür verschiedene. Man kann bspw. ein Switch-Item erstellen, dass nur eine Regel triggert, die dann mehrere Geräte bedienen würde.

Ziel dieses Tutorial ist es, ein Beispiel zu liefern, wie man unabhängig von Things zu jedem [Item Type](https://www.openhab.org/docs/configuration/items.html#type) ein Beispiel zu erzeugen. Dies soll die Funktionsweise einzelner Items und von openHAB näher bringen. Wir reden hier von statischen Beispielen, weil durch Regeln jedes dieser Beispiele einen Wert zugewiesen bekommen soll.

Anmerkung: Ich nutze solche Hello World Beispiele gerne bei der Entwicklung von verschiedenen Programmen, wie bspw. einen MQTT Event Bus, eine Bridge zwischen openHAB und ROS, ein CRUD über die REST API oder ein SSE Client für Item Events über die REST API und vielem mehr.

## Das Hello World Problem

In vielen Programmiersprachen gibt es ein Beispiel für Hello World. An diesem Beispiel werden die typischen Charakteristika dieser Programmiersprache festgehalten. Ich zeige mal ein Beispiel auf, wie man für Java ein solches Programm erstellen könnte, da openHAB in Java geschrieben ist:

```
public class HelloWorld 
{
 
       public static void main (String[] args)
       {
             String hello = "Hello World!"
             System.out.println(hello);
       }
}
```

Ich habe in diesem Hello World Beispiel die Ausgabe des Strings `"Hello World!"` leicht angepasst, sodass dieser String vorher in einer Variablen gespeichert wird. Denn genau dass ist, was in openHAB so nicht gemacht werden kann. Die Items werden fälschlicherweise oft als Variablen verstanden. Genauer genommen sind Items dann aber Objekte. Das wohl entscheidenste Attribut für die Wertzuweisung ist `state`. Wird ein Item-Objekt erzeugt, kann ich allerdings die Wertzuweisung für `state` nicht vornehmen. Andere Attribute wie `name`, `label` oder `icon` kann ich setzen. Oder auch ein Item einer Group zu ordnen, was wiederum ein anderes Item ist.

Was heißt dies konkret? Es gilt die folgende [Syntax](https://www.openhab.org/docs/configuration/items.html#item-definition-and-syntax) für die Item-Definition:

```
itemtype itemname "labeltext [stateformat]" <iconname> (group1, group2, ...) ["tag1", "tag2", ...] {bindingconfig}
```

Wenn ich mein Beispiel von oben aus dem Java-Programm nehmen würde, dann kann ich maximal ein

```
String hello "[%s]"
```

daraus machen. Eine Wertzuweisung wie

```
String hello="Hello World!" "[%s]"
```

oder

```
String hello state="Hello World!" "[%s]"
```

oder wie auch immer diese dann aussehen müsste, ist nicht möglich.

Im Übrigen erkennt man anhand von `{bindingconfig}` dann, ob ein Item gebunden ist oder nicht. In den `{}` müsste entweder auf ein `Binding` direkt oder auf ein `Channel` eines `Things` zugegriffen werden. Bei einem `ungebundenem Item` entfällt dies vollständig.

Das Problem von Hello World zeigt aber nicht nur auf, dass viele eine Art Wertzuweisung suchen, sondern auch eine Ausgabe. Um openHAB mal vereinfacht darzustellen:

| Art | 	Beschreibung | 	Wodurch |  Wo |
| :--: |:-------------:| :-----:| :-----:|
| Objektinstanziierung | Um ein `Item` zu erstellen, muss dieses Objekt erst einmal erzeugt werden. Ähnlich wie in der klassischen Programmierung kann man verschiedene Werte (`name`, `label`, `icon`, ...) an den Konstruktor übergeben. | `Items` | `main UI`, `.items`-Datei oder über die `REST API` |
| Wertzuweisung von Attributen | Unter Attribute nenne ich alle Attribute außer `state`. Klassischerweise werden viele Attribute bei der Erstellung des `Items` bereits gesetzt. Für die Anzeige in der `UI` durch `Sitemaps`, kann ich aber bspw. Attribute wie `label` oder `icon` überschreiben. Wahlweise kann ich auch über `Rules` zum Beispiel ein Attribut wie `label` überschreiben. | `Items`, `Sitemaps`, `Rules` | `main UI`, `.items`-Datei oder über die `REST API`, sowie in der `.sitemaps`-Datei oder in `.rules`-Dateien |
| Wertzuweisung von States | Im Normalfall wird der `State` durch ein `Thing` bzw. dessen `Channel` gesetzt, sobald ein Gerät bedient wird. Auch ein `Event` in openHAB (wie zum Beispiel das Bedienen eines UI-Elements) verändert den `State`. `Events` können aber auch genutzt werden, damit eine `Rule` getriggert wird. Über `sendCommand` oder `postUpdate` können in `Rules` ebenfalls Wertzuweisungen von `States` stattfinden. | `Things`, `Sitemaps`, `Rules` |  `main UI`, `.things`-Datei oder über die `REST API`, sowie in der `.sitemaps`-Datei oder in `.rules`-Dateien |
| Ausgabe | Eine Ausgabe von `Items` erfolgt in der UI. Klassischerweise nur in `Sitemaps`. Theoretisch gibt es noch eine Ausgabe in der `Karaf Konsole` und durch `Rules` könnte man zusätzlich die `Items` loggen. `Events` zu den `Items` werden automatisch geloggt. | `Sitemaps`, `Karaf Konsole` |  `main UI`, `.sitemaps`-Datei oder über die `REST API`, sowie in der `Karaf Konsole`. |

Wir beschränken uns daher darauf, dass wir in einer `.items`-Datei ein `Item`-Objekt instanziieren, in einer `.rules`-Datei dann die Werte von `States` zuweisen und durch eine `.sitemaps`-Datei deren Ausgabe definieren.

## Objektinstanziierung

### Group

### Color

### Contact

### DateTime

### Dimmer

### Image

### Location

### Number

### Player

### Rollershutter

### String

### Switch

### Gesamte Items

## Wertzuweisung von States

### Color

### Contact

### DateTime

### Dimmer

### Image

### Location

### Number

### Player

### Rollershutter

### String

### Switch

### Gesamte Rules

## Ausgabe

### Group

### Color

### Contact

### DateTime

### Dimmer

### Image

### Location

### Number

### Player

### Rollershutter

### String

### Switch

### Gesamte Sitemaps

## Zusatz: Wertveränderung

Um die `States` zu verändern kann man neben der Bedienung der Elemente in der `Sitemap` auch eine weitere `Rule` schreiben. Damit ich meine "Anwendungen" testen kann, habe ich mich für eine `Rule` mit einem `Cron trigger` von einer Minute entschieden.
