"use strict";
(self["webpackChunkserialhub"] = self["webpackChunkserialhub"] || []).push([["lib_plugin_js"],{

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./version */ "./lib/version.js");
// Copyright (c) cdr4eelz
// Distributed under the terms of the Modified BSD License.



const EXTENSION_ID = 'serialhub_plugin';
/*
namespace CommandIDs {
  export const connect = 'serialhub:connect'
  export const disconnect = 'serialhub:disconnect'
  export const test = 'serialhub:test'
}
*/
/**
 * The SerialHub plugin.
 */
const serialhubPlugin = {
    id: EXTENSION_ID,
    requires: [_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true
}; // as unknown as IPlugin<Application<Widget>, void>;
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (serialhubPlugin);
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    console.log('Registering serialhub widget...', _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION, _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_NAME);
    registry.registerWidget({
        name: _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_NAME,
        version: _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION,
        exports: _widget__WEBPACK_IMPORTED_MODULE_2__
    });
}
//# sourceMappingURL=plugin.js.map

/***/ })

}]);
//# sourceMappingURL=lib_plugin_js.73f4fb8c50aeae500020.js.map