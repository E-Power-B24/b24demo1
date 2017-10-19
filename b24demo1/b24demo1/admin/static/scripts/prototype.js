app = {};
app.conf = {
    format_currency: "###0.00",
    format_date: "yyyy-MM-dd",
    format_datetime: "yyyy-MM-dd HH:mm",
    format_qty: "#",
    format_time: "HH:mm",
};
app.fn = {};

// OBJECT MANIPULATION FUNCTION
app.fn.object = {};

app.fn.object.read = function (doc) {
    var tmp = {};
    $("[id]", doc).each(function () {
        var o = $(this),
	        id = o.attr("id");
        if (o.attr("type") == "checkbox") {
            tmp[id] = o.attr("checked");
        }
        else {

            var format = o.attr("format"),
	            val = o.val() || o.text();
            if (format) {
                format = format.toLowerCase();
                if (format == "decimal") val = val.toFloat();
                else if (format == "int") val = val.toInt();
                else if (format == "date") val = new Date(Date.parse(val));
                else if (format == "time") val = val; // nothing change to time
                else if (format == "datetime") val = new Date(Date.parse(val));
            }
            tmp[id] = val;
        }
    });
    return tmp;
};

app.fn.object.write = function (doc, obj, except) {
    if (typeof(obj)=="object"){
        for (var col in obj) {
            $("#" + col, doc).each(function () {
                var val = obj[col],
                    me = $(this);
                app.fn.object.write(me, val);
            });
        }
    }
    else{
        var tagName = doc[0].tagName,
			me = $(doc[0]),
            val = obj,
            format = $(doc[0]).attr("format");

        if (format) {
            format = format.toLowerCase();
            if (format == "decimal") val = val.toFloat().formatFloat();
            else if (format == "int") val = val.toInt().formatInt();
            else if (format == "date") val = new Date(Date.parse(val)).format(app.conf.format_date);
            else if (format == "time") val = new Date(Date.parse(val)).format(app.conf.format_time);
            else if (format == "datetime") val = new Date(Date.parse(val)).format(app.conf.format_datetime);
        }

        if (tagName == "INPUT") {
            if (me.attr("type") != "checkbox") {
                me.val(val);
            }
            else {
                me.attr("checked", val);
            }
        }
        else if (tagName == "SELECT") {
            me.val(val);
        }
        else if (tagName == "TEXTAREA") {
            me.val(val);
        }
        else if (tagName = "TD") {
            if (typeof val == "boolean") val = val ? "true" : "";
            me.html(val);
        }
    }
};



app.fn.object.compare = function (obj1, obj2) {
    for (var col in obj) {
        if (obj1[col] != obj2[col]) {
            return false;
        }
    }
    return true;
};
app.fn.object.copy = function (obj1, obj2) {
    for (var col in obj) {
        obj1[col] = obj1[col];
    }
};
app.fn.object.valueAt = function (obj, index) {
    var i = 0;
    for (var col in obj) {
        if (i == index) {
            return obj[col];
        }
        i = i + 1;
    }
    return undefined;
};

//UI FUNCTION
app.fn.ui = {};
// aliase to "app.fn.object.write"
app.fn.ui.bindDoc = function (doc, obj) {
    app.fn.object.write(doc, obj);
};
app.fn.ui.bindTable = function (table, data) {

    // clear data first
    $("tbody tr", table).remove().empty();
    var len = data.length,
	    bind = app.fn.object.write,
	    tbody = $("tbody", table),
	    tmp = $("thead", table);
    for (var i = 0; i < len; i++) {
        // bind data to row.
        bind(tmp, data[i]);
        // add new row with data to database.
        tbody.append(tmp.html());
    }
    // alternate row. 
    $("tbody tr:odd", table).addClass("alt");
    // handle event.
    $("tbody tr", table).click(function () {
        $(".selected", $(this).parent()).removeClass("selected");
        $(this).addClass("selected");
    });
};



