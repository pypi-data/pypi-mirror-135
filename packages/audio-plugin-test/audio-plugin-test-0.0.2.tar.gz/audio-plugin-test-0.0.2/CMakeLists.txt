cmake_minimum_required(VERSION 3.15)

project(aptest VERSION 0.0.1)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include(FetchContent)

FetchContent_Declare(
  dryjuce
  GIT_REPOSITORY https://github.com/galchinsky/dryjuce
  GIT_TAG        origin/main
)
FetchContent_MakeAvailable(dryjuce)

#add_subdirectory(dryjuce)

set(JUCE_BUILD_HELPER_TOOLS, 0)

add_library(aptest SHARED)
_juce_initialise_target(aptest ${ARGN})


target_sources(aptest
    PRIVATE
        source/audio_plugin_test/plugin.cpp
        source/audio_plugin_test/source.cpp
)

juce_generate_juce_header(aptest)

target_compile_definitions(aptest
    PRIVATE
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=0
        JUCE_PLUGINHOST_VST3=1
        JUCE_VST3_HOST_CROSS_PLATFORM_UID=1
        JUCE_APPLICATION_NAME_STRING="$<TARGET_PROPERTY:aptest,JUCE_PRODUCT_NAME>"
        JUCE_APPLICATION_VERSION_STRING="$<TARGET_PROPERTY:aptest,JUCE_VERSION>"
)

find_package(PythonLibs REQUIRED)
find_package(Boost COMPONENTS python COMPONENTS numpy REQUIRED)

target_include_directories(aptest SYSTEM PRIVATE ${PYTHON_INCLUDE_DIRS})

target_link_libraries(aptest
    PRIVATE
        juce::juce_gui_extra
        juce::juce_audio_basics
        juce::juce_audio_devices
        juce::juce_audio_formats
        juce::juce_audio_processors
        juce::juce_core
        juce::juce_cryptography
        juce::juce_data_structures
        juce::juce_events
        juce::juce_graphics
        juce::juce_gui_basics
        juce::juce_gui_extra
        juce::juce_opengl
        juce::juce_video
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags
        ${Boost_LIBRARIES})

install(TARGETS aptest LIBRARY DESTINATION .)
