/**
 * Module for handling RPC operations
 */
let rpcmanager = function() {
    "use strict";

    let config = {
        progressBar: "div#ys-progress",
        protoOpSelect: '#ys-proto-op',
        withDefaultsSelect: '#ys-with-defaults',
        editOpClass: '.ytool-edit-op',
        rpcConfigClass: '.ys-cfg-rpc',
        rpcInfoTextarea: 'textarea#ytool-rpc-info',
        rpcTextarea: 'textarea#ytool-rpc-data',
        deviceSelect: 'select#ys-devices-replay',
        deviceRunSelect: 'select#ys-open-device-window',
        datastoreGroup: '#ys-datastore-group',
        gentypeSelect: '#ys-rpctype',
        prefixSelect: '[name=ys-rpcprefixes]:checked',
        testDiv: 'div#ytool-test-col',
        getURI: '/netconf/getrpc/',
        getTaskURI: '/netconf/gettaskrpc/',
        commitURI: '/netconf/getcommit/',
        runURI: '/netconf/runrpc/',
        runResultURI: '/netconf/runresult/',
        segmentctr: 1,
        savedrpcs: [],
    };

    let locals = {
        keepAlives: {},
    };

    /**
     * This will be the new object created to send back config data
     * to construct a Netconf RPC
     *
     * @param {Object} node - A single jsTree node
     */
    function rpcCfg(node) {
        this.xpath = node.data.xpath_pfx;
    };

    /*
     * Find the module node that owns this node.
     * node.parents = [parent_id, grandpt_id, ..., module_id, "#"]
     */
    function getModule(node, modules, tree) {
        let moduleid = node.parents[node.parents.length - 2];
        let moduleNode = tree.get_node(moduleid);

        let moduleName = moduleNode.data.module;
        /* Initialize the config data for this module if needed. */
        if (!modules[moduleName]) {
            modules[moduleName] = {
                revision: moduleNode.data.revision,
                namespace_prefixes: moduleNode.data.namespace_prefixes,
                configs: {}
            };
        }
        return [modules, moduleName];
    }

    /**
     * Configured values were scraped from the HTML elements and
     * put in objects.  Here we pre-process the values and convert
     * them to JSON
     *
     * @param {Object} tree - Top of jsTree
     * @returns {object} rpcs - All data used to construct a collection of RPCs
     *
     * rpcs = {
     *   'proto-op': 'edit-config',
     *   'dsstore': 'running',
     *   'with-defaults': '',
     *   'modules': {
     *     'modA': {
     *       'revision': "2015-01-01",
     *       'namespace_prefixes': { ... },
     *       'configs': [ {...}, {...}, ],
     *     },
     *     'modB': {...}
     *   }
     * }
     */
    function getRPCconfigs(tree) {
        if (!tree.jstree(true)) {
            return;
        }

        let modules = {};
        let moduleName = "";
        let rpcs = {};
        let movedRows = {};

        rpcs['proto-op'] = ($(config.protoOpSelect).val() ||
                            $(config.protoOpSelect).attr('data-value'));
        rpcs['dsstore'] = ($(config.targetSelect).val() ||
                           $(config.datastoreGroup).find(".selected").attr('data-value'));
        rpcs['with-defaults'] = $(config.withDefaultsSelect).val();

        let listsMissingKeys = new Set();

        /*
         * Iterate over every user selection in the Value column and create
         * appropriate configuration for backend to build RPC.
         */
        $($(tree).closest('.jstree-grid-wrapper')[0])
            .find($(config.rpcConfigClass))
            .each(function(i, element) {
                /* Get the jstree node this element associates to. */
                let nodeid = element.getAttribute('nodeid');
                let node = tree.jstree(true).get_node(nodeid);
                let modules_name = getModule(node, modules, tree.jstree(true));

                modules = modules_name[0];
                moduleName = modules_name[1];

                /*
                 * For an edit-config (but not a get or get-config), it's
                 * probably not a valid RPC if we have list contents but
                 * haven't specified the list keys. Check for that.
                 */
                if (rpcs['proto-op'] == 'edit-config') {
                    let grandparentXPath = "";
                    /* Walk from the root of the tree down to the node itself */
                    for (let parentid of Array.from(node.parents).reverse()) {
                        if (parentid == "#") { continue; }
                        let parentNode = tree.jstree(true).get_node(parentid);
                        if (parentNode.data.nodetype == 'list') {
                            // Get just the last segment of the xpath
                            let xpathSegment = parentNode.data.xpath.replace(
                                grandparentXPath, '');
                            // How many predicates (list keys) does it contain?
                            let predicateCount = (xpathSegment.match(/\[/g)||[]).length;
                            if (predicateCount < parentNode.data.keys.length) {
                                listsMissingKeys.add(parentNode.data.xpath);
                            }
                        }
                        grandparentXPath = parentNode.data.xpath;
                    }
                }

                /* What row number of the visible jstree-grid are we in? */
                let row = $(element)
                    .closest(".jstree-grid-column")
                    .children("div")
                    .index(element.parentElement);

                /* Update existing entry for this row, or create a new one */
                let cfg = (modules[moduleName].configs[row] ||
                           modules[moduleName].configs[movedRows[row]] ||
                           new rpcCfg(node, tree));

                cfg['nodetype'] = node.data.nodetype || '';
                cfg['datatype'] = node.data.basetype || node.data.datatype;
                cfg['default'] = node.data.default || '';
                if (element.type == "textarea") {
                    // anyxml or anydata
                    cfg.xml_value = element.value;
                } else if (element.type != "checkbox" && element.type != "radio" && !node.data.novalue) {
                    cfg.value = element.value;
                }
                let isSubPath = false;
                for (let rowCfg of Object.entries(modules[moduleName].configs)) {
                    /* List nodes may already be represented in another path so
                     * don't add them, example:
                     * /my/list/node[key=value]
                     * /my/list/node[key=value]/already/in/leaf/node/xpath
                     */
                    if (cfg.xpath.includes(rowCfg[1].xpath)) {
                        if (cfg.xpath == rowCfg[1].xpath) {
                            modules[moduleName].configs[rowCfg[0]] = cfg;
                            movedRows[row] = rowCfg[0];
                            isSubPath = true;
                            break;
                        }
                    }
                }
                if (!isSubPath) {
                    modules[moduleName].configs[row] = cfg;
                }
            }); /* end inner function / .each() loop */
        /*
         * Iterate over every user selection in the Operation column and add
         * edit-ops to the configuration for backend build of RPC.
         */
        $($(tree).closest('.jstree-grid-wrapper')[0])
            .find($(config.editOpClass))
            .each(function(i, element) {
                /* Get the jstree node this element associates to. */
                let nodeid = element.getAttribute('nodeid');
                let node = tree.jstree(true).get_node(nodeid);
                let modules_name = getModule(node, modules, tree.jstree(true));
                let node_added = false

                modules = modules_name[0];
                moduleName = modules_name[1];

                /* What row number of the visible jstree-grid are we in? */
                let row = $(element)
                    .closest(".jstree-grid-column")
                    .children("div")
                    .index(element.parentElement);

                if ($.isEmptyObject(modules[moduleName].configs)) {
                    let cfg = new rpcCfg(node);
                    if (["container", "list"].indexOf(node.data.nodetype)> -1) {
                      cfg['edit-op'] = element.value;
                      cfg['nodetype'] = node.data.nodetype;
                      modules[moduleName].configs[row] = cfg;
                    } else if (["delete", "remove"].indexOf(element.value) > -1) {
                        cfg['edit-op'] = element.value;
                        cfg['nodetype'] = node.data.nodetype;
                        modules[moduleName].configs[row] = cfg;
                    }
                    node_added = true
                } else if (node.data.nodetype == "list") {
                    // edit-op on list so add config to correct location.
                    let cfg = new rpcCfg(node);
                    cfg['edit-op'] = element.value;
                    cfg['nodetype'] = node.data.nodetype;
                    for (let rowCfg of Object.entries(modules[moduleName].configs)) {
                        if (rowCfg[1].xpath.includes(cfg.xpath)) {
                            if( row < rowCfg[0]){
                                node_added = true
                                if (rowCfg[1].xpath == cfg.xpath) {
                                    /*
                                     * list operation with only the key in message
                                     * /xpath/to/list[key=value]
                                     */
                                    modules[moduleName].configs[rowCfg[0]] = cfg;
                                    break;
                                } else {
                                    /*
                                     * list operation and children are part of message
                                     * /xpath/to/list[key=value]/child
                                     *
                                     * add list with edit-op to message for this case
                                     */
                                    modules[moduleName].configs[row] = cfg;
                                    break;
                                }
                            } else {
                                /*
                                * List node is a sublist and  with operation value
                                *  /xpath/to/list[key=value]/child/list[key=value]
                                */
                                let moved_key = Object.keys(movedRows).find(key => movedRows[key] === rowCfg[0])
                                if (moved_key != undefined && row < moved_key) {
                                    modules[moduleName].configs[rowCfg[0]] = cfg;
                                    node_added = true
                                    break;
                              }
                           }
                        }
                    }
                } else if (node.data.nodetype == "container") {
                    // edit-op on container so add config to correct location
                    let cfg = new rpcCfg(node);
                    cfg['edit-op'] = element.value;
                    cfg['nodetype'] = node.data.nodetype;
                    let delCfgs = [];
                    for (let rowCfg of Object.entries(modules[moduleName].configs)) {
                        if (rowCfg[1].xpath.includes(cfg.xpath) && row < rowCfg[0]) {
                            modules[moduleName].configs[row] = cfg;
                            node_added = true
                        }
                        if (["delete", "remove"].indexOf(element.value) > -1) {
                            // All configs below deleted container are not needed
                            if (rowCfg[1].xpath.includes(cfg.xpath) && row < rowCfg[0]) {
                                delCfgs.push(rowCfg[0]);
                            }
                        }
                    }
                    // remove any configs not needed for delete/remove
                    for (let dcfg of delCfgs) {
                        delete modules[moduleName].configs[dcfg];
                    }
                } else {
                    // edit-op config is already in configs
                    for (let rowCfg of Object.entries(modules[moduleName].configs)) {
                        if (row in movedRows) {
                            row = movedRows[row];
                        }
                        if (row == rowCfg[0]) {
                            modules[moduleName].configs[row]['edit-op'] = element.value;
                            node_added = true
                            break;
                        }
                    }
                }
                //edit-op with out a value in value column
                if ((!Object.keys((modules[moduleName].configs)).includes(String(row))) && (node_added==false)){
                      let cfg = new rpcCfg(node);
                      if (["container", "list"].indexOf(node.data.nodetype)> -1) {
                        cfg['edit-op'] = element.value;
                        cfg['nodetype'] = node.data.nodetype;
                        modules[moduleName].configs[row] = cfg;
                      } else if (["delete", "remove"].indexOf(element.value) > -1) {
                          cfg['edit-op'] = element.value;
                          cfg['nodetype'] = node.data.nodetype;
                          modules[moduleName].configs[row] = cfg;
                      }
                }

            });
        if (listsMissingKeys.size > 0) {
            let warningDialog = $("<div>").text(
                "The following list(s) are missing values for one or more of " +
                    "their list keys. The resulting RPC may not be valid " +
                    "unless the keys are specified.");
            let warningList = $("<ul>");
            for (let lmk of listsMissingKeys) {
                warningList.append($("<li>").text(lmk));
            }
            warningDialog.append(warningList);
            warningDialog.dialog({
                height: "auto",
                maxHeight: $(window).height() * 0.9,
                width: "auto",
                maxWidth: $(window).width() * 0.9,
                title: "Missing list keys",
            }).dialog("open");
        }

        /*
         * Now we must make each module.configs into an Array of rpcCfg
         */
        for (let moduleName in modules) {
            if (!modules.hasOwnProperty(moduleName)) {
                continue;
            }
            let module = modules[moduleName];
            module.configs = Object.values(module.configs);
        }
        rpcs['modules'] = modules;

        return rpcs;
    };

    /**
     * Asynchronous function that resends node data to backend to change
     * the format of the display.
     *
     * @param {string} gentype - basic or raw format.
     * @param {string} prefix_namespaces - 'minimal' or 'always'
     */
    function reloadRPCs(gentype, prefix_namespaces) {
        if (config.savedrpcs.length < 1) {
            return;
        }
        if (gentype == "script") {
            /* Club all RPCs together into a single API call */
            let data = {"gentype" : "script",
                        "prefix_namespaces": prefix_namespaces};
            data['cfgd'] = config.savedrpcs;
            let lastrpc = config.savedrpcs[config.savedrpcs.length - 1];
            $.when(jsonPromise(config.getURI, data)).then(function(retObj) {
                let infostrings = [];
                $.each(config.savedrpcs, function(i, data) {
                    $.each(data.cfgd.modules, function(key, value) {
                        infostrings.push(key + ": " + value.revision);
                    });
                });
                updateRPCText(retObj.reply, infostrings);

                $(config.testDiv).remove();
            }, function(retObj) {
                popDialog("Error " + retObj.status + ": " + retObj.statusText);
            });
            return;
        }

        /* For all other gentypes, we request one RPC at a time. */
        $.each(config.savedrpcs, function(i, data) {
            data['gentype'] = gentype;
            data["prefix_namespaces"] = prefix_namespaces;
            $.when(jsonPromise(config.getURI, data)).then(function(retObj) {
                let infostrings = [];
                $.each(data['cfgd'].modules, function(key, value) {
                    infostrings.push(key + ": " + value['revision']);
                });
                updateRPCText(retObj.reply, infostrings);

                $(config.testDiv).remove();
            }, function(retObj) {
                popDialog("Error " + retObj.status + ": " + retObj.statusText);
            });
        });
    }

    /**
     * Download the RPCs as a standalone Python script
     */
    function downloadScript() {
        let data = {
            gentype: 'script',
            prefix_namespaces: $(config.prefixSelect).val(),
            cfgd: config.savedrpcs,
        };
        $.when(jsonPromise(config.getURI, data)).then(function(retObj) {
            let element = document.createElement("a");
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' +
                                 encodeURIComponent(retObj.reply));
            element.setAttribute('download', 'script.py');
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    /**
     * Asynchronous function that sends node data to backend to be converted
     * to XML format that complies with Netconf.
     *
     * @param {Object} tree - Top of jsTree.
     * @param {string} gentype - Format of display (basic, raw).
     * @param {string} addcommit - Specify whether to add a commit action.
     * @param {string} prefix_namespaces - Preferred handling for XML
     *                    namespace prefixes. Options: 'always', 'minimal'
     */
    function addRPC(tree, gentype, addcommit="", prefix_namespaces='always') {
        let data = {};
        let rpccfg = getRPCconfigs(tree);

        if ($.isEmptyObject(rpccfg.modules)) {
            if (rpccfg['proto-op'] == 'edit-config') {
                popDialog('To construct an "edit-config" RPC, you must ' +
                          'select at least one item in the Value and/or ' +
                          'Operation columns.');
                return;
            } else if (rpccfg['proto-op'] == 'rpc') {
                popDialog('To construct any given RPC, you must select ' +
                          'at least one item in the Value column.');
                return;
            } else {
                popDialog('Constructing an empty "' + rpccfg['proto-op'] + '"' +
                          ' RPC. If this is not what you intended to do, ' +
                          ' be sure to select at least one item in the Value column.');
                // continue;
            }
        }
        data['gentype'] = gentype;
        data['commit'] = addcommit;
        data['prefix_namespaces'] = prefix_namespaces;
        data['segment'] = config.segmentctr++;
        data['cfgd'] = rpccfg;

        config.savedrpcs.push(data);

        if (gentype == "script") {
            data = {'gentype': 'script', 'cfgd': config.savedrpcs};
            // We re-generate the entire script, so clear existing script:
            $(config.rpcTextarea).val('');
        }

        $.when(jsonPromise(config.getURI, data)).then(function(retObj) {
            let infostrings = [];
            $.each(rpccfg.modules, function(key, value) {
                infostrings.push(key + ": " + value['revision']);
            });
            updateRPCText(retObj.reply, infostrings);

            $(config.testDiv).remove();
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    /**
     * Clear data and counters for fresh start
     */
    function clearRPC() {
        config.segmentctr = 1;
        config.savedrpcs = [];
    }

    /**
     * Helper function for addRPC() and addCommit()
     *
     * @param {string} rpc string to populate XML in textarea.
     * @param {Array} infostrings - array of module information strings to
     *                              populate textarea.
     */
    function updateRPCText(rpc, infostrings) {
        for (let info of infostrings) {
            let oldinfo = $(config.rpcInfoTextarea).val();
            if (oldinfo && oldinfo.length == 0) {
                $(config.rpcInfoTextarea).val(info);
            } else if (oldinfo && oldinfo.length > 0 && oldinfo.indexOf(info) < 0) {
                $(config.rpcInfoTextarea).val(oldinfo + "\n" + info);
            }
        }
        let oldrpc = $(config.rpcTextarea).val();
        if (oldrpc) {
            oldrpc += "\n";
        }
        $(config.rpcTextarea).val(oldrpc + rpc);
    };

    /**
     * Helper function to clear info and rpc textarea
     */
    function clearRPCText() {
        $(config.rpcInfoTextarea).val("");
        $(config.rpcTextarea).val("");
    }

    /**
     * Polling mechanism between master window and result windows.
     *
     * @param {string} device - name of device assigned to window
     * @param {number} retry - if polling fails try it again
     */
    function checkKeepAlive(device, retry=1) {
        if (Object.keys(locals.keepAlives).length == 0) {
            console.log("keepAlives references are gone!");
            return;
        }
        let keepAlive = locals.keepAlives[device];
        if (!keepAlive) {
            console.log("keepAlive for " + device + " missing")
            return;
        }
        if (keepAlive.win.runStatus == "unknown") {
            /* window state not changed to alive */
            if (retry) {
                /* try one more time just in case we are out of sync */
                console.log("Retry keep alive - run window unknown state");
                checkKeepAlive(device, retry=0);
                return;
            }
            /* window has stopped pinging so stop checking */
            console.log("Run window not responding. Terminating session");
            clearInterval(keepAlive.clearID);
            delete locals.keepAlives[device];
            netconf.startEndSession(device, 'end');
            $(config.deviceRunSelect).val("none");
        } else if (keepAlive.win.runStatus == "alive") {
            /* window set alive state so reset it and wait for next check */
            keepAlive.win.runStatus = "unknown";
        } else {
            /* window state not determined */
            if (retry) {
                /* try one more time just in case we are out of sync */
                console.log("Retry keep alive - run window invalid state.");
                checkKeepAlive(device, retry=0);
                return;
            }
            console.log("Run window has invalid state. Terminating session");
            clearInterval(keepAlive.clearID);
            delete locals.keepAlives[device];
            netconf.startEndSession(device, 'end');
            $(config.deviceRunSelect).val("none");
        }
    }

    /**
     * Start a window that sets status to "alive" every "interval" seconds.
     * The parent that spawns the window can then check that status to make
     * sure the window is still alive.
     *
     * @param {object} index - Index to map that contains a window reference
     * @param {integer} interval - Seconds between status check
     */
    function openDeviceWindow(index, interval=1500, windowOrTab="tab") {
        if (!locals.keepAlives[index]) {
            let win = null;
            /* open a result window that sets status periodically */
            if (windowOrTab === "tab") {
                win = window.open(
                    config.runResultURI + index,
                    "_blank");
            } else if (windowOrTab === "pop") {
                win = window.open(
                    config.runResultURI + index,
                    'YANG Suite Run ' + index,
                    "height=2560px overflow=auto width=1271px, scrollbars=yes");
            } else {
                return;
            }
            if (!win) {
                alert("Window failed to open...popups blocked?");
                return;
            } else {
                win.runStatus = "alive";
                win.focus();
            }

            /* check every "interval" seconds to see if the window is still alive */
            let clearID = setInterval(function() {
                checkKeepAlive(index);
            }, interval);
            locals.keepAlives[index] = {win: win, clearID: clearID};
        }
    }

    /**
     * Asynchronous function that sends node data to backend to send to device.
     *
     * @param {string} device - Slug identifying device profile to send to
     * @param {string} datastore - Datastore RPC applies to, if any
     * @param {array, string} rpcs - Array of Objects that contains the node
     *     data, OR (if custom) an XML string.
     * @param {boolean} custom - Flag specifying a custom RPC to be sent instead
     *                           of node data.
     */
    function runRPC(device, rpcs, custom=false) {
        let data = {};

        if (!device) {
            popDialog("Please Select Device");
            return;
        }
        $(config.testDiv).remove();

        data = {
            device: device,
        };
        if (custom) {
            data['custom'] = "true";
            data['rpcs'] = rpcs;
        } else {
            data['rpcs'] = rpcs;
        }

        $.when(jsonPromise(config.runURI, data)).then(function(retObj) {
            if (!retObj) {
                // TODO is clearInterval appropriate here?
                clearInterval(locals.keepAlives[device]);
                delete locals.keepAlives[device];
                return;
            }
            if (retObj.error) {
                // TODO is clearInterval appropriate here?
                clearInterval(locals.keepAlives[device]);
                delete locals.keepAlives[device];
                return;
            }
            config.segmentctr = 1;
        }, function(retObj) {
            popDialog('Error' + retObj.status + ':' + retObj.statusText);
        });

    };

    /**
     * Send a canned 'commit' RPC to the given device.
     */
    function sendCommitRPC(device) {
        runRPC(device,
`<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <commit/>
</rpc>`, true);
    };

    /**
     * Send a canned unfiltered 'get-config' RPC for the given datastore
     */
    function sendGetConfigAllRPC(device, dsstore) {
        runRPC(device,
`<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get-config>
    <source>
      <${dsstore}/>
    </source>
  </get-config>
</rpc>`, true);
    };

    /**
     * Send a canned RFC 5277 'get streams' RPC to the given device
     */
    function sendGetStreamsRPC(device) {
        runRPC(device,
`<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get>
    <filter type="subtree">
      <netconf xmlns="urn:ietf:params:xml:ns:netmod:notification">
        <streams/>
      </netconf>
    </filter>
  </get>
</rpc>`, true);
    }

    /**
     * Send a canned RFC 5277 'create-subscription' RPC for the given stream.
     */
    function sendSubscribeRPC(device, eventstream) {
        runRPC(device,
`<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <create-subscription xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">
    <stream>${eventstream}</stream>
  </create-subscription>
</rpc>`, true);
    }

    /**
     * Load a replay task and create NETCONF RPCs based on the metadata
     *
     * @param {string} name - Name of replay task to load.
     */
    function loadTask(name, gentype="basic", category="default", variables={}) {

        let data = {'name': name,
                    'gentype': gentype,
                    'prefixes': $(config.prefixSelect).val(),
                    'dsstore': ($(config.targetSelect).val() ||
                                $(config.datastoreGroup).find(".selected").attr('data-value')),
                    'category': category,
                    'variables': JSON.stringify(variables)};

        let progressBar = startProgress($(config.progressBar), "", "",
                                        "Loading replay XML...");

        $.when(getPromise(config.getTaskURI, data))
        .then(function(retObj) {
            if (!retObj) {
                // TODO: fail/suscces not returned
                popDialog("GET Task " + name + " failed");
                return;
            }
            if (retObj.error) {
                popDialog(retObj.error);
                return;
            }

            clearRPCText();

            let text = "";
            for (let txt of retObj.info) {
                text += txt[0] + ": " + txt[1];
            }
            $(config.rpcInfoTextarea).val(text)

            updateRPCText(formatXml(retObj.segments), text);

            $(config.testDiv).remove();
            stopProgress(progressBar);
        })
        .fail(function(retObj) {
            stopProgress(progressBar);
            let t = retObj.responseText;
            popDialog(retObj.statusText + "<pre>" + t.slice(0, t.indexOf("\n\n")) + "</pre>");
        });
    };

    /**
     * Given replay contents as retrieved from tasks.getTask, populate
     * config.savedrpcs accordingly.
     */
    function populateSavedRPCsFromReplay(segments) {
        clearRPC();

        let anyCustom = false;
        for (let segment of segments) {
            if (segment.yang['proto-op'] == 'custom') {
                anyCustom = true;
                continue;
            }
            let segdata = {
                cfgd: {
                    dsstore: $(config.datastoreGroup).find(".selected").attr('data-value'),
                    modules: segment.yang.modules,
                    "proto-op": segment.yang['proto-op'],
                },
                commit: segment.commit,
                gentype: $(config.gentypeSelect).val(),
                prefix_namespaces: $(config.prefixSelect).val(),
                segment: segment.segment,
            };

            config.savedrpcs.push(segdata);
        }

        if (anyCustom) {
            $(config.rpcTextarea).trigger('change');
        }
    };

    /**
     * Replay a saved task in NETCONF protocol.
     *
     * @param {string} name - Name of task to run.
     * @param {string} category - Category of task
     */
    function runTask(name, category, variables={}) {
        let data = {'task': name,
                    'category': category,
                    'prefixes': $(config.prefixSelect).val(),
                    'device': $(config.deviceSelect).val(),
                    'dsstore': ($(config.targetSelect).val() ||
                                $(config.datastoreGroup).find(".selected").attr('data-value')),
                    'variables': JSON.stringify(variables),
                   };

        $.when(jsonPromise(config.runURI, data)).then(function(retObj) {
            if (!retObj) {
                $(config.runDiv).append("<pre>RUN Task " + name + " failed</pre>");
                clearInterval(locals.keepAlives[data.device]);
                delete locals.keepAlives[data.device];
                return;
            }
            if (retObj.error) {
                $(config.runDiv).append("<pre>" + retObj.error + "</pre>");
                clearInterval(locals.keepAlives[data.device]);
                delete locals.keepAlives[data.device];
                return;
            }
        });

        openDeviceWindow(data.device, 1500);
    }

    /**
     * Public APIs
     */
    return {
        config: config,
        addrpc: addRPC,
        clearrpcs: clearRPC,
        runrpc: runRPC,
        sendCommitRPC: sendCommitRPC,
        sendGetConfigAllRPC: sendGetConfigAllRPC,
        sendGetStreamsRPC: sendGetStreamsRPC,
        sendSubscribeRPC: sendSubscribeRPC,
        reloadrpcs: reloadRPCs,
        downloadScript: downloadScript,
        getRPCconfigs: getRPCconfigs,
        updateRPCText: updateRPCText,
        loadtask: loadTask,
        populateSavedRPCsFromReplay: populateSavedRPCsFromReplay,
        runtask: runTask,
        openDeviceWindow: openDeviceWindow,
    };

}();
