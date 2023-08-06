#pragma once

#include <random>
#include <array>
#include <iomanip>
#include <sstream>
#include <string>
#include <JuceHeader.h>

using namespace juce;

struct WrongInputShape{};
struct LoadPluginIndexTooHigh{};
struct LoadPluginError {
    std::string message;
    LoadPluginError(const std::string& message_):
    message(message_) {}
};


class Plugin {
public:
    Plugin (const std::string& path,
            int index,
            int sr, size_t bs) :
        sampleRate(sr),
        bufferSize(bs),
        plugin(nullptr) {
        loadPlugin(path, index);
    }

    virtual ~Plugin() {}

 	ScopedJuceInitialiser_GUI juceInit;
    std::string availablePluginsXml(const std::string& path);

    void availablePluginsInfo(const std::string& path,
                              AudioPluginFormatManager& pluginFormatManager,
                              OwnedArray<PluginDescription>& pluginDescriptions,
                              KnownPluginList& pluginList);

    int getLatency();
    void renderEffect(size_t nb_channels, std::vector<float>& wav);

    double sampleRate;
    size_t bufferSize;
    std::unique_ptr<AudioPluginInstance> plugin;

    void loadPlugin(const std::string& path, int index = 0);

};
