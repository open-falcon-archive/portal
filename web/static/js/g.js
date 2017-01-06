function err_message_quietly(msg, f) {
    $.layer({
        title: false,
        closeBtn: false,
        time: 2,
        dialog: {
            msg: msg
        },
        end: f
    });
}

function ok_message_quietly(msg, f) {
    $.layer({
        title: false,
        closeBtn: false,
        time: 1,
        dialog: {
            msg: msg,
            type: 1
        },
        end: f
    });
}

function my_confirm(msg, btns, yes_func, no_func) {
    $.layer({
        shade: [ 0 ],
        area: [ 'auto', 'auto' ],
        dialog: {
            msg: msg,
            btns: 2,
            type: 4,
            btn: btns,
            yes: yes_func,
            no: no_func
        }
    });
}

function handle_quietly(json, f) {
    if (json.msg.length > 0) {
        err_message_quietly(json.msg);
    } else {
        ok_message_quietly("successfully:-)", f);
    }
}

// - business function -
function query_user() {
    var query = $.trim($("#query").val());
    var mine = document.getElementById('mine').checked ? 1 : 0;
    window.location.href = '/?q=' + query + '&mine=' + mine;
}

function create_group() {
    var name = $.trim($("#grp_name").val());
    $.post('/group/create', {'grp_name': name}, function (json) {
        handle_quietly(json, function () {
            window.location.reload();
        });
    });
}

function delete_group(group_id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.getJSON('/group/delete/' + group_id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        });
    }, function () {
        return false;
    });
}

function edit_group(group_id, grp_name) {
    layer.prompt({title: 'input new name:', val: grp_name, length: 255}, function (val, index, elem) {
        $.post('/group/update/' + group_id, {'new_name': val}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        });
    })
}

function rename_group() {
    var old_str = $.trim($('#old_str').val());
    var new_str = $.trim($('#new_str').val());
    $.post('/group/rename', {'old_str': old_str, 'new_str': new_str}, function (json) {
        handle_quietly(json, function () {
            window.location.href = '/?q=' + new_str;
        });
    });
}

function bind_plugin(group_id) {
    var plugin_idr = $.trim($("#plugin_dir").val());
    $.post('/plugin/bind', {'group_id': group_id, 'plugin_dir': plugin_idr}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    });
}

function unbind_plugin(plugin_id) {
    my_confirm('确定要解除绑定？', ['确定', '取消'], function () {
        $.getJSON('/plugin/delete/' + plugin_id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        });
    }, function () {
        return false;
    });
}

function query_host() {
    var xbox = $("#xbox").val();
    var group_id = $("#group_id").val();
    var query = $.trim($("#query").val());
    var limit = $("#limit").val();
    var maintaining = document.getElementById('maintaining').checked ? 1 : 0;
    window.location.href = '/group/' + group_id + '/hosts?q=' + query + '&maintaining=' + maintaining + '&limit=' + limit + '&xbox=' + xbox;
}

function select_all() {
    var v = document.getElementById('chk').checked;
    $.each($("#hosts input[type=checkbox]"), function (i, n) {
        n.checked = v;
    });
}

function remove_hosts() {
    var ids = [];
    jQuery.each($("#hosts input[type=checkbox]"), function (i, n) {
        if (n.checked) {
            ids.push($(n).attr("hid"));
        }
    });
    if (ids.length == 0) {
        err_message_quietly('no hosts selected');
        return;
    }

    var group_id = $("#group_id").val();
    $.post("/host/remove", {'host_ids': ids.join(","), 'grp_id': group_id}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    });
}

function maintain() {
    var ids = [];
    jQuery.each($("#hosts input[type=checkbox]"), function (i, n) {
        if (n.checked) {
            ids.push($(n).attr("hid"));
        }
    });
    if (ids.length == 0) {
        err_message_quietly('no hosts selected');
        return;
    }

    var begin = $.trim($("#begin").val());
    var end = $.trim($("#end").val());

    if (begin.length == 0 || end.length == 0) {
        err_message_quietly('begin time and end time are necessary');
        return false;
    }

    var b = moment(begin, "YYYY-MM-DD HH:mm").unix();
    var e = moment(end, "YYYY-MM-DD HH:mm").unix();

    $.post('/host/maintain', {'begin': b, 'end': e, 'host_ids': ids.join(',')}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    });
}

