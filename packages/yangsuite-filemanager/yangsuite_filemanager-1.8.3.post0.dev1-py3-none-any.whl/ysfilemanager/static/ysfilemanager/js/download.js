/**
 * Module for using NETCONF to query and download YANG schemas from a device.
 * Depends on yangsuite-netconf plugin being installed on the server.
 */
let download = function() {
    "use strict";

    /**
     * Default configuration of this module.
     */
    let config = {
        // Strings used for jquery selectors
        schemaSelect: "select#ys-device-schemas-list",
        progress: 'div#ys-progress',
    };

    let c = config;  // internal alias for brevity

    /**
     * Get the list of supported schemas from the device and populate a
     * select element with this list.
     *
     * @param {string} profileName - Device profile name
     */
    function getSchemaList(profileName) {
        if (!profileName || profileName == "") {
            popDialog("No device profile specified.");
            return;
        }

        let p = getPromise("/netconf/schemas/list/", {"device": profileName});
        let progress = $(c.progress);
        progress.progressbar({value: false});

        $(c.schemaSelect).empty();

        $.when(p).then(function(retObj) {
            progress.progressbar("destroy");
            $.each(retObj.reply.schemas, function(i, obj) {
                yangsets.makeAppropriateChild($(c.schemaSelect),
                                              obj.name + ',' + obj.revision,
                                              obj.name + ' @ ' + obj.revision);
            });
        }, function(retObj, textStatus) {
            // Error response
            progress.progressbar("destroy");
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    }

    /**
     * Download the requested set of YANG schemas from the given device
     * to the given repository.
     *
     * @param {string} profileName - The device profile name
     * @param {string} repo - "user:reponame"
     */
    function downloadToRepo(profileName, repo) {
        if (!profileName || profileName == "") {
            popDialog("No device profile specified.");
            return;
        }

        if (!repo) {
            popDialog("No repository specified.");
            return;
        }

        let requestData = {device: profileName,
                           repository: repo,
                           schemas: yangsets.moduleStringsToJson(
                               $(c.schemaSelect).val())};

        let progress = $(c.progress);
        progress.progressbar({value: false});

        let p = getPromise("/netconf/schemas/download/", requestData);

        let progressInterval = setInterval(function() {
            updateProgress("/netconf/schemas/download/", progress,
                           {'device': profileName});
        }, 1000);

        return p.done(function(retObj) {
            progress.progressbar("destroy");
            clearInterval(progressInterval);
            repository.getRepoContents(repo);
            repository.checkRepo(repo);
        }).fail(function(retObj, textStatus) {
            // Error response
            progress.progressbar("destroy");
            clearInterval(progressInterval);
        });
    };

    /* Public API of this module */
    return {
        config:config,
        getSchemaList:getSchemaList,
        downloadToRepo:downloadToRepo,
    };
}();
