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

oder wie auch immer diese dann aussehen müsste, ist nicht möglich!

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

Wie oben bereits beschrieben werden die Objekte der Items in einer `.items`-Datei erzeugt.

### Group

Wir wollen eine übergeordnete Gruppe, also ein `Group Item` erstellen. Ein `Item` vom Typ `Group` besitzt keinen `State`. Für eine einfache Handhabung muss eigentlich nur der Name dieser Gruppe angegeben werden:

```
Group Static
```

Es wäre auch möglich, dass diese `Group` einer anderen `Group` untergeordnet werden würde. Man kann auch ein `Label` oder ein `Icon` angeben.

### Color

Bei einem `Color Item` muss für ein minimalistisches Beispiel auch nur der Name dieses `Items` angegeben werden. Da wir jedoch zuvor bereits ein `Group Item` erstellt haben, wollen wir dieses `Item` unserer `Group` unterordnen. Dies machen wir auch bei allen weiteren `Items` später.

```
Color testColor (Static)
```

Auf `Label` und `Icon` kann in einem einfachen Beispiel verzichtet werden!

### Contact

Das nächste `Item`, dass wir erstellen wollen, ist ein `Contact Item`. Dieses `Item` gibt klassischerweise an, ob bspw. eine Türe `OPEN` oder `CLOSED` ist, wenn ein entsprechender Sensor verwendet werden würde. Für eine spätere Ausgabe in unserer `Sitemap` müssen wir hier ein `Label` setzen:

```
Contact testContact "[%s]" (Static)
```

Das `[%s]` fügt später den `State` des `Items` als `String` hinzu. Ohne diese Angabe wäre nicht sichtbar, ob ein `Contact Item` den `State` `CLOSED` oder `OPEN` besitzt. Man kann in den `Labels` auch allgemein irgendeinen `String` eintragen. Somit wäre auch ein Präfix oder Postfix denkbar. Das könnten z.B. Einheiten sein. Dies wird hier jedoch nicht benötigt. Der Grund, warum man den `State` zu einem `String` parsen muss liegt daran, dass `OPEN` und `CLOSED` von `openHAB` als eigene Datentypen behandelt wird, was später in den `Rules` eine Rolle spielen wird.

Auf ein `Icon` wird in diesem Beispiel verzichtet!

### DateTime

Bei einem `DateTime Item` wird das `Label` wiederum verwendet, damit man den `Zeitstempel` in ein gewünschtes Ausgabeformat formatiert. Dies wird daher benötigt, da man in verschiedenen Ländern auf verschiedener Art und Weise ein Datum oder eine Uhrzeit angibt. Auch ist es denkbar, dass man nur das Datum oder nur die Uhrzeit angibt. Im nachfolgenden Beispiel soll vom zuletzt erfassten Zeitstempel nur die Uhrzeit ausgegeben werden, d.h., es soll die Uhrzeit in Stunden und Minuten (`HH:MM`) ausgegeben werden:

```
DateTime testDateTime "[%1$tH:%1$tM]" (Static)
```

Der Zeitstempel bezieht sich auf die erfasste Zeit. Es kommt nun auf die `Rule` an, was als letzter Zeitstempel gilt. Hierzu wird später bei den `Rules` noch einmal mehr gesagt. Ein `DateTime Item` wird in verschiedener Weise eingesetzt. Meist gibt es irgendwelche Sensorwerte und das `DateTime Item` gibt dann an, wann das letzte Mal eine Änderung dieser Sensorwerte erfasst worden ist.

Auf ein `Icon` wird in diesem Beispiel verzichtet!

### Dimmer

Ein `Dimmer` wird klassischerweise eingesetzt, um irgendetwas zu dimmen. Man kennt dieses Beispiel am ehesten bei Lampen und deren Helligkeit. Typischerweise liegen hier die `States` zwischen `0` und `100`, was bei zuvor genannten Beispiel ganz dunkel oder ganz hell bedeuten würde. Dies ist eine Prozentangabe. Ein anderes Beispiel wäre vielleicht ein Lautstärkeregler. Das `Item` sind in einem rudimentärem Beispiel wie folgt aus:

