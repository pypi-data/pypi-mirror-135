(self["webpackChunkidom_client_jupyter"] = self["webpackChunkidom_client_jupyter"] || []).push([["lib_labplugin_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

// Export widget models and views, and the npm package version number.
module.exports = __webpack_require__(/*! ./widget.js */ "./lib/widget.js");
module.exports.version = __webpack_require__(/*! ../package.json */ "./package.json").version;


/***/ }),

/***/ "./lib/labplugin.js":
/*!**************************!*\
  !*** ./lib/labplugin.js ***!
  \**************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var plugin = __webpack_require__(/*! ./index */ "./lib/index.js");
var base = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");

module.exports = {
  id: "idom-client-jupyter",
  requires: [base.IJupyterWidgetRegistry],
  activate: function (app, widgets) {
    widgets.registerWidget({
      name: "idom-client-jupyter",
      version: plugin.version,
      exports: plugin,
    });
  },
  autoStart: true,
};


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var widgets = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
var idomClientReact = __webpack_require__(/*! idom-client-react */ "webpack/sharing/consume/default/idom-client-react/idom-client-react");
var _ = __webpack_require__(/*! lodash */ "webpack/sharing/consume/default/lodash/lodash");

var IdomModel = widgets.DOMWidgetModel.extend({
  defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
    _model_name: "IdomModel",
    _view_name: "IdomView",
    _model_module: "idom-client-jupyter",
    _view_module: "idom-client-jupyter",
    _model_module_version: "0.4.0",
    _view_module_version: "0.4.0",
  }),
});

var _nextViewID = { id: 0 };

const jupyterServerBaseUrl = (() => {
  const jupyterConfig = document.getElementById("jupyter-config-data");
  if (jupyterConfig) {
    return JSON.parse(jupyterConfig.text)["baseUrl"];
  }
  return document.getElementsByTagName("body")[0].getAttribute("data-base-url");
})();

class IdomView extends widgets.DOMWidgetView {
  constructor(options) {
    super(options);
    this.render = this.render.bind(this);
    this.remove = this.remove.bind(this);
  }

  render() {
    this.viewID = _nextViewID.id;
    _nextViewID.id++;

    var saveUpdateHook = (updateHook) => {
      this.model.on("msg:custom", (msg, buffers) => {
        if (msg.viewID == this.viewID) {
          updateHook(...msg.data);
        }
      });
      this.send({
        type: "client-ready",
        viewID: this.viewID,
        data: null,
      });
    };

    var sendEvent = (event) => {
      this.send({
        type: "dom-event",
        viewID: this.viewID,
        data: event,
      });
    };

    const importSourceBaseUrl = concatAndResolveUrl(
      this.model.attributes._jupyter_server_base_url || jupyterServerBaseUrl,
      "_idom_web_modules"
    );
    var loadImportSource = (source, sourceType) => {
      return import( /* webpackIgnore: true */
        sourceType == "NAME" ? `${importSourceBaseUrl}/${source}` : source
      );
    };

    idomClientReact.mountLayout(this.el, {
      saveUpdateHook,
      sendEvent,
      loadImportSource,
    });
  }

  remove() {
    this.send({ type: "client-removed", viewID: this.viewID });
    return super.remove();
  }
}

function concatAndResolveUrl(url, concat) {
  var url1 = (url.endsWith("/") ? url.slice(0, -1) : url).split("/");
  var url2 = concat.split("/");
  var url3 = [];
  for (var i = 0, l = url1.length; i < l; i++) {
    if (url1[i] == "..") {
      url3.pop();
    } else if (url1[i] == ".") {
      continue;
    } else {
      url3.push(url1[i]);
    }
  }
  for (var i = 0, l = url2.length; i < l; i++) {
    if (url2[i] == "..") {
      url3.pop();
    } else if (url2[i] == ".") {
      continue;
    } else {
      url3.push(url2[i]);
    }
  }
  return url3.join("/");
}

module.exports = {
  IdomModel: IdomModel,
  IdomView: IdomView,
};


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"idom-client-jupyter","version":"0.4.0","description":"A client for IDOM implemented using Jupyter widgets","author":"Ryan Morshead","main":"lib/index.js","repository":{"type":"git","url":"https://github.com/idom-team/idom-jupyter.git"},"keywords":["jupyter","widgets","ipython","ipywidgets","jupyterlab-extension"],"files":["lib/**/*.js","dist/*.js"],"scripts":{"clean":"rimraf dist/ && rimraf ../idom_jupyter/labextension/ && rimraf ../idom_jupyter/nbextension","prepublish":"yarn run clean && yarn run build:prod","build":"webpack --mode=development && yarn run build:labextension:dev","build:prod":"webpack --mode=production && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","watch":"webpack --watch --mode=development","test":"echo \\"Error: no test specified\\" && exit 1","format":"prettier -w lib"},"devDependencies":{"@jupyterlab/builder":"^3.0.0","prettier":"^2.2.1","rimraf":"^2.6.1","webpack":"^5"},"dependencies":{"@jupyter-widgets/base":"^1.1 || ^2 || ^3 || ^4","idom-client-react":"^0.8.5","lodash":"^4.17.4","react":"^17.0.1","react-dom":"^17.0.1"},"jupyterlab":{"extension":"lib/labplugin","outputDir":"../idom_jupyter/labextension","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_labplugin_js.880fcc8acaeeb0542a5a.js.map