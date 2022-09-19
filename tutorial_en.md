# openHAB static examples

## Motivation

In openHAB items are usually created bound. This means that there is usually a physically existing device. About an appropriate binding to this device (sometimes it is also any online accounts), then a Thing is created. This Thing makes it possible to create corresponding items via channels, which can be used in openHAB to operate the device.

Detached from any devices, bindings, things or channels, it is possible to create so-called [unbound items](https://community.openhab.org/t/design-pattern-unbound-item-aka-virtual-item/15993), which can also be called virtual items. There are various application examples for this. For example, you can create a switch item that triggers only one rule, which would then serve multiple devices.

The goal of this tutorial is to provide an example of how to create an example for each [Item Type](https://www.openhab.org/docs/configuration/items.html#type) independently of Things. This is to give an understanding of how individual Items and openHAB work. We are talking about static examples here, because by rules each of these examples should have a value assigned to it.

Note: I like to use such Hello World examples in the development of various programs, such as an MQTT event bus, a bridge between openHAB and ROS, a CRUD via the REST API or an SSE client for item events via the REST API and much more.

## The Hello World Problem

In many programming languages there is an example for Hello World. This example shows the typical characteristics of this programming language. I will show an example how to create such a program for Java, because openHAB is written in Java:

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

I have slightly adjusted the output of the string `"Hello World!"` in this Hello World example, so that this string is stored in a variable beforehand. Because this is exactly what cannot be done in openHAB like this. The `Items` are often mistakenly understood as variables. But actually `Items` are objects. The most important attribute for value assignment is `state`. If an `Item` object is created, however, I cannot assign values to `state`. Other attributes like `name`, `label` or `icon` I can set. Or even assign an `item` to a `group`, which in turn is another `item`.

What does this mean in concrete terms? The following [syntax](https://www.openhab.org/docs/configuration/items.html#item-definition-and-syntax) applies to the item definition:

```
itemtype itemname "labeltext [stateformat]" <iconname> (group1, group2, ...) ["tag1", "tag2", ...] {bindingconfig}
```

The `state` of an `item` is not set when the `item` is defined or when the `item` object is instantiated! Typically a `thing` or a `rule` changes it.

If I would take my example from above from the Java program, the most I can do is to use a

```
String hello "[%s]"
```

out of it. A value assignment like

```
String hello="Hello World!" "[%s]"
```

or

```
String hello state="Hello World!" "[%s]"
```

or whatever it should look like then, is not possible!

By the way you can see by `{bindingconfig}` if an item is bound or not. In the `{}` either a `binding` directly or a `channel` of a `thing` would have to be accessed. With an `unbound item` this is completely omitted.

However, the Hello World problem not only points out that many are looking for some kind of value assignment, but also an output. To represent openHAB simplified:

| Type | Description | By | Where |
| :--: |:-------------:| :-----:| :-----:|
| Object instantiation | To create an 'item', this object must first be created. Similar to classical programming you can pass different values (`name`, `label`, `icon`, ...) to the constructor. | `Items` | `main UI`, `.items` file or via the `REST API` |
| Attribute value assignment | Under attributes I call all attributes except `state`. Classically, many attributes are already set when the `item` is created. But for the display in the `UI` by `sitemaps`, I can override e.g. attributes like `label` or `icon`. Optionally, I can also use `Rules` to override an attribute like `label`, for example. | `Items`, `Sitemaps`, `Rules` | `main UI`, `.items` file or via the `REST API`, as well as in the `.sitemaps` file or in `.rules` files |
| Value assignment of states | Normally, the `state` is set by a `thing` or its `channel` as soon as a device is served. Also an `event` in openHAB (like operating a UI element) changes the `state`. But `Events` can also be used to trigger a `Rule`. Via `sendCommand` or `postUpdate` value assignments of `States` can also take place in `Rules`. | `Things`, `Sitemaps`, `Rules` | `main UI`, `.things` file or via the `REST API`, as well as in the `.sitemaps` file or in `.rules` files |
| output | An output of `items` is done in the UI. Classically only in `sitemaps`. Theoretically there is still an output in the `Karaf console` and by `Rules` you could additionally log the `Items`. Events` for the `Items` are logged automatically. | `Sitemaps`, `Karaf Console` | `main UI`, `.sitemaps` file or via the `REST API`, as well as in the `Karaf Console`. |

We therefore limit ourselves to instantiating an `Item` object in a `.items` file, then assigning the values of `States` in a `.rules` file, and defining their output through a `.sitemaps` file.

## Object instantiation

As described above, the objects of the items are created in a `.items` file.

### Group

We want to create a parent group, i.e. a `group item`. An `item` of type `group` does not have a `state`. In fact, for ease of use, we only need to specify the name of this group:

```
Group Static
```

It would also be possible that this `Group` would be subordinated to another `Group`. You can also specify a `Label` or an `Icon`.

### Color

In the case of a `Color Item`, only the name of this `Item` needs to be specified for a minimalistic example. However, since we have already created a `Group Item` before, we want to subordinate this `Item` to our `Group`. We will also do this for all other `Items` later.

```
Color testColor (Static)
```

We can do without `Label` and `Icon` in a simple example!

### Contact

The next `Item` we want to create is a `Contact Item`. This `Item` classically indicates whether, for example, a door is `OPEN` or `CLOSED` if a corresponding sensor would be used. For a later output in our `Sitemap` we have to set a `Label` here:

```
Contact testContact "[%s]" (Static)
```

The `[%s]` later adds the `state` of the `item` as a `string`. Without this specification it would not be visible whether a `Contact Item` has the `State` `CLOSED` or `OPEN`. You can also enter any `String` in the `Labels` in general. Thus also a prefix or postfix would be conceivable. This could be e.g. units. But this is not needed here. The reason why you have to parse the `State` to a `String` is that `OPEN` and `CLOSED` are treated as own datatypes by `openHAB`, which will play a role later in the `Rules`.

An `icon` is not used in this example!

### DateTime

With a `DateTime Item` the `Label` is used again, so that one formats the `Timestamp` into a desired output format. This is needed because in different countries one specifies a date or time in different ways. Also it is conceivable that one specifies only the date or only the time. In the following example, only the time is to be output from the last recorded timestamp, i.e., the time is to be output in hours and minutes (`HH:MM`):

```
DateTime testDateTime "[%1$tH:%1$tM]" (Static)
```

The timestamp refers to the recorded time. It now depends on the `rule` what is considered as the last timestamp. More will be said about this later in the `Rules`. A `DateTime Item` is used in different ways. Mostly there are some sensor values and the `DateTime Item` then indicates when the last time a change of these sensor values has been recorded.

An `Icon` is not used in this example!

### Dimmer

A 'dimmer' is classically used to dim something. This example is most familiar with lamps and their brightness. Typically, the `states` here are between `0` and `100`, which would mean completely dark or completely bright in the previously mentioned example. This is a percentage. Another example might be a volume control. The `Item` are in a rudimentary example as follows:

```
Dimmer testDimmer (Static)
```

You can do without `label` and `icon` in a simple example!

### Image

In `openHAB` an `Image Item` is used to display images. This can be any kind of image. No matter if formats like `JPG`, `PNG`, if it is about photos or snapshots, single frames, wallpapers or for example an album cover for music. Whatever should be represented by an image. Only `GIF`s are not possible. Also a video stream would be only theoretically conceivable, in which one represents the frames one after the other.

```
Image testImage (Static)
```

You can do without `Label` and `Icon` in a simple example!

### Location

With a `Location Item` some kind of location is to be represented. The `State` contains `GPS coordinates` with longitude, latitude and the altitude. There are several application examples. For example, you could use your own weather station and it would have to be configured first or record where it is located. Maybe one has a robot (e.g. a lawn mowing robot) that has `GPS` or via a `binding` the vehicle would be linked to the smart home and as soon as one leaves the house the windows are locked.

```
Location testLocation "HS Furtwangen" <house> (Static)
```

Later we want to specify the coordinates of Furtwangen University as an example. Therefore we need the `label` `HS Furtwangen`. We can do without an `icon`, but since the university is a building, we use a `house` as `Ìcon`.

### Number

With a `number item` you can represent any kind of numbers. Again, a `label` is needed for formatting. For example, it is important how many decimal places should be displayed or whether one should be displayed at all. Also the number can refer to any unit, like `m`, `kmh` or `°C`. In the following we want to represent an integer (`integer`), which in the end would be nothing else than a floating point number (`float`) without a decimal place:

```
Number testNumber "[%.0f]" (Static)
```

As you can see, `%` is used as a placeholder for the number and at the end you define the data type like `float` with `f` and the decimal places (here: `0`). A temperature in degrees Celsius could be specified with `"[%.2f °C]"`. More information about [units](https://www.openhab.org/docs/concepts/units-of-measurement.html) can be found in the openHAB documentation!

We do without an `icon` in this simple example

### Player

An `Item` of the type `Player` is used for example if you want to play music or a video. You can play, pause, fast forward or rewind this medium. It is also conceivable that the next or previous medium would be played.

```
Player testPlayer (Static)
```

You can do without `Label` and `Icon` in a simple example!

### Rollershutter

The `Rollershutter Item` is not only used for roller shutters, but also for awnings or blinds. After all, they work almost the same way in principle. They are either retracted or extended. Optionally there is a value somewhere in between, because you have stopped the retraction or extension.

```
Rollershutter testRollershutter (Static)
```

You can do without `Label` and `Icon` in a simple example!

### String

A `String Item` does exactly what you expect. You pass some kind of string to this `Item`, consequently this `State` is a `String`. In principle, you can also treat a single `character` or `char` as a `string`. The `String Item` is used very versatile. It can be the title of a medium, the last message of a news feed, a selected mode of a device and much more. Strings can also be formatted in any dense way. To fully display a `string` you have to define the `label` accordingly as well:

```
String testString "[%s]" (Static)
```

Logically, you could also convert a numeric value to a string. But then you are actually using the wrong data type.

An `icon` can be omitted in a simple example!

### Switch

I honestly love the `Switch Item`! It is a simple switch that has the `states` `ON` and `OFF`. Besides whether a device is switched on, you can also use it to activate individual `rules`. Typically this is also used to activate or deactivate individual functionalities on a device. Or if you have a good style with rules, you can divide them into several parts and control them with several `Switch Items` in a row.

```
Switch testSwitch (Static)
```

You can do without `Label` and `Icon` in a simple example!

### Total items

This then results in our `.items` file, which looks like this:

```
Group Static

Color testColor (Static)
Contact testContact "[%s]" (Static)
DateTime testDateTime "[%1$tH:%1$tM]" (Static)
Dimmer testDimmer (Static)
Image testImage (Static)
Location testLocation "HS Furtwangen" <house> (Static)
Number testNumber "[%.0f]" (Static)
Player testPlayer (Static)
Rollershutter testRollershutter (Static)
String testString "[%s]" (Static)
Switch testSwitch (Static)
```

## Value assignment of states

Since we assume here a static example, i.e. that the values do not change, you can execute this `Rule` when you start `openHAB`. The `<TRIGGER_CONDITION>` `System started` is a so-called [system-based trigger](https://www.openhab.org/docs/configuration/rules-dsl.html#system-based-triggers).

```
rule `Started
when
    System started
then
    ...
end
```

In concrete terms, this means that as soon as `openHAB` is started, the `Items` should receive their values.

### Color

For a `Color Item`, values in `HSB` format are expected for the `State`:

```
testColor.postUpdate("120, 100, 100") // hue, saturation, brightness
```

This would correspond to `"0, 255, 0"` in `RGB`!

### Contact

For a `Contact Item` we simply assume that at system start the `State` is `CLOSED`:

```
testContact.postUpdate(CLOSED)
```

As we can see, in the `rule` we can use the `state` `CLOSED` directly and not mistakenly as a string `"CLOSED"`. We should remember this for all state representations! A `sendCommand` would not be possible for a `Contact Item`!

### DateTime

In most programming languages there is the possibility to create a date object in which a string is converted to a timestamp (often called `string to time`). In `openHAB` we ultimately do nothing else:

```
testDateTime.postUpdate(now.toLocalDateTime().toString())
```

In this case, however, we have taken our input from a date object that returns us the current time. This means that we have to convert the returned value to a string. For this we use `toString()`. A function that can often be useful in `Rules`.

### Dimmer

With a `Dimmer` you only have to make sure that you use an integer between `0` and `100`:

```
testDimmer.postUpdate(30)
```

### Image

Images are definitely a special case. I can`t just take any string and pass it. In `openHAB` an `Image Item` doesn`t work either by specifying the path to an image. One could perhaps assume that I can use an image by specifying only its path. In this case it might not matter if I specify an absolute and local path or if the path points to an online source. In `openHAB` an image is stored and used as an image. This has been implemented in such a way that many devices can also deliver images. You have to assume that a device sends an image and not that you just include any image without any context and use in `openHAB`. Similar to many other sensor values, this is useful data.

However, since we are not using such an image, such as a frame from a camera, the following script shows how to add an image from an online source:

```
var userImageDataBytes = newByteArrayOfSize(0)
var url = new URL("http://127.0.0.1:8080/static/webapps/Image.jpg") // please use the IP to your openHAB instance
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
    if (n > 0) {
        byteStreamOutput.write(buffer, 0, n)
    }
} while (n > 0)
userImageDataBytes = byteStreamOutput.toByteArray()

var String encodedString = Base64.getMimeEncoder().encodeToString(userImageDataBytes).replaceAll("\\r\\n", "")
var ImageTMP = "data:image/jpg;base64," + encodedString

testImage.postUpdate(ImageTMP)	
```

In this example we use the HTML directory (`/etc/openhab/html`) of `openHAB`. To extend this a bit, I created the subdirectory `webapps` and put an `image.jpg` in it. So if I want to add a local image from my server running `openHAB`, I would rather recommend to link a symbolic link into the HTML directory and proceed as above. Of course you can also add images using Java functions. This possibility allows you to add an image from other computers in the same network.

It is important that you work with `Streams` and that the image at the end is `Base64` encoded as a string and updated as `State`! Also a `sendCommand` is not possible with images!

### Location

As we have already noticed from the label, we want to use the `GPS` coordinates of Furtwangen University as `State` for the `Location Item`. This is also done by a string. However, we have to pass this to a `PointType` object:

```
// 48.051437316054006, 8.207755911376244
// latitude: 48.0501442
// longitude: 8.2014192
// altitude/elevation: 857.0
testLocation.postUpdate(new PointType("48.051437316054006, 8.207755911376244, 857.0"))
```

### Number

For a `Number Item` it does not matter in the end which number you assign. The important thing is that a `State` can contain e.g. a floating point number and in the `Sitemap` you still format to an integer! If one should access this `state`, one would have to consider this e.g. in a `rule` then:

```
testNumber.postUpdate(50)
```

### Player

For a player we can use `States` like `PLAY`, `PAUSE`, `REWIND`, `FASTFORWARD`, `PREVIOUS` or `NEXT`:

```
testPlayer.postUpdate(PAUSE)
```

Again, don't specify this as a string!

### Rollershutter

Likewise, `Rollershutter Items` do not use strings with their `Commands`. As an example, however, we want to set a `state`:

```
testRollershutter.postUpdate(0)
```

### String

As already mentioned, a string can be a classic string or contain a single character. The whole thing is processed as a string. As we know from many programming languages (here still Java), a string is nothing else than an `array` of `characters` or in other words an `array` of `characters`:

```
testString.postUpdate("Hello World")
```

### Switch

A `switch` can have either the `state` `ON` or `OFF`:

```
testSwitch.postUpdate(OFF)
```

### Total Rules

This then results in the following `rule`:

```
import java.util.Base64
import java.io.ByteArrayOutputStream
import java.net.URL

rule "Started
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
    var url = new URL("http://127.0.0.1:8080/static/webapps/Image.jpg") // please use the IP to your openHAB instance
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
        if (n > 0) {
            byteStreamOutput.write(buffer, 0, n)
        }
    } while (n > 0)
    userImageDataBytes = byteStreamOutput.toByteArray()

    var String encodedString = Base64.getMimeEncoder().encodeToString(userImageDataBytes).replaceAll("\\r\\n", "")
    var ImageTMP = "data:image/jpg;base64," + encodedString

    testImage.postUpdate(ImageTMP)	
end
```

## Output

## Output

You can add each `item` individually to a `sitemap` and you can also subdivide it as you like. No matter if this is organized in `Frames` or also in `Groups`. You can also set a (new) `label` or `icon` for each `item`. Unlike with `Items`, different representations can be considered, such as `Chart` or `Webview`. More about this can be found in the `openHAB` documentation at [Sitemaps](https://www.openhab.org/docs/ui/sitemaps.html).

### Entire sitemaps

Since we wanted a simple example for each `item`, we do not even have to experiment with many possibilities of the sitemap. It is enough for us to represent the whole thing by a `Group Item`:

```
sitemap Sitemap label="Sitemap" {
    Frame label="Static" {
        Group item=Static
    }
}
```

The finished sitemap looks like this:

![sitemap](https://raw.githubusercontent.com/Michdo93/openhab_static_examples/master/sitemap.png)

## Addition: Value change

To change the `States` you can write another `Rule` besides operating the elements in the `Sitemap`. So that I can test my `applications`, I decided to write a `Rule` with a `Cron trigger` of one minute. It actually works exactly the same as the `rule` that statically sets the values:

```
import java.util.Base64
import java.io.ByteArrayOutputStream
import java.net.URL

rule "Cron every minute
when
    Time cron "0 0/1 * * ?"   // every minute
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
    var url = new URL("http://127.0.0.1:8080/static/webapps/Image.jpg") // please use the IP to your openHAB instance
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
        if (n > 0) {
            byteStreamOutput.write(buffer, 0, n)
        }
    } while (n > 0)
    userImageDataBytes = byteStreamOutput.toByteArray()

    var String encodedString = Base64.getMimeEncoder().encodeToString(userImageDataBytes).replaceAll("\\r\\n", "")
    var ImageTMP = "data:image/jpg;base64," + encodedString

    testImage.postUpdate(ImageTMP)	
end
```

