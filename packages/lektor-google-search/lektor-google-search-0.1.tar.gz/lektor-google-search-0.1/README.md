# Lektor-Google-Search

This plugin add support for [Google Search](https://search.google.com/search-console/about) to [Lektor CMS](https://www.getlektor.com/)

Once the plugin is enabled, a `render_google_search()` function is available to be included in a taget `template` which autoatically
include Google-Search code in final HTML fles rendered by Lektor.

## How to Use the plugin ?

### Enable the plugin

To enable the plugin, add the following to your `.lektorproject` file:

```ini
[packages]
lektor-google-search = 0.1
```

### Configure the plugin

The plugin needs a config file with your `search Engine ID` code in it

- Create a file named `google-serch.ini` into `./configs` folder in your lektor project's base directory.
- Put the `SEARCH_ENGINE_ID` key with the value of your serch engine ID.

```ini
SEARCH_ENGINE_ID = 83892839209432084
```

### Usage in template

Add Google Search code snippet by calling the function `render_google_search()` in the template of your preference where you want the search box to appear.

```html
<div>{{ render_googe_search() }}</div>
```

Now, try to run `lektor server` to see the google search appear.
