#include "plugin.hpp"

void Plugin::availablePluginsInfo(const std::string& path,
                                  AudioPluginFormatManager& pluginFormatManager,
                                  OwnedArray<PluginDescription>& pluginDescriptions,
                                  KnownPluginList& pluginList) {
    pluginFormatManager.addDefaultFormats();
    for (int i = pluginFormatManager.getNumFormats(); --i >= 0;) {
        std::cout << "format " << pluginFormatManager.getFormat(i) << std::endl;
        pluginList.scanAndAddFile (String(path), true, pluginDescriptions,
                                   *pluginFormatManager.getFormat(i));
    }
}

std::string Plugin::availablePluginsXml(const std::string& path) {
    std::cout << "!!" << path << std::endl;
    AudioPluginFormatManager pluginFormatManager;
    OwnedArray<PluginDescription> pluginDescriptions;
    KnownPluginList pluginList;
    availablePluginsInfo(path,
                         pluginFormatManager,
                         pluginDescriptions,
                         pluginList);

    auto ptr = pluginList.createXml();
    String serialized = ptr->toString();

    return serialized.toStdString();
}

void Plugin::loadPlugin (const std::string& path, int index) {
    AudioPluginFormatManager pluginFormatManager;
    OwnedArray<PluginDescription> pluginDescriptions;
    KnownPluginList pluginList;
    std::cout << path << std::endl;
    availablePluginsInfo(path, pluginFormatManager,
                         pluginDescriptions, pluginList);

    if (index >= pluginDescriptions.size()) {
        return;
        throw LoadPluginIndexTooHigh();
    }

    String errorMessage;

    plugin = pluginFormatManager.createPluginInstance (*pluginDescriptions[index],
                                                       sampleRate,
                                                       bufferSize,
                                                       errorMessage);
    if (plugin != nullptr) {
        plugin->prepareToPlay(sampleRate, bufferSize);
        plugin->setNonRealtime(true);
        return;
    }

    throw LoadPluginError(errorMessage.toStdString());
}

int Plugin::getLatency() {
    return plugin->getLatencySamples();
}

void Plugin::renderEffect(size_t nb_channels, std::vector<float>& wav) {
    MidiBuffer midiNoteBuffer;

    size_t wav_size = wav.size();
    size_t renderLength = wav_size / nb_channels;
    size_t numberOfBuffers = size_t (std::ceil (renderLength / bufferSize));

    AudioSampleBuffer audioBuffer (plugin->getTotalNumOutputChannels(),
                                   bufferSize);

    plugin->prepareToPlay (sampleRate, bufferSize);

    size_t pos = 0;
    for (size_t buf_idx = 0; buf_idx < numberOfBuffers; ++buf_idx) {
        for (size_t chan = 0; chan < 2; ++chan) {
            float* ptr = audioBuffer.getWritePointer(chan);
            for (size_t i = 0; i < bufferSize; ++i) {
                if (wav_size <= 2*(pos + i)) {
                    break;
                }
                ptr[i] = wav[2*(pos + i) + chan];
            }
        }
        plugin->processBlock (audioBuffer, midiNoteBuffer);
        for (size_t chan = 0; chan < 2; ++chan) {
            const float* ptr = audioBuffer.getReadPointer(chan);
            for (size_t i = 0; i < bufferSize; ++i) {
                if (wav_size <= 2*(pos + i)) {
                    break;
                }
                wav[2*(pos + i) + chan] = ptr[i];
            }
        }
        pos = pos + bufferSize;
    }

}
