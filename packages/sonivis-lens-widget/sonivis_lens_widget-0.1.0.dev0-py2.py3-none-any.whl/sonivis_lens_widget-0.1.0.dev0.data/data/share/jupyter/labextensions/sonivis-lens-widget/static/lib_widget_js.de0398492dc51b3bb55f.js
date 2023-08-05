(self["webpackChunksonivis_lens_widget"] = self["webpackChunksonivis_lens_widget"] || []).push([["lib_widget_js"],{

/***/ "./lib/lensCursor.js":
/*!***************************!*\
  !*** ./lib/lensCursor.js ***!
  \***************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Alexander Rind & the SoniVis team.
// Distributed under the terms of the MIT License (see LICENSE.txt).
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.removeLensCursor = exports.LensCursor = void 0;
const d3 = __importStar(__webpack_require__(/*! d3 */ "webpack/sharing/consume/default/d3/d3"));
const DEFAULT_OPACITY = 0.3;
class LensCursor {
    constructor(view, gPlot, areaWidth, areaHeight) {
        this.smallerSize = 100;
        this.transform = (x, y) => {
            return { x, y };
        };
        this.view = view;
        this.smallerSize = Math.min(areaWidth, areaHeight);
        this.selLens = gPlot
            .append('g')
            .classed('cursor lens', true)
            .style('opacity', 0)
            .attr('transform', 'translate(0, 0)');
        this.updateLensShape();
        this.view.model.on('change:shape', () => this.updateLensShape(), this.view);
        this.updateLensDiameter();
        this.view.model.on('change:diameter', () => this.updateLensDiameter(), this.view);
        // add invisible rect to track mouse position (as last svg element)
        gPlot
            .append('rect')
            .classed('cursor overlay', true)
            .attr('x', 0)
            .attr('width', areaWidth)
            .attr('y', 0)
            .attr('height', areaHeight)
            // .on('touchstart', (event) => event.preventDefault())
            .on('mouseenter', () => {
            this.selLens.style('opacity', DEFAULT_OPACITY);
        })
            .on('mouseleave', () => {
            this.selLens.style('opacity', 0);
        })
            .on('wheel', (evt) => {
            evt.preventDefault();
            const oldDiameter = this.view.model.get('diameter');
            const scaledDiameter = oldDiameter * Math.pow(1.25, evt.deltaY / -100);
            const newDiameter = Math.min(1, Math.max(0.01, scaledDiameter));
            //   console.log(evt, newDiameter);
            this.view.model.set('diameter', newDiameter);
            this.view.model.save_changes();
        })
            .on('mousemove', (evt) => {
            const rawX = d3.pointer(evt)[0];
            const rawY = d3.pointer(evt)[1];
            // circle.attr('cx', rawX).attr('cy', rawY);
            this.selLens.attr('transform', `translate(${rawX}, ${rawY})`);
        })
            // .on('mousedown touchstart', mousedown);
            .on('pointerdown', (evt) => {
            evt.preventDefault();
            // recover coordinate we need
            const rawX = d3.pointer(evt)[0];
            const rawY = d3.pointer(evt)[1];
            if (rawX < 0 || rawY < 0) {
                return;
            }
            // delegate coordinate transformations to caller
            const center = this.transform(rawX, rawY);
            // console.log(center);
            // TODO assumption of a linear scale
            const corner = this.transform(rawX + this.rPixels, rawY - this.rPixels);
            view.send(Object.assign(Object.assign({ event: 'lens' }, center), { edgeX: corner.x, edgeY: corner.y }));
        });
        // TODO change lense diameter by multi-touch cp. <https://observablehq.com/@d3/multitouch#cell-308>
    }
    updateLensDiameter() {
        const diameter = this.view.model.get('diameter');
        // console.log('client swidth ', this.smallerSize);
        this.rPixels = (diameter * this.smallerSize) / 2.0;
        // this.selLens.attr('r', this.rPixels);
        // console.log(this.selLens.selectAll('*'));
        this.selLens.selectAll('*').attr('transform', `scale(${this.rPixels})`);
    }
    updateLensShape() {
        //   this.selLens.html('');
        if (this.view.model.get('shape') === 'circle') {
            this.selLens.html(`<circle r="1" cx="0", cy="0" transform="scale(${this.rPixels})"/>`);
        }
        else if (this.view.model.get('shape') === 'square') {
            this.selLens.html(`<rect x="-1" y="-1" width="2" height="2" transform="scale(${this.rPixels})"/>`);
        }
    }
}
exports.LensCursor = LensCursor;
function removeLensCursor(gPlot) {
    gPlot.selectAll('.cursor').remove();
}
exports.removeLensCursor = removeLensCursor;
//# sourceMappingURL=lensCursor.js.map

/***/ }),