function no_maintain() {
    var ids = [];
    jQuery.each($("#hosts input[type=checkbox]"), function (i, n) {
        if (n.checked) {
            ids.push($(n).attr("hid"));
        }
    });
    if (ids.length == 0) {
        err_message_quietly('no hosts selected');
        return;
    }

    $.post('/host/reset', {'host_ids': ids.join(',')}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    });
}

function batch_add_host() {
    var hosts = $.trim($("#hosts").val());
    if (hosts.length == 0) {
        err_message_quietly('请填写机器列表，一行一个');
        return false;
    }

    $.post('/host/add', {'group_id': $("#group_id").val(), 'hosts': hosts}, function (json) {
        if (json.msg.length > 0) {
            err_message_quietly(json.msg);
        } else {
            $("#message").html(json.data);
        }
    });
}

function host_unbind_group(host_id, group_id) {
    $.getJSON('/host/unbind', {'host_id': host_id, 'group_id': group_id}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    })
}

function query_expression() {
    var query = $.trim($("#query").val());
    var mine = document.getElementById('mine').checked ? 1 : 0;
    window.location.href = '/expressions?q=' + query + '&mine=' + mine;
}

function delete_expression(id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.getJSON('/expression/delete/' + id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        })
    }, function () {
        return false;
    });
}

function update_expression() {
    var callback_url = $.trim($("#callback_url").val());
    var need_callback = callback_url.length > 0 ? 1 : 0;
    $.post(
        '/expression/update',
        {
            'expression': $.trim($("#expression").val()),
            'func': $.trim($("#func").val()),
            'op': $("#op").val(),
            'right_value': $.trim($("#right_value").val()),
            'uic': $.trim($("#uic").val()),
            'max_step': $.trim($("#max_step").val()),
            'priority': $.trim($("#priority").val()),
            'note': $.trim($("#note").val()),
            'url': callback_url,
            'callback': need_callback,
            'before_callback_sms': document.getElementById("before_callback_sms").checked ? 1 : 0,
            'before_callback_mail': document.getElementById("before_callback_mail").checked ? 1 : 0,
            'after_callback_sms': document.getElementById("after_callback_sms").checked ? 1 : 0,
            'after_callback_mail': document.getElementById("after_callback_mail").checked ? 1 : 0,
            'expression_id': $("#expression_id").val()
        },
        function (json) {
            handle_quietly(json);
        }
    );
}

function pause_expression(id) {
    var pause = '1';
    if ($('#i-' + id).attr('class').indexOf('play') > 0) {
        // current: pause
        pause = '0'
    }
    $.getJSON("/expression/pause", {'id': id, 'pause': pause}, function (json) {
        if (json.msg.length > 0) {
            err_message_quietly(json.msg);
        } else {
            if (pause == '1') {
                $('#i-' + id).attr('class', 'glyphicon glyphicon-play orange')
            } else {
                $('#i-' + id).attr('class', 'glyphicon glyphicon-pause orange')
            }
        }
    });
}

function make_select2_for_uic_group(selector) {
    $(selector).select2({
        placeholder: "input uic team name",
        allowClear: true,
        multiple: true,
        quietMillis: 100,
        minimumInputLength: 2,
        id: function (obj) {
            return obj.name;
        },
        ajax: {
            url: "/api/uic/group",
            dataType: 'json',
            data: function (term, page) {
                return {
                    query: term,
                    limit: 20
                };
            },
            results: function (json, page) {
                return {results: json.data};
            }
        },

        initSelection: function (element, callback) {
            var data = [];
            $($(element).val().split(",")).each(function () {
                data.push({id: this, name: this});
            });
            callback(data);
        },

        formatResult: function (obj) {
            return obj.name
        },
        formatSelection: function (obj) {
            return obj.name
        }
    });
}

