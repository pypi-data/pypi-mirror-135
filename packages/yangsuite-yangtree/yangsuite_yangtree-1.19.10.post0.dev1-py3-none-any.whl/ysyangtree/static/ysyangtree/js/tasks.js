/**
  * Module for handling tasks.  Tasks are made up of YANG metadata used to form
  * YANG messages.  This metadata can be used by any transport to create the
  * YANG message in the transports format.
  *
  * This module should be reusable for all transports.
  */
let tasks = function() {
    "use strict";

    /**
     * Default configurations
     */
    let config = {
        categorySelect: 'select#ys-replay-cat-list',
        select: 'select#ytool-task-list',
        textarea: 'textarea#ytool-rpc-data',
        textareaInfo: 'textarea#ytool-rpc-info',
        deviceSelect: 'select#ys-devices-replay',
        prefixSelect: 'select#ys-rpcprefixes',
        datastoreGroup: '#ys-datastore-group',
        savetaskdialog: 'div#ys-save-task',
        testDiv: 'div#ytool-test-col',
        runDiv: 'div#ytool-run-dialog',
        variablesGroup: 'form-group#ys-variables',
        variableMsg: "#ys-variable-msg",
        progressBar: "#ys-progress",
        getURI: '/yangtree/gettask/',
        getTaskListURI: '/yangtree/gettasklist/',
        getVarsURI: '/yangtree/getvariables/',
        saveURI: '/yangtree/savetask/',
        editURI: '/yangtree/edittask/',
        deleteURI: '/yangtree/deltask/',
        saveYamlReplayURI: '/yangtree/saveyamlreplay/',
        getCategoriesURI: '/yangtree/getcategories/',
        deleteCategoryURI: '/yangtree/delcategory/',
        changeCategoryURI: '/yangtree/changecategory/',
        inputTopDir: 'input#ys-replay-dir',
        getTopDirURI: '/yangtree/getreplaydir/',
        topDirURI:'/yangtree/setreplaydir/',
        resetTopDirURI:'/yangtree/resetreplaydir/',
        buttonTopDir: 'button#ys-replay-dir-btn',
        buttonTopDirReset: 'button#ys-reset-replay-dir-btn',

        generateReplaysDialog: "div#ys-generate-replays-dialog",
        savereplayyamlURI: '/yangtree/savereplayyaml/'
    };

    let c = config;

    let locals = {
        taskSegmentCtr: 0,
        taskCurrent: null,
        manifest: {default: null},
        lastReplay: null
    };

    /**
     * Retrieve a list of replay categories available.
     *
     * @param {boolean} generated_only - If true, only categories containing
     *        generated replays will be listed.
     */
    function getCategories(generated_only=false) {
        let progressBar = startProgress($(config.progressBar), null, {},
                                        "Loading replay categories...");

        return $.when($.get(c.getCategoriesURI, {generated_only: generated_only}))
            .then(function(retObj) {
                stopProgress(progressBar);
                return retObj;
            }, function(retObj) {
                stopProgress(progressBar);
                popDialog(retObj.reason);
                return retObj;
            });
    };

    /**
     * Retrieve a task or a list of tasks from the local file system.
     *
     * @param {string} category - Name of the category whose tasks we want to fetch.
     */
    function getTaskList(category="") {
        return $.when(getPromise(config.getTaskListURI, {category: category}));
    }


    /**
     * Retrieve a task or a list of tasks from the local file system.
     *
     * @param {string} name - Name of task to retrieve.  If the name is blank,
     *        a list of tasks are retrieved.
     * @param {function} callback - Caller may have other ways to present
     *.                             tasks.
     */
    function getTasks(name="", callback=null) {
        let categories = [];
        let currentCat = $(config.categorySelect).val();
        let currentTask = $(config.select).val();

        let progressText = (name ?
                            "Loading replay \"" + name + "\"..." :
                            "Loading replay list...");
        let progressBar = startProgress($(config.progressBar), null, {},
                                        progressText);

        return $.when(getPromise(config.getURI, { name: name }))
            .then(function (retObj) {
                if (callback) {
                    callback(retObj);
                } else {
                    if ($.isEmptyObject(retObj)) {
                        stopProgress(progressBar);
                        $(config.categorySelect).empty().append($('<option>').val(''));
                        $(config.select).empty().append($('<option>').val(''));
                        return;
                    }
                    locals.manifest = retObj;
                    categories = (Object.keys(retObj));
                    if (categories.indexOf(currentCat) < 0) {
                        /* current category was removed */
                        currentCat = categories[0];
                    }
                    categories.sort();
                    $(config.select).empty();
                    $(config.categorySelect).empty();
                    let hasCurrentCategory = false;
                    for (let key of categories) {
                        $(config.categorySelect).append($('<option>')
                            .text(key)
                            .prop('value', key));
                        if (key == currentCat) {
                            hasCurrentCategory = true;
                        }
                    }

                    if (!hasCurrentCategory) {
                        currentCat = categories[0];
                    }

                    $(config.categorySelect).val(currentCat);
                    $(config.categorySelect).trigger("chosen:updated");

                    let hasCurrentTask = false;
                    let currentTasks = locals.manifest[currentCat];
                    for (let tsk of currentTasks) {
                        $(config.select).append($('<option>')
                            .text(tsk[0])
                            .prop('value', tsk[0]));
                        if (tsk[0] == currentTask) {
                            hasCurrentTask = true;
                        }

                    }
                    if (!hasCurrentTask) {
                        currentTask = currentTasks[0];
                    }
                    $(config.select).val(currentTask);
                    $(config.select).trigger("chosen:updated");

                    $(config.categorySelect).change(function () {
                        let currentTasks = locals.manifest[$(config.categorySelect).val()];
                        $(config.select).empty();
                        for (let tsk of currentTasks) {
                            $(config.select).append($('<option>')
                                .text(tsk[0])
                                .prop('value', tsk[0]));
                        }
                        $(config.select).trigger("chosen:updated");
                    });

                    $(config.select).change(function () {
                        let selectedTask = $(config.select).val();
                        let selectedCategory = $(config.categorySelect).val();
                        if (typeof (selectedTask) == "string") {
                            getTaskVariables(selectedTask, selectedCategory);
                        } // else it's an array, and getTaskVariables doesn't apply
                    });
                }
                stopProgress(progressBar);
            })
            .fail(function (retObj) {
                stopProgress(progressBar);
                popDialog(retObj.reason);
            });
    };

    /**
     * Helper function to getTasks().
     * Retrieves the specified replay and parses its contents to identify
     * any/all variables present, then calls replayVariablesPopulate
     * with the list of variables.
     *
     * @param {string} name - Name of replay task to load variables.
     * @param {string} category - Name of task category to load variables.
     */
    function getTaskVariables(name,category){
        let data = {'name': name, 'category': category};

        return $.get(config.getVarsURI, data).then(function(retObj) {
            // Convert list of variables to dictionary of variable: value
            let variables = {};
            for (let v of retObj.variables) {
                variables[v] = "";
            }
            replayVariablesPopulate(variables);
        }, function(retObj) {
            popDialog(retObj.reason);
        });

    }

    /**
     * Retrieve task data
     *
     * @param {string} name - Name of task to retrieve.
     * @param {string} category - category task resides in.
     */
    function getTask(name, category, callback=null) {

        return $.when(getPromise(config.getURI, {name: name, category: category}))
        .then(function(retObj) {
            locals.lastReplay = retObj.task;
            if (callback) {
                callback(retObj);
            } else {
                return retObj;
            }
        });
    }

    /**
     * Remove prefixes not in configuration xpaths
     *
     * @param {array} prefixes - All possible prefies used in a module.
     * @param {array} configs - The xpath with value of a configuration.
     */
    function trimPrefixes(prefixes, configs) {
        let trimmedPrefixes = {};
        for (let cfg of configs) {
            for (let pfx of Object.keys(prefixes)) {
                if (cfg.xpath.indexOf("/" + pfx + ":") > -1) {
                    trimmedPrefixes[pfx] = prefixes[pfx];
                }
                if (cfg['value'] && cfg['value'].startsWith(pfx + ":")) {
                    trimmedPrefixes[pfx] = prefixes[pfx];
                }
            }
        }
        return trimmedPrefixes;
    }

    /**
     * Save a task on the local file system.  Get RPCs saved by addRPC.
     *
     * @param {string} name -  Name of task to save.
     * @param {string} desc - Description of task.
     * @param {Object} segments - Collections of YANG metadata with each segment
     *        segment representing a YANG action defined from a single YANG
     *        module.
     * @param {array} devices - Devices task was run on.
     * @param {string} images - Images task was run on.
     *                          (comma or newline delimited)
     * @param {string} category - category task reside in.
     * @param {boolean} overwrite - whether to overwrite any existing replay
     * @param {boolean} autogenerated - whether this is an autogenerated replay
     */
    function saveTask(name, desc, segments, devices, images, category,
                      overwrite=false, autogenerated=false) {
        if (segments.length < 1) {
            popDialog("No RPCs Built to save");
            return;
        }

        let segs = [];
        if (typeof(segments) == "string") {
            // Custom RPC
            segs = segments;
        } else {
            $.each(segments, function(i, seg) {
                if (seg.cfgd) {
                    // Fix format and trim prefixes.
                    let segment = {
                        'segment': ++i,
                        'commit': seg.commit,
                    };

                    let modules = {};

                    for (let mod of Object.keys(seg.cfgd.modules)) {
                        // Remove uneeded prefixes.
                        let pfxs = trimPrefixes(seg.cfgd.modules[mod].namespace_prefixes,
                                                seg.cfgd.modules[mod].configs);
                        modules[mod] = {
                            "namespace_prefixes": pfxs,
                            "configs": seg.cfgd.modules[mod].configs,
                            "revision": seg.cfgd.modules[mod].revision
                        }
                    }

                    segment['yang'] = {
                        "proto-op": seg.cfgd["proto-op"],
                        "modules": modules
                    };

                    segs.push(segment);
                } else {
                    // This one is good to go
                    segs.push(seg);
                }
            });
        }

        let data = {'name': name,
                    'description': desc,
                    'segments': segs,
                    'devices': devices,
                    'images': images,
                    'category': category,
                    'autogenerated': autogenerated,
                    'overwrite': overwrite
        };

        return $.when(jsonPromise(config.saveYamlReplayURI, data)).then(function(retObj) {
            getTasks();
            popDialog(retObj.reply);
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    function updateTaskData() {
        let rpc;
        if ($("#ys-rpctype").val() == "custom" ||
            $("#ytool-rpc-data").hasClass("source-of-truth")) {
            rpc = $("#ytool-rpc-data").val();
        } else {
            rpc = rpcmanager.config.savedrpcs;
        }
        if (!rpc || rpc.length < 1) {
            popDialog("No RPC data to save as replay");
        }
        return saveTask(locals.lastReplay.name,
                        locals.lastReplay.description,
                        rpc,
                        [],  // devices
                        locals.lastReplay.images,
                        locals.lastReplay.category,
                        true, // overwrite
                        locals.lastReplay.autogenerated,
                        );
    };

    /**
     * Delete a task from the local file system.
     *.
     * This function should be reusable for all transports.
     *
     * @param {string} name - Name of task to delete.
     * @param {string} category - category task reside in.
     */
    function deleteTask(name_or_names, category) {
        let data = {category: category};
        if (typeof(name_or_names) == 'string') {
            data['name'] = name_or_names;
        } else {
            data['names[]'] = name_or_names;
        }

        return $.when(getPromise(config.deleteURI, data))
        .then(function(retObj) {
            getTasks();
            popDialog(retObj.reply);
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    /**
     * Delete a category of replays and all replays it contains.
     *
     * @param {string} category - Category to delete.
     */
    function deleteCategory(category) {
        let pb = startProgress($(config.progressBar));
        return getPromise(config.deleteCategoryURI, {category: category})
            .then(function(retObj) {
                progressComplete(pb, retObj.result);
                getTasks();
            }, function(retObj) {
                popDialog("Error " + retObj.status + ": " + retObj.statusText);
                stopProgress(pb);
            });
    };

    /**
     * Change the category of an existing replay(s) without otherwise
     * editing its contents.
     */
    function changeCategory(replays, oldCat, newCat) {
        let pb = startProgress($(config.progressBar));
        let data = {replays: replays, old_category: oldCat, new_category: newCat};
        return getPromise(config.changeCategoryURI, data).then(function(retObj) {
            if (!retObj.errors || retObj.errors.length == 0) {
                progressComplete(pb, retObj.result);
            } else {
                let msg = $("<div>").text(retObj.result);
                let list = $("<ul>");
                msg.append(list);
                for (let error of retObj.errors) {
                    list.append($("<li>").text(error));
                }
                stopProgress(pb);
                popDialog(msg);
            }
            getTasks();
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
            stopProgress(pb);
        });
    };

    /**
     * Construct a pseudo-combobox consisting of a text <input> and
     * a <button> with a Bootstrap dropdown menu of default options,
     * where selecting any value from the dropdown populates it into the
     * <input>, but the user can also enter arbitrary values as well.
     *
     * @param {jQuery} container: Containing element (div, td, etc.)
     * @param {string} name: name attribute to set on the input element
     * @param {Array} options: list of values to populate the dropdown
     * @param {string} initial: initial value to set on the input
     *
     * @return {jQuery} input + button + dropdown
     */
    function comboBox(container, name, options, initial="") {
        let inputID = "input-" + name;
        let buttonID = "dropdown-" + name;

        // Input textbox
        let input = $("<input>", {
            class: 'form-control',
            name: name,
            value: initial,
            type: "text",
            id: inputID,
        });

        // Dropdown-triggering button
        let button = $("<button>", {
            class: "btn btn--dropdown btn--icon btn--small",
            type: "button",
            id: buttonID,
        });

        button.click(function(e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            $(this).parent().toggleClass("active");
        });

        // Menu and its contents
        let menu = $("<div>", {
            class: "dropdown__menu dropdown__menu--openleft"
        }).css({'white-space': 'normal'});
        for (let option of options) {
            let link = $("<a>" + option + "</a>");
            link.click(function() {
                $('input[name="' + name + '"]').val(option);
                // Close the menu
                $(this).parent().parent().toggleClass("active");
            });
            menu.append(link);
        }

        container
            .append($('<div class="input-group" style="white-space: nowrap">')
                    .append(input)
                    .append($('<div class="dropdown dropdown--left">')
                            .append(button)
                            .append(menu)
                            )
                    );

        // Make sure the dropdown will be visible
        container.css({
            overflow: 'visible',
            'white-space': 'normal'
        });

        return container;
    };

    function getEditDialog(name, category) {
        return getTask(name, category, popEditDialog);
    }

    /**
     * Helper function to popEditDialog() and getSaveDialog().
     */
    function fillSaveTaskDialog(task) {
        let dialogHtml = $("<div>");
        dialogHtml
            .append($('<div class="form-group label--inline">')
                    .append($('<div class="form-group__text">')
                            .append('<label for="ys-task-name">Replay Name</label>')
                            .append('<input type=text id="ys-task-name" />')))
            .append($('<div class="form-group label--inline">')
                    .append($('<div class="form-group__text">')
                            .append('<label>Category (enter new category or choose from existing)')
                            .append($('<div id="ys-task-category" style="order: 3"/>'))))
            .append($('<div class="form-group label--inline">')
                    .append('<label for="ys-task-desc">Description</label>')
                    .append('<textarea id="ys-task-desc" class="textarea"' +
                            ' rows="2" style="width:100%"' +
                            ' placeholder="Describe this replay" ></textarea>'))
            .append($('<div class="form-group">')
                    .append('<div id="ys-dev">Select all devices tested by task</div>')
                    .append('<select id="ys-replay-device" multiple><pre id="ys-platforms">'))
            .append($('<div class="form-group">')
                    .append('<label for="ys-task-imgs">Tested images (comma or newline separated)</label>')
                    .append('<textarea id="ys-task-imgs" class="textarea"' +
                            ' rows="3" style="width:100%"' +
                            ' placeholder="image1, image2, ..."></textarea>'))
        ;

        $(config.savetaskdialog).empty().html(dialogHtml);

        if (!task) {
            return;
        }

        $("#ys-task-name").val(task.name);
        $("#ys-task-desc").val(task.description);

        let cats = [];
        $("#ys-replay-cat-list option").each(function(i, cat) {
            cats.push($(cat).val());
        });
        if (cats) {
            comboBox($("#ys-task-category"), "ysCategory", cats, task.category);
        }

        if (task.images) {
            $("#ys-task-imgs").val(task['images'].toString());
        }
        let devices = [];
        $("#ys-devices-replay option").each(function(i, val) {
            if ($(val).val() == "") {
                return true;
            }
            if (task.devices) {
                if (task.devices.indexOf($(val).val()) > -1) {
                    $("#ys-replay-device").append('<option value="'+$(val).val()+'" selected=true>'+$(val).text()+'</option>');
                    task.devices.splice(task.devices.indexOf($(val).val()), 1);
                    return true;
                }
            }
            $("#ys-replay-device").append('<option value="'+$(val).val()+'">'+$(val).text()+'</option>');
        });
        if (task.devices) {
            task.devices.sort();
            $.each(task.devices, function(i, dev) {
                $("#ys-replay-device").append('<option value="'+dev+'" selected=true>'+dev+'</option>');
            })
        }
        if (task.platforms) {
            let platforms = "<pre><strong>Platforms already tested:</strong>\n"
            for (let p of task.platforms) {
                platforms += p + "\n";
            }
            platforms += "</pre>";
            $("#ys-replay-device").after(platforms);
        }
    }

    function popEditDialog(replay) {
        if (!replay) {
            popDialog("No replay to modify");
            return;
        }
        let task = replay.task;

        $(config.savetaskdialog)
        .dialog({
            title: "Modify Replay Settings",
            minHeight: 222,
            minWidth: 760,
            buttons: {
                "Modify Replay": function () {
                    let newName = $("#ys-task-name").val();
                    let desc = $("#ys-task-desc").val();
                    let devs = [];
                    let images = $("#ys-task-imgs").val();
                    let cat = $("[name=ysCategory]").val();
                    $("#ys-replay-device :selected").each(function() {
                        devs.push($(this).val());
                    });
                    if (!newName || !cat) {
                        $("#ys-task-name").prev().css("color", "FireBrick");
                        $("#ys-task-category").prev().css("color", "FireBrick");
                        popDialog("Fields highlighted are required");
                        return;
                    }
                    if (images.indexOf(",") == -1) {
                        images = images.split("\n");
                    } else {
                        images = images.split(",");
                    }
                    let category;
                    if (task.category) {
                        category = task.category;
                    } else {
                        /* old tasks don't have categories */
                        category = 'default';
                    }

                        let data = {'name': task.name,
                                    'newName': newName,
                                    'description': desc,
                                    'devices': devs,
                                    'images': images,
                                    'category': category,
                                    'newCat': cat
                        };

                        $.when(jsonPromise(config.editURI, data)).then(function (retObj) {
                            popDialog(retObj.reply);
                            getTasks();
                        }, function (retObj) {
                            popDialog("Error " + retObj.status + ": " + retObj.statusText);
                            getTasks();
                        });

                        $(this).dialog("close");
                    },
                    "Cancel": function () {
                        $(this).dialog("close")
                    }
                }
            });

        fillSaveTaskDialog(task);

    }

    /**
     * Open the dialog box for "Save for Replay" values.
     *
     */
    function getSaveDialog() {
        fillSaveTaskDialog();

        $(config.savetaskdialog)
            .dialog({
                title: "Save Replay Settings",
                minHeight: 222,
                minWidth: 760,
                buttons: {
                    "Save Replay": function () {
                        let name = $("#ys-task-name").val();
                        let desc = $("#ys-task-desc").val();
                        let devs = [];
                        let images = $("#ys-task-imgs").val();
                        let cat = $("[name=ysCategory]").val();
                        $("#ys-replay-device :selected").each(function () {
                            devs.push($(this).val());
                        });
                        if (!name || !cat) {
                            $("#ys-task-name").prev().css("color", "FireBrick");
                            $("#ys-task-category").prev().css("color", "FireBrick");
                            popDialog("Fields highlighted are required");
                            return;
                        } else if ($("#ytool-task-list option[value='" + name + "']").length > 0) {
                            popDialog("Replay already exists; Delete old replay or choose another name.", true);
                            return;
                        } else if ($("#ys-rpctype").val() == "custom" ||
                            $("#ytool-rpc-data").hasClass("source-of-truth")) {
                            let rpc = $("#ytool-rpc-data").val();
                            if (!rpc) {
                                popDialog("No custom data to save.");
                                return;
                            }
                            saveTask(name, desc, rpc, devs, images, cat);
                            $(this).dialog("close");
                            return;
                        } else if (rpcmanager.config.savedrpcs.length < 1) {
                            popDialog("No YANG data for replay");
                            return;
                        }
                        if (images) {
                            images = images.split(/[\s,]+/);
                        }
                        saveTask(name, desc, rpcmanager.config.savedrpcs, devs, images, cat);

                        $(this).dialog("close");
                    },
                    "Cancel": function () {
                        $(this).dialog("close")
                    }
                }
            });

        let cats = [];
        $("#ys-replay-cat-list option").each(function(i, cat) {
            cats.push($(cat).val());
        });
        if (cats) {
            comboBox($("#ys-task-category"), "ysCategory", cats);
        }

        $("#ys-devices-replay option").each(function(name, val) {
            if ($(val).val() == "") {
                return true;
            }
            $("#ys-replay-device").append('<option value="'+$(val).val()+'">'+$(val).text()+'</option>');
        });

    }

    /**
     * Operate on the user-entered replay variables:
     * - "clear" all user inputs
     * - "add" an additional variable-value field pair
     * - "retrieve" all variable-value pairs as a dictionary.
     */
    function replayVariables(action) {
        switch(action) {
            case "clear":
                $(config.variablesGroup).empty();
                $(config.variableMsg).show();
            case "add":
                $(config.variablesGroup).append(
                      '<div class="ys-var-pair">\
                       <input class="ys-var-name" placeholder="interface" />\
                       <input class="ys-var-val" placeholder="GigabitEthernet2" />\
                      </div>');
                      $(config.variableMsg).show();
                break;
            case "retrieve":
                let variables = {};
                $.each($(".ys-var-pair"), function(i, varpair) {
                    let name = $(varpair).find(".ys-var-name").val().trim();
                    let val = $(varpair).find(".ys-var-val").val().trim();
                    if (name && val) {
                        variables[name] = val;
                    }
                });
                return variables;
                break;
        }
    };

    /**
     * Helper to getTasks/getTaskVariables.
     * For the given dictionary of variables-to-values, construct the UI input
     * elements used to define the variable values for later use with
     * the replayVariables() function.
     */
    function replayVariablesPopulate(variables){
        $(config.variablesGroup).empty();
        if (Object.keys(variables).length === 0) {
            $(config.variablesGroup).append(
                '<div class="ys-var-pair">\
                 <input class="ys-var-name" placeholder="interface" />\
                 <input class="ys-var-val" placeholder="GigabitEthernet2" />\
                </div>');
            $(config.variableMsg).show();
        }
        else {
            for (var index in variables) {
                if (variables[index].length == 0) {
                    $(config.variablesGroup).append(
                        '<div class="ys-var-pair">\
                            <input class="ys-var-name" value="' + index + '"/>\
                            <input class="ys-var-val" placeholder="' + index + '"/>\
                            </div>');
                    }
                    else{
                        $(config.variablesGroup).append(
                            '<div class="ys-var-pair">\
                            <input class="ys-var-name" value="' + index + '"/>\
                            <input class="ys-var-val" value="' + variables[index] + '"/>\
                            </div>');
                }
                $(config.variableMsg).hide();
            }
        }
    };

    /**
     * Render an HTML representation of the given replay to the given target.
     */
    function renderReplay(category, replayName, target) {
        function render(data, parent) {
            if (Array.isArray(data)) {
                for (let entry of data) {
                    let item = $("<li>");
                    let sublist = $("<ul>");
                    render(entry, sublist);
                    item.append(sublist);
                    parent.append(item);
                }
            } else {
                for (let key of Object.keys(data)) {
                    let item = $("<li>").append($("<strong>").text(key + ": "));
                    if (Array.isArray(data[key])) {
                        let sublist = $('<ol>');
                        render(data[key], sublist);
                        item.append(sublist);
                    } else if (typeof(data[key]) == "object") {
                        let sublist = $('<ul>');
                        render(data[key], sublist);
                        item.append(sublist);
                    } else {
                        item.append($('<pre style="display: inline-block; vertical-align: top">')
                                    .text(data[key]));
                    }
                    parent.append(item);
                }
            }
        };
        return getTask(replayName, category, function(retObj) {
            let listing = $("<ul>");
            render(retObj, listing);
            target.html(listing);
        });
    };

    function getTopReplayDir() {
        return $.get(config.getTopDirURI).then(function(retObj) {
            $(config.inputTopDir).val(retObj.replaydir);
        });
    };

    /**
     * Sets the replay directory path
     */
    function setTopReplayDir() {
        let replay_dir = $(config.inputTopDir).val();
        return $.when(getPromise(config.topDirURI, {replay_dir: replay_dir, createDirectory: false}))
        .then(function (data) {
            getTasks();
            $(config.inputTopDir).val(data.replay_dir_path);
            popDialog("Replay Directory : " + data.replay_dir_path + " is set");
        })
        .fail(function (retObj) {
            if(retObj.status == "404"){
                var replayDir = JSON.parse(retObj.responseText).replay_dir_path;
                showCreateReplayDirDialog(replayDir);
            }else{
                popDialog("Status: " + retObj.status + "\n" + retObj.statusText);
            }
        });
    }

    /**
     * Displays popup dialog if replay directory does not exists.
     * @param {*} replayDirPath
     */
    function showCreateReplayDirDialog(replayDirPath) {
        let dialog = $("<p><b><q>" + replayDirPath + "</q></b> does not exist. Create it?</p>").dialog({
            maxWidth: 600,
            maxHeight: 500,
            width: 425,
            height: 200,
            modal: true,
            title : "YANG Suite",
            buttons: {
                "Create": function () {
                    dialog.dialog('close');
                    createNewTopReplayDir(replayDirPath);
                },
                "Cancel": function () {
                    dialog.dialog('close');
                }
            }
        });
    }
    /**
     * Creates a new replay directory at the specified path
     * @param {*} replay_dir
     */
    function createNewTopReplayDir(replay_dir) {
        return $.when(getPromise(config.topDirURI, {replay_dir: replay_dir, "createDirectory": true}))
            .then(function(data) {
                $(config.inputTopDir).val(data.replay_dir_path);
                popDialog("New Replay Directory : " + data.replay_dir_path + " is set");
                getTasks();
            })
            .fail(function(retObj){
                popDialog("Status: " + retObj.status + "\n" + retObj.statusText);
            });
    }

    function resetTopReplayDir() {
        return $.when(getPromise(config.resetTopDirURI))
        .then(function(retObj) {
            $(config.inputTopDir).val(retObj.replaydir);
            getTasks();
        })
        .fail(function (retObj) {
            popDialog("Status: " + retObj.status + "\n" + retObj.statusText);
        });
    }

    /**
     * Display the dialog box for generating replays.
     */
    function generateReplaysUI(yangset, module, xpath) {
        $(c.genReplaysYangset).val(yangset);
        $(c.genReplaysModule).val(module);
        $(c.genReplaysXpath).val(xpath);
        $(c.genReplaysCategory).val("");
        $(c.genReplaysOutput).val("");

        let oldInputTopDir = config.inputTopDir;
        config.inputTopDir = c.genReplaysOutput;
        getTopReplayDir().then(function() {
            config.inputTopDir = oldInputTopDir;
        });

        $(c.generateReplaysDialog).dialog({
            title: "Generate replays",
            width: 700,
        }).dialog("open");
    };
    /**
     * Save task data
     *
     * @param {string} name - Name of task to save.
     * @param {string} category - category task resides in.
     * @param {string} segments - segments task resides in.
     */
     function savereplayyaml(name, category, segments, callback=null) {
         let task = {
                 'category':category,
                  'segments':segments,
                  'name':name
                }

        return $.when(getPromise(config.savereplayyamlURI, {name: name, category: category, task: JSON.stringify(task)}))
        .then(function(retObj) {
            if (callback) {
                callback(retObj);
            } else {
                return retObj;
            }
        });
    }

    /**
     * Public APIs
     */
    return {
        config: config,
        getCategories: getCategories,
        getTask: getTask,
        getTasks: getTasks,
        saveTask: saveTask,
        updateTaskData: updateTaskData,
        deleteTask: deleteTask,
        deleteCategory: deleteCategory,
        changeCategory: changeCategory,
        getSaveDialog: getSaveDialog,
        getEditDialog: getEditDialog,
        replayVariables: replayVariables,
        replayVariablesPopulate: replayVariablesPopulate,
        renderReplay: renderReplay,
        resetTopReplayDir: resetTopReplayDir,
        getTopReplayDir: getTopReplayDir,
        setTopReplayDir: setTopReplayDir,
        generateReplaysUI: generateReplaysUI,
        getTaskList: getTaskList,
        savereplayyaml:savereplayyaml,
    };
}();
