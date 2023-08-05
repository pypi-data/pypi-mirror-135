"use strict";
(self["webpackChunkserialhub"] = self["webpackChunkserialhub"] || []).push([["lib_widget_js"],{

/***/ "./lib/serialhubport.js":
/*!******************************!*\
  !*** ./lib/serialhubport.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SerialHubPort": () => (/* binding */ SerialHubPort)
/* harmony export */ });
// Copyright (c) cdr4eelz
// Distributed under the terms of the Modified BSD License.
/* SerilHubPort class to simplify access to WebSerial ports */
class SerialHubPort {
    constructor() {
        this.port = null;
        this.writer = null;
        this.reader = null;
    }
    /* connect the SerialHubPort by requesting and then opening a Web Serial port */
    async connect(requestOpts, serialOpts) {
        const NAV = window.navigator;
        if (!NAV || !NAV.serial) {
            throw new TypeError('Web Serial API not supported');
        }
        if (this.port) {
            throw new TypeError('WebSerial port is already connected');
        }
        const rawPort = await NAV.serial.requestPort(requestOpts);
        if (!rawPort) {
            //The requestPort() probably threw error, but in case not...
            throw new TypeError('FAILED request a port from user');
        }
        //TODO: Install an this.ondisconnect(event) handler to rawPort
        console.log('OPENING PORT:', rawPort, rawPort.getInfo());
        this.port = rawPort;
        await this.port.open(serialOpts);
        //Note that getReader & getWriter "lock" the port to the reader
        this.writer = this.port.writable.getWriter();
        this.reader = this.port.readable.getReader();
        console.log('CONNECTED: ', this, this.port, this.port.getInfo());
        //Let cbConnect initiate this.readLoop(f);
    }
    /* disconnect the SerialHubPort by closing the associated Web Serial port */
    async disconnect() {
        var _a, _b, _c;
        console.log('CLOSE: ', this);
        //TODO: Verify proper closing steps for reader/writer vs the port itself
        // Helpful hints about closing https://wicg.github.io/serial/#close-method
        try {
            //await this.port?.readable?.cancel('Closing port');
            await ((_a = this.reader) === null || _a === void 0 ? void 0 : _a.cancel('Closing port')); //Should indirectly signal readLoop to terminate
        }
        catch (e) {
            console.error('Ignoring error while closing readable', e);
            //Ignore exception on reader
        }
        finally {
            this.reader = null;
        }
        try {
            //await this.port?.writable?.abort('Closing port');
            //await this.writer?.abort('Closing port');
            await ((_b = this.writer) === null || _b === void 0 ? void 0 : _b.close());
        }
        catch (e) {
            console.error('Ignoring error while closing writable', e);
            //Ignore exception on writer
        }
        finally {
            this.writer = null;
        }
        //Hopefully the above have unlocked the reader/writer of the port???
        // and allowed the readLoop to fall-through before we close the port.
        try {
            await ((_c = this.port) === null || _c === void 0 ? void 0 : _c.close()); //Let exceptions through from here
        }
        finally {
            this.port = null; //But clear this.port reference
        }
    }
    /* writeToStream writes and awaits multiple buffers to the serial port */
    writeToStream(data) {
        if (!this.writer) {
            throw new TypeError('Stream not open');
        }
        data.forEach(async (d) => {
            var _a;
            //Anonymous function is ASYNC so it can AWAIT the write() call below
            console.log('[WRITE]', d, d.byteLength);
            await ((_a = this.writer) === null || _a === void 0 ? void 0 : _a.write(d)); //AWAIT in sequence, to avoid parallel promises
        });
        let nWritten = 0;
        for (const d of data) {
            nWritten += d.byteLength; //TODO: What about offsets in ArrayBufferView???
        }
        console.log('[WROTE]', nWritten);
        return nWritten;
    }
    /* readLoop to be called back to by Web Serial API as data is read from the serial port */
    async readLoop(cbRead) {
        var _a;
        //Possibly "SerialPort.readable" goes null if disconnected?
        while (this.reader && ((_a = this.port) === null || _a === void 0 ? void 0 : _a.readable)) {
            //TODO: Inner loop for non-fatal errors & re-allocate local reader
            //console.log('[readLoop] LOOP');
            const { value, done } = await this.reader.read();
            if (value) {
                //console.log('[readLoop] VALUE', value);
                cbRead(value);
            }
            if (done) {
                console.log('[readLoop] DONE', done);
                this.reader.releaseLock();
                break;
            }
        }
        console.log('[readLoop] EXIT');
    }
    /* Static function to check if browser supports Web Serial API */
    static isSupported() {
        return 'serial' in navigator;
        /*
        const NAV: Navigator = window.navigator;
        if (NAV === undefined || NAV === null) {
          return false;
        }
        const SER: any = (NAV as any).serial;
        if (SER === undefined || SER === null) {
          return false;
        }
        return true;
        */
    }
    /* createOneHub() is a wrapper around "new SerialHubPort()" which
        attempts to auto-disconnect a prior port so that re-opening
        has a chance of succeeding.  Otherwise one tends to get a
        port already open error.
    */
    static createOneHub() {
        const oldSER = window.serPort; //Get prior stashed value
        if (oldSER) {
            console.log('Closing left over port', oldSER);
            try {
                oldSER.disconnect(); //Dispose of prior "port" if passed to us
            }
            catch (e) {
                console.error('Ignoring close error', e);
            }
            finally {
                window.serPort = null;
            }
        }
        const newSHP = new SerialHubPort();
        window.serPort = newSHP; //Stash in a global location
        return newSHP;
    }
}
//# sourceMappingURL=serialhubport.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MODULE_VERSION": () => (/* binding */ MODULE_VERSION),
/* harmony export */   "MODULE_NAME": () => (/* binding */ MODULE_NAME)
/* harmony export */ });
// Copyright (c) cdr4eelz
// Distributed under the terms of the Modified BSD License.
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
const MODULE_VERSION = data.version;
/*
 * The current package name.
 */
const MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SerialHubModel": () => (/* binding */ SerialHubModel),
/* harmony export */   "SerialHubView": () => (/* binding */ SerialHubView)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./version */ "./lib/version.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _serialhubport__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./serialhubport */ "./lib/serialhubport.js");
// Copyright (c) cdr4eelz
// Distributed under the terms of the Modified BSD License.


// Import the CSS
 //was '../css/widget.css'



class SerialHubModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: SerialHubModel.model_name, _model_module: SerialHubModel.model_module, _model_module_version: SerialHubModel.model_module_version, _view_name: SerialHubModel.view_name, _view_module: SerialHubModel.view_module, _view_module_version: SerialHubModel.view_module_version, is_supported: false, status: 'Initializing...', value: 'Loading...', request_options: {}, serial_options: {}, pkt_recv_front: [0, 0], pkt_send_front: [0, 0], pkt_recv_back: [0, 0], pkt_send_back: [0, 0] });
    }
    static get mytempid() {
        return SerialHubModel._mytempid;
    }
}
SerialHubModel._mytempid = _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.uuid();
SerialHubModel.serializers = Object.assign({}, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel.serializers
// Add any extra serializers here
);
SerialHubModel.model_name = 'SerialHubModel';
SerialHubModel.model_module = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_NAME;
SerialHubModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_VERSION;
SerialHubModel.view_name = 'SerialHubView'; // Set to null if no view
SerialHubModel.view_module = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_NAME; // Set to null if no view
SerialHubModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_VERSION;
class SerialHubView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetView {
    constructor() {
        super(...arguments);
        this._el_status = null;
        this._el_prompt = null;
        this._el_stats = null;
        this._el_value = null;
        this._shp = null;
    }
    render() {
        console.log('RENDER serialhub widget');
        this.el.id = this.id || _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.UUID.uuid4();
        this.el.classList.add('xx-serialhub-widget');
        /* Create a couple sub-Elements for our custom widget */
        this._el_status = window.document.createElement('button');
        this._el_status.classList.add('xx-serialhub-status');
        this._el_prompt = window.document.createElement('span');
        this._el_prompt.classList.add('xx-serialhub-prompt');
        this._el_stats = window.document.createElement('pre');
        this._el_stats.classList.add('xx-serialhub-stats');
        this._el_value = window.document.createElement('pre');
        this._el_value.classList.add('xx-serialhub-value');
        /* Click events wrapped to capture "this" object */
        this._el_status.onclick = (ev) => this.click_status(ev);
        this._el_value.onclick = (ev) => this.click_value(ev);
        /* Append each of the sub-components to our main widget Element */
        this.el.append(this._el_status, this._el_prompt, this._el_stats, this._el_value);
        this.changed_status();
        this.changed_value();
        this.changed_stats();
        this.update_stats_title();
        this.model.on('change:status', this.changed_status, this);
        this.model.on('change:value', this.changed_value, this);
        this.model.on('change:request_options', this.changed_request_options, this);
        this.model.on('change:serial_options', this.changed_serial_options, this);
        this.model.on('change:pkt_recv_front', this.changed_stats, this);
        this.model.on('change:pkt_recv_back', this.changed_stats, this);
        this.model.on('change:pkt_send_front', this.changed_stats, this);
        this.model.on('change:pkt_send_back', this.changed_stats, this);
        this.model.on('msg:custom', this.msg_custom, this);
        const supported = _serialhubport__WEBPACK_IMPORTED_MODULE_4__.SerialHubPort.isSupported();
        this.model.set('is_supported', supported);
        this.model.set('status', supported ? 'Supported' : 'Unsupported');
        if (supported) {
            this._el_prompt.textContent = '<<< Click to connect/disconnect a port';
        }
        this.touch();
        return this;
    }
    get_port_options() {
        return [
            this.model.get('request_options'),
            this.model.get('serial_options')
        ];
    }
    update_stats_title() {
        var _a, _b;
        const [reqOpts, serOpts] = this.get_port_options();
        let title = 'Request-Options: ' +
            JSON.stringify(reqOpts) +
            '\r\nSerial-Options: ' +
            JSON.stringify(serOpts);
        const serInfo = (_b = (_a = this._shp) === null || _a === void 0 ? void 0 : _a.port) === null || _b === void 0 ? void 0 : _b.getInfo();
        if (serInfo) {
            title += '\r\nPort-Info:' + JSON.stringify(serInfo);
        }
        if (this._el_prompt) {
            this._el_prompt.title = title;
        }
    }
    changed_request_options() {
        console.log('SET request_options:', this.model.get('request_options'));
        this.update_stats_title();
    }
    changed_serial_options() {
        console.log('SET serial_options:', this.model.get('serial_options'));
        this.update_stats_title();
    }
    changed_status() {
        if (this._el_status && this.model) {
            this._el_status.textContent = this.model.get('status');
        }
    }
    changed_value() {
        if (this._el_value && this.model) {
            this._el_value.textContent = this.model.get('value');
        }
    }
    changed_stats() {
        if (this._el_stats) {
            let stats = '';
            stats += ' RecvF:' + this.model.get('pkt_recv_front');
            stats += ' SendF:' + this.model.get('pkt_send_front');
            stats += '  (Front-End)\r\n';
            stats += ' RecvB:' + this.model.get('pkt_recv_back');
            stats += ' SendB:' + this.model.get('pkt_send_back');
            stats += '  (Back-End)';
            this._el_stats.textContent = stats;
        }
    }
    /* stats_zero set all frontend & backend stats to 0 */
    stats_zero() {
        this.model.set('pkt_recv_front', [0, 0]);
        this.model.set('pkt_send_front', [0, 0]);
        //this.model.send({ type: 'RSTS' }, {}); //Send message to reset backend stats
        this.model.set('pkt_recv_back', [0, 0]);
        this.model.set('pkt_send_back', [0, 0]);
        this.touch();
    }
    stats_inc_tuple(key, nBytes, nPackets = 1) {
        const [oByt, oPkt] = this.model.get(key);
        const nStats = [oByt + nBytes, oPkt + nPackets];
        this.model.set(key, nStats);
        this.touch();
        return nStats;
    }
    cb_read(value) {
        console.log('DATA-IN', value.length, value);
        const nStat = this.stats_inc_tuple('pkt_recv_front', value.length);
        try {
            this.model.send({ type: 'RECV', pkt_recv_front: nStat }, {}, [value]);
        }
        catch (e) {
            console.log('FAILED send of serial data to backend.', e);
            //TODO: Shutdown the reader & connection on fatal errors
            throw e; //Rethrow exception
        }
    }
    cb_connect() {
        var _a;
        console.log('cb_connect', this._shp);
        this.update_stats_title(); //Update serialPortInfo since we connected
        this.stats_zero(); //Reset statistics on fresh connection
        (_a = this._shp) === null || _a === void 0 ? void 0 : _a.readLoop((value) => {
            this.cb_read(value);
        });
        console.log('DONE cb_connect');
    }
    widget_connect() {
        this._shp = new _serialhubport__WEBPACK_IMPORTED_MODULE_4__.SerialHubPort(); //was SerialHubPort.createOneHub();
        //const reqOpts = { filters: [{usbVendorId: 0x2047}] }; // TI proper ; unused 0x0451 for "TUSB2046 Hub"
        //const serOpts = { baudRate: 115200 };
        const [reqOpts, serOpts] = this.get_port_options(); //Unpack options to local vars
        console.log('CONNECT options', reqOpts, serOpts);
        this._shp.connect(reqOpts, serOpts).then(() => {
            this.model.set('status', 'Connected');
            this.cb_connect();
        }, (reason) => {
            this.model.set('status', 'Disconnected');
            this._shp = null;
        });
    }
    widget_disconnect() {
        var _a;
        console.log('DISconnect', this, this._shp);
        (_a = this._shp) === null || _a === void 0 ? void 0 : _a.disconnect().then(() => {
            this.model.set('status', 'Disconnected');
            this._shp = null;
        }, (reason) => {
            this.model.set('status', 'Stuck');
        });
    }
    click_status(ev) {
        console.log('click_status', this, this.model, ev);
        if (this._shp) {
            this.widget_disconnect();
        }
        else {
            this.widget_connect();
        }
        console.log('click_status DONE', this._shp);
    }
    click_value(ev) {
        if (!this || !this.model) {
            return;
        }
    }
    msg_custom(mData, mBuffs) {
        //console.log(this, mData, mBuffs);
        const msgType = mData['type'];
        if (msgType === 'SEND') {
            console.log('MSG-SEND', mBuffs);
            if (this._shp) {
                const nWritten = this._shp.writeToStream(mBuffs);
                this.stats_inc_tuple('pkt_send_front', nWritten);
            }
        }
        else {
            console.log('UNKNOWN MESSAGE: ', msgType, mData, mBuffs);
        }
    }
}
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"serialhub","version":"0.0.37","description":"WebSerial widget for JupyterLab","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"homepage":"https://github.com/cdr4eelz/serialhub","bugs":{"url":"https://github.com/cdr4eelz/serialhub/issues"},"license":"BSD-3-Clause","author":{"name":"cdr4eelz","email":"1408777+cdr4eelz@users.noreply.github.com"},"files":["lib/**/*.{d.ts,eot,gif,html,jpg,js,js.map,json,png,svg,woff2,ttf}","style/**/*.{css,js,eot,gif,html,jpg,json,png,svg,woff2,ttf}","schema/*.json"],"main":"lib/index.js","types":"lib/index.d.ts","style":"style/index.css","repository":{"type":"git","url":"https://github.com/cdr4eelz/serialhub.git"},"scripts":{"build":"jlpm run build:lib && jlpm run build:labextension:dev","build:prod":"jlpm run clean && jlpm run build:lib && jlpm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack --node-env production","build:all":"jlpm run build:lib && jlpm run build:labextension:dev && jlpm run build:nbextension","webpack:help":"webpack --help","webpack:version":"webpack -v","test":"jlpm run test:pytest","test:pytest":"pytest -v","coverage":"jlpm run coverage:pytest","coverage:pytest":"pytest -vv --cov=serialhub --cov-report=term-missing serialhub/tests/","clean":"jlpm run clean:lib","clean:lib":"rimraf lib tsconfig.tsbuildinfo","clean:labextension":"rimraf serialhub/labextension","clean:nbextension":"rimraf serialhub/nbextension/static/index.js","clean:all":"jlpm run clean:lib && jlpm run clean:labextension && jlpm run clean:nbextension","eslint":"eslint . --ext .ts,.tsx --fix","eslint:check":"eslint . --ext .ts,.tsx","pylint":"pylint -v serialhub/","lint":"jlpm run lint:all","lint:all":"jlpm run eslint:check && jlpm run pylint","install:extension":"jlpm run build","watch":"run-p watch:src watch:labextension","watch:src":"tsc -w","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^2 || ^3 || ^4","@jupyterlab/application":"^3.1.0","@jupyterlab/coreutils":"^5.1.0","@jupyterlab/services":"^6.1.0","@lumino/coreutils":"^1.5.3","@lumino/widgets":"^1.19.0","lodash":"^4.17.21","minimist":"^1.2.5"},"devDependencies":{"@jupyterlab/builder":"~3.2.6","@types/backbone":"~1.4.15","@typescript-eslint/eslint-plugin":"^5.9.0","@typescript-eslint/parser":"^5.9.0","css-loader":"^6.5.1","eslint":"^8.6.0","eslint-config-prettier":"^6.15.0","eslint-plugin-prettier":"^3.1.4","mkdirp":"^1.0.4","npm-run-all":"^4.1.5","postcss":"^8.2.13","prettier":"^2.5.1","react":"^17.0.1","rimraf":"^3.0.2","source-map-loader":"^0.2.4","style-loader":"^3.3.1","ts-loader":"^9.2.6","typanion":"~3.7.1","typescript":"~4.2","webpack":"^5.65","webpack-cli":"^4.9.1","yjs":"^13.5.17"},"sideEffects":["style/*.css","style/index.js"],"styleModule":"style/index.js","publishConfig":{"access":"public"},"jupyterlab":{"sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}},"discovery":{"server":{"managers":["pip"],"base":{"name":"serialhub"}}},"extension":"lib/plugin","outputDir":"serialhub/labextension"},"jupyter-releaser":{"hooks":{"before-build-npm":["python -m pip install jupyterlab~=3.1","jlpm"]}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.fd6f21af19df40826804.js.map