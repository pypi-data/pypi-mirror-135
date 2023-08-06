Python audio plugin host, based on JUCE

Goals:

* python package out of the box
* continious-integration friendly

Known issues:

JUCE's plugin loading routine is too shy, so if plugin hasn't been loaded,
it's hard to determine why, especially in release where asserts are turned off. It will look like it's not found.

Example:

```python
import audio_plugin_test as aptest
import numpy as np

sample_rate = 44100
buffer_size = 512

path = "Plugin.vst3"
engine = aptest.Plugin(path, 0, sample_rate, buffer_size)
print (engine.plugins_at_path(path))
a = np.zeros((88200, 2), dtype=np.float32)
a = a + 0.5
print (engine.get_parameters())
engine.update_parameters({"Strength" : 0.1 })
print (engine.get_parameters())
engine.set_parameter("Strength", 0.2)
print (engine.get_parameters())
```

Sources are initially based on https://github.com/fedden/RenderMan

You may want to look at https://github.com/DBraun/DawDreamer if you want a more sophisticated python plugin host.