function query_template() {
    var query = $.trim($("#query").val());
    var mine = document.getElementById('mine').checked ? 1 : 0;
    window.location.href = '/templates?q=' + query + '&mine=' + mine;
}

function delete_template(id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.getJSON('/template/delete/' + id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        })
    }, function () {
        return false;
    });
}

function create_template() {
    var tpl_name = $.trim($("#tpl_name").val());
    $.post('/template/create', {'name': tpl_name}, function (json) {
        if (json.msg.length > 0) {
            err_message_quietly(json.msg);
        } else {
            location.href = '/template/update/' + json.id;
        }
    });
}

function make_select2_for_template(selector) {
    $(selector).select2({
        placeholder: "input template name",
        allowClear: true,
        quietMillis: 100,
        minimumInputLength: 2,
        id: function (obj) {
            return obj.id;
        },
        ajax: {
            url: "/api/template/query",
            dataType: 'json',
            data: function (term, page) {
                return {
                    query: term,
                    limit: 10
                };
            },
            results: function (json, page) {
                return {results: json.data};
            }
        },

        initSelection: function (element, callback) {
            var tpl_id = $(element).val();
            $.getJSON("/api/template/" + tpl_id, function (json) {
                callback(json.data);
            });
        },

        formatResult: function (obj) {
            return obj.name
        },
        formatSelection: function (obj) {
            return obj.name
        }
    });
}

function make_select2_for_metric(selector) {
    $(selector).select2({
        placeholder: "监控项名，如:df.bytes.free.percent",
        allowClear: true,
        quietMillis: 100,
        minimumInputLength: 2,
        id: function (obj) {
            return obj.name;
        },
        ajax: {
            url: "/api/metric/query",
            dataType: 'json',
            data: function (term, page) {
                return {
                    query: term,
                    limit: 10
                };
            },
            results: function (json, page) {
                return {results: json.data};
            }
        },

        initSelection: function (element, callback) {
            var val = $(element).val();
            callback({id: val, name: val});
        },

        formatResult: function (obj) {
            return obj.name
        },
        formatSelection: function (obj) {
            return obj.name
        }
    });
    $(selector).on("change", function (e) { 
        var val = $('#metric').val(); 
        var i=val.indexOf('/');
        if(i > 0){
            $('#metric').val(val.substring(0,i));
            $('#select2-chosen-4').text(val.substring(0,i));
            $('#tags').val(val.substr(i+1));
        }
    });
}

function update_template() {
    var tpl_id = $('#tpl_id').val();
    var name = $.trim($("#name").val());
    var parent_id = $("#parent_id").val();
    $.post('/template/rename/' + tpl_id, {'name': name, 'parent_id': parent_id}, function (json) {
        handle_quietly(json);
    });
}

function save_action_for_tpl(tpl_id) {
    var callback_url = $.trim($("#callback_url").val());
    var need_callback = callback_url.length > 0 ? 1 : 0;
    $.post(
            '/template/action/update/' + tpl_id,
        {
            'uic': $.trim($("#uic").val()),
            'url': callback_url,
            'callback': need_callback,
            'before_callback_sms': document.getElementById("before_callback_sms").checked ? 1 : 0,
            'before_callback_mail': document.getElementById("before_callback_mail").checked ? 1 : 0,
            'after_callback_sms': document.getElementById("after_callback_sms").checked ? 1 : 0,
            'after_callback_mail': document.getElementById("after_callback_mail").checked ? 1 : 0
        },
        function (json) {
            handle_quietly(json);
        }
    );
}

function goto_strategy_add_div() {
    $("#add_div").show('fast');
    $("#current_sid").val('');
    location.href = "#add";
}

