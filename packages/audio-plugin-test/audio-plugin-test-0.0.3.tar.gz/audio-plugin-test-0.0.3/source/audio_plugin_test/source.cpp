#include "plugin.hpp"

#define BOOST_ALLOW_DEPRECATED_HEADERS
#define BOOST_BIND_GLOBAL_PLACEHOLDERS
#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

namespace wrap {

    namespace p = boost::python;
    namespace np = boost::python::numpy;

    class PluginWrapper : public Plugin {
    public:
        PluginWrapper (const std::string& path,
                       int index,
                       int sr, int bs) :
            Plugin (path, index, sr, bs)
        { }

        int wrapperGetLatency() {
            return Plugin::getLatency();
        }

        void wrapperRenderEffect(np::ndarray arr) {
            if (arr.get_dtype() != np::dtype::get_builtin<float>()) {
                throw WrongInputShape();
            }
            int nd = arr.get_nd();
            if (nd != 2) {
                throw WrongInputShape();
            }
            if (arr.get_shape()[1] != 2) {
                throw WrongInputShape();
            }
            std::vector<float> v(size_t(arr.get_shape()[0]*arr.get_shape()[1]));
            float* input_ptr = reinterpret_cast<float*>(arr.get_data());
            for (size_t i = 0; i < v.size(); ++i) {
                v[i] = input_ptr[i];
            }
            Plugin::renderEffect(2, v);
            for (size_t i = 0; i < v.size(); ++i) {
                input_ptr[i] = v[i];
            }
        }

        p::dict wrapperGetParameters() {
            p::dict out;
            for (const auto& parameter : plugin->getParameters()) {
                out[parameter->getName(256).toStdString()] = parameter->getValue();
            }
            return out;
        }

        void wrapperUpdateParameters(p::dict paramsToUpdate) {
            p::list items = paramsToUpdate.items();
            // O(N^2)
            for(ssize_t i = 0; i < p::len(items); ++i) {
                std::string key = p::extract<std::string>(items[i][0]);
                float value = p::extract<float>(items[i][1]);
                for (const auto& parameter : plugin->getParameters()) {
                    if (parameter->getName(256).toStdString() == key) {
                        parameter->setValue(value);
                        break;
                    }
                }
            }
        }

        void wrapperSetParameter(std::string name, float value) {
            for (const auto& parameter : plugin->getParameters()) {
                if (parameter->getName(256).toStdString() == name) {
                    parameter->setValue(value);
                    break;
                }
            }
        }

        p::dict wrapperGetPluginNames(const std::string& path) {
            AudioPluginFormatManager pluginFormatManager;
            OwnedArray<PluginDescription> pluginDescriptions;
            KnownPluginList pluginList;
            availablePluginsInfo(path, pluginFormatManager, pluginDescriptions, pluginList);

            p::dict out;
            int index = 0;
            for (const auto& pluginDescription : pluginList.getTypes()) {
                out[pluginDescription.name.toStdString()] = index;
                index++;
            }
            return out;
        }
    };

    void translator_WrongInputShape(WrongInputShape const& ) {
        PyErr_SetString(PyExc_ValueError,
                        "Provide numpy arrays with shape (N, 2) and dtype=float");
    }

    void translator_LoadPluginError(LoadPluginError const& ) {
        PyErr_SetString(PyExc_ValueError,
                        "Error while loading plugin");
    }

    void translator_LoadPluginIndexTooHigh(LoadPluginIndexTooHigh const& e) {
        PyErr_SetString(PyExc_ValueError,
                        "Plugin index is higer than amount of found plugins");
    }

}

BOOST_PYTHON_MODULE(libaptest)
{
    using namespace boost::python;
    using namespace wrap;

    numpy::initialize();

    register_exception_translator<WrongInputShape>(translator_WrongInputShape);
    register_exception_translator<LoadPluginError>(translator_LoadPluginError);
    register_exception_translator<LoadPluginIndexTooHigh>(translator_LoadPluginIndexTooHigh);

    class_<PluginWrapper, boost::noncopyable>("Plugin",
                                              init<const std::string&, int, int, int>())
    .def("get_latency", &PluginWrapper::wrapperGetLatency)
    .def("render_effect", &PluginWrapper::wrapperRenderEffect)
    .def("update_parameters", &PluginWrapper::wrapperUpdateParameters)
    .def("set_parameter", &PluginWrapper::wrapperSetParameter)
    .def("get_parameters", &PluginWrapper::wrapperGetParameters)
    .def("plugins_at_path", &PluginWrapper::availablePluginsXml);

}

