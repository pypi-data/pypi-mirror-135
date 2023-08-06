;
(function ($) {
    'use strict';
    var tplhandler = tplHandler(routes.TEMPLATE);

    function render(obj) {
        var $container = $(obj.container)
        var data = obj.data
        var tpl = obj.tpl
        var callback = obj.callback
        var html = ""
        tplhandler.getTpl(tpl, function (tpl) {
            data.map(function (el) {
                html += tpl(el)
            })
            $container.empty().append(html)
            callback && callback(data)
        });
    }

    function update(res, data) {
        switch (res.msg) {
            case "change_perm":
                render({
                    container: "[data-permdelete]",
                    data: res.groupperm,
                    tpl: "perm_del_tpl",
                    callback: deleteperm
                })
                break;
            case "change_user":
                render({
                    container: "[data-userdelete]",
                    data: res.elements,
                    tpl: "user_del_tpl",
                    callback: deleteuser
                })
                break;
            default:
                break;
        }
    }
    // Callbacks
    var deleteperm = function (data) {
        $(".deleteperm").off().on("click", function (ev) {
            $.ajax(routes.REMOVE_PERM.replace("-1", $(this).closest("li").attr("data-id")), {
                datatype: "json",
                success: function (res) {
                    if (res.res) {
                        update(res, data)
                    } else {
                        alert(res.msg)
                    }
                },
                error: function (res) {
                    console.log("error");
                }
            });
        });
    }
    var addperm = function (data) {
        $(".addperm").off().on("click", function (ev) {
            $.ajax(routes.ADD_PERM.replace("-1", $(this).closest("li").attr("data-id")), {
                datatype: "json",
                success: function (res) {
                    if (res.res) {
                        update(res, data)
                    } else {
                        alert(res.msg)
                    }

                },
                error: function (res) {
                    console.log("error");
                }
            });
        });
    }
    var deleteuser = function (data) {
        $(".deleteuser").off().on("click", function (ev) {
            $.ajax(routes.REMOVE_USER.replace("-1", $(this).closest("li").attr("data-userid")), {
                datatype: "json",
                success: function (res) {
                    if (res.res) {
                        update(res, data)
                    } else {
                        alert(res.msg)
                    }
                },
                error: function (res) {
                    console.log("error");
                }
            });
        });
    }
    var adduser = function (data) {
        $(".adduser").off().on("click", function (ev) {
            console.log("click");

            $.ajax(routes.ADD_USER.replace("-1", $(this).closest("li").attr("data-userid")), {
                datatype: "json",
                success: function (res) {
                    console.log(res);

                    if (res.res) {
                        update(res, data)
                    } else {
                        alert(res.msg)
                    }
                },
                error: function (res) {
                    console.log("error");
                }
            });
        });
    }
    var userAddAutoComplete = $("[data-user-autocomplete]");
    userAddAutoComplete.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: routes.SEARCH_USER,
                dataType: "json",
                data: {
                    q: request.term
                },
                success: function (data) {
                    if (!data.res) {
                        alert("No match found")
                    } else {
                        response(data.elements);
                        adduser()
                    }
                },
                error: function (data) {
                    console.log(data);
                }
            });
        },
        delay: 500,
        minLength: 2
    });
    userAddAutoComplete.autocomplete("instance")._renderItem = function (ul, item) {
        $(ul).addClass("list-group");
        return $("<li>")
            .attr("data-userid", item.id)
            .addClass("list-group-item")
            .append(item.username)
            .append('<span class="pull-right label label-success command adduser">+</span>')
            .appendTo(ul);
    };
    userAddAutoComplete.autocomplete("instance")._resizeMenu = function () {
        this.menu.element.outerWidth(userAddAutoComplete.outerWidth());
    }


    var CONFIG = [{
        container: "[data-permdelete]",
        data: currentPermissions,
        tpl: "perm_del_tpl",
        callback: deleteperm
    }, {
        container: "[data-permadd]",
        data: availablePermissions,
        tpl: "perm_add_tpl",
        callback: addperm
    }, {
        container: "[data-userdelete]",
        data: currentUsers,
        tpl: "user_del_tpl",
        callback: deleteuser
    }, {
        container: "[data-useradd]",
        data: allUsers,
        tpl: "user_add_tpl",
        callback: adduser
    }];
    CONFIG.map(function (obj) {
        render(obj)
    })

})(jQuery);