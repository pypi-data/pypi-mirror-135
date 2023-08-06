/**
 * Module for setting up user context for a particular yangset and retrieving
 * and displaying a JSTree corresponding to a particular module in the yangset.
 */
let yangtree = function () {
    /**
     * Default configuration of this module.
     */
    let config = {
        nodeInfo: "#ytool-prop-info",
        tree: "#tree",
        progress: 'div#ys-progress',
        yangsetSel: '#ytool-yangset',
        modulesSel: '#ytool-models',
        legendSel: '#ysyangtree-legend',
        initialModuleSelection: null,
        nodeTypeSel: null,
        exploreStateURI: '/yangtree/explore/',
        exploreStateTitle: 'Exploring YANG',
        treeURI: '/yangtree/gettree/',

        /* Items for node search */
        nodeSearchToggle: ".ys-search-toggle",
        nodeSearchMaxMatches: 100,
        nodeSearchOffset: 0,
        nodeSearchOffsetSelect: "#ys-search-offset-select",
        nodeSearchTotalText: "#ys-search-total-matches",

        /* Items for xpath search */
        xpathSearchStringEntry: "#ys-xpath-search-string",
        xpathSearchResultsSelect: "#ys-xpath-search-results",
        xpathSearchResultsText: "#ys-xpath-search-results-text",
    };

    let c = config;    // internal alias for brevity

    let state = {
        setNodeIconsOnOpen: true,  // Set to false to disable icon updates
        nodeSearchMatchesFound: 0,
    };

    let exploreCtxMenu = {
        select_node: false,
        items: function (node) {
            return {
                'showModule': {
                    label: ('View text of module "' +
                        (node.data.submodule || node.data.module)
                        + '"'),
                    action: function () {
                        window.open("/filemanager/yangsets/show/" +
                            yangset + "/module/" +
                            (node.data.submodule || node.data.module));
                    }
                }
            }
        }
    }

    let replayCtxMenu = {
        select_node: true,
        items: function (node) {
            return {
                'showModule': {
                    label: ('View text of module "' +
                        (node.data.submodule || node.data.module)
                        + '"'),
                    action: function () {
                        window.open("/filemanager/yangsets/show/" +
                            yangset + "/module/" +
                            (node.data.submodule || node.data.module));
                    }
                },
                'generateReplays': {
                    label: 'Generate replays based on this node/subtree...',
                    action: function () {
                        // We need the name of the root module,
                        // which may or may not be the module that
                        // owns the selected node. If the selected
                        // node is not a module root, need to find
                        // the module root to get its name.
                        let module = node.data.module;
                        if (node.parents.length >= 2) {
                            module = $(c.tree)
                                .jstree(true)
                                .get_node(node.parents[node.parents.length - 2])
                                .data.module;
                        }
                        tasks.generateReplaysUI($(c.yangsetSel).val(), module, node.data.xpath);
                    }
                }
            }
        }
    }

    const DEFAULT_NODETYPES = [
        'action',
        'anydata',
        'anyxml',
        'case',
        'choice',
        'container',
        'input',
        'leaf',
        'leaf-list',
        'list',
        'module',
        'notification',
        'output',
        'rpc',
        'submodule',
    ];

    const ALL_NODETYPES = [
        'action',
        'anydata',
        'anyxml',
        'case',
        'choice',
        'container',
        'grouping',
        'identity',
        'input',
        'leaf',
        'leaf-list',
        'list',
        'module',
        'notification',
        'output',
        'rpc',
        'submodule',
        'typedef',
    ]

    /**
     * Retrieve the jstree JSON data from the server.
     *
     * @param {list} names Module name(s) to retrieve
     * @param {str} yangset YANG module set to retrieve modules from
     * @param {list} nodetypes Node types to include in the data
     */
    function getJSTreeData(names, yangset, nodetypes = undefined) {
        let progressBarDiv = startProgress($(c.progress), c.treeURI, params = { yangset: yangset }) || $(c.progress);
        if (!nodetypes) {
            nodetypes = DEFAULT_NODETYPES;
        }
        return getPromise(c.treeURI, {
            names: names,
            yangset: yangset,
            path: JSON.stringify(["yang"]),
            included_nodetypes: nodetypes,
        }).then(function (retObj) {
            stopProgress(progressBarDiv);
            return retObj;
        }, function (retObj) {
            stopProgress(progressBarDiv);
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    }

    /**
     * Retrieve and render the data tree describing the given module.
     *
     * @param {list} names Module name(s) to render
     * @param {str} yangset YANG module set to retrieve modules from
     * @param {object} extraOptions Extra/overridden args to pass to jstree().
     * @param {object} callback Function to call after tree is initialized
     */
    function makeJSTree(names, yangset,
        nodetypes = undefined, extraOptions = null, callback = null) {
        $.jstree.destroy($(c.tree));
        $.vakata.context.settings.hide_onmouseleave = true;
        return getJSTreeData(names, yangset, nodetypes).then(function (retObj) {
            if (!retObj.data) {
                popDialog("Success but no data??");
                return;
            }

            let allEmptyTrees = true;
            let emptyTree = false;
            for (let root of retObj.data) {
                prepNodeIcons(root);
                if (!root.children) {
                    emptyTree = true;
                } else {
                    allEmptyTrees = false;
                }
            }
            let msg = "";
            if (allEmptyTrees) {
                msg += ("<p>The loaded module(s) have no tree(s) to " +
                    "display.</p>" +
                    "<p>Most likely this is because they are meant " +
                    "to support (augment, extend, etc.) other " +
                    "modules and are not intended to be directly " +
                    "consumed by a user.</p>");
            } else if (emptyTree && c.nodeTypeSel) {
                // Only inform about a mix of tree and non-tree modules
                // if the user has the option to opt in to show more nodes.
                msg += ("<p>One or more loaded module(s) have no tree(s) " +
                    "to display.</p>" +
                    "<p>Most likely this is because they are meant " +
                    "to support (augment, extend, etc.) other " +
                    "modules and are not intended to be directly " +
                    "consumed by a user.</p>");
            }

            if (msg) {
                popDialog(msg);
            }

            let options = {
                plugins: ["themes", "search", "contextmenu"],
                core: {
                    animation: 0,
                    multiple: true,
                    check_callback: true,
                    themes: {
                        theme: "classic",
                        dots: true,
                        icons: true
                    },
                    expand_selected_onload: true,
                    data: retObj.data
                },
                search: {
                    search_callback: function (searchStr, node) {
                        /*
                         * Get up to (config.nodeSearchMaxMatches) matches,
                         * starting with the (config.nodeSearchOffset + 1)st match.
                         */
                        if (node.text.indexOf(searchStr) != -1) {
                            state.nodeSearchMatchesFound += 1;
                            return (state.nodeSearchMatchesFound > config.nodeSearchOffset &&
                                state.nodeSearchMatchesFound - config.nodeSearchOffset <= config.nodeSearchMaxMatches);
                        }
                        return false;
                    },
                },
                contextmenu: {
                    select_node: false,
                    items: function (node) {
                        return {
                            'showModule': {
                                label: ('View text of module "' +
                                    (node.data.submodule || node.data.module)
                                    + '"'),
                                action: function () {
                                    window.open("/filemanager/yangsets/show/" +
                                        yangset + "/module/" +
                                        (node.data.submodule || node.data.module));
                                }
                            }
                        }
                    }
                }
            };
            if (extraOptions) {
                options = Object.assign(options, extraOptions);
            }

            buildLegend($(c.legendSel), retObj.included_nodetypes);
            $(c.tree).jstree(options);

            $(c.tree).bind("after_open.jstree", function (e, data) {
                let tree = data.instance;
                let node = data.node;
                if (node.children.length == 1) {
                    // Only one child - open it too to save the user a click
                    tree.open_node(tree.get_node(node.children[0]));
                }
                if (state.setNodeIconsOnOpen) {
                    // Craft badged icons for the newly displayed nodes
                    $.each(tree.get_children_dom(node), function (i, node_elem) {
                        $.each($(node_elem).find("a .fa-layers:not(:has(>svg))"), function (i, iElem) {
                            setNodeIcon(tree.get_node(iElem), iElem);
                        });
                    });
                }
            });

            $(c.tree).bind("close_node.jstree", function (e, data) {
                let node = data.node;
                if (node.hasOwnProperty('children_d')) {
                    for (let nodeid of node.children_d) {
                        let node = $(c.tree).jstree(true).get_node(nodeid)
                        if (node.data.nodetype == 'leaf' && node.data.hasOwnProperty('key')) {
                            rpc_ui.updateListKeyXPaths(node, '', $(c.tree));
                        }
                    }
                }
            });
            
            /*
             * When tree is first drawn, or
             * redrawn after nodes are hidden/shown, icons need to
             * be re-constructed for the affected nodes.
             */
            $(c.tree).bind("redraw.jstree", function (e, data) {
                let tree = data.instance;
                // Get all icon-less tree nodes
                let nodeElems = ($(c.tree).find("a .fa-layers:not(:has(>svg))"));
                $.each(nodeElems, function (i, nodeElem) {
                    setNodeIcon(tree.get_node(nodeElem), nodeElem);
                });
                /*
                 * If a node search is in effect, scroll to center the first match.
                 */
                let first = $(c.tree + " .jstree-search:first");
                if (first.length > 0) {
                    let col = $(c.tree).scrollParent();
                    col.scrollTop(first.offset().top - $(c.tree).offset().top - (col.height() / 2));
                }
            });

            /*
             * After search is completed, show UI elements that only now apply,
             * populate the UI with the number of potential matches, and
             * populate the UI with the ability to select match ranges.
             */
            $(c.tree).bind("search.jstree", function (e, data) {
                $(c.nodeSearchToggle).show();
                $(c.nodeSearchTotalText).text(state.nodeSearchMatchesFound);
                $(c.nodeSearchOffsetSelect).empty();
                for (let i = 0; i < state.nodeSearchMatchesFound; i += c.nodeSearchMaxMatches) {
                    let start = i + 1;
                    let end = (i + c.nodeSearchMaxMatches < state.nodeSearchMatchesFound ?
                        i + c.nodeSearchMaxMatches : state.nodeSearchMatchesFound);
                    $(c.nodeSearchOffsetSelect).append('<option value="' + i + '">' +
                        start + '-' + end +
                        '</option>');
                }
                $(c.nodeSearchOffsetSelect).val(c.nodeSearchOffset);
            });

            /*
             * After search is cleared, hide UI elements that no longer apply
             */
            $(c.tree).bind("clear_search.jstree", function (e, data) {
                $(c.nodeSearchToggle).hide();
            });

            if (callback) {
                callback(retObj);
            }

            return retObj;
        });
    };

    /**
     * Recurse through the given jstree data and strip out the provided
     * icons - lay the groundwork to later use Font Awesome icon layering.
     *
     * This function is to called on the json data, prior to constructing the
     * jstree; see also setNodeIcon().
     */
    function prepNodeIcons(node) {
        // Potentially multipart icon; to be done in setNodeIcon()
        node.icon = 'fa-fw fa-layers';
        if (node.children) {
            for (let child of node.children) {
                prepNodeIcons(child);
            }
        }
    }

    /**
     * Add Font Awesome icon(s) to the given element based on the given node.
     *
     * NOTE: any changes to this function need to be reflected in buildLegend()!
     *
     * This function is to be called from an after_open() jstree callback;
     * see also prepNodeIcons().
     */
    function setNodeIcon(node, elem) {
        const PFX = '<span class="';
        const SFX = '"></span>';

        /* Construct base icon for datatype */
        switch (node.data.nodetype || node.data.modtype) {
            case 'action':
                $(elem).append(PFX + 'fas fa-lg fa-bullseye ystree-root"' + SFX);
                break;
            case 'anydata':
                $(elem).append(PFX + 'fas fa-lg fa-asterisk ystree-leaf"' + SFX);
                break;
            case 'anyxml':
                $(elem).append(PFX + 'fas fa-lg fa-code ystree-leaf"' + SFX);
                break;
            case 'case':
                $(elem).append(PFX + 'fas fa-lg fa-arrow-right ystree-node' + SFX);
                break;
            case 'choice':
                // Three arrows from a common point
                $(elem).append(PFX + 'fas fa-long-arrow-alt-right ystree-node"' +
                    ' data-fa-transform="rotate-40 left-1 down-5' + SFX);
                $(elem).append(PFX + 'fas fa-long-arrow-alt-right ystree-node' + SFX);
                $(elem).append(PFX + 'fas fa-long-arrow-alt-right ystree-node"' +
                    ' data-fa-transform="rotate--40 left-1 up-5' + SFX);
                break;
            case 'container':
                $(elem).append(PFX + 'far fa-lg fa-folder-open ystree-node' + SFX);
                break;
            case 'grouping':
                $(elem).append(PFX + 'fas fa-lg fa-cube ystree-definition' + SFX);
                break;
            case 'identity':
                $(elem).append(PFX + 'fas fa-lg fa-info ystree-definition' + SFX);
                break;
            case 'input':
                $(elem).append(PFX + 'fas fa-lg fa-sign-in-alt ystree-node' + SFX);
                break;
            case 'leaf':
                $(elem).append(PFX + 'fas fa-lg fa-leaf ystree-leaf' + SFX);
                break;
            case 'leaf-list':
                // Vertical stack of three small leafs
                $(elem).append(PFX + 'fas fa-leaf ystree-leaf' +
                    '" data-fa-transform="shrink-5 up-8' + SFX);
                $(elem).append(PFX + 'fas fa-leaf ystree-leaf' +
                    '" data-fa-transform="shrink-5' + SFX);
                $(elem).append(PFX + 'fas fa-leaf ystree-leaf' +
                    '" data-fa-transform="shrink-5 down-8' + SFX);
                break;
            case 'list':
                $(elem).append(PFX + 'fas fa-lg fa-list ystree-node' + SFX);
                break;
            case 'module':
                $(elem).append(PFX + 'fas fa-lg fa-cubes ystree-root' + SFX);
                break;
            case 'notification':
                $(elem).append(PFX + 'fas fa-lg fa-gift ystree-root' + SFX);
                break;
            case 'output':
                $(elem).append(PFX + 'fas fa-lg fa-sign-out-alt ystree-node' + SFX);
                break;
            case 'rpc':
                $(elem).append(PFX + 'far fa-lg fa-envelope ystree-root' + SFX);
                break;
            case 'submodule':
                $(elem).append(PFX + 'fas fa-cube ystree-root' +
                    '" data-fa-transform="shrink-5' + SFX);
                break;
            case 'typedef':
                $(elem).append(PFX + 'far fa-lg fa-star ystree-definition' + SFX);
                break;
            case undefined:
                $(elem).append(PFX + "fas fa-square ystree-placeholder" + SFX);
                break;
            default:
                $(elem).append(PFX + 'fas fa-lg fa-exclamation-circle ystree-node' + SFX);
                break;
        }

        /* Add modifiers based on node status */
        if (node.data.deviation == 'not-supported') {
            $(elem).find("span").addClass("ystree-not-supported");
        }
        if (node.data.status == 'deprecated') {
            $(elem).find("span").addClass("ystree-status-deprecated");
        } else if (node.data.status == 'obsolete') {
            $(elem).find("span").addClass("ystree-status-obsolete");
        }

        /* Add badges for various node data */

        if (node.data.key) {
            // Leaf node acting as list key - brown "key" at lower right
            $(elem).append('<span class="fas fa-key"' +
                ' data-fa-transform="shrink-4 down-6 right-6"' +
                ' style="color:brown"></span>');
        }

        if (node.data.presence) {
            // Presence container - "Cisco Sage Green" "leaf" at lower right
            $(elem).append('<span class="fas fa-leaf"' +
                ' data-fa-transform="shrink-5 down-6 right-6"' +
                ' style="color:#abc223"></span>');
        }

        if (node.data.mandatory) {
            // Mandatory node - green circled "!" at lower left
            $(elem).append('<span class="fas fa-circle"' +
                ' data-fa-transform="shrink-4 down-6 left-6"' +
                ' style="color:white"></span>');
            $(elem).append('<span class="fas fa-exclamation-circle"' +
                ' data-fa-transform="shrink-4 down-6 left-6"' +
                'style="color:darkgreen"></span>');
        }

        if (node.data.must) {
            // Node has a 'must' constraint - red "link" at upper left
            $(elem).append('<span class="fas fa-link"' +
                ' data-fa-transform="shrink-4 up-6 left-6"' +
                ' style="color:#e2231a"></span>');
        }

        if (node.data.when) {
            // Node has a 'when' constraint - blue "link" at upper left
            $(elem).append('<span class="fas fa-link"' +
                ' data-fa-transform="shrink-4 up-6 left-4"' +
                ' style="color:blue"></span>');
        }

        if (node.data.datatype == "leafref" ||
            node.data.basetype == "leafref") {
            // Leafref to another leaf - blue "out arrow" at upper right
            $(elem).append('<span class="fas fa-square"' +
                ' data-fa-transform="shrink-4 up-6 right-6"' +
                ' style="color:white"></span>');
            $(elem).append('<span class="fas fa-external-link-square-alt"' +
                ' data-fa-transform="shrink-4 up-6 right-6"' +
                ' style="color:blue"></span>');
        }
    };

    /**
     * Render a legend of yangtree icons as constructed by setNodeIcon().
     *
     * @param {jquery} parent - jQuery of a <div> or <table> to populate
     * @param {Array} included_nodetypes - Node types to include in the legend.
     */
    function buildLegend(parent, included_nodetypes = undefined) {
        let entryName = "";
        let iconName = "";
        let textName = "";
        if (parent[0].nodeName == "DIV") {
            entryName = "<li>";
            iconName = "<span>";
            textName = "<span>";
        } else if (parent[0].nodeName == "TABLE") {
            entryName = "<tr>";
            iconName = "<td>";
            textName = "<td>";
        } else {
            console.log("Unsure how to generate legend for " + parent);
            return;
        }

        parent.empty();

        let entry;
        let icon;
        let text;

        let iconGrouping;
        if (parent[0].nodeName == "DIV") {
            iconGrouping = $('<ul class="list list--inline list--regular">')
                .appendTo(parent);
            iconGrouping.append($('<li class="text-muted">').text("Node Icons"));
        } else if (parent[0].nodeName == "TABLE") {
            parent.append($("<tr>").append($("<th colspan=2>").text("Node Icons")));
            iconGrouping = parent;
        }

        if (!included_nodetypes) {
            included_nodetypes = DEFAULT_NODETYPES;
        }

        /* Add icons for nodetypes */
        for (let nodetype of included_nodetypes) {
            entry = $(entryName);
            iconGrouping.append(entry);
            icon = $('<span class="fa-fw fa-layers">');
            setNodeIcon({ data: { nodetype: nodetype } }, icon);
            text = $(textName);
            text.text(" " + nodetype);
            entry.append($(iconName).append(icon)).append(text);
        }

        /* Add node status */
        if (parent[0].nodeName == "DIV") {
            iconGrouping = $('<ul class="list list--inline list--regular">')
                .appendTo(parent);
            iconGrouping.append($('<li class="text-muted">').text("Node Support"));
        } else if (parent[0].nodeName == "TABLE") {
            parent.append($("<tr>").append($("<th colspan=2>").text("Node Support")));
            iconGrouping = parent;
        }

        $.each({
            "status:&nbsp;deprecated": { data: { status: 'deprecated' } },
            "status:&nbsp;obsolete": { data: { status: 'obsolete' } },
            "deviation:&nbsp;not-supported": {
                data: { deviation: 'not-supported' },
                a_attr: { 'class': "ystree-not-supported" }
            },
        }, function (label, node) {
            entry = $(entryName);
            iconGrouping.append(entry);
            icon = $('<span class="fa-fw fa-layers">');
            node['data']['nodetype'] = 'leaf';
            setNodeIcon(node, icon);
            text = $(textName);
            text.html("&nbsp;" + label);
            if (node['a_attr']) {
                text.addClass(node['a_attr']['class']);
            }
            entry.append($(iconName).append(icon)).append(text);
        });

        /* Add badge icons */
        if (parent[0].nodeName == "DIV") {
            iconGrouping = $('<ul class="list list--inline list--regular">')
                .appendTo(parent);
            iconGrouping.append($('<li class="text-muted">').text("Node Badges"));
        } else if (parent[0].nodeName == "TABLE") {
            parent.append($("<tr>").append($("<th colspan=2>").text("Node Badges")));
            iconGrouping = parent;
        }

        $.each({
            "list&nbsp;key": { data: { key: true } },
            "presence&nbsp;container": { data: { presence: true } },
            "mandatory&nbsp;node": { data: { mandatory: true } },
            "<q>must</q>&nbsp;constraint": { data: { must: "../" } },
            "<q>when</q>&nbsp;constraint": { data: { when: "../" } },
            "leafref": { data: { datatype: 'leafref' } },
        }, function (label, node) {
            entry = $(entryName);
            iconGrouping.append(entry);
            icon = $('<span class="fa-fw fa-layers">');
            setNodeIcon(node, icon);
            text = $(textName);
            text.html("&nbsp;" + label);
            entry.append($(iconName).append(icon)).append(text);
        });
    }

    /**
     * Retrieve the RFC content from Json object
     * append the retrieved content on to textarea.
     */
    function getRFCData(nodetype) {
        let p = getPromise('/yangtree/getrfc/', { 'nodetype': nodetype });
        $.when(p).then(function (response) {
            if (response.content != 'Failed') {
                if (response.content != 'module') {
                    let contents = response.content;
                    let reference = response.reference;
                    if (reference != "") {
                        $(c.nodeInfo).append("<h4>Reference URL: " +
                            '<a target="_blank" href="' + reference + '">' +
                            reference + "</a></h4>");
                    }
                    $(c.nodeInfo).append('<pre>' + contents + '</pre>');
                }
                else {
                    $(c.nodeInfo)
                        .append('<h4>The Yang Module:</h4>')
                        .append('<p>A YANG module defines a hierarchy of nodes that can be used for NETCONF-based operations.  With its definitions and the definitions it imports or includes from elsewhere, a module is self-contained and "compilable".</p>')
                        .append('<h4>Complete information on Yang Module can be found in the RFC 6020 webpage</h4>')
                        .append('<a target="_blank" href="https://tools.ietf.org/html/rfc6020">https://tools.ietf.org/html/rfc6020</a>');
                }
            }
            else {
                popDialog('cannot access RFC 6020 information from https://tools.ietf.org/html/rfc6020 , check your network connection');
            }
        });
    };

    /**
     * Render the dictionary of node data to a human-readable HTML string.
     */
    function formatNodeData(node, brief = false) {
        let content = $("<div>");
        let table = $('<table>');
        content.append(table);

        for (key in node.data) {
            // Skip keys that are either excessively verbose or
            // are for use by APIs rather than anything human-readable
            // Also skip keys will null values
            if (key.startsWith("_") ||
                key == "title" || key == 'typespec' ||
                key == 'options' || key == 'xpath_pfx' ||
                node.data[key] === null) {
                continue;
            }
            if (brief) {
                // Keep it even shorter
                if (key == "access" ||
                    key == "description") {
                    continue;
                }
                if (node.data.modtype) {
                    // Module
                    if (key == "modtype" ||
                        key == "namespace_prefixes" ||
                        key == "operations" ||
                        key == "revision_info") {
                        continue;
                    }
                } else {
                    // Node
                    if (key == "module" ||
                        key == "prefix" ||
                        key == "revision" ||
                        key == "bits" ||
                        key == "min" ||
                        key == "max" ||
                        key == "ranges" ||
                        key == "fraction_digits" ||
                        key == "members" ||
                        key == "schema_node_id") {
                        continue;
                    }
                }
            }
            let row = $("<tr>");
            row.append($('<th scope="row">').text(key.replace(/_/g, " ")));
            let data = node.data[key];
            let td = $("<td>");
            if (typeof (data) == 'string' ||
                typeof (data) == 'number' ||
                typeof (data) == 'boolean') {
                td.text(data);
            } else if (Array.isArray(data)) {
                if (key == "ranges") {
                    let txt = "";
                    let first = true;
                    for (let range of data) {
                        if (first) {
                            first = false;
                        } else {
                            txt += ', ';
                        }
                        let rmin = range[0];
                        let rmax = range[1];
                        if (rmax && rmax != rmin) {
                            txt += rmin + '-' + rmax;
                        } else {
                            txt += rmin;
                        }
                    }
                    td.text(txt);
                } else {
                    let sublist = $("<ul>");
                    $.each(data, function (i, entry) {
                        sublist.append($("<li>").text(JSON.stringify(entry)));
                    });
                    td.append(sublist);
                }
            } else {
                // Assume type is Object
                let subtable = $('<table class="table" style="width: 100%">');
                $.each(data, function (k, v) {
                    subtable.append($("<tr>").append($("<th>").text(k))
                        .append($("<td>").text(v)));
                });
                td.append(subtable);
            }
            row.append(td);
            table.append(row);
        }

        return content.html();
    }

    /**
     * Callback function for bootstrap tooltip() API
     */
    function formatNodeToolTip() {
        return formatNodeData(
            $(c.tree).jstree(true).get_node($(this).parent().attr('id')),
            brief = true);
    }

    /*
     * Function to get the nodetype of the selected node
     * Retrive and display the node properties and RFC info of each nodetype
     */
    function getNodeRFCData(e, data) {
        let txt = "";
        if (!data.node) {
            return;
        }
        let node = $(this).jstree(true).get_node(data.node.id);
        let nodetype = node.data['nodetype'];

        $(c.nodeInfo).html('<h3 align="center">Node Properties</h3>');
        $(c.nodeInfo).append(formatNodeData(node));

        $(c.nodeInfo).visible = true;

        getRFCData(nodetype);
    };

    /**
     * Retrieve a list of all YANG models associated to a YANG set.
     * If config.initialModuleSelection is set, will select the given module(s)
     * after the list is loaded, then clear this variable.
     *
     * @param {string} yangset - YANG set name (user+setname). If unset,
     *                           defaults to the value of config.yangsetSel
     * @param {Object} widget - Selector to populate with the models.
     *                          If unset, defaults to config.modulesSel
     */
    function getModels(yangset = undefined, widget = undefined) {
        if (!yangset) {
            yangset = $(c.yangsetSel).val();
        }
        if (!widget) {
            widget = $(c.modulesSel);
        }
        return yangsets.getYangSetContents(yangset).done(function (retObj) {
            if (widget.prop("tagName").toLowerCase() == 'input') {
                /* Old usage - set autocomplete for this text field */
                let models = [];
                $.each(retObj.modules, function (i, entry) {
                    models.push(entry.name);
                });
                widget.autocomplete({ source: models });
            } else {
                /* Newer usage - populate <select> with entries */
                $.each(retObj.modules, function (i, entry) {
                    yangsets.makeAppropriateChild(widget, entry.name, entry.name);
                });
            }

            if (c.initialModuleSelection) {
                widget.val(c.initialModuleSelection);
                c.initialModuleSelection = null;
            }
        });
    };

    /**
     * Update the window's 'explore' URI without reloading the page
     */
    function pushExploreState(yangset = '', modulenames = []) {
        $("ul.breadcrumb li:not('.breadcrumb-static')").remove();
        let url = c.exploreStateURI;
        let title = c.exploreStateTitle;
        if (yangset) {
            const yangsetName = $(c.yangsetSel).find('[value="' + yangset + '"]').text();
            $("ul.breadcrumb").append('<li><a href="' + url + '">' + title + '</li>')
            url += yangset + "/";
            if (modulenames) {
                $("ul.breadcrumb").append('<li><a href="' + url + '">' +
                    'YANG set <q>' + yangsetName + '</q></li>');
                url += modulenames.join(',');
                title += ' module(s) "' + modulenames.join('", "') + '"';
                $("ul.breadcrumb").append('<li>Modules</li>');
            } else {
                $("ul.breadcrumb").append('<li>YANG set <q>' + yangsetName + '</q></li>');
            }
        } else {
            $("ul.breadcrumb").append('<li>' + title + '</li>');
        }
        document.title = title;
        window.history.pushState('', title, url);
    }

    function searchTreeNodes(searchStr) {
        if ($(c.tree).jstree(true)) {
            let progressBarDiv = startProgress($(c.progress)) || $(c.progress);
            state.nodeSearchMatchesFound = 0;
            /* Updating the node icons as the search opens various nodes
             * is quite slow. It's faster to wait until the search is
             * done then call redraw() to update all the icons at once.
             */
            state.setNodeIconsOnOpen = false;
            $(c.tree).jstree(true).search(searchStr);
            state.setNodeIconsOnOpen = true;
            $(c.tree).jstree(true).redraw();
            stopProgress(progressBarDiv);
        }
        else {
            alert("Please load module(s)");
        }
    };

    /**
     * Custom search function, as jstree.search() is really slow to redraw the
     * screen when large numbers of matches are found.
     * Returns an array of [nodeId, xpath] entries.
     */
    function searchTreeXpaths(searchStr) {
        if ($(c.tree).jstree(true)) {
            let progressBarDiv = startProgress($(c.progress)) || $(c.progress);
            let matches = [];

            let data = $(c.tree).jstree(true).get_json($(c.tree), { flat: true });
            let lastParent = null;
            for (let entry of data) {
                if (entry.data.xpath && entry.data.xpath.indexOf(searchStr) != -1) {
                    /*
                     * To keep result length reasonable, match the head of a
                     * subtree but not every node under the subtree
                     */
                    if (lastParent && entry.data.xpath.indexOf(lastParent) == 0) {
                        continue;
                    }
                    lastParent = entry.data.xpath;
                    matches.push([entry.id, entry.data.xpath]);
                }
            }
            stopProgress(progressBarDiv);
            return matches;
        }
        else {
            alert("Please load module(s)");
        }
    };

    function searchXpathsFormSubmit(e) {
        e.preventDefault();
        e.stopPropagation();
        let searchStr = $(c.xpathSearchStringEntry).val();
        if (!searchStr) {
            alert("Please enter a search string");
            return;
        }
        let results = searchTreeXpaths(searchStr);
        $(c.xpathSearchResultsSelect).empty();
        let resultsText = "";
        for (let result of results) {
            let id = result[0];
            let xpath = result[1];
            $(c.xpathSearchResultsSelect).append(
                '<option value="' + id + '">' + xpath + '</option>');
            resultsText += "\n" + xpath;
        }
        $(c.xpathSearchResultsText).val(resultsText);
    };

    function selectNodes(nodes) {
        if ($(c.tree).jstree(true)) {
            $(c.tree).jstree(true).deselect_all(true);
            $(c.tree).jstree(true).select_node(nodes);
            /* Scroll so first selected node is onscreen */
            let first = $(c.tree + " .jstree-clicked:first");
            if (first.length > 0) {
                let col = $(c.tree).scrollParent();
                col.scrollTop(first.offset().top -
                    $(c.tree).offset().top -
                    (col.height() / 2));
            }
        }
        else {
            alert("Please load module(s)");
        }
    };

    /* Public API */
    return {
        config: config,
        DEFAULT_NODETYPES: DEFAULT_NODETYPES,
        ALL_NODETYPES: ALL_NODETYPES,
        getJSTreeData: getJSTreeData,
        makeJSTree: makeJSTree,
        prepNodeIcons: prepNodeIcons,
        setNodeIcon: setNodeIcon,
        buildLegend: buildLegend,
        getRFCData: getRFCData,
        formatNodeData: formatNodeData,
        formatNodeToolTip: formatNodeToolTip,
        getNodeRFCData: getNodeRFCData,
        getModels: getModels,
        pushExploreState: pushExploreState,
        searchTreeNodes: searchTreeNodes,
        searchTreeXpaths: searchTreeXpaths,
        searchXpathsFormSubmit: searchXpathsFormSubmit,
        selectNodes: selectNodes,
    }
}();
