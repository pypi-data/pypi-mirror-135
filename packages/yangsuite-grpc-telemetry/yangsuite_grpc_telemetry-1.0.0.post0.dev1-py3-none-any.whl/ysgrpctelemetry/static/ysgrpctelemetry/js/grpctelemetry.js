/**
 * Module for gRPC Telemetry web UI.
 */
let grpctelemetry = function() {
    "use strict";

    /**
     * Default configuration of this module.
     */
    let config = {
        /* Selector string for a progressbar */
        listenIp: "#ys-listen-ip",
        listenPort: "#ys-listen-port",
        outputArea: "#ys-telemetry-output",
        tlsDeviceChkBox: "#ys-tls-device",
    };

    let c = config;     // internal alias for brevity

    let state = {
        updater: null
    }

    function addOutput(input, output, indent=0) {
        for (let key of Object.keys(input)) {
            if (typeof input[key] == 'object') {
                output = addOutput(input[key], output, 2);
            } else {
                for (let i = indent; i > 0; i--) {
                    output += " ";
                }
                output += key + ':  ' + input[key] + "\n";
            }
        };
        return output;
    }

    /**
     * Function: getOutPut
     *
     * Interval function to display servicer(s) output.
     */
    function getOutput() {
        const localGetUri = '/grpctelemetry/servicer/output';
        $.getJSON(localGetUri, function(data) {
            if (data.output.length == 0) {
                return;
            }
            let output = '<pre>';
            for (let block of data.output) {
                output = addOutput(block, output);
                $("#ys-grpc-output").append(output += '</pre>')
                output = '<pre>';
            }
        });
    }

    /**
     * startListening
     *
     * @param {string} port to listen on.
     * @param {string} address to listen on.
     * @param {string} secure device that contains server certificate/key.
     */
    function startListening(port, address, secure) {
        if (!address || address == "127.0.0.1" || address == "localhost") {
            alert("Enter a routable IP address");
            return;
        }
        if (!port) {
            port = alert("Enter TCP port to listen on.");
            return;
        }
        const localStartUri = '/grpctelemetry/servicer/' + port + '/start'
        getPromise(localStartUri, {address: address, secure: secure})
            .then(function(retObj) {
                alert(retObj.message);
                if (!retObj.result) {
                    return;
                }
                if (!state.updater) {
                    state.updater = setInterval(getOutput, 250);
                }
            });
    };

    /**
     * stopListening
     *
     * @param {string} port to stop listening on.
     */
    function stopListening(port) {
        const localStopUri = '/grpctelemetry/servicer/' + port + '/stop'
        getPromise(localStopUri)
            .then(function(retObj) {
                alert(retObj.message);
                getServicers();
            });
    };

    /**
     * getServicers
     *
     * Pop up dialog with table of active servisers which
     * users can choose to stop specific servisers.
     */
    function getServicers() {
        const servicerListUri = '/grpctelemetry/servicer/list';
        getPromise(servicerListUri)
        .then(function(retObj) {
            if (retObj.servers.length == 0) {
                alert("No live receivers");
                if (state.updater) {
                    clearInterval(state.updater);
                    state.updater = null;
                }
                return;
            }
            if (retObj.servers.length > 0 && !state.updater) {
                state.updater = setInterval(getOutput, 250);
            }
            let fileOut = retObj.fileout;
            let uriOut = retObj.uri;
            let table = '<table class="grpc-config"><th>IP Address</th><th>Port</th>';
            table += '<th>TLS</th>';
            for (let s of retObj.servers) {
                table += "<tr><td readonly>" + s[0] + "</td>";
                table += "<td readonly>" + s[1] + "</td>";
                table += "<td readonly>" + s[2] + "</td>";
                table += '<td><button "btn btn--small btn--primary"' + ' port=' + s[1];
                table += ' class="ys-server-stop">Stop</button></td>';
            }
            table += '<div class="row"><label><strong>Output file</strong></label></div>';
            table += '<div class="row"><input size="60" id="ys-output-file" value="'+ fileOut;
            table += '" placeholder="File path for telemtry output."/></div><hr>';
            table += '<div class="row"><lable><strong>Elasticsearch Output URI</strong></label></div>';
            table += '<div class="row"><input size="60" id="ys-output-uri" value="'+ uriOut;
            table += '" placeholder="example: http//localhost:9200"/></div><hr>';
            table += '<button "btn btn--small btn--primary" ';
            table += 'id="ys-output-config">Set Output(s)</button><hr>';

            $("#ys-servers-dialog").dialog({
                title: "Telemetry Receivers",
                width: "auto",
                height: "auto",
                buttons: {
                    "Exit": function () {
                        $(this).dialog("close");
                    }
                }
            }).html(table);
            $("#ys-servers-dialog").dialog("open");
            $(".ys-server-stop").click(function(){
                let port = $(this).attr("port");
                stopListening(port);
                $("#ys-servers-dialog").dialog("close");
            });
            $("#ys-output-config").click(function(){
                let port = $(this).attr("port");
                let file = $("#ys-output-file").val();
                let uri = $("#ys-output-uri").val();
                $("#ys-servers-dialog").dialog("close");
                outputConfig(port, file, uri);
            });
        });
    }

    /**
     * checkServicers
     *
     * When navigating back and forth to the grpc telemetry page, make
     * sure any live servicers continue streaming data to the web page.
     */
     function checkServicers() {
        const servicerListUri = '/grpctelemetry/servicer/list';
        getPromise(servicerListUri)
        .then(function(retObj) {
            if (retObj.servers.length > 0 && !state.updater) {
                state.updater = setInterval(getOutput, 250);
            }
        });
    }

    function outputConfig(port, file, uri) {
        const outputConfigUri = "/grpctelemetry/servicer/config";
        let outputCfg = {
            port: port,
            file: file,
            uri: uri,
        }
        getPromise(outputConfigUri, outputCfg)
        .then(function(retObj) {
            getServicers();
        });
    }

    /**
     * Public API.
     */
    return {
        config:config,
        startListening: startListening,
        getServicers: getServicers,
        checkServicers: checkServicers,
    };
}();
