/**
 * Module for requesting the server to obtain files via Git
 */
let git = function() {
    "use strict";

    /**
     * Default configuration of this module.
     */
    let config = {
        requestURI: "/filemanager/git/to_repository/",
        progress: 'div#ys-progress',
    };

    let c = config;    // internal alias for brevity

    /**
     * Clone the given Git repository and add files to a YANG repo
     */
    function gitToRepo(repo, url, branch, subdir,
                      include_subdirs=false) {
        
        let progressBarDiv = startProgress($(c.progress), c.requestURI) || $(c.progress);

        return getPromise(c.requestURI, {
            repository: repo,
            url: url,
            branch: branch,
            subdirectory: subdir,
            include_subdirs: include_subdirs,
        }).done(function () {
            repository.getRepoContents(repo);
            stopProgress(progressBarDiv);
            repository.checkRepo(repo);
        }).fail(function() {
            stopProgress(progressBarDiv);
        });
    };

    /* Public API */
    return {
        config:config,
        gitToRepo: gitToRepo,
    };
}();