app.fn.ui.bindList = function (select, data, all, choose) {
    $(select).html("");
    if (typeof all === "string") {
        all = all == "" ? "" : app.res.list_all.format(all);
        $(select).append('<option value="0">' + all + '</option>');
    }
    if (typeof choose === "string") {
        var display = "&nbsp;";
        if (choose) {
            display = app.res.list_choose.format(choose);
        }
        $(select).append('<option value="-1">' + display + '</option>');
    }

    for (var i = 0; i < data.length; i++) {
        var val = typeof data[i] === "object" ? app.fn.object.valueAt(data[i], 0) : data[i];
        var dis = typeof data[i] === "object" ? app.fn.object.valueAt(data[i], 1) : data[i];
        $(select).append('<option value="' + val + '">' + dis + '</option>');
    }

};
app.fn.ui.selectRow = function (table, columName, columnValue) {
    // this method not work/test
    $("tr", table).each(function () {
        if ($("#" + columName, $(this)).text() == "" + columnValue) {
            $(this).addClass("select");
        }
    });
};

app.fn.ui.applyRes = function (doc) {
    $("*[res]", doc).each(function () {
        var text = app.res[$(this).attr("res")];
        if (typeof text === "string") {
            $(this).text(text);
        }
        else {
            $(this).text('"' + $(this).attr("res") + '"');
        }
    });
    $("button[id],td[id],a[id]", doc).each(function () {
        var text = app.res[$(this).attr("id")];
        if (typeof text === "string") {
            $(this).html(text);
        }
        else {
            $(this).html('"' + $(this).attr("id") + '"');
        }
    });

};
app.fn.ui.validInput = function (doc) {
    var valid = function (input) {
        var rules = {
            "email": "^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$",
            "username": "^[^ ]{1,}$",
            "password": "^[^ ]{1,}$",
            "website": "^[^ ]{1,}$",
            "phone": "^[0-9 ]{9,}$",
            "int": "^[-]?[0-9]{1,12}$",
            "date": "^[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}$",
            "time": "^[0-9]{1,2}:[0-9]{1,2}[:[0-9]{1,2}]{0,1}$",
            "datetime": "[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}[:[0-9]{1,2}]{0,1}",
            "dec": "^[-]?[0-9,]{1,12}[.]{0,1}[0-9]{0,6}$",
            "uint": "^[0-9]{1,12}$",
            "udec": "^[0-9,]{1,12}[.]{0,1}[0-9]{0,6}$",
            "require": "[^ ]{1}",
            "code": "^[a-zA-Z0-9_\-]{1,25}$"
        };
        var rule = $(input).attr("rule");
        var val = $(input).val();
        var regex = new RegExp(rules[rule]);
        return regex.test(val);
    };
    var result = true;
    var first = undefined;
    $("select[rule='require']").each(function () {
        var obj = $(this);
        if (obj.val() && obj.val() > -1) {
            obj.removeClass("invalid");
        }
        else {
            obj.addClass("invalid");
            result = false;

            // add invalid class to object.  
            if (typeof first === "undefined") {
                first = obj;
            }
        }
    });
    $("input[rule],textarea[rule]", doc).each(function () {
        if (valid(this)) {
            $(this).removeClass("invalid");
        }
        else {
            $(this).addClass("invalid");
            result = false;

            // add invalid class to object.  
            if (typeof first === "undefined") {
                first = $(this);
            }
        }
    });

    // send focus to first invalid control.
    if (first) {
        first.focus();
    }
    return result;
};


app.fn.download = function (url) {
    $("#download").attr("src", url);
};


/***************************** PROTOTYPE ************************************************/

