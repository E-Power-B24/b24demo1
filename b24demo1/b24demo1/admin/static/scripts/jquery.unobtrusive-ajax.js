/// <reference path="jquery-1.5.1.js" />

/*!
** Unobtrusive Ajax support library for jQuery
** Copyright (C) Microsoft Corporation. All rights reserved.
*/

/*jslint white: true, browser: true, onevar: true, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, strict: false */
/*global window: false, jQuery: false */

(function ($) {
    var data_click = "unobtrusiveAjaxClick",
        data_validation = "unobtrusiveValidation";

    function getFunction(code, argNames) {
        var fn = window, parts = (code || "").split(".");
        while (fn && parts.length) {
            fn = fn[parts.shift()];
        }
        if (typeof (fn) === "function") {
            return fn;
        }
        argNames.push(code);
        return Function.constructor.apply(null, argNames);
    }

    function isMethodProxySafe(method) {
        return method === "GET" || method === "POST";
    }

    function asyncOnBeforeSend(xhr, method) {
        if (!isMethodProxySafe(method)) {
            xhr.setRequestHeader("X-HTTP-Method-Override", method);
        }
    }

    function asyncOnSuccess(element, data, contentType) {
        var mode;

        if (contentType.indexOf("application/x-javascript") !== -1) {  // jQuery already executes JavaScript for us
            return;
        }

        mode = (element.getAttribute("data-ajax-mode") || "").toUpperCase();
        $(element.getAttribute("data-ajax-update")).each(function (i, update) {
            var top;

            switch (mode) {
                case "BEFORE":
                    top = update.firstChild;
                    $("<div />").html(data).contents().each(function () {
                        update.insertBefore(this, top);
                    });
                    break;
                case "AFTER":
                    $("<div />").html(data).contents().each(function () {
                        update.appendChild(this);
                    });
                    break;
                default:
                    $(update).html(data);
                    break;
            }
        });
         
    }

    function asyncRequest(element, options) {
        var confirm, loading, method, duration;

        confirm = element.getAttribute("data-ajax-confirm");
        if (confirm && !window.confirm(confirm)) {
            return;
        }

        loading = $(element.getAttribute("data-ajax-loading"));
        duration = element.getAttribute("data-ajax-loading-duration") || 0;

        $.extend(options, {
            type: element.getAttribute("data-ajax-method") || undefined,
            url: element.getAttribute("data-ajax-url") || undefined,
            beforeSend: function (xhr) {
                var result;
                asyncOnBeforeSend(xhr, method);
                result = getFunction(element.getAttribute("data-ajax-begin"), ["xhr"]).apply(this, arguments);
                if (result !== false) {
                    loading.show(duration);
                }
                return result;
            },
            complete: function (e) {

                //find first input element
                //$("input:visible:enabled:not(.datetime), select:visible:enabled,textarea:enabled").first().focus();

                // register validation
                $.validate.unobtrusive($);

                // ready
                app.ready();

                loading.hide(duration);

                getFunction(element.getAttribute("data-ajax-complete"), ["xhr", "status"]).apply(this, arguments);

                // display message on error or unauthorized.
                if (e.status == 400) {
                    //alert(e.responseText)
                    //$("<div></div>").append(e.responseText).dialog({ modal: true, width: 500, height: 175, title: "Access Deny", resizable: true });

                    var header = "<div class='modal-header'>" +
                                    "<button type='button' class='close' data-dismiss='modal'>" +
                                        "<span aria-hidden='true'>" +
                                            "<i class='fa fa-2x'>&times;</i>" +
                                        "</span>" +
                                        "<span class='sr-only'>Close</span>" +
                                    "</button>" +
                                    "<h4 class='modal-title'>Access Deny</h4>" +
                                 "</div>";
                    var body = "<div class='modal-body'><p>" + e.responseText + "</p></div>";
                    var footer = "<div class='modal-footer'>" +
                                 "<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>" +
                                 "</div>";
                    $('<div class="modal fade" role="dialog">').append('<div class="modal-dialog"><div class="modal-content">' + header + body + footer + '</div></div></div>').modal('show');

                } else if (e.status == 500) {
                   alert(e.responseText)
                   // $("<div></div>").append(e.responseText).dialog({ modal: true, width: 500, height: 175, resizable: true, title: "Error" });
                }
            },
            success: function (data, status, xhr) {
                asyncOnSuccess(element, data, xhr.getResponseHeader("Content-Type") || "text/html");
                getFunction(element.getAttribute("data-ajax-success"), ["data", "status", "xhr"]).apply(this, arguments);
            },
            error: getFunction(element.getAttribute("data-ajax-failure"), ["xhr", "status", "error"])

        });

        options.data.push({ name: "X-Requested-With", value: "XMLHttpRequest" });

        method = options.type.toUpperCase();
        if (!isMethodProxySafe(method)) {
            options.type = "POST";
            options.data.push({ name: "X-HTTP-Method-Override", value: method });
        }

        $.ajax(options);
    }

    function validate(form) {
        var validationInfo = $(form).data(data_validation);
        return !validationInfo || !validationInfo.validate || validationInfo.validate();
    } 
      
    $("body a[href][data-ajax!=false],[data-ajax=true]").live("click", function (evt) {
        evt.preventDefault();
        app.wait();
        var obj = $(this);

        if (obj.attr('href') == '#' || obj.attr('href') == 'javascript:void(0)') return false;

        var updateTarget = obj.attr("data-ajax-update") || "#content";
        obj.attr("data-ajax-update", updateTarget);
        var loading = obj.attr("data-ajax-loading") || "#ajaxCall";
        obj.attr("data-ajax-loading", loading);

        asyncRequest(this, {
            url: this.href,
            type: "GET",
            data: []
        });
        return false;
    });  

    $("body form[data-ajax!=false],#wrapper form[data-ajax-update]").live("submit", function (evt) {
        var clickInfo = $(this).data(data_click) || [];
        evt.preventDefault();
        if (!validate(this)) {
            return;
        }
        app.wait();

        var obj = $(this);
        var updateTarget = obj.attr("data-ajax-update") || "#content";
        obj.attr("data-ajax-update", updateTarget);
        obj.attr("method", obj.attr("method") || "POST");
        var loading = obj.attr("data-ajax-loading") || "#ajaxCall";
        obj.attr("data-ajax-loading", loading);
        asyncRequest(this, {
            url: this.action,
            type: this.method || "POST",
            contentType: this.enctype,
            data: clickInfo.concat($(this).serializeArray())
        });
    });

} (jQuery)); 