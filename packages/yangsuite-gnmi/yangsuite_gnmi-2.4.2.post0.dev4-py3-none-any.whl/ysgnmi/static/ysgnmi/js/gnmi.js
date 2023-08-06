/**
 * Module for YANG Suite gNMI / gRPC client.
 */
let gnmi = function() {
    "use strict";

    /**
     * Default configuration of this module.
     */
    let config = {
        /* Selector string for a progressbar */
        progressBar: "#ys-progress",

        tree: "#tree",
        serviceDialog: "#gnmi-service-dialog",
        rpcOpGroup: '#ys-rpc-group',
        editOpClass: '.ytool-edit-op',
        rpcConfigClass: '.ys-cfg-rpc',
        rpcInfoTextarea: 'textarea#ys-gnmi-content',
        deviceSelect: '#ys-devices-replay',
        getType: '[name=ys-get-type]:checked',
        originType: '[name=ys-origin-type]:checked',
        otherOrigin: '#ys-origin-other',
        prefixSupport: '#ys-prefix',
        base64: '#ys-base64',
        encodingType: '[name=ys-encoding-type]:checked',
        subscribeMode: '[name=ys-subscribe-mode]:checked',
        subscribeSubMode: '[name=ys-subscribe-submode]:checked',
        sampleInterval: '#ys-sample-interval',
        rawGNMI: "textarea#ys-gnmi-content",

        buildGetURI: '/gnmi/build_get/',
        buildSetURI: '/gnmi/build_set/',
        runURI: '/gnmi/run/',
        stopSessionURI: '/gnmi/stop/session/',
        runResultURI: '/gnmi/runresult/',
        runReplayURI: '/gnmi/runreplay/',
        showReplayURI: '/gnmi/showreplay/',
    };

    let c = config;     // internal alias for brevity

    let winref = {}

    /**
     * getNamespaceModules
     *
     * Collect special gNMI tree {prefix: module name} object needed to convert
     * prefixes in Xpaths to module names.
     *
     * @param {Object} data: Configuration data for request.
     */
    function getNamespaceModules(data) {
        // First config node is sufficent (for one module, one gNMI message).
        let cfgEle = $(rpcmanager.config.rpcConfigClass)[0];
        if (!cfgEle) {
            alert("Cannot build JSON without values set in tree.");
            return;
        }
        let nodeId = cfgEle.getAttribute('nodeid');
        let node = $(c.tree).jstree(true).get_node(nodeId);
        let moduleid = node.parents[node.parents.length - 2];
        let module = $(c.tree).jstree(true).get_node(moduleid);
        Object.keys(data.modules).forEach(function(key) {
            data.modules[key]['namespace_modules'] = module.data.namespace_modules;
        });
    }

    function buildJSON(device) {
        let data = rpcmanager.getRPCconfigs($(c.tree));
        getNamespaceModules(data);
        let action = $(config.rpcOpGroup + ' .selected').attr('data-value');
        let uri;
        if (action == 'get') {
            uri = config.buildGetURI;
            data['get_type'] = $(c.getType).val();
        } else if (action == 'subscribe') {
            uri = config.buildGetURI;
            data['request_mode'] =  $(c.subscribeMode).val();
            data['sub_mode'] =  $(c.subscribeSubMode).val();
            data['sample_interval'] =  $(c.sampleInterval).val();
        } else if (action == 'set') {
            uri = config.buildSetURI;
        }
        let origin = "";
        origin = $(c.originType).val();
        if (origin == 'other') {
            origin = $(c.otherOrigin).val();
        }
        data['origin'] = origin;
        data['prefix'] = $(c.prefixSupport).prop("checked");
        data['device'] = device;
        data['encoding'] = $(c.encodingType).val();
        data['base64'] = $(c.base64).prop("checked");
        data['action'] = action;
        data['run'] = false;
        jsonPromise(uri, data).then(function(retObj) {
            $(config.rpcInfoTextarea).val(retObj.gnmiMsgs);
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };


    function runGNMI(device, data) {
        if (!device) {
            popDialog("Please select a device");
            return;
        }
        if (!$("textarea#ys-gnmi-content").val().trim()) {
            alert('"Build JSON" from tree or paste gNMI message in run frame.');
            return;
        }
        if (!data.raw) {
            data = rpcmanager.getRPCconfigs($(c.tree));
            getNamespaceModules(data);
            let origin = "";
            origin = $(c.originType).val();
            if (origin == 'other') {
                origin = $(c.otherOrigin).val();
            }
            data['origin'] = origin;
            data['prefix'] = $(c.prefixSupport).prop("checked");
            data['base64'] = $(c.base64).prop("checked");
            data['run'] = true;
            data['encoding'] = $(c.encodingType).val();
        }
        data['action'] = $(config.rpcOpGroup + ' .selected').attr('data-value');
        data['device'] = device;
        if (data['action'] == 'subscribe') {
            data['request_mode'] =  $(c.subscribeMode).val();
            data['sub_mode'] =  $(c.subscribeSubMode).val();
            data['sample_interval'] =  $(c.sampleInterval).val();
        }

        $.when(jsonPromise(config.runURI + device, data))
        .then(function(retObj) {
            if (!retObj) {
                popDialog("<pre>RUN " + data['action'].toUpperCase() + " failed</pre>");
                if (winref.device) {
                    winref.device.close();
                    delete winref.device;
                }
                return;
            }
            if (retObj.response) {
                popDialog("<pre>" + retObj.response + "</pre>");
                if (winref.device) {
                    winref.device.close();
                    delete winref.device;
                }
                return;
            }
        })
        .fail(function(retObj) {
            popDialog("<pre>Status: " + retObj.status + "\n" + retObj.statusText + "</pre>");
            if (winref.device) {
                winref.device.close();
                delete winref.device;
            }
        });

        if (!winref.device) {
            winref[device] = window.open(
                config.runResultURI + device, device,
                "height=700 overflow=auto width=800, scrollbars=yes"
            );
        }
    };

    function runCapabilities(device, data) {
        if (!device) {
            popDialog("Please select a device");
            return;
        }

        let pb = startProgress($(config.progressBar)) || $(config.progressBar);

        return jsonPromise(config.runURI + device, data).then(function(retObj) {
            stopProgress(pb);
            return retObj;
        }, function(retObj) {
            stopProgress(pb);
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    function stopSession(device) {
        return jsonPromise(config.stopSessionURI + device);
    }

    function runReplay(device, data) {
        if (!device) {
            popDialog("Please select a device");
            return;
        }

        let pb = startProgress($(config.progressBar)) || $(config.progressBar);

        return jsonPromise(config.runReplayURI + device, data).then(function(retObj) {
            stopProgress(pb);
            return retObj;
        }, function(retObj) {
            stopProgress(pb);
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    function showReplay(data) {
        data['get_type'] = $(c.getType).val();
        data['origin'] = $(c.originType).val();

        jsonPromise(config.showReplayURI, data).then(function(retObj) {
            let replay = '';
            let segments = retObj["gnmi_replay"];
            for (let segment of segments) {
                replay +=  stringify(segment) + "\n";
            }
            $(config.rpcInfoTextarea).val(replay);
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    }

    /**
     * Public API.
     */
    return {
        config:config,
        buildJSON: buildJSON,
        runGNMI: runGNMI,
        stopSession: stopSession,
        runCapabilities: runCapabilities,
        runReplay: runReplay,
        showReplay: showReplay,
    };
}();
