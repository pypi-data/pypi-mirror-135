(self["webpackChunkjupyterlab_myst"] = self["webpackChunkjupyterlab_myst"] || []).push([["lib_index_js"],{

/***/ "./lib/builtins/amsmath.js":
/*!*********************************!*\
  !*** ./lib/builtins/amsmath.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "amsmath": () => (/* binding */ amsmath)
/* harmony export */ });
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @agoose77/jupyterlab-markup */ "webpack/sharing/consume/default/@agoose77/jupyterlab-markup");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../tokens */ "./lib/tokens.js");


/**
 * Provides amsmath support
 */
const amsmath = (0,_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__.simpleMarkdownItPlugin)(_tokens__WEBPACK_IMPORTED_MODULE_1__.PACKAGE_NS, {
    id: 'markdown-it-amsmath',
    title: 'amsmath',
    description: 'Plugin for amsmath LaTeX environments',
    documentationUrls: {
        Plugin: 'https://github.com/executablebooks/markdown-it-amsmath'
    },
    examples: {
        'Example ': '\\begin{equation}\na = 1\n\\end{equation}'
    },
    plugin: async () => {
        const amsmathPlugin = await __webpack_require__.e(/*! import() | markdown-it-amsmath */ "markdown-it-amsmath").then(__webpack_require__.t.bind(__webpack_require__, /*! markdown-it-amsmath */ "webpack/sharing/consume/default/markdown-it-amsmath/markdown-it-amsmath", 23));
        return [amsmathPlugin.default];
    }
});


/***/ }),

/***/ "./lib/builtins/docutils.js":
/*!**********************************!*\
  !*** ./lib/builtins/docutils.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "docutils": () => (/* binding */ docutils)
/* harmony export */ });
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @agoose77/jupyterlab-markup */ "webpack/sharing/consume/default/@agoose77/jupyterlab-markup");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../tokens */ "./lib/tokens.js");


/**
 * Provides docutils roles and directives
 */
const docutils = (0,_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__.simpleMarkdownItPlugin)(_tokens__WEBPACK_IMPORTED_MODULE_1__.PACKAGE_NS, {
    id: 'markdown-it-docutils',
    title: 'Docutils',
    description: 'Plugin for implementing docutils style roles (inline extension point) and directives (block extension point)',
    documentationUrls: {
        Plugin: 'https://github.com/executablebooks/markdown-it-docutils'
    },
    examples: {
        'Example ': '```{name} argument\n:option: value\n\ncontent\n```'
    },
    plugin: async () => {
        const docutilsPlugin = await __webpack_require__.e(/*! import() | markdown-it-docutils */ "markdown-it-docutils").then(__webpack_require__.t.bind(__webpack_require__, /*! markdown-it-docutils */ "webpack/sharing/consume/default/markdown-it-docutils", 23));
        return [docutilsPlugin.default];
    }
});


/***/ }),

/***/ "./lib/builtins/front-matter.js":
/*!**************************************!*\
  !*** ./lib/builtins/front-matter.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "frontMatter": () => (/* binding */ frontMatter)
/* harmony export */ });
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @agoose77/jupyterlab-markup */ "webpack/sharing/consume/default/@agoose77/jupyterlab-markup");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../tokens */ "./lib/tokens.js");


/**
 * Provides front-matter support
 */
const frontMatter = (0,_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__.simpleMarkdownItPlugin)(_tokens__WEBPACK_IMPORTED_MODULE_1__.PACKAGE_NS, {
    id: 'markdown-it-front-matter',
    title: 'Front Matter',
    description: 'Plugin for processing front matter for markdown-it markdown parser',
    documentationUrls: {
        Plugin: 'https://github.com/ParkSB/markdown-it-front-matter'
    },
    examples: {
        'Example ': '---\nvalid-front-matter: true\n---'
    },
    plugin: async () => {
        const frontMatterPlugin = await __webpack_require__.e(/*! import() | markdown-it-front-matter */ "markdown-it-front-matter").then(__webpack_require__.t.bind(__webpack_require__, /*! markdown-it-front-matter */ "webpack/sharing/consume/default/markdown-it-front-matter/markdown-it-front-matter", 23));
        function handleMarkup(markup) {
            // Do nothing for now
        }
        function plugin(md, options) {
            frontMatterPlugin.default(md, handleMarkup);
        }
        return [plugin];
    }
});


/***/ }),

/***/ "./lib/builtins/index.js":
/*!*******************************!*\
  !*** ./lib/builtins/index.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BUILTINS": () => (/* binding */ BUILTINS)
/* harmony export */ });
/* harmony import */ var _front_matter__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./front-matter */ "./lib/builtins/front-matter.js");
/* harmony import */ var _docutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./docutils */ "./lib/builtins/docutils.js");
/* harmony import */ var _amsmath__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./amsmath */ "./lib/builtins/amsmath.js");
/* harmony import */ var _myst_extras__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./myst-extras */ "./lib/builtins/myst-extras.js");




/**
 * Builtin plugins provided by this labextension
 */
const BUILTINS = [_front_matter__WEBPACK_IMPORTED_MODULE_0__.frontMatter, _docutils__WEBPACK_IMPORTED_MODULE_1__.docutils, _amsmath__WEBPACK_IMPORTED_MODULE_2__.amsmath, _myst_extras__WEBPACK_IMPORTED_MODULE_3__.mystExtras];


/***/ }),

/***/ "./lib/builtins/myst-extras.js":
/*!*************************************!*\
  !*** ./lib/builtins/myst-extras.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "mystExtras": () => (/* binding */ mystExtras)
/* harmony export */ });
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @agoose77/jupyterlab-markup */ "webpack/sharing/consume/default/@agoose77/jupyterlab-markup");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../tokens */ "./lib/tokens.js");


/**
 * Provides extra MyST support
 */
const mystExtras = (0,_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__.simpleMarkdownItPlugin)(_tokens__WEBPACK_IMPORTED_MODULE_1__.PACKAGE_NS, {
    id: 'markdown-it-myst-extras',
    title: 'MyST Extras',
    description: 'Additional markdown-it plugins required for the MyST specification',
    documentationUrls: {
        Plugin: 'https://github.com/executablebooks/markdown-it-myst-extras'
    },
    examples: {
        Blockquotes: '% comment',
        'Block Breaks': '+++',
        'MyST Targets': '(name)='
    },
    plugin: async () => {
        const mystExtrasPlugin = await __webpack_require__.e(/*! import() | markdown-it-myst-extras */ "markdown-it-myst-extras").then(__webpack_require__.t.bind(__webpack_require__, /*! markdown-it-myst-extras */ "webpack/sharing/consume/default/markdown-it-myst-extras/markdown-it-myst-extras", 23));
        return [mystExtrasPlugin.mystBlockPlugin];
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
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _builtins__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./builtins */ "./lib/builtins/index.js");

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_builtins__WEBPACK_IMPORTED_MODULE_0__.BUILTINS);


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
const PACKAGE_NS = 'executablebooks/jupyterlab-markup';


/***/ })

}]);
//# sourceMappingURL=lib_index_js.80a2b6f9942bb1f43e2f.js.map