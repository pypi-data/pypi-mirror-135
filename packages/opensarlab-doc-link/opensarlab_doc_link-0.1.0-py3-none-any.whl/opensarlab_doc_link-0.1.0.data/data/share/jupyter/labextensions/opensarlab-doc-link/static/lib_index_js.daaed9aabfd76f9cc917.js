"use strict";
(self["webpackChunkopensarlab_doc_link"] = self["webpackChunkopensarlab_doc_link"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var jupyterlab_topbar__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jupyterlab-topbar */ "webpack/sharing/consume/default/jupyterlab-topbar/jupyterlab-topbar");
/* harmony import */ var jupyterlab_topbar__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jupyterlab_topbar__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
// pip install jupyterlab-topbar
// jlpm add jupyterlab-topbar


class DocsAnchorWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    constructor() {
        super();
        this.hyperlink = document.createElement('a');
        this.hyperlink.text = 'OpenSARlab Docs';
        this.hyperlink.href = 'https://opensarlab-docs.asf.alaska.edu/user-guides/how_to_run_a_notebook/';
        this.hyperlink.target = 'blank';
        this.addClass('docs-anchor-widget');
        this.node.appendChild(this.hyperlink);
    }
}
const extension = {
    id: 'jupyterlab-topbar-doclink',
    autoStart: true,
    requires: [jupyterlab_topbar__WEBPACK_IMPORTED_MODULE_0__.ITopBar],
    activate: (app, topBar) => {
        const docLinkWidget = new DocsAnchorWidget();
        topBar.addItem('doc_link', docLinkWidget);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.daaed9aabfd76f9cc917.js.map