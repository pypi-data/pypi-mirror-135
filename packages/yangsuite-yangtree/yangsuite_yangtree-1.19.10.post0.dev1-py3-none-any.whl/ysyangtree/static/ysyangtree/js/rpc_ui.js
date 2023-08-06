/**
 * Module providing shared UI functions for RPC plugins (NETCONF, gNMI, etc.)
 */
let rpc_ui = function () {

    let config = {
        progressBar: "div#ys-progress",

        /* Function returning 'get', 'get-config', 'edit-config', 'action', or 'rpc' */
        getProtocolOperation: undefined,

        /* Function building HTML to populate into the 'Operation' column */
        buildEditProtocolOperationMenu: undefined,

        /* Div to use to pop up a dialog for inputting anyxml data */
        anyxmlDialog: "div#ys-anyxml-dialog",
        /* Textarea within anyxmlDialog */
        anyxmlTextArea: "#ys-anyxml-text",
        /* Div to use to pop up a dialog for inputting bits data */
        bitsDialog: "div#ys-bits-dialog",

        /* Data keys to update in updateListKeyXPaths() */
        listKeyXpaths: ['xpath', 'xpath_pfx'],

        /* Callback function to construct the context menu for a node in the tree */
        nodeContextMenu: undefined,   // initialized below
        stripPredicate: new RegExp(
            `\\[[^\\[\\]]+=("[^"]*"|'[^']*'|` +
            `concat\\((?:"[^"]*"|'[^']*')(?: *, *(?:"[^"]*"|'[^']*'))*\\))\\]`),
        addListNodesRpc:[]
    };

    let c = config;  // internal alias for brevity

    /**
     * Creates different input types in tree cells depending on
     * value choices of node
     *
     * @param {Object} node JSTree node for a YANG leaf, container, etc...
     * @param {boolean} allowEmpty Is an empty value for this item valid?
     * @return HTML fragment
     */
    function buildInputType(node, tree, allowEmpty) {
        if (node.data.hasOwnProperty('modtype')) {
            /* Module or submodule - not an input */
            return "";
        }
        let id = node.id;
        let data = node.data;
        let ntype = data['nodetype'];
        let attrStr = ' nodeid="' + id + '" class="ys-cfg-rpc" ';
        let target = null;

        /*
         * Special cases for non-leaf, non-leaf-list nodes that still take
         * values as input:
         */
        if (ntype == 'choice' || ntype == 'case' ||
            ntype == 'input' || ntype == 'output') {
            // Non-data node types; these never have an associated input
            return "";
        } else if (ntype == 'container') {
            if (data['presence']) {
                // No value, just present/absent
                return $('<label' + attrStr + '>' +
                    '<input type="radio" checked>presence</label>');
            } else if (allowEmpty) {
                return $('<input type="checkbox"' + attrStr + 'checked>');
            }
        } else if (ntype == 'list' && allowEmpty) {
            return $('<input type="checkbox"' + attrStr + 'checked>');
        } else if (ntype == 'anyxml' || ntype == 'anydata') {
            /*
             * This data can potentially be quite large, so we'll create
             * a pop-up dialog for the user input.
             */
            target = $("<span>");
            let button = $('<button class="btn btn--small btn-jstree-grid">' +
                'XML&hellip;</button>');
            let textarea = $('<textarea' + attrStr + 'hidden' +
                ' placeholder="XML string"></textarea>');
            $(c.anyxmlDialog).dialog({
                title: ntype + ' data for ' + node.text,
                autoOpen: false,
                width: 650,
                minWidth: 650,
                height: 'auto',
            });
            button.click(function () {
                $(c.anyxmlTextArea).val(textarea.val());
                $(c.anyxmlDialog).dialog({
                    buttons: {
                        'Save': function () {
                            let val = $(c.anyxmlTextArea).val();
                            try {
                                $.parseXML(val);
                                textarea.val(val);
                                $(this).dialog("close");
                            } catch (e) {
                                popDialog("Invalid XML - please double-check your input.");
                            }
                        },
                        'Cancel': function () { $(this).dialog("close"); }
                    }
                }).dialog("open");
            });
            target.append(button);
            target.append(textarea);
            return (target);
        } else if (ntype == 'rpc' || ntype == 'action') {
            return $('<input type="checkbox"' + attrStr + 'checked>');
        }

        if (ntype != 'leaf' && ntype != 'leaf-list') {
            return "";
        }

        /*
         * Handling for various leaf/leaf-list datatypes follows
         */
        let dtype = data['datatype'];
        if (dtype == 'empty') {
            // No value, just present/absent
            return $('<input type="checkbox"' + attrStr + 'checked>');
        } else if (data.hasOwnProperty('bits')) {
            target = $('<button' + attrStr + 'value="">--</button>');
            target.addClass("btn-jstree-grid");
            target.click(function (e) {
                e.preventDefault();
                e.stopImmediatePropagation();
                $(c.bitsDialog).empty();
                for (let bitname of data.bits) {
                    $(c.bitsDialog).append(
                        '<div><label class="ys-cfg-label">' +
                        '<input type="checkbox" name="' + bitname + '">' +
                        bitname + '</label>');
                    $('#ys-bits-dialog input[name="' + bitname + '"]')
                        .prop('checked',
                            target.val().split(' ').includes(bitname));
                }
                $(c.bitsDialog).dialog({
                    title: 'Bits setting for "' + node.text + '"',
                    minWidth: 400,
                    height: 'auto',
                    buttons: {
                        'Set bits': function () {
                            let setBits = $(c.bitsDialog + " :checked")
                                .map(function () {
                                    return $(this).attr('name');
                                })
                                .get();
                            target.val(setBits.join(' '));
                            target.text(setBits.join(' | ') || '--');
                            /* Trigger "change" event if appropriate */
                            if (data.hasOwnProperty('key')) {
                                updateListKeyXPaths(node, target.val(), tree);
                            }
                            $(this).dialog("close");
                        },
                        'Cancel': function () { $(this).dialog("close"); }
                    }
                }).dialog("open");
            });
            /* Go ahead and pop the dialog immediately */
            //btn.trigger('click');
            target.trigger('click');
        } else if (data.hasOwnProperty('leafref_path')) {
            /* TODO: autocomplete with user-entered values of target leaf? */
            target = $('<input type="text"' + attrStr +
                'placeholder="-> ' + data.leafref_path + '">');
        } else if (data.hasOwnProperty('min') ||
            (data.hasOwnProperty('typespec') &&
                data['typespec'].hasOwnProperty('min'))) {
            /*
             * data['typespec']['min'] is old and busted
             * data['min'] is the new hotness
             */
            let min = data.hasOwnProperty('min') ? data['min'] : data['typespec']['min'];
            let max = data.hasOwnProperty('max') ? data['max'] : data['typespec']['max'];

            let placeholder = dtype + ': ';
            if (data.hasOwnProperty('ranges')) {
                let first = true;
                for (let range of data.ranges) {
                    if (first) {
                        first = false;
                    } else {
                        placeholder += ', ';
                    }
                    let rmin = range[0];
                    let rmax = range[1];
                    if (rmax && rmax != rmin) {
                        placeholder += rmin + '-' + rmax;
                    } else {
                        placeholder += rmin;
                    }
                }
            } else {
                // Simple min-max range
                placeholder += min + '-' + max;
            }

            let step = 1;
            if (data.hasOwnProperty('fraction_digits')) {
                step = 10 ** (-data.fraction_digits);
            }

            target = $('<input type="number"' + attrStr +
                'min="' + min + '" max="' + max + '" step="' + step + '"' +
                ' placeholder="' + placeholder + '">');
        } else if (data.hasOwnProperty('options')) {
            target = $('<select' + attrStr + '>');
            if (allowEmpty) {
                // Include a valid "empty" option for use in config filters, etc.
                target.append('<option value="" selected></option>');
            } else {
                // Need an empty option (so we don't default to some arbitrary
                // value) but it's not valid to select it.
                target.append('<option disabled value="" selected></option>');
            }
            for (let optname of data.options) {
                target.append('<option>' + optname + '</option>')
            }
            target.click(function (e) { e.stopImmediatePropagation(); });
        } else if (data.hasOwnProperty('typespec')) {
            /* backwards compatibility */
            if (data.typespec.hasOwnProperty('iref')) {
                target = $('<select' + attrStr + '>');
                $.each(data['typespec'].iref, function (i, val) {
                    target.append('<option>' + val.name + '</option>')
                });
            } else if (data.typespec.hasOwnProperty('values')) {
                target = $('<select' + attrStr + '>');
                $.each(data['typespec'].values, function (i, val) {
                    target.append('<option>' + val[0] + '</option>')
                });

            } else {
                console.log("Unexpected/unsupported typespec data for dtype " + dtype);

            }
        }
        /* TODO - handle 'union' dtype */

        /* Fallback */
        if (!target) {
            target = $('<input type=text' + attrStr + 'placeholder="' + dtype + '">');
        }

        /* Hook up change action if appropriate */
        if (data.hasOwnProperty('key')) {
            switch (target[0].tagName) {
                case "INPUT":
                case "SELECT":
                    target.change(function () {
                        updateListKeyXPaths(node, target.val(), tree);
                    });
                    break;
                case "BUTTON":
                    /* Bits case is handled above in the bits dialog submit function */
                    break;
                case "TEXTAREA": /* anydata/anyxml - not a leaf, shouldn't be a key */
                default:
                    console.log("buildInputType: Unknown/unexpected target element " +
                        target[0].tagName);
                    break;
            }
        }

        return target;
    }

    /**
     * Callback function after editing the value of a list-key leaf node.
     * Update the XPath of the parent list node and all of its descendants to
     * include the correct XPath predicate for this key/value.
     *
     * @param {Object} keyNode: List-key leaf node whose value was just edited
     * @param {string} newValue: New value of this node.
     *
     * Some explanation is in order.
     *
     * As initially retrieved in the jstree, each node's xpath starts as a generic
     * xpath without any key predicates:
     *   /container/listA/container/listB/leaf
     *
     * For each list key in the path, a valid RPC can only be constructed when the
     * XPath has been updated with predicates for the keys/values, specifying the
     * actual list entries in question:
     *   /container/listA[keyA="valueA"]/container/listB[keyB1="1"][keyB2="2"]/leaf
     *
     * This function handles the proper insertion of these list-key predicates.
     *
     * If we're adding the first key for a given list this is an easy predicate to
     * insert:
     *   --> /container/listA/container/listB[key1="value"]/leaf
     *
     * If we're changing a previously defined key, we need to replace the predicate:
     *   --> /container/listA/container/listB[key1="new-value"]/leaf
     *
     * If a key is being cleared (set to empty), we need to delete the predicate:
     *   --> /container/listA/container/listB/leaf
     *
     * If other keys were also defined, we need to not mangle them:
     * --> /container/listA[A="1"]/container/listB[key1="value"][key2="x"]/leaf
     *
     * Because the server-side API doesn't have any knowledge of the key ordering
     * required by the list, we are responsible for ensuring that the key predicates
     * are ordered consistent with the key order:
     *   /listB[key1="x"][key2="y"]/    !=    /listB[key2="y"][key1="x"]/
     *
     * Furthermore, we must handle special characters in key values (/, ", ', etc.)
     * when inserting, replacing, and deleting key values into the xpath:
     *   /container/listA/container/listB[key1="ethernet0/0/0/0"]/leaf
     *   /container/listA/container/listB[key1='"hello, world!"']/leaf
     *   /listB[key1=concat('he said "', "I said 'hello!'", '" again')]
     *
     * References:
     * https://www.w3.org/TR/1999/REC-xpath-19991116/#location-paths
     * https://www.w3.org/TR/1999/REC-xpath-19991116/#path-abbrev
     * https://tools.ietf.org/html/rfc6020#section-6.4
     * https://tools.ietf.org/html/rfc6020#section-9.13
     */
    function updateListKeyXPaths(keyNode, newValue, inputTree) {
        let tree = inputTree.jstree(true);
        if (!tree) {
            return;
        }
        /* The keyNode is a direct child of the list node itself. */
        let listId = tree.get_parent(keyNode.id);
        let listNode = tree.get_node(listId);
        let listParentId = tree.get_parent(listId);
        let listParentNode = tree.get_node(listParentId);
        let key = keyNode.text;

        /* Update both "xpath" and "xpath_pfx" data */
        for (let dataKey of config.listKeyXpaths) {
            let parentXPath = listParentNode.data[dataKey];
            /*
             * Every part of the list XPath that is common with its parent node
             * needs to remain unchanged. Change only happens in the list-specific
             * part of the XPath.
             */
            let xpathBase = listNode.data[dataKey];
            /* Sanity check */
            if (!xpathBase.startsWith(parentXPath)) {
                console.log("ERROR: list XPath " + xpathBase +
                    "does not match parent XPath " + parentXPath);
                return;
            }

            let xpathNewBase = xpathBase;

            for (let k of listNode.data['keys']) {
                if (k == key || listNode.data.prefix + ':' + k == key) {
                    let start = xpathBase.slice(0, xpathBase.lastIndexOf("["+key+"="));
                    if (xpathBase.lastIndexOf("["+key+"=") > -1 &&
                        start.endsWith(listNode.data.name)) {
                        // replacement of original key
                        let end = xpathBase.slice(xpathBase.lastIndexOf("["+key+"="));
                        let rplStr = end.slice(0, end.indexOf("]")+1);
                        xpathNewBase = xpathBase.replace(rplStr, "["+key+'="'+newValue+'"]');
                    } else {
                        xpathNewBase += '[' + key + '=' + quotedXPathValue(newValue) + ']';
                    }
                }
            }
            /*
             * Replace the old XPath segment with the new
             * from the list node down through all of its children recursively.
             */
            function updateXPath(node) {
                if (keyNode.id == node.id) {
                    node.data[dataKey] = xpathNewBase;
                    // leaf node that is a key so don't add value
                    node.data.novalue = true;
                } else {
                    node.data[dataKey] = node.data[dataKey].replace(
                        xpathBase,
                        xpathNewBase
                    );
                }
                for (childId of node.children) {
                    updateXPath(tree.get_node(childId));
                }
            };
            updateXPath(listNode);
        }
        $(yangtree.config.tree).jstree('redraw');
    }

    /**
     * Helper function for updateListKeyXPaths().
     *
     * Properly quote the given value for use in the xpath as a node value.
     */
    function quotedXPathValue(value) {
        if (!value.includes('"')) {
            return '"' + value + '"';
        } else if (!value.includes("'")) {
            return "'" + value + "'";
        } else {
            /* Mix of single and double quotes - use concat() to construct it */
            return 'concat("' + value.split('"').join('", \'"\', "') + '")';
        }
    }

    function clearGrid() {
        $.each($(".ys-cfg-label"), function (i, obj) {
            obj.remove();
        });
        $.each($(".ys-cfg-rpc"), function (i, obj) {
            obj.remove();
        });
        $.each($(".ytool-edit-op"), function (i, obj) {
            obj.remove();
        });
        /* Reset node XPaths as well, stripping all list key predicates */
        let tree = $(yangtree.config.tree).jstree(true);
        $.each(tree.get_node('#').children, function (i, id) {
            let node = tree.get_node(id);
            args = { 'tree': tree };
            clearPredicates(node, args);
        });
    }

    /**
     * Remove list key predicates from the given node and its children.
     * Helper function to clearGrid() and nodeContextMenu().
     *
     * @param {object} node - Tree node data object
     * @param {object} args - Additional arguments
     *
     * Most often args will contain only a xpath and xpath_pfx value
     * from the parent. Those values are passed into clearPredicates
     * to avoid wiping out the predicates for the parent.
     * If "node" is a self-contained subtree (contains all of its children),
     * then "tree" arg may be omitted; if "node" only references its child IDs,
     * then "tree" arg is required, used to look up the actual child objects.
     */
    function clearPredicates(node, args) {
        let predicate = new RegExp(
            `\\[[^=]+=("[^"]*"|'[^']*'|` +
            `concat\\((?:"[^"]*"|'[^']*')(?: *, *(?:"[^"]*"|'[^']*'))*\\))\\]`,
            'g');

        for (let key of config.listKeyXpaths) {
            if (node.data.hasOwnProperty(key)) {
                // Handle case when tree is being cleared and
                // xpath and xpath_pfx are not available. Base would be undefined otherwise.
                let base = args[key] || node.data[key];
                node.data[key] = base + node.data[key].slice(base.length).replace(predicate, '');
            }
        }
        for (let child of node.children) {
            if (typeof (child) == "string") {
                clearPredicates(args['tree'].get_node(child), args);
            } else {
                clearPredicates(child, args);
            }
        }
    };

    /**
     * Used when changing RPC modes. Keep UI elements that are still applicable,
     * and clear those that are not.
     */
    function refreshGrid(allowReadOnly, allowEmpty) {
        // Remove all edit-op configs in "Operation" column.
        $.each($(".ytool-edit-op"), function (i, obj) {obj.remove()});

        let tree = $(yangtree.config.tree).jstree(true);
        $.each($(".ys-cfg-rpc"), function (i, obj) {
            let nodeid = obj.getAttribute("nodeid");
            let node = tree.get_node(nodeid);

            if (node.data.access == 'read-only' && !allowReadOnly) {
                obj.remove();
                return;
            }

            if (!allowEmpty && node.data.nodetype == 'container' && !node.data.presence) {
                obj.remove();
                return;
            }

            if (node.data.hasOwnProperty('options')) {
                let emptyOption = $(obj).find('option[value=""]');
                if (allowEmpty) {
                    emptyOption.prop("disabled", false);
                } else {
                    emptyOption.prop("disabled", true);
                }
            }

        });
    };

    function propertiesDialog(obj) {
        let node = $(yangtree.config.tree).jstree(true).get_node(obj.reference);
        let txt = yangtree.formatNodeData(node);
        $("#ytool-dialog")
            .html('<div class="ysyangtree-info" style="height:auto; border:none">' +
                txt + '</div>')
            .dialog({
                minHeight: 500,
                maxHeight: 700,
                height: "auto",
                minWidth: 500,
                width: 600
            })
            .dialog("open");
    }

    function makeJSTreeGrid(names, yangset, operation = true) {
        let column_choice = [
            {
                width: "auto",
                minWidth: 300,
                header: "Nodes"
            },
            {
                width: "25%",
                minWidth: 130,
                header: "Value",
                headerClass: "jtreeHeader",
                wideCellClass: "jtreeCell",
                value: "value",
            },
            {
                width: "10%",
                minWidth: 110,
                header: "Operation",
                headerClass: "jtreeHeader",
                wideCellClass: "jtreeCell",
            }
        ]
        if (!operation) {
            column_choice = column_choice.slice(0, -1);
        }
        let extraOptions = {
            plugins: ["themes", "contextmenu", "search", "grid"],
            grid: {
                columns: column_choice,
                height: 'calc(100% - 6px)',
                width: '100%',
                resizable: true,
                contextmenu: true,
                gridcontextmenu: function (grid, tree, node, val, col, t, target) {
                    return {
                        "clear": {
                            label: "Clear",
                            icon: "icon-delete",
                            "action": function (data) {
                                // Checking class of UI component
                                if (data.reference.firstElementChild.className == "ys-cfg-rpc"){
                                    let node = $(yangtree.config.tree)
                                        .jstree(true)
                                        .get_node(data.reference
                                            .getAttribute('data-jstreegrid'));
                                    if (node.data.hasOwnProperty('key')) {
                                        /* Clear data from xpaths */
                                        updateListKeyXPaths(node, '', $(yangtree.config.tree));
                                    }
                                    $(data.reference).empty();
                                }
                                else{
                                    $(data.reference).empty();
                                }
                            }
                        },
                        "cancel": {
                            label: "Cancel",
                            icon: "icon-exit",
                            "action": function (data) {
                                return;
                            }
                        }
                    }
                },
            },
            contextmenu: {
                select_node: false,
                items: config.nodeContextMenu,
            },
        };
        return yangtree.makeJSTree(names, yangset,
            yangtree.DEFAULT_NODETYPES,
            extraOptions);
    }

    /**
     * Main processor of jsTree events
     */
    function changeTree(tree) {

        function addInput(gridNode, treeNode, tree, allowEmpty = false) {
            let cfg = gridNode.grid.find(".ys-cfg-rpc");
            if (cfg.length === 0) {
                let elem = buildInputType(treeNode, tree, allowEmpty);
                gridNode.grid.html(elem);
                if (elem) {
                    elem.focus();
                }
            } else {
                if (cfg[0].type == "checkbox") {
                    // This acts as a toggle for the checkbox
                    gridNode.grid.empty();
                }
            }
        }

        tree.on("select_cell.jstree-grid", function (e, data) {
            let jstree = tree.jstree(true);
            let node = jstree.get_node(data.node.attr("id"));

            if (node.data.hasOwnProperty('modtype')) {
                /* Module or submodule - not an input */
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                return;
            }

            let proto_op = undefined;
            if (config.getProtocolOperation) {
                proto_op = config.getProtocolOperation();
            }

            if (jstree.is_disabled(node)) {
                ;  // never add options for a disabled node
            } else if (data.column == "Operation") {
                if (proto_op == "edit-config" &&
                    data.grid.find(".ytool-edit-op").length === 0) {
                    if (node.data.access != "read-only") {
                        if (config.buildEditProtocolOperationMenu) {
                            data.grid.append(c.buildEditProtocolOperationMenu(node));
                        }
                    }
                }
            } else if (data.column == "Value") {
                if (node.data.access != "read-only" ||
                    proto_op == 'get' ||
                    proto_op == 'action') {
                    addInput(data, node, tree, (proto_op == 'get' ||
                        proto_op == 'get-config' ||
                        proto_op == 'action'));
                }
            }
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
        });
    }

    /*
     * Adds a new blank list entry to tree.
     */
    function addTreeListEntry(listNodeId, tree, redraw=true) {
        let node = tree.get_node(listNodeId);
        let subtreeJson = tree.get_json(node.id);

        let parentID = tree.get_parent(node);
        let parentNode = tree.get_node(parentID);
        let parentData = parentNode['data'];
        let parentXpath = parentData['xpath'];
        let parentXpathPfx = parentData['xpath_pfx'];
        let args = { 'xpath': parentXpath, 'xpath_pfx': parentXpathPfx };
        rpc_ui.clearPredicates(subtreeJson, args);
        function cleanIds(currentNode) {
            delete currentNode.id;
            delete currentNode.li_attr.id;
            delete currentNode.a_attr.id;
            for (child of currentNode.children) {
                cleanIds(child);
            }
        }
        cleanIds(subtreeJson);
        let parent_id = tree.get_parent(node.id);
        let added_node_id = tree.create_node(parent_id, subtreeJson,
            tree.get_node(parent_id).children.indexOf(node.id) + 1);
        c.addListNodesRpc.push(added_node_id)
        if (redraw) {
            tree.redraw();
        }
        return added_node_id;
    }

    /*
     * Removes an added list entry from the tree.
     * Always leaves at least one entry.
     */
    function removeTreeListEntry(listNodeID, tree, redraw=true) {
        let node = tree.get_node(listNodeID);
        tree.delete_node(node);
        if (c.addListNodesRpc.indexOf(listNodeID) > -1) {
            let index = c.addListNodesRpc.indexOf(listNodeID);
            c.addListNodesRpc.splice(index, 1);
        }
        if (redraw) {
            tree.redraw();
        }
    }

    /*
     * Removes all added list entries from the tree.
     * Always leaves at least one entry.
     */
    function removeAllTreeListEntry(tree, redraw=true) {
        let node = {};
        if (rpc_ui.config.addListNodesRpc.length > 0) {
            for (let entryId of rpc_ui.config.addListNodesRpc) {
                node = tree.get_node(entryId);
                tree.delete_node(node);
            }
            rpc_ui.config.addListNodesRpc = [];
        }
        if (redraw) {
            tree.redraw();
        }
    }

    /**
     * Default callback function for jstree.contextmenu plugin.
     * Builds the context menu for a given tree node.
     */
    function nodeContextMenu(node) {
        let items = {};

        if (!node) {
            return items;
        }

        let tree = $(yangtree.config.tree).jstree(true);

        if (node.data.nodetype == 'list' || node.data.nodetype == 'leaf-list') {
            items['addEntry'] = {
                label: `Add another ${node.data.nodetype} entry`,
                action: function (data) {
                    addTreeListEntry(node.id, tree);
                }
            };

            // If there are at least two entries, allow delete of one
            let allowDelete = false;
            for (child_id of tree.get_node(tree.get_parent(node)).children) {
                if (child_id == node.id) {
                    continue;
                }
                child = tree.get_node(child_id);
                if (child.text == node.text) {
                    allowDelete = true;
                    break;
                }
            }
            if (allowDelete) {
                items['deleteEntry'] = {
                    label: `Delete this ${node.data.nodetype} entry`,
                    action: function (data) {
                        removeTreeListEntry(node.id, tree);
                    }
                };
            }
        }

        items['properties'] = {
            label: "Properties",
            action: propertiesDialog
        };

        return items;
    };

    config.nodeContextMenu = nodeContextMenu;

    /**
     * Public APIs
     */
    return {
        config: config,
        makeJSTreeGrid: makeJSTreeGrid,
        changeTree: changeTree,
        clearGrid: clearGrid,
        clearPredicates: clearPredicates,
        refreshGrid: refreshGrid,
        propertiesDialog: propertiesDialog,
        updateListKeyXPaths: updateListKeyXPaths,
        addTreeListEntry: addTreeListEntry,
        removeTreeListEntry: removeTreeListEntry,
        removeAllTreeListEntry: removeAllTreeListEntry,
    };
}();