```
Dimmer testDimmer (Static)
```

Auf `Label` und `Icon` kann in einem einfachen Beispiel verzichtet werden!

### Image

In `openHAB` wird ein `Image Item` dazu verwendet, dass man Bilder darstellen kann. Hierbei kann es sich um sämtliche Arten von Bilder handeln. Egal ob Formate wie `JPG`, `PNG`, ob es sich um Fotos bzw. Schnappschüsse handelt, einzelne Frames, Wallpaper oder meinetwegen ein Album Cover bei Musik. Was auch immer letztlich durch ein Bild dargestellt werden soll. Lediglich `GIF`s sind nicht möglich. Auch wäre ein Videostream nur theoretisch denkbar, in dem man hintereinander die Frames darstellt.

```
Image testImage (Static)
```

Auf `Label` und `Icon` kann in einem einfachen Beispiel verzichtet werden!

### Location

Mit einem `Location Item` soll irgendeine Art von Lokation dargestellt werden. Der `State` beinhaltet `GPS Koordinaten` mit Längengrad, Breitengrad und die Höhe. Anwendungsbeispiele gibt es verschiedene. Man könnte bspw. eine eigene Wetterstation verwenden und diese müsste erst konfiguriert werden oder erfassen, wo sie sich befindet. Vielleicht hat man auch einen Roboter (z.B. einen Rasenmähroboter), der `GPS` besitzt oder über ein `Binding` wäre das Fahrzeug mit dem Smart Home verknüpft und sobald man das Haus verlässt, werden die Fenster verriegelt.

```
Location testLocation "HS Furtwangen" <house>  (Static)
```

Wir wollen später beispielhaft die Koordinaten der Hochschule Furtwangen angeben. Daher benötigen wir das `Label` `HS Furtwangen`. Auf ein `Icon` kann verzichtet werden, aber da die Hochschule ein Gebäude ist, verwenden wir ein `house` als `Ìcon`.

### Number

Mit einem `Number Item` kann man jegliche Art von Zahlen darstellen. Für die Formatierung wird wieder ein `Label` benötigt. Zum Beispiel ist es wichtig, wie viele Kommastellen dargestellt werden sollen oder ob überhaupt eine dargestellt werden soll. Auch kann sich die Zahl ja auf irgendeine Einheit beziehen, wie bspw. `m`, `kmh` oder `°C`. Nachfolgend wollen wir eine Ganzzahl (`integer`) darstellen, was letzten Endes nichts anders wäre, als eine Fließkommazahl (`float`) ohne eine Nachkommastelle:

```
Number testNumber "[%.0f]" (Static)
```

