(self["webpackChunkjupyterlab_js_logs"] = self["webpackChunkjupyterlab_js_logs"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/logconsole */ "webpack/sharing/consume/default/@jupyterlab/logconsole");
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _logLevelSwitcher__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./logLevelSwitcher */ "./lib/logLevelSwitcher.js");
/* harmony import */ var _style_js_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/js.svg */ "./style/js.svg");







/**
 * The command IDs used by the js-logs plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.checkpoint = 'js-logs:checkpoint';
    CommandIDs.clear = 'js-logs:clear';
    CommandIDs.level = 'js-logs:level';
    CommandIDs.open = 'js-logs:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main jupyterlab-js-logs plugin.
 */
const extension = {
    id: 'js-logs',
    autoStart: true,
    requires: [_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.IRenderMimeRegistry],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: (app, rendermime, palette, restorer) => {
        const { commands } = app;
        let logConsolePanel = null;
        let logConsoleWidget = null;
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'jupyterlab-js-logs'
        });
        const jsIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.LabIcon({
            name: 'js-logs:js-icon',
            svgstr: _style_js_svg__WEBPACK_IMPORTED_MODULE_5__.default
        });
        const createLogConsoleWidget = () => {
            logConsolePanel = new _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__.LogConsolePanel(new _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__.LoggerRegistry({
                defaultRendermime: rendermime,
                maxLength: 1000
            }));
            logConsolePanel.source = 'js-logs';
            logConsoleWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                content: logConsolePanel
            });
            logConsoleWidget.addClass('jp-LogConsole');
            logConsoleWidget.title.label = 'Dev Tools Console Logs';
            logConsoleWidget.title.icon = jsIcon;
            logConsoleWidget.toolbar.addItem('checkpoint', new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButton({
                commands,
                id: CommandIDs.checkpoint
            }));
            logConsoleWidget.toolbar.addItem('clear', new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButton({
                commands,
                id: CommandIDs.clear
            }));
            logConsoleWidget.toolbar.addItem('level', new _logLevelSwitcher__WEBPACK_IMPORTED_MODULE_6__.default(logConsoleWidget.content));
            logConsoleWidget.disposed.connect(() => {
                logConsoleWidget = null;
                logConsolePanel = null;
                commands.notifyCommandChanged();
            });
            app.shell.add(logConsoleWidget, 'main', { mode: 'split-bottom' });
            void tracker.add(logConsoleWidget);
            logConsoleWidget.update();
            commands.notifyCommandChanged();
        };
        commands.addCommand(CommandIDs.checkpoint, {
            execute: () => { var _a; return (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.checkpoint(); },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.addIcon,
            isEnabled: () => (logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.source) !== null,
            label: 'Add Checkpoint'
        });
        commands.addCommand(CommandIDs.clear, {
            execute: () => { var _a; return (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.clear(); },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.clearIcon,
            isEnabled: () => (logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.source) !== null,
            label: 'Clear Log'
        });
        commands.addCommand(CommandIDs.level, {
            execute: (args) => {
                if (logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) {
                    logConsolePanel.logger.level = args.level;
                }
            },
            isEnabled: () => (logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.source) !== null,
            label: args => `Set Log Level to ${args.level}`
        });
        commands.addCommand(CommandIDs.open, {
            label: 'Show Dev Tools Console Logs',
            caption: 'Show Dev Tools Console Logs',
            isToggled: () => logConsoleWidget !== null,
            execute: () => {
                if (logConsoleWidget) {
                    logConsoleWidget.dispose();
                }
                else {
                    createLogConsoleWidget();
                }
            }
        });
        window.onerror = (msg, url, lineNo, columnNo, error) => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.log({
                type: 'text',
                level: 'critical',
                data: `${url}:${lineNo} ${msg}\n${error}`
            });
            return false;
        };
        const _debug = console.debug;
        const _log = console.log;
        const _info = console.info;
        const _warn = console.warn;
        const _error = console.error;
        const _exception = console.exception;
        const _trace = console.trace;
        const _table = console.table;
        // https://stackoverflow.com/a/11616993
        // We need to clear cache after each use.
        let cache = [];
        const refReplacer = (key, value) => {
            if (typeof value === 'object' && value !== null) {
                if (cache.indexOf(value) !== -1) {
                    return;
                }
                cache.push(value);
            }
            return value;
        };
        const parseArgs = (args) => {
            let data = '';
            args.forEach(arg => {
                try {
                    data +=
                        (typeof arg === 'object' && arg !== null
                            ? JSON.stringify(arg)
                            : arg) + ' ';
                }
                catch (e) {
                    try {
                        const msg = 'This error contains a object with a circular reference. Duplicated attributes might have been dropped during the process of removing the reference.\n';
                        const obj = JSON.stringify(arg, refReplacer);
                        cache = [];
                        console.error(msg, obj);
                        data += obj;
                    }
                    catch (e) {
                        data += ' ';
                    }
                }
            });
            return data;
        };
        window.console.debug = (...args) => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.log({
                type: 'text',
                level: 'debug',
                data: parseArgs(args)
            });
            _debug(...args);
        };
        window.console.log = (...args) => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.log({
                type: 'text',
                level: 'debug',
                data: parseArgs(args)
            });
            _log(...args);
        };
        window.console.info = (...args) => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.log({
                type: 'text',
                level: 'info',
                data: parseArgs(args)
            });
            _info(...args);
        };
        window.console.warn = (...args) => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.log({
                type: 'text',
                level: 'warning',
                data: parseArgs(args)
            });
            _warn(...args);
        };
        window.console.error = (...args) => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.log({
                type: 'text',
                level: 'critical',
                data: parseArgs(args)
            });
            _error(...args);
        };
        window.console.exception = (message, ...args) => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.log({
                type: 'text',
                level: 'critical',
                data: `Exception: ${message}\n${parseArgs(args)}`
            });
            _exception(...args);
        };
        window.console.trace = (...args) => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.log({
                type: 'text',
                level: 'info',
                data: parseArgs(args)
            });
            _trace(...args);
        };
        window.console.table = (...args) => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.log({
                type: 'text',
                level: 'info',
                data: parseArgs(args)
            });
            _table(...args);
        };
        if (palette) {
            palette.addItem({
                command: CommandIDs.open,
                category: 'Developer'
            });
        }
        if (restorer) {
            restorer.restore(tracker, {
                command: CommandIDs.open,
                name: () => 'js-logs'
            });
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/logLevelSwitcher.js":
/*!*********************************!*\
  !*** ./lib/logLevelSwitcher.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ LogLevelSwitcher)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);




/**
 * A toolbar widget that switches log levels.
 */
class LogLevelSwitcher extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    /**
     * Construct a new cell type switcher.
     *
     * @param widget The log console panel
     */
    constructor(widget) {
        super();
        /**
         * Handle `change` events for the HTMLSelect component.
         *
         * @param event The HTML select event.
         */
        this.handleChange = (event) => {
            if (this._logConsole.logger) {
                this._logConsole.logger.level = event.target.value;
            }
            this.update();
        };
        /**
         * Handle `keydown` events for the HTMLSelect component.
         *
         * @param event The keyboard event.
         */
        this.handleKeyDown = (event) => {
            if (event.keyCode === 13) {
                this._logConsole.activate();
            }
        };
        this._id = `level-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.UUID.uuid4()}`;
        this.addClass('jp-LogConsole-toolbarLogLevel');
        this._logConsole = widget;
        this._logConsole.logger.level = 'debug';
        if (widget.source) {
            this.update();
        }
        widget.sourceChanged.connect(this._updateSource, this);
    }
    _updateSource(sender, { oldValue, newValue }) {
        // Transfer stateChanged handler to new source logger
        if (oldValue !== null) {
            const logger = sender.loggerRegistry.getLogger(oldValue);
            logger.stateChanged.disconnect(this.update, this);
        }
        if (newValue !== null) {
            const logger = sender.loggerRegistry.getLogger(newValue);
            logger.stateChanged.connect(this.update, this);
        }
        this.update();
    }
    render() {
        const logger = this._logConsole.logger;
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement((react__WEBPACK_IMPORTED_MODULE_3___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("label", { htmlFor: this._id, className: logger === null
                    ? 'jp-LogConsole-toolbarLogLevel-disabled'
                    : undefined }, "Log Level:"),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.HTMLSelect, { id: this._id, className: "jp-LogConsole-toolbarLogLevelDropdown", onChange: this.handleChange, onKeyDown: this.handleKeyDown, value: logger === null || logger === void 0 ? void 0 : logger.level, "aria-label": "Log level", disabled: logger === null, options: logger === null
                    ? []
                    : [
                        'Critical',
                        'Error',
                        'Warning',
                        'Info',
                        'Debug'
                    ].map(label => ({ label, value: label.toLowerCase() })) })));
    }
}


