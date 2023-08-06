/**
 * Module for reporting and requesting updates to installed YANG Suite plugins.
 */
let plugins = function() {
    /**
     * Default configuration of this module.
     */
    let config = {
        corePluginTable: 'table tbody#core-plugins',
        extraPluginTable: 'table tbody#extra-plugins',
        availablePluginTable: 'table tbody#available-plugins',

        anyPluginTable: 'table tbody#core-plugins, table tbody#extra-plugins, table tbody#available-plugins',
    };

    let c = config;    // internal alias for brevity

    function tableForPackage(packageName) {
        let corePlugins = [
            'yangsuite',
            'yangsuite-filemanager',
            'yangsuite-devices',
            'yangsuite-yangtree',
        ];
        if (corePlugins.includes(packageName)) {
            return $(c.corePluginTable);
        } else {
            return $(c.extraPluginTable);
        }
    };

    /**
     * Get the plugin list from the server and update the pluginTable.
     */
    function listPlugins() {
        return $.ajax({
            url: "/yangsuite/plugins/list",
            type: 'GET',
            datatype: 'json',
            success: function(retObj) {
                let plugin_error = false;
                $(c.anyPluginTable).empty();
                for (let e of retObj.plugins) {
                    let tbody = tableForPackage(e.package_name);
                    let tr = $('<tr data-value="' + e.package_name + '">' +
                               '<td colspan="2"><code>' + e.package_name + '</code></td>' +
                               '<td class="description">' + e.verbose_name +
                               '</td><td class="plugin-installed-cell">' +
                               "<code>" + e.installed_version + "</code>" +
                               '</td><td class="plugin-latest-cell">' +
                               "</td></tr>");
                    if (e.error_message) {
                        tr.addClass("danger");
                        tr.find("td.description").html(
                            $(" <strong>").text(e.error_message));
                        plugin_error = true;
                    }
                    tbody.append(tr);
                }
                if (plugin_error) {
                    popDialog("Some plugins failed to load. Please review " +
                              "any errors shown here and report them to an " +
                              "administrator as appropriate.");
                }
            }
        });
    };

    /**
     * Check whether the plugins are up-to-date and update the pluginTable.
     */
    function checkPlugins() {
        $(c.anyPluginTable).find(".plugin-latest-cell").html("Checking&hellip;");
        let pb = startProgress($("#ys-progress"), "", "", "Checking plugins...");
        return $.ajax({
            url: "/yangsuite/plugins/check_versions",
            type: 'GET',
            datatype: 'json',
            success: function(retObj) {
                stopProgress(pb);
                $(c.anyPluginTable).find("tr").each(function() {
                    let latestCell = $(this).find(".plugin-latest-cell");
                    latestCell.html("None known");
                });

                for (let entry of retObj.apps) {
                    let pkgName = entry['package_name'];
                    let tr = $(c.anyPluginTable).find('tr[data-value="' +
                                                      pkgName + '"]');
                    let pkgLatestVersion = entry['latest_version'];
                    if (tr.length > 0) {
                        /* This plugin is installed */
                        let latestCell = tr.find(".plugin-latest-cell");
                        if (pkgLatestVersion) {
                            latestCell.html("<code>" + pkgLatestVersion + "</code>");
                            let installedCell = tr.find(".plugin-installed-cell");
                            if (latestCell.text().trim() != installedCell.text().trim()) {
                                tr.addClass("warning");
                            }
                            tr.attr('data-latest-version', pkgLatestVersion);
                        }
                    } else {
                        /* This plugin is not installed - add it to the available list */
                        tr = $('<tr data-value="' + pkgName + '">' +
                               '<td><input type="radio" name="selection" id="' +
                               entry.package_name + '" data-latest-version="' +
                               pkgLatestVersion + '"></td>' +
                               '<td><code>' + entry.package_name + '</code></td>' +
                               '<td class="description" colspan="2">' +
                               entry.description + '</td>' +
                               '<td class="plugin-latest-cell"><code>' +
                               pkgLatestVersion + '</code></td></tr>');
                        $(c.availablePluginTable).append(tr);
                    }
                };
            }
        });
    };

    /**
     * Install a new plugin
     */
    function installPlugin() {
        let selection = $(c.anyPluginTable).find("input:checked").toArray();
        if (selection.length == 0) {
            popDialog("No plugins selected");
            return;
        }
        let data = [];
        for (let input of selection) {
            data.push({plugin: input.getAttribute('id'),
                       version: input.getAttribute("data-latest-version")});
        }
        installUpdatePlugins(data);
    }

    /**
     * Update all installed plugins to their latest value
     */
    function updatePlugins() {
        let data = [];
        let developmentVersionInstalled = false;
        $(c.corePluginTable + ", " + c.extraPluginTable).find("tr").each(function() {
            let latestVersion = $(this).attr('data-latest-version');
            if (latestVersion) {
                let installedVersion = $(this).find(".plugin-installed-cell code").text();
                if (installedVersion == latestVersion) {
                    return;
                }
                if (installedVersion.includes('dev')) {
                    developmentVersionInstalled = true;
                }
                data.push({plugin: $(this).attr('data-value'),
                           version: latestVersion});
            }
        });

        if (developmentVersionInstalled) {
            if (!confirm("You have development/pre-release versions " +
                         "of some plugins installed. Continuing will replace " +
                         "these with the latest released versions. " +
                         "Continue anyway?")) {
                return;
            }
        }
        installUpdatePlugins(data);
    }

    /**
     * Helper to installPlugin and updatePlugins()
     */
    function installUpdatePlugins(data) {
        $("#ys-progress").progressbar({value: false});
        let p = getPromise("/yangsuite/plugins/update", {plugins: JSON.stringify(data)});
        return $.when(p).then(function(retObj) {
            $("#ys-progress").progressbar("destroy");
            let list = $('<ul class="list-unstyled">');
            let anyUpdated = false;
            for (plugin of Object.keys(retObj.result.plugins)) {
                let result = retObj.result.plugins[plugin];
                if (result == 'updated') {
                    list.append($("<li>" + plugin + " updated successfully</li>"));
                    anyUpdated = true;
                } else if (result == 'unchanged') {
                    list.append($("<li>" + plugin + " not updated - no update available? </li>"));
                } else {
                    list.append($("<li>" + plugin + " update result: " + result + "</li>"));
                }
            }
            let msg = $("<div>").text(retObj.result.message);
            msg.prepend(list);
            popDialog(msg);
            if (anyUpdated) {
                /*
                 * Server will restart after plugin update -
                 * give it a few seconds before we query it again
                 */
                setTimeout(function() { listPlugins().done(checkPlugins) },
                           5000);
            }
        }, function() {
            /*
             * 'Failure' here probably means the server updated the plugin
             * successfully then restarted before sending our response.
             * Treat this as a successful update, and re-query after a few secs.
             */
            $("#ys-progress").progressbar("destroy");
            setTimeout(function() { listPlugins().done(checkPlugins) }, 5000);
        });
    };

    /* Public API */
    return {
        config:config,
        listPlugins:listPlugins,
        checkPlugins:checkPlugins,
        installPlugin:installPlugin,
        updatePlugins:updatePlugins,
    };
}();
