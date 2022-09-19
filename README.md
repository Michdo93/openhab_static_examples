# openhab_static_examples
An example for static items to each openhab item type

The static examples are in `items/static.items`. With the rule file `rules/static.rules` all items which are null or empty will be populated by a rule. The file `rules/cron.rules` will update this items every minute. With this rule it is possible to receive changes. Please make sure that in both files you should change the `ip address` in the URL for the static image. This static image is in `html/webapps/Image.jpg`. The URL should be `http://<your_ip>:8080/static/webapps/Image.jpg`.

## Installation

You have to go to your openhab folder and clone it in the current directoy by using a dot at the end of your command:

```
git clone https://github.com/Michdo93/openhab_static_examples
cd openhab_static_examples
sudo cp -r * /etc/openhab
cd ..
sudo rm -r openhab_static_examples
sudo chown -R openhab:openhab /etc/openhab
```

![Sitemap](https://raw.githubusercontent.com/Michdo93/openhab_static_examples/master/sitemap.png)