function save_strategy() {
    var sid = $("#current_sid").val();
    $.post('/strategy/update', {
        'sid': sid,
        'metric': $.trim($("#metric").val()),
        'tags': $.trim($("#tags").val()),
        'max_step': $.trim($("#max_step").val()),
        'priority': $.trim($("#priority").val()),
        'note': $.trim($("#note").val()),
        'func': $.trim($("#func").val()),
        'op': $.trim($("#op").val()),
        'right_value': $.trim($("#right_value").val()),
        'run_begin': $.trim($("#run_begin").val()),
        'run_end': $.trim($("#run_end").val()),
        'tpl_id': $.trim($("#tpl_id").val())
    }, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    })
}

function clone_strategy(sid) {
    $("#current_sid").val('');
    fill_fields(sid);
}

function modify_strategy(sid) {
    $("#current_sid").val(sid);
    fill_fields(sid);
    $('[data-toggle="tooltip"]').tooltip();
}

function fill_fields(sid) {
    $("#add_div").show('fast');
    location.href = "#add";
    $.getJSON('/strategy/' + sid, {}, function (json) {
        $("#metric").val(json.data.metric);
        $("#tags").val(json.data.tags);
        $("#max_step").val(json.data.max_step);
        $("#priority").val(json.data.priority);
        $("#note").val(json.data.note);
        $("#func").val(json.data.func);
        $("#op").val(json.data.op);
        $("#right_value").val(json.data.right_value);
        $("#run_begin").val(json.data.run_begin);
        $("#run_end").val(json.data.run_end);
        make_select2_for_metric("#metric");
    });
}

function delete_strategy(id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.getJSON('/strategy/delete/' + id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        })
    }, function () {
        return false;
    });
}

function tpl_unbind_group(tpl_id, grp_id) {
    my_confirm('确定要解除绑定关系？', ['确定', '取消'], function () {
        $.getJSON('/template/unbind/group', {'tpl_id': tpl_id, 'grp_id': grp_id}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        })
    }, function () {
        return false;
    });
}

function fork_template(tpl_id) {
    $.getJSON('/template/fork/' + tpl_id, {}, function (json) {
        if (json.msg.length > 0) {
            err_message_quietly(json.msg);
        } else {
            location.href = '/template/update/' + json.id;
        }
    });
}

function bind_template(grp_id) {
    var tpl_id = $.trim($("#tpl_id").val());
    $.getJSON('/group/bind/template', {'grp_id': grp_id, 'tpl_id': tpl_id}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        })
    });
}

function node_unbind_tpl(grp_name, tpl_id) {
    my_confirm('确定要解除绑定关系？', ['确定', '取消'], function () {
        $.getJSON('/template/unbind/node', {'tpl_id': tpl_id, 'grp_name': grp_name}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        })
    }, function () {
        return false;
    });
}

function node_bind_tpl() {
    var node = $.trim($("#node").val());
    var tpl_id = $("#tpl_id").val();
    $.post('/template/bind/node', {'node': node, 'tpl_id': tpl_id}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    });
}

function create_cluster_monitor_metric(grp_id) {
    $.post('/group/' + grp_id + '/cluster/creator', {
        'numerator': $("#numerator").val(),
        'denominator': $("#denominator").val(),
        'endpoint': $("#endpoint").val(),
        'metric': $("#metric").val(),
        'tags': $("#tags").val(),
        'step': $("#step").val()
    }, function (json) {
        handle_quietly(json, function () {
            location.href = "/group/" + grp_id + "/cluster";
        });
    })
}

function update_cluster_monitor_metric(cluster_id, grp_id) {
    $.post('/cluster/edit/' + cluster_id, {
        'numerator': $("#numerator").val(),
        'denominator': $("#denominator").val(),
        'endpoint': $("#endpoint").val(),
        'metric': $("#metric").val(),
        'tags': $("#tags").val(),
        'step': $("#step").val(),
        'grp_id': grp_id
    }, function (json) {
        handle_quietly(json);
    });
}

function delete_cluster_monitor_item(cluster_id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.post('/cluster/delete/' + cluster_id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            })
        });
    }, function () {
        return false;
    });
}