Wie man sieht, wird `%` als Platzhalter für die Zahl verwendet und hinten dran definiert man dann den Datentyp wie z.B. `float` mit `f` und die Nachkommastellen (hier: `0`). Eine Temperatur in Grad Celsius könnte man mit `"[%.2f °C]"` angeben. Weitere Informationen zu [Einheiten](https://www.openhab.org/docs/concepts/units-of-measurement.html) findet man in der openHAB Dokumentation!

Auf ein `Icon` verzichten wir in diesem einfachen Beispiel

### Player

Ein `Item` vom Typ `Player` verwendet man bspw., wenn man Musik oder ein Video wiedergeben will. Man kann dieses Medium abspielen, pausieren, vorspulen oder zurückspulen. Ebenfalls ist es denkbar, dass das nächste oder vorherige Medium abgespielt werden würde.

```
Player testPlayer (Static)
```

Auf `Label` und `Icon` kann in einem einfachen Beispiel verzichtet werden!

### Rollershutter

Das `Rollershutter Item` wird nicht nur bei Rollläden, sondern gerne auch bei Markisen oder Jalousien verwendet. Letzten Endes funktionieren diese ja vom Prinzip nahezu gleich. Sie sind entweder eingefahren oder ausgefahren. Optional gibt es noch irgendwo einen Wert dazwischen, weil man das Ein- oder Ausfahren gestoppt hat.

```
Rollershutter testRollershutter (Static)
```

Auf `Label` und `Icon` kann in einem einfachen Beispiel verzichtet werden!

### String

Ein `String Item` macht genau dass, was man erwartet. Man übergibt irgendeine Art von Zeichenkette an dieses `Item`, folglich ist dieser `State` ein `String`. Prinzipiell kann man auch ein einzelnen `Character` bzw. `Char` wie ein `String` behandeln. Das `String Item` wird sehr vielseitig eingesetzt. Es kann der Titel eines Mediums sein, die letzte Nachricht eines News Feeds, ein gewählter Modus von einem Gerät und vieles mehr. `Strings` können auch wieder auf irgendeine verschieden denbkare Art formatiert werden. Um einen `String` voll anzuzeigen, muss man das `Label` auch entsprechend definieren:

```
String testString "[%s]" (Static)
```

Logischerweise könnte man auch Zahlenwert zu einem String konvertieren. Dann verwendet man aber ehrlicherweise eigentlich den falschen Datentyp.

Auf ein `Icon` kann in einem einfachen Beispiel verzichtet werden!

### Switch

Ich liebe ehrlicherweise das `Switch Item`! Es ist ein einfacher Schalter, der die `States` `ON` und `OFF` besitzt. Neben dem, ob ein Gerät eingeschalten ist, kann man darüber ja auch einzelne `Rules` aktivieren. Typischerweise werden so auch einzelne Funktionalitäten an einem Gerät aktiviert oder deaktiviert. Oder wer einen guten Stil bei Rule verwendet, der unterteilt diese gerne auch in mehrere Parts und regelt dies über mehrere `Switch Items` hintereinander.

```
Switch testSwitch (Static)
```

Auf `Label` und `Icon` kann in einem einfachen Beispiel verzichtet werden!

### Gesamte Items

Dies ergibt dann unsere `.items`-Datei, die wie folgt aussieht:

```
Group Static

Color testColor (Static)
Contact testContact "[%s]" (Static)
DateTime testDateTime "[%1$tH:%1$tM]" (Static)
Dimmer testDimmer (Static)
Image testImage (Static)
Location testLocation "HS Furtwangen" <house>  (Static)
Number testNumber "[%.0f]" (Static)
Player testPlayer (Static)
Rollershutter testRollershutter (Static)
String testString "[%s]" (Static)
Switch testSwitch (Static)
```

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

Daraus ergibt sich dann folgende `Rule`:

```
import java.util.Base64
import java.io.ByteArrayOutputStream
import java.net.URL

rule "Started"
when
    System started
then
    testColor.postUpdate("100, 100, 100")
    testContact.postUpdate(CLOSED)
    testDateTime.postUpdate(now.toLocalDateTime().toString())
    testDimmer.postUpdate(30)
    testNumber.postUpdate(50)
    testPlayer.postUpdate(PAUSE)
    testRollershutter.postUpdate(0)
    testString.postUpdate("Hello World")
    testSwitch.postUpdate(OFF)

    // 48.051437316054006, 8.207755911376244
    // latitude: 48.0501442
    // longitude: 8.2014192
    // elevation: 857.0
    testLocation.postUpdate(new PointType("48.051437316054006, 8.207755911376244, 857.0"))

    var userImageDataBytes = newByteArrayOfSize(0)
    var url = new URL("http://127.0.0.1:8080/static/webapps/Image.jpg")   // please use the IP to your openHAB instance
    var byteStreamOutput = new ByteArrayOutputStream()
    var urlConnection = url.openConnection()
    var userpass = "openhabian" + ":" + "openhabian";
    var basicAuth = "Basic " + new String(Base64.getEncoder().encode(userpass.getBytes()));
    urlConnection.setRequestProperty ("Authorization", basicAuth);
    var inputStream = urlConnection.getInputStream()
    var n = 0
    var buffer = newByteArrayOfSize(1024)
    do {
        n = inputStream.read(buffer)
        if (n > 0)  {
            byteStreamOutput.write(buffer, 0, n)
        }
    } while (n > 0)
    userImageDataBytes = byteStreamOutput.toByteArray()

    var String encodedString = Base64.getMimeEncoder().encodeToString(userImageDataBytes).replaceAll("\\r\\n", "")
    var ImageTMP = "data:image/jpg;base64," + encodedString

    testImage.postUpdate(ImageTMP)	
end
```

## Ausgabe

Man kann jedes `Item` einzeln zu einer `Sitemap` hinzufügen und kann diese auch beliebig unterteilen. Egal ob dies in `Frames` oder auch in `Groups` organisiert wird. Man kann auch zu jedem `Item` ein (neues) `Label` oder `Icon` setzen. Anders als bei `Items` sind auch verschiedene Repräsentation berücksichtbar, wie bspw. `Chart` oder `Webview`. Mehr dazu findet man in der `openHAB` Dokumentation unter [Sitemaps](https://www.openhab.org/docs/ui/sitemaps.html).

### Gesamte Sitemaps

Da wir zu jedem `Item` ein einfaches Beispiel wollten, müssen wir mit vielen Möglichkeiten der Sitemap gar nicht erst experimentieren. Uns genügt es, dass ganze durch ein  `Group Item` darzustellen:

```
sitemap Sitemap label="Sitemap" {
    Frame label="Static" {
        Group item=Static
    }
}
```

Die fertige Sitemap sieht wie folgt aus:

![Sitemap](https://raw.githubusercontent.com/Michdo93/openhab_static_examples/master/sitemap.png)

## Zusatz: Wertveränderung

Um die `States` zu verändern kann man neben der Bedienung der Elemente in der `Sitemap` auch eine weitere `Rule` schreiben. Damit ich meine "Anwendungen" testen kann, habe ich mich für eine `Rule` mit einem `Cron trigger` von einer Minute entschieden. Die funktioniert eigentlich genau gleich, wie die `Rule`, die statisch die Werte setzt:

```
import java.util.Base64
import java.io.ByteArrayOutputStream
import java.net.URL

rule "Cron every minute"
when
    Time cron "0 0/1 * * * ?"   // every minute
then
    testColor.postUpdate(NULL)
    testContact.postUpdate(NULL)
    testDateTime.postUpdate(NULL)
    testDimmer.postUpdate(NULL)
    testNumber.postUpdate(NULL)
    testPlayer.postUpdate(NULL)
    testRollershutter.postUpdate(NULL)
    testString.postUpdate(NULL)
    testSwitch.postUpdate(NULL)
    testLocation.postUpdate(NULL)
    testImage.postUpdate(NULL)

    testColor.postUpdate("100, 100, 100")
    testContact.postUpdate(CLOSED)
    testDateTime.postUpdate(now.toLocalDateTime().toString())
    testDimmer.postUpdate(30)
    testNumber.postUpdate(50)
    testPlayer.postUpdate(PAUSE)
    testRollershutter.postUpdate(0)
    testString.postUpdate("Hello World")
    testSwitch.postUpdate(OFF)

    // 48.051437316054006, 8.207755911376244
    // latitude: 48.0501442
    // longitude: 8.2014192
    // elevation: 857.0
    testLocation.postUpdate(new PointType("48.051437316054006, 8.207755911376244, 857.0"))

    var userImageDataBytes = newByteArrayOfSize(0)
    var url = new URL("http://127.0.0.1:8080/static/webapps/Image.jpg")   // please use the IP to your openHAB instance
    var byteStreamOutput = new ByteArrayOutputStream()
    var urlConnection = url.openConnection()
    var userpass = "openhabian" + ":" + "openhabian";
    var basicAuth = "Basic " + new String(Base64.getEncoder().encode(userpass.getBytes()));
    urlConnection.setRequestProperty ("Authorization", basicAuth);
    var inputStream = urlConnection.getInputStream()
    var n = 0
    var buffer = newByteArrayOfSize(1024)
    do {
        n = inputStream.read(buffer)
        if (n > 0)  {
            byteStreamOutput.write(buffer, 0, n)
        }
    } while (n > 0)
    userImageDataBytes = byteStreamOutput.toByteArray()

    var String encodedString = Base64.getMimeEncoder().encodeToString(userImageDataBytes).replaceAll("\\r\\n", "")
    var ImageTMP = "data:image/jpg;base64," + encodedString

    testImage.postUpdate(ImageTMP)	
end
```

