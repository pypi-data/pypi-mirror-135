/**
 * Django Image Uploader Widget - An image uploader widget for django.
 * @version v0.1.3
 * @author Eduardo Oliveira (EduardoJM) <eduardo_y05@outlook.com>.
 * @link https://github.com/inventare/django-image-uploader-widget
 * 
 * Licensed under the MIT License (https://github.com/inventare/django-image-uploader-widget/blob/main/LICENSE).
 */

"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var ImageUploaderWidget = /*#__PURE__*/function () {
  function ImageUploaderWidget(_element) {
    var _this = this;

    _classCallCheck(this, ImageUploaderWidget);

    _defineProperty(this, "element", void 0);

    _defineProperty(this, "fileInput", void 0);

    _defineProperty(this, "checkboxInput", void 0);

    _defineProperty(this, "emptyMarker", void 0);

    _defineProperty(this, "canDelete", false);

    _defineProperty(this, "dragging", false);

    _defineProperty(this, "canPreview", true);

    _defineProperty(this, "raw", null);

    _defineProperty(this, "file", null);

    _defineProperty(this, "onEmptyMarkerClick", function () {
      _this.fileInput.click();
    });

    _defineProperty(this, "onDrop", function (e) {
      var _e$dataTransfer;

      e.preventDefault();
      _this.dragging = false;

      _this.element.classList.remove('drop-zone');

      if ((_e$dataTransfer = e.dataTransfer) !== null && _e$dataTransfer !== void 0 && _e$dataTransfer.files.length) {
        _this.fileInput.files = e.dataTransfer.files;
        _this.file = _this.fileInput.files[0];
        _this.raw = null;

        _this.renderWidget();
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
      if (e.relatedTarget && e.relatedTarget.closest('.iuw-root') === _this.element) {
        return;
      }

      _this.dragging = false;

      _this.element.classList.remove('drop-zone');
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

    _defineProperty(this, "onImagePreviewClick", function (e) {
      if (e && e.target) {
        var targetElement = e.target;

        if (targetElement.closest('.iuw-delete-icon')) {
          var _element$parentElemen;

          var element = targetElement.closest('.iuw-image-preview');
          element === null || element === void 0 ? void 0 : (_element$parentElemen = element.parentElement) === null || _element$parentElemen === void 0 ? void 0 : _element$parentElemen.removeChild(element);

          if (_this.checkboxInput) {
            _this.checkboxInput.checked = true;
          }

          _this.fileInput.value = '';
          _this.file = null;
          _this.raw = null;

          _this.renderWidget();

          return;
        }

        if (targetElement.closest('.iuw-preview-icon')) {
          var _element2 = targetElement.closest('.iuw-image-preview');

          var image = _element2 === null || _element2 === void 0 ? void 0 : _element2.querySelector('img');

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
      }

      _this.fileInput.click();
    });

    _defineProperty(this, "onFileInputChange", function () {
      var _this$fileInput$files;

      if ((_this$fileInput$files = _this.fileInput.files) !== null && _this$fileInput$files !== void 0 && _this$fileInput$files.length) {
        _this.file = _this.fileInput.files[0];
      }

      _this.renderWidget();
    });

    this.element = _element;

    var fileInput = _element.querySelector('input[type=file]');

    var checkBoxInput = _element.querySelector('input[type=checkbox]');

    if (!fileInput) {
      throw new Error('no-file-input-found');
    }

    this.fileInput = fileInput;
    this.checkboxInput = checkBoxInput;
    this.emptyMarker = _element.querySelector('.iuw-empty');
    this.canDelete = _element.getAttribute('data-candelete') === 'true';
    this.dragging = false; // add events

    this.fileInput.addEventListener('change', this.onFileInputChange);

    if (this.emptyMarker) {
      this.emptyMarker.addEventListener('click', this.onEmptyMarkerClick);
    }

    this.element.addEventListener('dragenter', this.onDragEnter);
    this.element.addEventListener('dragover', this.onDragOver);
    this.element.addEventListener('dragleave', this.onDragLeave);
    this.element.addEventListener('dragend', this.onDragLeave);
    this.element.addEventListener('drop', this.onDrop); // init

    this.raw = _element.getAttribute('data-raw');
    this.file = null;
    this.renderWidget();
  }

  _createClass(ImageUploaderWidget, [{
    key: "renderPreview",
    value: function renderPreview(url) {
      var preview = document.createElement('div');
      preview.classList.add('iuw-image-preview');
      var img = document.createElement('img');
      img.src = url;
      preview.appendChild(img);

      if (this.canDelete) {
        var span = document.createElement('span');
        span.classList.add('iuw-delete-icon');
        span.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path></svg>';
        preview.appendChild(span);
      }

      if (this.canPreview) {
        var _span = document.createElement('span');

        _span.classList.add('iuw-preview-icon');

        if (!this.canDelete) {
          _span.classList.add('iuw-only-preview');
        }

        _span.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-zoom-in" viewBox="0 0 16 16" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"></path><path xmlns="http://www.w3.org/2000/svg" d="M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z"></path><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z"></path></svg>';
        preview.appendChild(_span);
      }

      return preview;
    }
  }, {
    key: "renderWidget",
    value: function renderWidget() {
      var _this2 = this;

      if (!this.file && !this.raw) {
        this.element.classList.remove('non-empty');

        if (this.checkboxInput) {
          this.checkboxInput.checked = true;
        }
      } else {
        this.element.classList.add('non-empty');

        if (this.checkboxInput) {
          this.checkboxInput.checked = false;
        }
      }

      Array.from(this.element.querySelectorAll('.iuw-image-preview')).forEach(function (item) {
        return _this2.element.removeChild(item);
      });

      if (this.file) {
        var url = URL.createObjectURL(this.file);
        this.element.appendChild(this.renderPreview(url));
      } else if (this.raw) {
        this.element.appendChild(this.renderPreview(this.raw));
      }

      Array.from(this.element.querySelectorAll('.iuw-image-preview')).forEach(function (item) {
        return item.addEventListener('click', _this2.onImagePreviewClick);
      });
    }
  }]);

  return ImageUploaderWidget;
}();

document.addEventListener('DOMContentLoaded', function () {
  Array.from(document.querySelectorAll('.iuw-root')).map(function (element) {
    return new ImageUploaderWidget(element);
  });

  if (window && window.django && window.django.jQuery) {
    var $ = window.django.jQuery;
    $(document).on('formset:added', function (_, row) {
      if (!row.length) {
        return;
      }

      Array.from(row[0].querySelectorAll('.iuw-root')).map(function (element) {
        return new ImageUploaderWidget(element);
      });
    });
  }
}); // export for testing