/***/ }),

/***/ "./style/js.svg":
/*!**********************!*\
  !*** ./style/js.svg ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 630 630\">\n<rect width=\"630\" height=\"630\" fill=\"#f7df1e\"/>\n<path d=\"m423.2 492.19c12.69 20.72 29.2 35.95 58.4 35.95 24.53 0 40.2-12.26 40.2-29.2 0-20.3-16.1-27.49-43.1-39.3l-14.8-6.35c-42.72-18.2-71.1-41-71.1-89.2 0-44.4 33.83-78.2 86.7-78.2 37.64 0 64.7 13.1 84.2 47.4l-46.1 29.6c-10.15-18.2-21.1-25.37-38.1-25.37-17.34 0-28.33 11-28.33 25.37 0 17.76 11 24.95 36.4 35.95l14.8 6.34c50.3 21.57 78.7 43.56 78.7 93 0 53.3-41.87 82.5-98.1 82.5-54.98 0-90.5-26.2-107.88-60.54zm-209.13 5.13c9.3 16.5 17.76 30.45 38.1 30.45 19.45 0 31.72-7.61 31.72-37.2v-201.3h59.2v202.1c0 61.3-35.94 89.2-88.4 89.2-47.4 0-74.85-24.53-88.81-54.075z\"/>\n</svg>");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.28d635131a21b65e54b4.js.map