// STRING ================================================================================
String.prototype.format = function () {
    if (typeof arguments[0] == "object") {
        // "{id} {name}".format({id:01,name:"yellow"});
        var args = arguments[0];
        var pattern = /\{[A-Za-z0-9_]+\}/g;
        return this.replace(pattern, function (capture) { return args[capture.match(/[A-Za-z0-9_]+/)]; });
    }
    else {
        //"{0} {1} {2} {0}".format(1,2,3);
        var args = arguments;
        var pattern = /\{\d+\}/g;
        return this.replace(pattern, function (capture) { return args[capture.match(/\d+/)]; });
    }
};
// ARRAY ==================================================================================
Array.prototype.where = function (cond) {
    if (typeof cond === "function") {
        var len = this.length;
        var tmp = [];
        for (var i = 0; i < len; i++) {
            if (cond(this[i])) {
                tmp.push(this[i]);
            }
        }
        return tmp;
    }
    else if (typeof cond === "object") {
        // where({id:123,name:"item"});
        var len = this.length;
        var tmp = [];
        for (var i = 0; i < len; i++) {
            var found = true;
            for (var key in cond) {
                if (cond[key] != this[i][key]) {
                    found = false;
                }
            }
            if (found == true) {
                tmp.push(this[i]);
            }
        }
        return tmp;
    }
};
Array.prototype.select = function (fn) {
    if (typeof fn === "function") {
        var len = this.length;
        var tmp = [];
        for (var i = 0; i < len; i++) {
            tmp.push(fn(this[i]));
        }
        return tmp;
    }
    else {
        return this;
    }
};
Array.prototype.single = function (arg) {
    if (typeof arg === "function") {
        var len = this.length;
        for (var i = 0; i < len; i++) {
            if (arg(this[i])) {
                return this[i];
            }
        }
    }
    if (typeof arg === "object") {
        var len = this.length;
        for (var i = 0; i < len; i++) {
            var found = true;
            for (var key in arg) {
                if (arg[key] != this[i][key]) {
                    found = false;
                }
            }
            if (found) {
                return this[i];
            }
        }
    }
    else {
        // check for primary key.
        var len = this.length;
        for (var i = 0; i < len; i++) {
            if (app.fn.object.valueAt(this[i], 0) == arg) {
                return this[i];
            }
        }
    }
};

Array.prototype.sum = function (exp) {
    var len = this.length,
        tmp = 0;
    if (typeof exp == "function") {
        for (var i = 0; i < len; i++) {
            tmp += exp(this[i]);
        }
    }
    else if (exp) {
        for (var i = 0; i < len; i++) {
            tmp += this[i][exp];
        }
    }
    else {
        for (var i = 0; i < len; i++) {
            tmp += this[i];
        }
    }
    return tmp;
}

Array.prototype.add = function (obj) {
    this.push(obj);
};
Array.prototype.insert = function (obj, index) {
    // todo: emplement insert at.
};
Array.prototype.remove = function (obj) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == obj) {
            this.splice(i, 1);
            break;
        }
    }
};
Array.prototype.removeAt = function (obj) {
    this.splice(index, 1);
};

Array.prototype.clear = function () {

};


/*
 * Date Format 1.2.3
 * (c) 2007-2009 Steven Levithan <stevenlevithan.com>
 * MIT license
 *
 * Includes enhancements by Scott Trenda <scott.trenda.net>
 * and Kris Kowal <cixar.com/~kris.kowal/>
 *
 * Accepts a date, a mask, or a date and a mask.
 * Returns a formatted version of the given date.
 * The date defaults to the current date/time.
 * The mask defaults to dateFormat.masks.default.
 */
