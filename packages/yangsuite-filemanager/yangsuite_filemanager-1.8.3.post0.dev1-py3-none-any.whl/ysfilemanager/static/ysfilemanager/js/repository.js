/**
 * Module for managing YANG module repositories and their contents.
 */
let repository = function() {
    "use strict";

    /**
     * Default configuration of this module.
     */
    let config = {
        reposMenu: 'select#ys-repos',
        moduleListing: 'select#ys-repo-contents',
        repoStatusContainer: 'div#ys-repo-status-container',
        repoStatusText: 'div#ys-repo-status',
        missingModulesList: 'ul#ys-repo-missing-modules',
        progress: 'div#ys-progress',
    };

    let c = config;    // internal alias for brevity

    let store = {
        /* List of 'name,rev' strings for the current repository */
        repositoryModules: [],
        /* Flag indicating 'readiness' of repositoryModules */
        repositoryModulesReady: false,
    }

    /**
     * Get the list of existing repositories and populate the repos menu.
     *
     * TODO: this is 90% identical to yangsets.getYangSets - can we merge?
     */
    function getRepos(selection="") {
        let menu = $(c.reposMenu);
        menu.empty();
        return $.ajax({
            url: '/filemanager/repository/list/',
            type: 'GET',
            dataType: 'json',
            success: function(retObj) {
                /* Always have a 'none of the below' option */
                menu.append('<option value=""></option>');
                /*
                 * Expected format is {'user': [{data}, {data}, ], ...}
                 * If we have more than one user, group the repos by username.
                 */
                let optgroups = false;
                if (Object.keys(retObj.repositories).length > 1) {
                    optgroups = true;
                }

                let selectionFound = false;
                $.each(retObj.repositories, function(username, repos) {
                    let target = menu;
                    if (optgroups) {
                        menu.append('<optgroup label="' + username + '">' +
                                    '</optgroup>');
                        target = menu.children("optgroup:last");
                    }
                    $.each(repos, function(i, data) {
                        if (data['slug'] == selection) {
                            selectionFound = true;
                        }
                        yangsets.makeAppropriateChild(
                            target, data['slug'], data['name']);
                    });
                });
                if (selection && selectionFound) {
                    menu.val(selection);
                }
                menu.trigger("change");
                /* Don't let the user choose 'none of the below' */
                menu.children('option[value=""]').prop("disabled", true);
            },
            error: function(retObj) {
                popDialog("Error " + retObj.status + ": " + retObj.statusText);
            }
        });
    };

    /**
     * Get the list of modules contained in the given repository
     *
     * @param {string} repo YANG repository "owner:reponame"
     */
    function getRepoContents(repo) {
        if (!repo) {
            popDialog("Please specify a repository to retrieve.");
            return;
        }
        let progressBarDiv = startProgress($(c.progress), "", "", "Fetching repo contents") || $(c.progress);
        $(c.moduleListing).empty();
        store.repositoryModulesReady = false;
        store.repositoryModules = [];
        let data = {'repository': repo};
        return $.ajax({
            url: '/filemanager/repository/get/',
            type: 'GET',
            data: data,
            dataType: 'json'})
            .done(function(retObj) {
                store.repositoryModules = [];
                $.each(retObj.modules, function(i, module) {
                    let entry = yangsets.moduleNameRevToValueText(module);
                    store.repositoryModules.push(entry.value);
                    yangsets.makeAppropriateChild($(c.moduleListing),
                                                  entry.value, entry.text);
                });
                store.repositoryModulesReady = true;
                stopProgress(progressBarDiv);
            })
            .fail(function(retObj) {
                stopProgress(progressBarDiv);
                popDialog("Error " + retObj.status + ": " + retObj.statusText);
            });
    };

    /**
     * Create a new repository
     */
    function createRepo(name, source, otherrepo) {
        if (!name) {
            popDialog("Please enter a repository name to create");
            return;
        }
        let letters = /^(?!.*[-_]{2})(?=.*[a-z0-9]$)[a-z0-9][a-z0-9_-]*$/gmi;
        if (!letters.test(name)) {
          popDialog("<b>Repository name is not valid.</b> </br>" +
                    "<b>Make sure:</b> </br> " +
                    "<ul><li>It should have atleast one character.</li>" +
                    "<li>Special characters allowed are: '-' and '_'.</li>" +
                    "<li>It should not start with any " +
                    "special character.</li></ul>")
          return;
        }
        let data = {'reponame': name};
        if (source == 'clone') {
            if (!otherrepo) {
                popDialog("Please select the repository to clone from");
                return;
            }
            data['source'] = otherrepo;
        }
        let p = getPromise('/filemanager/repository/create/', data);
        $.when(p).then(function(retObj) {
            getRepos(retObj.repository);
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    /**
     * Delete an existing repository
     */
    function deleteRepo(repo) {
        if (!repo) {
            popDialog("Please select the repository to delete.");
            return;
        }
        let data = {'repository': repo};
        let p = getPromise('/filemanager/repository/delete/', data);
        $.when(p).then(function(retObj) {
            getRepos();
            popDialog("Repository '" + repo + "' deleted successfully");
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    /**
     * Delete modules from an existing repo
     */
    function deleteModules(repo, modules) {
        if (!repo) {
            popDialog("Please select the repository to delete modules from.");
            return;
        }
        if (!modules) {
            popDialog("Please select module(s) to delete.");
            return;
        }
        let data = {'repository': repo,
                    'modules': yangsets.moduleStringsToJson(modules)};
        let p = getPromise('/filemanager/repository/deletemodules/', data);
        $.when(p).then(function(retObj) {
            getRepoContents(repo);
            let msg = $("<div>").append($("<div>").text("Request complete."));
            if (retObj.module_errors.length > 0) {
                let errors = $('<div class="text-danger">' +
                               "The following modules errored on deletion:</div>");
                let errorList = $("<ul>");
                $.each(retObj.module_errors, function(i, err) {
                    errorList.append($("<li>")
                                     .text(err[0] + " @ " + err[1] + ": " + err[2]));
                });
                errors.append(errorList);
                msg.append(errors);
            }
            if (retObj.yangset_errors.length > 0) {
                let errors = $('<div class="text-danger">' +
                               "Some modules could not be deleted because they are " +
                               "in use by the following yangsets:</div>");
                let errorList = $("<ul>");
                $.each(retObj.yangset_errors, function(i, err) {
                    let entry = $("<li>").text(err[0]);
                    let modList = $("<ul>");
                    $.each(err[1], function(i, modrev) {
                        modList.append($("<li>").text(modrev));
                    });
                    entry.append(modList);
                    errorList.append(entry);
                });
                errors.append(errorList);
                msg.append(errors);
            }
            popDialog(msg);
            $("#ytool-dialog").dialog("option", "minWidth", "500");
            checkRepo(repo);
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    /**
     * Check the status of the given repo and report it.
     */
    function checkRepo(repo) {
        let data = {'repository': repo};
        let progressBarDiv = startProgress($(c.progress), "/filemanager/repository/check/", data, "Checking repo") || $(c.progress);
        let p = getPromise("/filemanager/repository/check/", data);
        $.when(p).then(function(retObj) {
            reportRepoCheck(retObj.reply);
            stopProgress(progressBarDiv);
        }, function(retObj) {
            stopProgress(progressBarDiv);
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    /**
     * Private helper to checkRepo()
     *
     * Similar to yangsets.reportModuleValidation but simpler - just reports
     * the modules that are missing from this repo.
     */
    function reportRepoCheck(data) {
        $(c.missingModulesList).empty();
        $.each(data, function(i, module) {
            if (!module.found) {
                yangsets.makeAppropriateChild(
                    $(c.missingModulesList),
                    module.name + " @ " + module.revision);
            }
        });

        if ($(c.missingModulesList).children().length > 0) {
            /* At least one missing module */
            $(c.repoStatusContainer).attr("class", "text-danger");
            $(c.repoStatusText).html(
                "<p>It appears that the modules currently in " +
                    "this repository depend on the following " +
                    "missing modules.</p>" +
                    "<p>Please add the missing dependencies or else YANG " +
                    "sets using this repository may be incomplete or invalid." +
                    "</p>");
        } else {
            /* Nothing missing */
            $(c.repoStatusContainer).attr("class", "text-success");
            $(c.repoStatusText).html(
                "<p>It appears that all necessary dependencies of the " +
                    "modules in this repository are present as well.</p>" +
                    "<p>You can add more modules as desired, or you can " +
                    'proceed to <a href="/filemanager/yangsets/manage">' +
                    "define YANG module sets</a> based against this " +
                    "repository.</p>");
        }
    };

    /**
     * Update the window's 'manage' URI and breadcrumbs without reloading the page
     */
    function pushManageState(repository='', reponame='') {
        $("ul.breadcrumb li:not('.breadcrumb-static')").remove();
        let url = "/filemanager/repository/manage/";
        if (repository && !reponame) {
            reponame = repository;
        }
        if (repository) {
            $("ul.breadcrumb").append('<li><a href="' + url + '">' +
                                      'YANG module repositories</a></li>');
            url += repository;
            $("ul.breadcrumb").append($("<li>").text(reponame));
        } else {
            $("ul.breadcrumb").append("<li>YANG module repositories</li>");
        }
        window.history.pushState('', '', url);
    }

    /**
     * Display a dialog summarizing the results of an attempt to add modules.
     * Used by upload(), scp(), git(), etc.
     */
    function reportRepoModificationResults(retObj) {
        let message = $("<div>");
        /* Report each error in depth */
        if (retObj.reply.errors.length > 0) {
            let errdiv = $('<div class="text-danger">Errors were encountered:</div>');
            let errlist = $('<ul class="list-unstyled">');
            for (let err of retObj.reply.errors) {
                /* Each err is a pair of (file_or_dir, message) */
                errlist.append($("<li>")
                               .append($("<em>").text(err[0] + ": "))
                               .append($("<span>").text(err[1])));
            }
            errdiv.append(errlist);
            message.append(errdiv);
        }
        /* Report summary statistics for others */
        let statlist = $('<ul class="list-unstyled">');
        Object.keys(retObj.reply).forEach(function(key, i) {
            if (key != "errors") { // already handled above
                let val = retObj.reply[key].length;
                if (val) {
                    statlist.append("<li>" + val + " module(s) " + key);
                }
            }
        });
        message.append(statlist);
        popDialog(message);
    };

    /* Public API */
    return {
        config:config,
        store:store,
        getRepos:getRepos,
        getRepoContents:getRepoContents,
        createRepo:createRepo,
        deleteRepo:deleteRepo,
        deleteModules:deleteModules,
        checkRepo:checkRepo,
        pushManageState:pushManageState,
        reportRepoModificationResults:reportRepoModificationResults,
    };
}();