/***/ "./lib/scatterPlot.js":
/*!****************************!*\
  !*** ./lib/scatterPlot.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Alexander Rind & the SoniVis team.
// Distributed under the terms of the MIT License (see LICENSE.txt).
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ScatterPlot = void 0;
const d3 = __importStar(__webpack_require__(/*! d3 */ "webpack/sharing/consume/default/d3/d3"));
const lensCursor_1 = __webpack_require__(/*! ./lensCursor */ "./lib/lensCursor.js");
const width = 400;
const height = 400;
const MARGIN = { top: 20, right: 10, bottom: 30, left: 30 };
const RADIUS = 2;
class ScatterPlot {
    constructor(view) {
        const g = d3
            .select(view.el)
            .append('svg')
            .attr('width', width + MARGIN.left + MARGIN.right)
            .attr('height', height + MARGIN.top + MARGIN.bottom)
            .append('g')
            .classed('substrate', true)
            .attr('transform', 'translate(' + MARGIN.left + ',' + MARGIN.top + ')');
        // set the scales
        const x = prepareScale([], [0, width]);
        const y = prepareScale([], [height, 0]);
        // add the X Axis
        g.append('g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x));
        // add the Y axis
        g.append('g').attr('class', 'y axis').call(d3.axisLeft(y));
        this.lensCursor = new lensCursor_1.LensCursor(view, g, width, height);
        console.log('end constr');
    }
    updateScatterPlot(view) {
        console.log('%% updated scatter ');
        const xValues = view.model.get('_marks_x');
        const yValues = view.model.get('_marks_y');
        // set the scales
        const xScale = prepareScale(xValues, [0, width]);
        const yScale = prepareScale(yValues, [height, 0]);
        this.lensCursor.transform = (x, y) => {
            return { x: xScale.invert(x), y: yScale.invert(y) };
        };
        // console.log('%% length x: ' + xValues.length + ' , y: ' + yValues.length);
        const gSubstrate = d3.select(view.el).select('g.substrate');
        // add the scatterplot without data transformations
        // <https://stackoverflow.com/a/17872039/1140589>
        gSubstrate
            .selectAll('circle.dot')
            .data(xValues.length < yValues.length ? xValues : yValues)
            .join('circle')
            .classed('dot', true)
            .attr('r', RADIUS)
            .attr('cx', (d, i) => xScale(xValues[i]))
            .attr('cy', (d, i) => yScale(yValues[i]));
        // update the X Axis
        gSubstrate.select('.x.axis').call(d3.axisBottom(xScale));
        gSubstrate
            .selectAll('.x.label')
            .data([view.model.get('x_field')])
            .join('text')
            .attr('class', 'x label')
            // .attr("transform", "rotate(-90)")
            .attr('y', height + 26)
            .attr('x', width + MARGIN.right)
            .style('text-anchor', 'end')
            .text((d) => d);
        // update the Y axis
        gSubstrate.select('.y.axis').call(d3.axisLeft(yScale));
        gSubstrate
            .selectAll('.y.label')
            .data([view.model.get('y_field')])
            .join('text')
            .attr('class', 'y label')
            // .attr("transform", "rotate(-90)")
            .attr('y', -8)
            .attr('x', -MARGIN.left)
            .style('text-anchor', 'start')
            .text((d) => d);
    }
}
exports.ScatterPlot = ScatterPlot;
function prepareScale(values, range) {
    const xMin = d3.min(values) || 0;
    const xMax = d3.max(values) || 1;
    // console.log('%% domain: [' + xMin + ' ,' + xMax + ']');
    const space = (xMax - xMin) * 0.05;
    const xSpacedMin = xMin - space < 0 && xMin >= 0 ? 0 : xMin - space;
    return d3
        .scaleLinear()
        .range(range)
        .domain([xSpacedMin, xMax + space]);
}
//# sourceMappingURL=scatterPlot.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Alexander Rind & the SoniVis team.
// Distributed under the terms of the MIT License (see LICENSE.txt).
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Alexander Rind & the SoniVis team.
// Distributed under the terms of the MIT License (see LICENSE.txt).
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.LensView = exports.LensModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
const scatterPlot_1 = __webpack_require__(/*! ./scatterPlot */ "./lib/scatterPlot.js");
class LensModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: LensModel.model_name, _model_module: LensModel.model_module, _model_module_version: LensModel.model_module_version, _view_name: LensModel.view_name, _view_module: LensModel.view_module, _view_module_version: LensModel.view_module_version, x_field: '', y_field: '', _marks_x: [], _marks_y: [], diameter: 0.1, shape: 'circle' });
    }
}
exports.LensModel = LensModel;
LensModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
LensModel.model_name = 'LensModel';
LensModel.model_module = version_1.MODULE_NAME;
LensModel.model_module_version = version_1.MODULE_VERSION;
LensModel.view_name = 'LensView'; // Set to null if no view
LensModel.view_module = version_1.MODULE_NAME; // Set to null if no view
LensModel.view_module_version = version_1.MODULE_VERSION;
class LensView extends base_1.DOMWidgetView {
    render() {
        this.scatterPlot = new scatterPlot_1.ScatterPlot(this);
        this.value_changed();
        this.model.on('change:_marks_x', this.value_changed, this);
        this.model.on('change:_marks_y', this.value_changed, this);
    }
    value_changed() {
        // console.log('field ' + this.model.get('x_field'));
        // console.log(this.model.get('_marks_x'));
        this.scatterPlot.updateScatterPlot(this);
    }
}
exports.LensView = LensView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".custom-widget {\n  background-color: lightseagreen;\n  padding: 0px 2px;\n}\n\n.substrate .label {\n  font-size: 10px;\n  font-family: sans-serif;\n  color: #404040;\n}\n\n.substrate .axis {\n  font-size: 10px;\n  font-family: sans-serif;\n  color: #404040;\n}\n\n.substrate {\n  pointer-events: none;\n}\n\n.cursor.overlay {\n  pointer-events: all;\n  fill: none;\n  cursor: crosshair;\n  shape-rendering: auto;\n}\n\n.cursor.lens * {\n  stroke: none;\n  fill: rgb(0, 0, 165);\n  /* opacity: 0; */\n}\n\n.cursor.lens.active {\n  stroke: none;\n  fill: rgb(165, 0, 0);\n  opacity: 0;\n}\n", "",{"version":3,"sources":["webpack://./css/widget.css"],"names":[],"mappings":"AAAA;EACE,+BAA+B;EAC/B,gBAAgB;AAClB;;AAEA;EACE,eAAe;EACf,uBAAuB;EACvB,cAAc;AAChB;;AAEA;EACE,eAAe;EACf,uBAAuB;EACvB,cAAc;AAChB;;AAEA;EACE,oBAAoB;AACtB;;AAEA;EACE,mBAAmB;EACnB,UAAU;EACV,iBAAiB;EACjB,qBAAqB;AACvB;;AAEA;EACE,YAAY;EACZ,oBAAoB;EACpB,gBAAgB;AAClB;;AAEA;EACE,YAAY;EACZ,oBAAoB;EACpB,UAAU;AACZ","sourcesContent":[".custom-widget {\n  background-color: lightseagreen;\n  padding: 0px 2px;\n}\n\n.substrate .label {\n  font-size: 10px;\n  font-family: sans-serif;\n  color: #404040;\n}\n\n.substrate .axis {\n  font-size: 10px;\n  font-family: sans-serif;\n  color: #404040;\n}\n\n.substrate {\n  pointer-events: none;\n}\n\n.cursor.overlay {\n  pointer-events: all;\n  fill: none;\n  cursor: crosshair;\n  shape-rendering: auto;\n}\n\n.cursor.lens * {\n  stroke: none;\n  fill: rgb(0, 0, 165);\n  /* opacity: 0; */\n}\n\n.cursor.lens.active {\n  stroke: none;\n  fill: rgb(165, 0, 0);\n  opacity: 0;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";

      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }

      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }

      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }

      content += cssWithMappingToString(item);

      if (needLayer) {
        content += "}";
      }

      if (item[2]) {
        content += "}";
      }

      if (item[4]) {
        content += "}";
      }

      return content;
    }).join("");
  }; // import a list of modules into the list


  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }

      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }

      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }

      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }

      list.push(item);
    }
  };

  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {

"use strict";


module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || "").concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join("\n");
  }

  return [content].join("\n");
};

/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"sonivis-lens-widget","version":"0.1.0","description":"jupyter notebook widget with a scatter plot and an interactive lens","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/fhstp/sonivis-lens-widget","bugs":{"url":"https://github.com/fhstp/sonivis-lens-widget/issues"},"license":"MIT","author":{"name":"Alexander Rind","url":"https://github.com/alex-rind/"},"contributors":[],"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/fhstp/sonivis-lens-widget"},"scripts":{"build":"npm run build:lib && npm run build:nbextension && npm run build:labextension:dev","build:prod":"npm run build:lib && npm run build:nbextension && npm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"npm run clean:lib && npm run clean:nbextension && npm run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf sonivis_lens_widget/labextension","clean:nbextension":"rimraf sonivis_lens_widget/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"npm run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","d3":"^7.2.1"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/d3":"^7.1.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^6.5.1","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"sonivis_lens_widget/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.de0398492dc51b3bb55f.js.map