var dateFormat = function () {
    var token = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,
		timezone = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,
		timezoneClip = /[^-+\dA-Z]/g,
		pad = function (val, len) {
		    val = String(val);
		    len = len || 2;
		    while (val.length < len) val = "0" + val;
		    return val;
		};

    // Regexes and supporting functions are cached through closure
    return function (date, mask, utc) {
        var dF = dateFormat;

        // You can't provide utc if you skip other args (use the "UTC:" mask prefix)
        if (arguments.length == 1 && Object.prototype.toString.call(date) == "[object String]" && !/\d/.test(date)) {
            mask = date;
            date = undefined;
        }

        // Passing date through Date applies Date.parse, if necessary
        date = date ? new Date(date) : new Date;
        if (isNaN(date)) throw SyntaxError("invalid date");

        mask = String(dF.masks[mask] || mask || dF.masks["default"]);

        // Allow view the utc argument via the mask
        if (mask.slice(0, 4) == "UTC:") {
            mask = mask.slice(4);
            utc = true;
        }

        var _ = utc ? "getUTC" : "get",
			d = date[_ + "Date"](),
			D = date[_ + "Day"](),
			M = date[_ + "Month"](),
			y = date[_ + "FullYear"](),
			H = date[_ + "Hours"](),
			m = date[_ + "Minutes"](),
			s = date[_ + "Seconds"](),
			L = date[_ + "Milliseconds"](),
			o = utc ? 0 : date.getTimezoneOffset(),
			flags = {
			    d: d,
			    dd: pad(d),
			    ddd: dF.i18n.dayNames[D],
			    dddd: dF.i18n.dayNames[D + 7],
			    M: M + 1,
			    MM: pad(M + 1),
			    MMM: dF.i18n.monthNames[M],
			    MMMM: dF.i18n.monthNames[M + 12],
			    yy: String(y).slice(2),
			    yyyy: y,
			    h: H % 12 || 12,
			    hh: pad(H % 12 || 12),
			    H: H,
			    HH: pad(H),
			    m: m,
			    mm: pad(m),
			    s: s,
			    ss: pad(s),
			    l: pad(L, 3),
			    L: pad(L > 99 ? Math.round(L / 10) : L),
			    t: H < 12 ? "a" : "p",
			    tt: H < 12 ? "am" : "pm",
			    T: H < 12 ? "A" : "P",
			    TT: H < 12 ? "AM" : "PM",
			    Z: utc ? "UTC" : (String(date).match(timezone) || [""]).pop().replace(timezoneClip, ""),
			    o: (o > 0 ? "-" : "+") + pad(Math.floor(Math.abs(o) / 60) * 100 + Math.abs(o) % 60, 4),
			    S: ["th", "st", "nd", "rd"][d % 10 > 3 ? 0 : (d % 100 - d % 10 != 10) * d % 10]
			};

        return mask.replace(token, function ($0) {
            return $0 in flags ? flags[$0] : $0.slice(1, $0.length - 1);
        });
    };
}();

// Some common format strings
dateFormat.masks = {
    "default": "ddd MMM dd yyyy HH:mm:ss",
    shortDate: "m/d/yy",
    mediumDate: "MMM d, yyyy",
    longDate: "MMMM d, yyyy",
    fullDate: "dddd, MMMM d, yyyy",
    shortTime: "h:MM TT",
    mediumTime: "h:MM:ss TT",
    longTime: "h:MM:ss TT Z",
    isoDate: "yyyy-mm-dd",
    isoTime: "HH:MM:ss",
    isoDateTime: "yyyy-mm-dd'T'HH:MM:ss",
    isoUtcDateTime: "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
};

