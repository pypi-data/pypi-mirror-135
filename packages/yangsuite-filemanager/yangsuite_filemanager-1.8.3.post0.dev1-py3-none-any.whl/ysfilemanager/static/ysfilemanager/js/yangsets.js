/**
 * Module for managing and validating YANG module sets.
 */
let yangsets = function() {
    /**
     * Default configuration of this module.
     */
    let config = {
        yangsetsSelect: 'select#ys-yangsets',

        successMsg: "#ys-validation-success",
        successSection: ".ys-validation-success-section",
        yangsetMods: '#ys-yangset-contents',
        yangsetModsSection: ".ys-yangset-contents-section",
        missingMods: '#ys-missing-dependencies',
        missingModsSection: ".ys-missing-dependencies-section",
        identityDerivingMods: '#ys-identity-deriving-modules-list',
        identityDerivingModsSection: '.ys-identity-deriving-modules-section',
        augmentingMods: '#ys-augmenting-modules-list',
        augmentingModsSection: '.ys-augmenting-modules-section',
        upstreamMods: "#ys-upstream-modules-list",
        upstreamModsSection: ".ys-upstream-modules-section",
        relatedMods: "#ys-related-modules-list",
        relatedModsSection: ".ys-related-modules-section",

        /* URL prefixs for various operations */
        urlPrefix: "/filemanager/yangsets/",

        accordion: '.accordion',

        progress: 'div#ys-progress',
    };

    let c = config;   // internal alias for brevity

    let store = {
        /* List of 'name,rev' strings for the current yangset */
        yangsetModules: [],
        /* Flag indicating 'readiness' of yangsetModules */
        yangsetModulesReady: false,
        /* Last set of modules selected in any given element. */
        lastSelection: {},
        /* How many things are updating the results section? */
        updatingResultsDisplay: 0,
    };

    /**
     * Get the list of existing yangsets and populate the yangsetsSelect menu.
     */
    function getYangSets(selection="", readOnly=true) {
        let menu = $(c.yangsetsSelect);
        menu.empty();
        return $.ajax({
            url: c.urlPrefix + "list/",
            type: 'GET',
            data: {readonly: readOnly},
            dataType: 'json',
            success: function(retObj) {
                /* Always have a 'none of the below' option */
                menu.append('<option value=""></option>');
                /*
                 * Expected format is {'user': [{data}, {data},], 'user2': ...}
                 * If we have more than one user, group the sets by username.
                 */
                let optgroups = false;
                if (Object.keys(retObj.yangsets).length > 1) {
                    optgroups = true;
                }

                let selectionFound = false;
                $.each(retObj.yangsets, function(username, sets) {
                    let target = menu;
                    if (optgroups) {
                        menu.append('<optgroup label="' + username + '">' +
                                    '</optgroup>');
                        target = menu.children("optgroup:last-child");
                    }
                    $.each(sets, function(i, data) {
                        if (data['slug'] == selection) {
                            selectionFound = true;
                        }
                        makeAppropriateChild(target,
                                             data['slug'], data['name']);
                    });
                });
                if (selection && selectionFound) {
                    menu.val(selection);
                }
                menu.trigger("change");
                menu.children('option[value=""]').prop("disabled", true);
            }
        });
    };

    /**
     * Get the list of modules contained in the given yangset and update
     * store.yangsetModules and store.yangsetModulesReady with the results.
     * Returns the deferred object for method chaining purposes.
     */
    function getYangSetContents(yangset) {
        if (!yangset) {
            popDialog("Please specify a YANG set to retrieve.");
            return;
        }
        let progressBarDiv = startProgress($(c.progress)) || $(c.progress);
        store.yangsetModules = [];
        store.yangsetModulesReady = false;
        let data = {'yangset': yangset};
        return $.ajax({
            url: c.urlPrefix + 'get/',
            type: 'GET',
            data: data,
            dataType: 'json'})
            .done(function(retObj) {
                store.yangsetModules = [];
                $.each(retObj.modules, function(i, module) {
                    entry = moduleNameRevToValueText(module);
                    store.yangsetModules.push(entry.value);
                });
                store.yangsetModulesReady = true;
                stopProgress(progressBarDiv);
            })
            .fail(function(retObj) {
                stopProgress(progressBarDiv);
                popDialog("Error " + retObj.status + ": " + retObj.statusText);
            });
    };

    /**
     * Create a new, empty YANG set, or clone an existing one
     *
     * @param {string} setname  New YANG set name
     * @param {string} repository Repository slug
     * @param {string} source Slug for YANG set, if any, to clone
     */
    function createYangSet(setname, repository, source='') {
        var letters = /[a-zA-Z]|[a-zA-Z]+[0-9]+$/;
        var specials = /^\W|_/g;
        if (!setname || !repository) {
            popDialog("Please enter a YANG set name and select its " +
                      "associated repository");
            return;
        }

        if (!setname.match(letters) || setname.match(specials)) {
            popDialog("<b>YANG set name is not valid.</b> </br>" +
                      "<b>Make sure:</b> </br> " +
                      "<ul><li>It should have atleast one character.</li>" +
                      "<li>It should not start with any " +
                      "special character.</li></ul>")
            return;
        }

        let data = {
            'setname': setname,
            'repository': repository,
            'source': source,
        };
        return getPromise(c.urlPrefix + 'create/', data)
            .done(function(retObj) {
                getYangSets(retObj.slug);
            })
            .fail(function(retObj) {
                popDialog("Error " + retObj.status + ": " + retObj.statusText);
            });
    };

    /**
     * Update the module list and/or repository association
     * of the selected yangset.
     *
     * @param {string} yangset YANG set slug
     * @param {string} repository Repository slug
     * @param {list} modules List of 'name,revision' strings,
     * or undefined, if no change
     * @param {string} operation Handling of module listing - 'add' or 'replace'
     */
    function updateYangSet(yangset, repository, modules=undefined,
                           operation='replace') {
        if (yangset == "") {
            popDialog("Please specify a YANG set to update.");
            return;
        }
        /* Mandatory params */
        let data = {yangset: yangset, operation: operation, repository: repository};
        /* Optional params */
        if (modules !== undefined) {
            data['modules'] = moduleStringsToJson(modules);
        }
        return getPromise(c.urlPrefix + 'update/', data)
            .then(function() {
                return $.when(
                    checkYangSet(yangset, true),
                    getRelatedModules(yangset, repository),
                );
            }, function(retObj) {
                let msg = $("<div>").text("Error " + retObj.status + ": " + retObj.statusText);
                data = $.parseJSON(retObj.responseText);
                if (data.details) {
                    let details = $("<ul>");
                    $.each(data.details, function(i, detail) {
                        details.append($("<li>").text(detail));
                    })
                    msg.append(details);
                }
                popDialog(msg);
            });
    };

    /**
     * Delete the specified YANG set and refresh the yangsetsSelect menu.
     *
     * @param {string} yangset YANG set slug
     */
    function deleteYangSet(yangset) {
        let data = {'yangset': yangset};

        let p = getPromise(c.urlPrefix + "delete/", data);
        $.when(p).then(function(retObj) {
            getYangSets();
            popDialog(retObj.reply);
        });
    };

    var lastCheckWasQuick = null;

    /**
     * Validate the specified yang set.
     *
     * @param {string} yangset YANG set slug
     * @param {boolean} quick Validate quickly or thoroughly?
     */
    function checkYangSet(yangset, quick=false) {
        if (yangset == "") {
            return;
        }
        let progressBarDiv = startProgress($(c.progress), c.urlPrefix + "validate/") || $(c.progress);
        store.updatingResultsDisplay += 1;
        $(c.yangsetMods).empty();
        $(c.missingMods).empty();
        let p = getPromise(c.urlPrefix + "validate/",
                           {'yangset': yangset, quick: quick});
        return $.when(p).then(function(retObj) {
            stopProgress(progressBarDiv);
            store.updatingResultsDisplay -= 1;
            lastCheckWasQuick = quick;
            reportModuleValidation(retObj.reply);
        }, function(retObj) {
            stopProgress(progressBarDiv);
            store.updatingResultsDisplay -= 1;
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    /**
     * Render module validation results.
     *
     * @param {list} data List of objects with keys 'name', 'revision',
     * 'usable', 'in_yangset', 'found', 'errors', 'warnings'.
     *
     * - Entries that are 'in_yangset' and 'found' will be rendered under
     *   config.yangsetMods if set
     * - Entries that are not 'in_yangset' will be rendered under
     *   config.missingMods if set
     */
    function reportModuleValidation(data) {
        $(c.yangsetMods).empty();
        $(c.missingMods).empty();
        /* Render individual results */
        $.each(data, function(i, obj) {
            reportOneModule(obj);
        });

        updateResultsDisplay();
    };

    /**
     * Private helper function - refresh and toggle visibility of the various
     * 'results' sections of the page.
     */
    function updateResultsDisplay() {
        let active = false;
        $(c.successSection).show();
        $(c.missingModsSection).show();
        $(c.yangsetModsSection).show();
        $(c.identityDerivingModsSection).show();
        $(c.augmentingModsSection).show();
        $(c.upstreamModsSection).show();
        $(c.relatedModsSection).show();
        if ($(c.accordion).accordion('instance')) {
            active = $(c.accordion).accordion("option", "active");
            $(c.accordion).accordion('refresh');
        } else {
            $(c.accordion).accordion({heightStyle: 'content', collapsible: true});
        }

        let numMissing = $(c.missingMods).children().length;
        if (numMissing == 0) {
            $(c.missingModsSection).hide();
        }

        let numMods = $(c.yangsetMods).children().length;
        if (numMods == 0) {
            $(c.yangsetModsSection).hide();
        }

        let numIdentityDerivers = $(c.identityDerivingMods).children().length;
        if (numIdentityDerivers == 0) {
            $(c.identityDerivingModsSection).hide();
        }

        let numAugmenters = $(c.augmentingMods).children().length;
        if (numAugmenters == 0) {
            $(c.augmentingModsSection).hide();
        }

        let numUpstream = $(c.upstreamMods).children().length;
        if (numUpstream == 0) {
            $(c.upstreamModsSection).hide();
        }

        let numRelated = $(c.relatedMods).children().length;
        if (numRelated == 0) {
            $(c.relatedModsSection).hide();
        }

        if (numMods > 0 || numMissing > 0) {
            $(c.successSection).hide();
        } else if (store.yangsetModules.length == 0) {
            $(c.successMsg)
                .html("<p>This YANG set is currently empty.</p>" +
                      "<p>Please add one or more YANG modules to this set.</p>");
        } else {
            if (lastCheckWasQuick) {
                $(c.successMsg).html(
                    "<p>Initial <q>quick</q> validation of this " +
                        " YANG set was successful, with no errors found.</p>" +
                        "<p>You may now wish to request a more in-depth " +
                        "validation of the various modules in this set.</p>");
            } else {
                $(c.successMsg).html(
                    "<p>This YANG set and its modules have fully passed " +
                        "in-depth validation. You're good to go!</p>");
            }
            if (numIdentityDerivers > 0 || numAugmenters > 0) {
                $(c.successMsg).append(
                    "<p>Please review the additional module(s) " +
                        "suggested below to ensure your YANG set contains " +
                        "any desired additional capabilities.</p>");
            } else if (numUpstream > 0 || numRelated > 0) {
                $(c.successMsg).append(
                    "<p>You may want to consider adding any additional " +
                        "module(s) suggested below, but doing so is " +
                        "entirely optional.</p>");
            }
        }

        /* Only refresh active selection if we're not in mid-update */
        if (active != false && store.updatingResultsDisplay == 0) {
            if (!$($(c.accordion).find('h3')[active]).is(":visible")) {
                active = false;
            }
        }
        if (active == false) {
            // Make the first visible section active
            first_visible = $(c.accordion).find('h3:visible:first')[0];
            active = $(c.accordion).find('h3').index(first_visible);
        }

        $(".accordion").accordion("option", "active", active);

    };

    /**
     * Private helper function to reportModuleValidation. Render one result.
     *
     * - Entries that are 'in_yangset' and 'found' will be rendered under
     *   config.yangsetMods if set
     * - Entries that are not 'in_yangset' will be rendered under
     *   config.missingMods if set
     *
     * @param {object} obj object with keys 'name', 'revision',
     * 'usable', 'in_yangset', 'found', 'errors', 'warnings'.
     */
    function reportOneModule(obj) {
        if (obj.in_yangset == false) {
            // in_yangset undefined implies in_yangset==true
            let entry = moduleNameRevToValueText(obj, "(any revision)");
            let text = entry.text;
            let val = entry.value;
            makeAppropriateChild($(c.missingMods), val, text);
            return;
        }
        let entry = moduleNameRevToValueText(obj);
        let text = entry.text;
        let val = entry.value;
        /* else, need to report more... */
        let warnerrors = 0;
        let modnamelink = ('<a href="/filemanager/yangsets/show/' +
                           $(c.yangsetsSelect).val() + '/module/' +
                           text.split(" ")[0] + '" target="_blank">' + text + '</a>');
        let icon = $('<span>');
        if (!obj.usable) {
            icon.addClass('icon-error');
            icon.addClass('result-error');
            warnerrors += 1;
        }
        if (Array.isArray(obj.errors)) {
            if (warnerrors == 0 && obj.errors.length > 0) {
                icon.addClass('icon-exclamation-triangle');
                icon.addClass('result-error');
            }
            warnerrors += obj.errors.length;
        }
        if (Array.isArray(obj.warnings)) {
            if (warnerrors == 0 && obj.warnings.length > 0) {
                icon.addClass('icon-exclamation-circle');
                icon.addClass('result-warning');
            }
            warnerrors += obj.warnings.length;
        }
        if (warnerrors == 0) {
            //Don't report success, it just takes up space
            return;
        }
        // We report errors/warnings as a sub-list under the element
        let errorList = $("<ul>");
        if (!obj.usable && warnerrors == 1) {
            // Not usable but no specific error given
            errorList.append('<li class="result-error">unknown error</li>');
        }
        if (Array.isArray(obj.errors)) {
            $.each(obj.errors, function(i, err) {
                errorList.append($('<li class="result-error">').text(err));
            });
        }
        if (Array.isArray(obj.warnings)) {
            $.each(obj.warnings, function(i, warn) {
                errorList.append($('<li class="result-warning">').text(warn));
            });
        }
        if (c.yangsetMods) {
            let entry = makeAppropriateChild($(c.yangsetMods), val, text);
            entry.html(modnamelink).append("&nbsp;").append(icon).append(errorList);
        }
    };

    /**
     * Get a list of modules that are related to or 'upstream' from
     * this yangset but not currently part of it, and display this information.
     *
     * @param {string} yangset YANG set slug
     * @param {string} repository Repository slug
     */
    function getRelatedModules(yangset, repository) {
        if (yangset == "") {
            return;
        }
        store.updatingResultsDisplay += 1;
        c.identityDerivingMods && $(c.identityDerivingMods).empty();
        c.augmentingMods && $(c.augmentingMods).empty();
        c.upstreamMods && $(c.upstreamMods).empty();
        c.relatedMods && $(c.relatedMods).empty();
        return $.ajax({
            url: c.urlPrefix + 'getrelated/',
            type: 'GET',
            data: {'yangset': yangset},
            datatype: 'json',
            success: function(data) {
                /* Given "module @ revision", get the href to view this from the repo */
                function hrefForText(text) {
                    return ("/filemanager/repository/show/" + repository + "/module/" +
                            text.split(' ')[0]);
                };

                if (data.hasOwnProperty("identity_deriving_modules") &&
                    data.identity_deriving_modules.length > 0) {
                    for (let module of data.identity_deriving_modules) {
                        let entry = moduleNameRevToValueText(module);
                        makeAppropriateChild($(c.identityDerivingMods),
                                             entry.value, entry.text,
                                             hrefForText(entry.text));
                    }
                }

                if (data.hasOwnProperty("augmenter_modules") &&
                    data.augmenter_modules.length > 0) {
                    $.each(data.augmenter_modules, function(i, module) {
                        let entry = moduleNameRevToValueText(module);
                        makeAppropriateChild($(c.augmentingMods),
                                             entry.value, entry.text,
                                             hrefForText(entry.text));
                    });
                }

                if (data.hasOwnProperty("upstream_modules") &&
                    data.upstream_modules.length > 0) {
                    $.each(data.upstream_modules, function(i, module) {
                        let entry = moduleNameRevToValueText(module);
                        makeAppropriateChild($(c.upstreamMods),
                                             entry.value, entry.text,
                                             hrefForText(entry.text));
                    });
                }

                if (data.hasOwnProperty("related_modules") &&
                    data.related_modules.length > 0) {
                    $.each(data.related_modules, function(i, module) {
                        let entry = moduleNameRevToValueText(module);
                        makeAppropriateChild($(c.relatedMods),
                                             entry.value, entry.text,
                                             hrefForText(entry.text));
                    });
                }

                store.updatingResultsDisplay -= 1;
                updateResultsDisplay();
            },
            error: function(retObj) {
                store.updatingResultsDisplay -= 1;
                popDialog("Error " + retObj.status + ": " + retObj.statusText);
            }
        });
    };

    /**
     * Given a module {'name': 'foo', 'revision': 'bar'}, return
     * {value: 'foo,bar', text='foo @ bar'}
     */
    function moduleNameRevToValueText(module, unknown_rev="unknown") {
        const name = module.name;
        const rev = module.revision;
        const value = name + ',' + rev;
        const text = name + ' @ ' + (rev != "unknown" ? rev : unknown_rev);
        return {'value': value, 'text': text};
    };

    /**
     * Create the appropriate child element of the given parent(s).
     * select -> option, ul -> li, ol -> li, etc.
     */
    function makeAppropriateChild(parent, value, text='', href=null) {
        if (!parent || parent.length < 1) {
            return;
        }
        const pt = parent.prop("tagName").toLowerCase();
        if (pt == 'select' || pt == 'optgroup') {
            ct = 'option';
        } else if (pt == 'ul' || pt == 'ol') {
            ct = 'li';
            if (!text) {
                text = value;
            }
        } else {
            ct = 'p';
        }

        child = $('<' + ct + '>').appendTo(parent);
        if (ct == 'option') {
            child.prop('value', value);
        }
        child.attr('data-value', value);
        if (href) {
            child.append($('<a href="' + href + '" target="_blank">').text(text));
        } else {
            child.text(text);
        }
        return child;
    }

    /**
     * Map list of 'name,rev' strings to JSON [["name", "rev"], ["name", "rev"]]
     */
    function moduleStringsToJson(schemaList) {
        let result = [];
        if (schemaList) {
            $.each(schemaList, function(i, val) {
                let modrev = val.split(",");
                result.push(modrev);
            });
        }
        return JSON.stringify(result);
    };

    /**
     * Don't allow the user to select multiple revisions of the same module for
     * inclusion into a yangset.
     * 1) If the user selects a revision while other revision(s) previously
     * selected, deselect the other(s).
     * 2) If the user selects multiple revisions simultaneously (e.g.,
     * shift-click), leave only the newest such revision selected.
     */
    function onlyOneRevisionPerModule(select) {
        let selid = select.attr("id");
        const selections = select.val();

        /* delta is the set of *new* selection entries just selected. */
        let delta = selections;
        if (store.lastSelection[selid] != null) {
            delta = $(delta).not(store.lastSelection[selid]).get();
        }

        already_processed = {};

        /*
         * Within the modules affected by delta, do we now have any modules
         * that have multiple revisions selected?
         */
        $.each(delta, function(i, selection) {
            sel = selection.split(',');
            const mod = sel[0];
            /*
             * Only handle each module name once even if there are multiple
             * revisions of this module in delta
             */
            if (already_processed[mod]) {
                $.continue;
            }
            /* Get all selected options with this mod and any revision */
            const modselected = select.children(':selected' +
                                                '[value^="' + mod + ',"]');
            if (modselected.length > 1) {
                /*
                 * We now have multiple selections for this module.
                 * Fix this.
                 */
                deltaValue = null;
                $.each(delta, function(i, deltaItem) {
                    /*
                     * Get the value in delta that we want to keep selected.
                     * We don't break after a match is found, because if there
                     * are multiple revisions of this module in delta, we want
                     * the last (newest) such revision.
                     */
                    if (deltaItem.split(',')[0] == mod) {
                        deltaValue = deltaItem;
                    }
                });
                /* Deselect all */
                modselected.removeAttr("selected");
                /* (Re)select our preferred item */
                select.children('[value="' + deltaValue + '"]')
                    .prop("selected", "selected");
            }

            already_processed[mod] = true;
        });

        store.lastSelection[selid] = select.val();
    };

    /**
     * Update the window's 'manage' URI and breadcrumbs without reloading the page
     */
    function pushManageState(yangset='', yangsetname='') {
        $("ul.breadcrumb li:not('.breadcrumb-static')").remove();
        let url = c.urlPrefix + "manage/";
        if (yangset) {
            $("ul.breadcrumb").append('<li><a href="' + url + '">' +
                                      'YANG module sets</a></li>');
            url += yangset + "/";
            $("ul.breadcrumb").append($("<li>").text(yangsetname));
        } else {
            $("ul.breadcrumb").append('<li>YANG module sets</li>');
        }
        window.history.pushState('', '', url);
    }

    /* Public API */
    return {
        config:config,
        store:store,
        getYangSets:getYangSets,
        getYangSetContents:getYangSetContents,
        createYangSet:createYangSet,
        updateYangSet:updateYangSet,
        deleteYangSet:deleteYangSet,
        checkYangSet:checkYangSet,
        reportModuleValidation:reportModuleValidation,
        getRelatedModules:getRelatedModules,
        makeAppropriateChild:makeAppropriateChild,
        moduleNameRevToValueText:moduleNameRevToValueText,
        moduleStringsToJson:moduleStringsToJson,
        onlyOneRevisionPerModule:onlyOneRevisionPerModule,
        pushManageState:pushManageState,
    };
}();
