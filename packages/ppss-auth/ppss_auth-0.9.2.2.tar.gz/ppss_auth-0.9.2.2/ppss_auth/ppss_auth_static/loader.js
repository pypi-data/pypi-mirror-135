function tplHandler(ep, deferload) {

    this._getMyTemplats = function (templates) {
        if (!templates) { // called without parameter
            tpl = this.templates;
        } else {
            tpl = templates;
        }
        return tpl;
    };

    this._loadtpl = function (templates) {
        //var deferred = Array();
        for (i in this.ep) {
            this.deferred.push(
                jQuery.get(this.ep, function (resp) {
                    $("body").append('<div id="tplHandlercontainer">' + resp + '</div>');
                    var tpl = _getMyTemplats(templates);
                    $("#tplHandlercontainer").find(".hbltpl").each(function (i, e) {
                        var el = $(e);
                        var name = el.attr("data-name") || "tpl_" + i;
                        tpl[name] = Handlebars.compile(el.html());
                    });
                    $("#tplHandlercontainer").remove();
                    this.deferred = Array();
                })
            );
            this.loadedEP.push(i);
        }
        this.ep = Array();
        return this.deferred;
    };

    this.getTpl = function (name, cb, templates) {
        templates = _getMyTemplats(templates);
        if (name in templates) {
            cb(templates[name]);
        } else {
            $.when.apply($, this._loadtpl(templates)).then(function () {
                cb(templates[name]);
            });
        }
        return this;
    };

    this.addEPs = function (ep) {
        if (ep) {
            if (ep.constructor === Array) {
                this.ep = this.ep.concat(ep);
            } else {
                this.ep = Array(ep);
            }
            if (!deferload) {
                _loadtpl();
            }
        }
        return this;
    }

    this.init = function (ep, deferload) {
        this.deferred = Array();
        this.loadedEP = Array();
        this.templates = Array();
        deferload = deferload || false;
        if (ep) {
            if (ep.constructor === Array) {
                this.ep = ep;
            } else {
                this.ep = Array(ep);
            }
            if (!deferload) {
                _loadtpl();
            }
        } else {
            this.ep = Array();
        }
    }

    this.init(ep, deferload);
    return this;
}