// Internationalization strings
dateFormat.i18n = {
    dayNames: [
		"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat",
		"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ],
    monthNames: [
		"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
		"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ]
};

// For convenience...
Date.prototype.format = function (mask, utc) {
    return dateFormat(this, mask, utc);
};

// override parse prototype to support dash ("-")
// to fix firefox problem.
Date.prototype.parse = function (val) {
    return this.parse(val.replace(/\-/g, "/"));
};






/**
* Formats the number according to the 'format' string;
* adherses to the american number standard where a comma
* is inserted after every 3 digits.
*  note: there should be only 1 contiguous number in the format,
* where a number consists of digits, period, and commas
*        any other characters can be wrapped around this number, including '$', '%', or text
*        examples (123456.789):
*          '0′ - (123456) show only digits, no precision
*          '0.00′ - (123456.78) show only digits, 2 precision
*          '0.0000′ - (123456.7890) show only digits, 4 precision
*          '0,000′ - (123,456) show comma and digits, no precision
*          '0,000.00′ - (123,456.78) show comma and digits, 2 precision
*          '0,0.00′ - (123,456.78) shortcut method, show comma and digits, 2 precision
*
* @method format
* @param format {string} the way you would like to format this text
* @return {string} the formatted number
* @public
*/
Number.prototype.format = function (format) {

    if (typeof format != 'string') { return ''; } // sanity check 

    format = format.replace(/#/g, "?");

    var hasComma = -1 < format.indexOf(','),
         //psplit = format.stripNonNumeric().split('.'),
          psplit = format.split('.'),
          that = this;

    // compute precision
    if (1 < psplit.length) {
        // fix number precision
        that = that.toFixed(psplit[1].length);
    }
        // error: too many periods
    else if (2 < psplit.length) {
        throw ('NumberFormatException: invalid format, formats should have no more than 1 period: ' + format);
    }
        // remove precision
    else {
        that = that.toFixed(0);
    }

    // get the string now that precision is correct
    var fnum = that.toString();

    // format has comma, then compute commas
    if (hasComma) {
        // remove precision for computation
        psplit = fnum.split('.');

        var cnum = psplit[0],
          parr = [],
          j = cnum.length,
          m = Math.floor(j / 3),
          n = cnum.length % 3 || 3; // n cannot be ZERO or causes infinite loop 

        // break the number into chunks of 3 digits; first chunk may be less than 3
        for (var i = 0; i < j; i += n) {
            if (i != 0) { n = 3; }
            parr[parr.length] = cnum.substr(i, n);
            m -= 1;
        }
        // put chunks back together, separated by comma
        fnum = parr.join(',');

        // add the precision back in
        if (psplit[1]) { fnum += '.' + psplit[1]; }
    }
    // replace the number portion of the format with fnum
    return format.replace(/[\d,?\.?]+/, fnum);
};



// fixing error.
Number.prototype.formatFloat = function () {
    var x = (this >= 0)
          ? this.format("###0.00##")
          : "-" + Math.abs(this).format("###0.00##");

    return x.replace(/0$/, '')
            .replace(/0$/, '');
};
Number.prototype.formatInt = function () {
    return (this >= 0)
        ? this.format("#")
        : "-" + Math.abs(this).format("#");
};

Number.prototype.toFloat = function () {
    return (isNaN(this)) ? 0 : this.valueOf();
};
Number.prototype.toInt = function () {
    return (isNaN(this)) ? 0 : this.valueOf();
};


// fixing parse
String.prototype.toFloat = function () {
    var tmp = this.replace(/,/g, '');//= this.replace(/[^0-9. ]/g,'');
    if (tmp) return parseFloat(tmp);
    else return 0.0;
};
String.prototype.toInt = function () {
    var tmp = this.replace(/,/g, '');//= this.replace(/[^0-9. ]/g,'');
    if (tmp) return parseInt(tmp);
    else return 0;
};
String.prototype.toDate = function () {
    return new Date(Date.parse(this.valueOf()));
};



//trimming space from both side of the string
String.prototype.trim = function () {
    return this.replace(/^\s+|\s+$/g, "");
}

//trimming space from left side of the string
String.prototype.trimLeft = function () {
    return this.replace(/^\s+/, "");
}

//trimming space from right side of the string
String.prototype.trimRight = function () {
    return this.replace(/\s+$/, "");
}

//pads left
String.prototype.padLeft = function (padString, length) {
    var str = this;
    while (str.length < length)
        str = padString + str;
    return str;
}
//pads right
String.prototype.padRight = function (padString, length) {
    var str = this;
    while (str.length < length)
        str = str + padString;
    return str;
}

String.prototype.escapse = function () { return this.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&") };


