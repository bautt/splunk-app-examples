
// Copyright 2011 Splunk, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License"): you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

// This example will login to Splunk, and create a saved search.

let splunkjs = require('splunk-sdk');

exports.main = function (opts, done) {
    // This is just for testing - ignore it
    opts = opts || {};

    let username = opts.username    || "admin";
    let password = opts.password    || "changed!";
    let scheme   = opts.scheme      || "https";
    let host     = opts.host        || "localhost";
    let port     = opts.port        || "8089";
    let version  = opts.version     || "default";

    let service = new splunkjs.Service({
        username: username,
        password: password,
        scheme: scheme,
        host: host,
        port: port,
        version: version
    });

    // First, we log in
    service.login(function (err, success) {
        // We check for both errors in the connection as well
        // as if the login itself failed.
        if (err || !success) {
            console.log("Error in logging in");
            done(err || "Login failed");
            return;
        }

        let savedSearchOptions = {
            name: "My Awesome Saved Search",
            search: "index=_internal error sourcetype=splunkd* | head 10"
        };

        // Now that we're logged in, Let's create a saved search
        service.savedSearches().create(savedSearchOptions, function (err, savedSearch) {
            if (err && err.status === 409) {
                console.error("ERROR: A saved search with the name '" + savedSearchOptions.name + "' already exists");
                done();
                return;
            }
            else if (err) {
                console.error("There was an error creating the saved search:", err);
                done(err);
                return;
            }

            console.log("Created saved search: " + savedSearch.name);
            done();
        });
    });
};

if (module === require.main) {
    exports.main({}, function () { /* Empty function */ });
}
