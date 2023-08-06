(self["webpackChunkjupyterlab_myst"] = self["webpackChunkjupyterlab_myst"] || []).push([["lib_index_js"],{

/***/ "./lib/blocks.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "blocks": () => (/* binding */ blocks)
/* harmony export */ });
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @agoose77/jupyterlab-markup */ "webpack/sharing/consume/default/@agoose77/jupyterlab-markup/@agoose77/jupyterlab-markup");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");


function blocksPlugin(md, options) {
    // TODO
}
/**
 * Provides text-based diagrams in code plugin
 */
const blocks = (0,_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__.simpleMarkdownItPlugin)(_tokens__WEBPACK_IMPORTED_MODULE_1__.PACKAGE_NS, {
    id: 'markdown-it-diagrams',
    title: 'Diagrams',
    description: 'Diagrams in code plugin from mermaid and svgbob',
    documentationUrls: {
        Plugin: 'https://github.com/agoose77/markdown-it-diagrams',
        MermaidJS: 'https://mermaid-js.github.io/mermaid',
        svgbob: 'https://github.com/ivanceras/svgbob'
    },
    examples: {
        'MyST ': '```{directive}\n' + ':option: value\n' + '\n' + 'content\n' + '```'
    },
    plugin: async () => {
        return [blocksPlugin];
    }
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "blocks": () => (/* reexport safe */ _blocks__WEBPACK_IMPORTED_MODULE_0__.blocks)
/* harmony export */ });
/* harmony import */ var _blocks__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./plugin */ "./lib/blocks.js");



/***/ }),

/***/ "./lib/tokens.js":
/*!***********************!*\
  !*** ./lib/tokens.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PACKAGE_NS": () => (/* binding */ PACKAGE_NS)
/* harmony export */ });
/**
 * The ID stem for all plugins
 */
const PACKAGE_NS = '@agoose77/jupyterlab-markup';


/***/ })

}]);
//# sourceMappingURL=lib_index_js.0fd7816ddad0d229519a.js.map
