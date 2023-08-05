/**
 * Django Image Uploader Widget - An image uploader widget for django.
 * @version v0.1.3
 * @author Eduardo Oliveira (EduardoJM) <eduardo_y05@outlook.com>.
 * @link https://github.com/inventare/django-image-uploader-widget
 * 
 * Licensed under the MIT License (https://github.com/inventare/django-image-uploader-widget/blob/main/LICENSE).
 */

"use strict";

function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var ImageUploaderInline = /*#__PURE__*/function () {
  function ImageUploaderInline(_element) {
    var _this = this;

    _classCallCheck(this, ImageUploaderInline);

    _defineProperty(this, "element", void 0);

    _defineProperty(this, "inlineGroup", void 0);

    _defineProperty(this, "inlineFormset", void 0);

    _defineProperty(this, "tempFileInput", null);

    _defineProperty(this, "next", 0);

    _defineProperty(this, "dragging", false);

    _defineProperty(this, "canPreview", true);

    _defineProperty(this, "onDrop", function (e) {
      var _e$dataTransfer;

      e.preventDefault();
      _this.dragging = false;

      _this.element.classList.remove('drop-zone');

      if ((_e$dataTransfer = e.dataTransfer) !== null && _e$dataTransfer !== void 0 && _e$dataTransfer.files.length) {
        var _iterator = _createForOfIteratorHelper(e.dataTransfer.files),
            _step;

        try {
          for (_iterator.s(); !(_step = _iterator.n()).done;) {
            var file = _step.value;

            _this.addFile(file);
          }
        } catch (err) {
          _iterator.e(err);
        } finally {
          _iterator.f();
        }
      }
    });

    _defineProperty(this, "onDragEnter", function () {
      _this.dragging = true;

      _this.element.classList.add('drop-zone');
    });

    _defineProperty(this, "onDragOver", function (e) {
      if (e) {
        e.preventDefault();
      }
    });

    _defineProperty(this, "onDragLeave", function (e) {
      if (e.relatedTarget && e.relatedTarget.closest('.iuw-inline-root') === _this.element) {
        return;
      }

      _this.dragging = false;

      _this.element.classList.remove('drop-zone');
    });

    _defineProperty(this, "onRelatedItemClick", function (e) {
      if (!e || !e.target) {
        return;
      }

      var target = e.target;
      var item = target.closest('.inline-related');

      if (target.closest('.iuw-delete-icon')) {
        if (item !== null && item !== void 0 && item.getAttribute('data-raw')) {
          item === null || item === void 0 ? void 0 : item.classList.add('deleted');
          var checkboxInput = item.querySelector('input[type=checkbox]');
          checkboxInput.checked = true;
        } else {
          var _item$parentElement;

          item === null || item === void 0 ? void 0 : (_item$parentElement = item.parentElement) === null || _item$parentElement === void 0 ? void 0 : _item$parentElement.removeChild(item);
        }

        _this.updateEmpty();

        return;
      }

      if (target.closest('.iuw-preview-icon')) {
        var image = item === null || item === void 0 ? void 0 : item.querySelector('img');

        if (image) {
          image = image.cloneNode(true);

          var modal = _this.createPreviewModal(image);

          setTimeout(function () {
            modal.classList.add('visible');
            modal.classList.remove('hide');
            document.body.style.overflow = 'hidden';
          }, 50);
          return;
        }
      }

      var fileInput = item === null || item === void 0 ? void 0 : item.querySelector('input[type=file]');

      if (e.target === fileInput) {
        return;
      }

      fileInput === null || fileInput === void 0 ? void 0 : fileInput.click();
    });

    _defineProperty(this, "onFileInputChange", function (e) {
      var _target$closest;

      var target = e.target;

      if (target.tagName !== 'INPUT') {
        return;
      }

      var fileInput = target;
      var files = fileInput.files;

      if (!(files !== null && files !== void 0 && files.length)) {
        return;
      }

      var imgTag = (_target$closest = target.closest('.inline-related')) === null || _target$closest === void 0 ? void 0 : _target$closest.querySelector('img');

      if (imgTag) {
        imgTag.src = URL.createObjectURL(files[0]);
      }
    });

    _defineProperty(this, "closePreviewModal", function () {
      document.body.style.overflow = 'auto';
      var modal = document.getElementById('iuw-modal-element');

      if (modal) {
        modal.classList.remove('visible');
        modal.classList.add('hide');
        setTimeout(function () {
          var _modal$parentElement;

          (_modal$parentElement = modal.parentElement) === null || _modal$parentElement === void 0 ? void 0 : _modal$parentElement.removeChild(modal);
        }, 300);
      }
    });

    _defineProperty(this, "onModalClick", function (e) {
      if (e && e.target) {
        var element = e.target;

        if (element.closest('img.iuw-modal-image-preview-item')) {
          return;
        }
      }

      _this.closePreviewModal();
    });

    _defineProperty(this, "createPreviewModal", function (image) {
      image.className = '';
      image.classList.add('iuw-modal-image-preview-item');
      var modal = document.createElement('div');
      modal.id = 'iuw-modal-element';
      modal.classList.add('iuw-modal', 'hide');
      modal.addEventListener('click', _this.onModalClick);
      var preview = document.createElement('div');
      preview.classList.add('iuw-modal-image-preview');
      preview.innerHTML = '<span class="iuw-modal-close"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path></svg></span>';
      preview.appendChild(image);
      modal.appendChild(preview);
      document.body.appendChild(modal);
      return modal;
    });

    _defineProperty(this, "onTempFileChange", function () {
      var _this$tempFileInput, _this$tempFileInput2, _this$tempFileInput3, _this$tempFileInput3$;

      var filesList = (_this$tempFileInput = _this.tempFileInput) === null || _this$tempFileInput === void 0 ? void 0 : _this$tempFileInput.files;

      if (!(filesList !== null && filesList !== void 0 && filesList.length)) {
        return;
      }

      (_this$tempFileInput2 = _this.tempFileInput) === null || _this$tempFileInput2 === void 0 ? void 0 : _this$tempFileInput2.removeEventListener('change', _this.onTempFileChange);
      (_this$tempFileInput3 = _this.tempFileInput) === null || _this$tempFileInput3 === void 0 ? void 0 : (_this$tempFileInput3$ = _this$tempFileInput3.parentElement) === null || _this$tempFileInput3$ === void 0 ? void 0 : _this$tempFileInput3$.removeChild(_this.tempFileInput);
      _this.tempFileInput = null;

      _this.addFile(filesList[0]);
    });

    _defineProperty(this, "onChooseAddImageAreaClick", function () {
      if (!_this.tempFileInput) {
        _this.tempFileInput = document.createElement('input');

        _this.tempFileInput.setAttribute('type', 'file');

        _this.tempFileInput.classList.add('temp_file');

        _this.tempFileInput.setAttribute('accept', 'image/*');

        _this.tempFileInput.style.display = 'none';

        _this.tempFileInput.addEventListener('change', _this.onTempFileChange);

        _this.element.appendChild(_this.tempFileInput);
      }

      _this.tempFileInput.click();
    });

    this.element = _element;

    var inlineGroup = _element.closest('.inline-group');

    if (!inlineGroup) {
      throw new Error('no-inline-group-found');
    }

    this.inlineGroup = inlineGroup;
    var formSetDataString = this.inlineGroup.getAttribute('data-inline-formset');

    if (!formSetDataString) {
      throw new Error('no-formset-data-found');
    }

    this.inlineFormset = JSON.parse(formSetDataString);
    this.updateEmpty();
    this.updateAllIndexes();
    Array.from(this.element.querySelectorAll('.inline-related')).forEach(function (item) {
      return _this.adjustInlineRelated(item);
    });
    Array.from(this.element.querySelectorAll('.iuw-add-image-btn, .iuw-empty')).forEach(function (item) {
      return item.addEventListener('click', _this.onChooseAddImageAreaClick);
    });
    this.element.addEventListener('dragenter', this.onDragEnter);
    this.element.addEventListener('dragover', this.onDragOver);
    this.element.addEventListener('dragleave', this.onDragLeave);
    this.element.addEventListener('dragend', this.onDragLeave);
    this.element.addEventListener('drop', this.onDrop);
  }

  _createClass(ImageUploaderInline, [{
    key: "updateEmpty",
    value: function updateEmpty() {
      var _this$element$querySe = this.element.querySelectorAll('.inline-related:not(.empty-form):not(.deleted)'),
          length = _this$element$querySe.length;

      if (length > 0) {
        this.element.classList.add('non-empty');
      } else {
        this.element.classList.remove('non-empty');
      }
    }
  }, {
    key: "updateElementIndex",
    value: function updateElementIndex(element, prefix, index) {
      var id_regex = new RegExp("(".concat(prefix, "-(\\d+|__prefix__))"));
      var replacement = "".concat(prefix, "-").concat(index);
      var forAttr = element.getAttribute('for');

      if (forAttr) {
        element.setAttribute('for', forAttr.replace(id_regex, replacement));
      }

      if (element.id) {
        element.id = element.id.replace(id_regex, replacement);
      }

      var nameAttr = element.getAttribute('name');

      if (nameAttr) {
        element.setAttribute('name', nameAttr.replace(id_regex, replacement));
      }
    }
  }, {
    key: "updateAllIndexes",
    value: function updateAllIndexes() {
      var _this2 = this;

      var prefix = this.inlineFormset.options.prefix;

      var _Array$from$map$map = Array.from(this.element.querySelectorAll('.inline-related:not(.empty-form)')).map(function (item) {
        return item;
      }).map(function (item, index) {
        _this2.updateElementIndex(item, prefix, index);

        Array.from(item.querySelectorAll('*')).map(function (childItem) {
          return childItem;
        }).forEach(function (childItem) {
          _this2.updateElementIndex(childItem, prefix, index);
        });
        return item;
      }),
          count = _Array$from$map$map.length;

      this.next = count;
      var totalFormsInput = document.getElementById("id_".concat(prefix, "-TOTAL_FORMS"));
      totalFormsInput.value = String(this.next);
      var maxFormsInput = document.getElementById("id_".concat(prefix, "-MAX_NUM_FORMS"));
      var maxNumber = parseInt(maxFormsInput.value, 10);

      if (Number.isNaN(maxNumber)) {
        maxNumber = 0;
      }

      if (maxFormsInput.value === '' || maxNumber - this.next > 0) {
        var _this$element$querySe2;

        (_this$element$querySe2 = this.element.querySelector('.iuw-add-image-btn')) === null || _this$element$querySe2 === void 0 ? void 0 : _this$element$querySe2.classList.add('visible-by-number');
      } else {
        var _this$element$querySe3;

        (_this$element$querySe3 = this.element.querySelector('.iuw-add-image-btn')) === null || _this$element$querySe3 === void 0 ? void 0 : _this$element$querySe3.classList.remove('visible-by-number');
      }
    }
  }, {
    key: "adjustInlineRelated",
    value: function adjustInlineRelated(element) {
      var inputs = Array.from(element.querySelectorAll('input[type=hidden], input[type=checkbox], input[type=file]')).map(function (item) {
        var _item$parentElement2;

        (_item$parentElement2 = item.parentElement) === null || _item$parentElement2 === void 0 ? void 0 : _item$parentElement2.removeChild(item);
        return item;
      }); // get raw image url

      var rawImage = document.querySelector('p.file-upload a');

      if (element.classList.contains('empty-form')) {
        rawImage = null;
      }

      var hrefAttr = null;

      if (rawImage) {
        hrefAttr = rawImage.getAttribute('href');

        if (hrefAttr) {
          element.setAttribute('data-raw', hrefAttr);
        }
      } // clear element


      element.innerHTML = '';
      inputs.forEach(function (item) {
        return element.appendChild(item);
      }); // apply raw image

      if (hrefAttr) {
        this.appendItem(element, hrefAttr);
      }
    }
  }, {
    key: "appendItem",
    value: function appendItem(element, url) {
      var delete_icon = null;
      var related = element.closest('.inline-related');

      if ((related === null || related === void 0 ? void 0 : related.getAttribute('data-candelete')) === 'true') {
        delete_icon = document.createElement('span');
        delete_icon.classList.add('iuw-delete-icon');
        delete_icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path></svg>';
      }

      if (this.canPreview) {
        var span = document.createElement('span');
        span.classList.add('iuw-preview-icon');

        if ((related === null || related === void 0 ? void 0 : related.getAttribute('data-candelete')) !== 'true') {
          span.classList.add('iuw-only-preview');
        }

        span.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-zoom-in" viewBox="0 0 16 16" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"></path><path xmlns="http://www.w3.org/2000/svg" d="M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z"></path><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z"></path></svg>';
        element.appendChild(span);
      }

      var img = document.createElement('img');
      img.src = url;
      element.appendChild(img);

      if (delete_icon) {
        element.appendChild(delete_icon);
      }

      related === null || related === void 0 ? void 0 : related.removeEventListener('click', this.onRelatedItemClick);
      related === null || related === void 0 ? void 0 : related.addEventListener('click', this.onRelatedItemClick);
      var fileInput = related === null || related === void 0 ? void 0 : related.querySelector('input[type=file]');
      fileInput === null || fileInput === void 0 ? void 0 : fileInput.removeEventListener('change', this.onFileInputChange);
      fileInput === null || fileInput === void 0 ? void 0 : fileInput.addEventListener('change', this.onFileInputChange);
    }
  }, {
    key: "addFile",
    value: function addFile(file) {
      var _template$parentEleme;

      var template = this.element.querySelector('.inline-related.empty-form');

      if (!template) {
        return;
      }

      var row = template.cloneNode(true);
      row.classList.remove('empty-form');
      row.classList.remove('last-related');
      row.setAttribute('data-candelete', 'true');
      row.id = "".concat(this.inlineFormset.options.prefix, "-").concat(this.next);
      (_template$parentEleme = template.parentElement) === null || _template$parentEleme === void 0 ? void 0 : _template$parentEleme.insertBefore(row, template);
      var dataTransferList = new DataTransfer();
      dataTransferList.items.add(file);
      var rowFileInput = row.querySelector('input[type=file]');
      rowFileInput.files = dataTransferList.files;
      this.appendItem(row, URL.createObjectURL(file));
      this.updateEmpty();
      this.updateAllIndexes();
    }
  }]);

  return ImageUploaderInline;
}();

document.addEventListener('DOMContentLoaded', function () {
  Array.from(document.querySelectorAll('.iuw-inline-root')).map(function (element) {
    return new ImageUploaderInline(element);
  });
}); // export for testing