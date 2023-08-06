/**
 * Module for requesting the server to obtain files via SCP
 */
let scp = function() {
    "use strict";

    /**
     * Default configuration of this module.
     */
    let config = {
        requestURI: "/filemanager/scp/to_repository/",
        progress: 'div#ys-progress',
    };

    let c = config;    // internal alias for brevity

    /**
     * SCP YANG files from the given host + path to the given repo
     */
    function scpToRepo(repo, host, username, password, path,
                       include_subdirs=false, remote_type=undefined) {

        let progressBarDiv = startProgress($(c.progress), c.requestURI) || $(c.progress);

        return getPromise(c.requestURI, {
            repository: repo,
            host: host,
            ssh_username: username,
            ssh_password: password,
            remote_path: path,
            remote_type: remote_type,
            include_subdirs: include_subdirs,
        }).done(function () {
            repository.getRepoContents(repo);
            stopProgress(progressBarDiv);
            repository.checkRepo(repo);
        }).fail(function () {
            stopProgress(progressBarDiv);
        });
    }

    /* Public API */
    return {
        config:config,
        scpToRepo:scpToRepo,
    };
}();
