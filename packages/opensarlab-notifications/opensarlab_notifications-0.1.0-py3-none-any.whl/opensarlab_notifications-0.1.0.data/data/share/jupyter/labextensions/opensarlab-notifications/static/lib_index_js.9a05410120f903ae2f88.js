"use strict";
(self["webpackChunkopensarlab_notifications"] = self["webpackChunkopensarlab_notifications"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "webpack/sharing/consume/default/jquery/jquery?322d");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var toastr__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! toastr */ "webpack/sharing/consume/default/toastr/toastr");
/* harmony import */ var toastr__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(toastr__WEBPACK_IMPORTED_MODULE_1__);


const extension = {
    id: 'jupyterlab-topbar-opensarlab-notifications',
    autoStart: true,
    activate: async (app) => {
        try {
            let toastrLink = document.createElement('link');
            toastrLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css';
            toastrLink.rel = 'stylesheet';
            document.head.appendChild(toastrLink);
            jquery__WEBPACK_IMPORTED_MODULE_0___default()(document).ready(function () {
                (toastr__WEBPACK_IMPORTED_MODULE_1___default().options) = {
                    "closeButton": true,
                    "newestOnTop": true,
                    "progressBar": true,
                    "positionClass": "toast-top-right",
                    "preventDuplicates": false,
                    "onclick": null,
                    "showDuration": 30,
                    "hideDuration": 1,
                    "timeOut": 0,
                    "extendedTimeOut": 0,
                    "showEasing": "swing",
                    "hideEasing": "linear",
                    "showMethod": "fadeIn",
                    "hideMethod": "fadeOut"
                };
                fetch(window.location.origin + '/opensarlab-notifications/notifications')
                    .then(response => response.json())
                    .then(notes => {
                    console.log(notes);
                    notes['data'].forEach(function (entry) {
                        (toastr__WEBPACK_IMPORTED_MODULE_1___default())[entry.type](entry.message, entry.title);
                    });
                })
                    .catch(error => console.log(error));
            });
        }
        catch (reason) {
            console.error(`Error on GET /opensarlab-notifications/notifications.\n${reason}`);
        }
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.9a05410120f903ae2f88.js.map