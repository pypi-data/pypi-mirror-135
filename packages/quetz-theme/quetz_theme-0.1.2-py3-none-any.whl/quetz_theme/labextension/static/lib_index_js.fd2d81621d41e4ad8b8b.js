"use strict";
(self["webpackChunkquetz_theme"] = self["webpackChunkquetz_theme"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * Initialization data for the quetz-theme extension.
 */
const extension = {
    id: 'quetz-theme',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    autoStart: true,
    activate: (app, manager) => {
        const style = 'quetz-theme/index.css';
        manager.register({
            name: 'Quetz',
            isLight: false,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.fd2d81621d41e4ad8b8b.js.map