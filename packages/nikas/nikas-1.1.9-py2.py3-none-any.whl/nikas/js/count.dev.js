(function () {
/**
 * @license almond 0.3.3 Copyright jQuery Foundation and other contributors.
 * Released under MIT license, http://github.com/requirejs/almond/LICENSE
 */
//Going sloppy to avoid 'use strict' string cost, but strict practices should
//be followed.
/*global setTimeout: false */

var requirejs, require, define;
(function (undef) {
    var main, req, makeMap, handlers,
        defined = {},
        waiting = {},
        config = {},
        defining = {},
        hasOwn = Object.prototype.hasOwnProperty,
        aps = [].slice,
        jsSuffixRegExp = /\.js$/;

    function hasProp(obj, prop) {
        return hasOwn.call(obj, prop);
    }

    /**
     * Given a relative module name, like ./something, normalize it to
     * a real name that can be mapped to a path.
     * @param {String} name the relative name
     * @param {String} baseName a real name that the name arg is relative
     * to.
     * @returns {String} normalized name
     */
    function normalize(name, baseName) {
        var nameParts, nameSegment, mapValue, foundMap, lastIndex,
            foundI, foundStarMap, starI, i, j, part, normalizedBaseParts,
            baseParts = baseName && baseName.split("/"),
            map = config.map,
            starMap = (map && map['*']) || {};

        //Adjust any relative paths.
        if (name) {
            name = name.split('/');
            lastIndex = name.length - 1;

            // If wanting node ID compatibility, strip .js from end
            // of IDs. Have to do this here, and not in nameToUrl
            // because node allows either .js or non .js to map
            // to same file.
            if (config.nodeIdCompat && jsSuffixRegExp.test(name[lastIndex])) {
                name[lastIndex] = name[lastIndex].replace(jsSuffixRegExp, '');
            }

            // Starts with a '.' so need the baseName
            if (name[0].charAt(0) === '.' && baseParts) {
                //Convert baseName to array, and lop off the last part,
                //so that . matches that 'directory' and not name of the baseName's
                //module. For instance, baseName of 'one/two/three', maps to
                //'one/two/three.js', but we want the directory, 'one/two' for
                //this normalization.
                normalizedBaseParts = baseParts.slice(0, baseParts.length - 1);
                name = normalizedBaseParts.concat(name);
            }

            //start trimDots
            for (i = 0; i < name.length; i++) {
                part = name[i];
                if (part === '.') {
                    name.splice(i, 1);
                    i -= 1;
                } else if (part === '..') {
                    // If at the start, or previous value is still ..,
                    // keep them so that when converted to a path it may
                    // still work when converted to a path, even though
                    // as an ID it is less than ideal. In larger point
                    // releases, may be better to just kick out an error.
                    if (i === 0 || (i === 1 && name[2] === '..') || name[i - 1] === '..') {
                        continue;
                    } else if (i > 0) {
                        name.splice(i - 1, 2);
                        i -= 2;
                    }
                }
            }
            //end trimDots

            name = name.join('/');
        }

        //Apply map config if available.
        if ((baseParts || starMap) && map) {
            nameParts = name.split('/');

            for (i = nameParts.length; i > 0; i -= 1) {
                nameSegment = nameParts.slice(0, i).join("/");

                if (baseParts) {
                    //Find the longest baseName segment match in the config.
                    //So, do joins on the biggest to smallest lengths of baseParts.
                    for (j = baseParts.length; j > 0; j -= 1) {
                        mapValue = map[baseParts.slice(0, j).join('/')];

                        //baseName segment has  config, find if it has one for
                        //this name.
                        if (mapValue) {
                            mapValue = mapValue[nameSegment];
                            if (mapValue) {
                                //Match, update name to the new value.
                                foundMap = mapValue;
                                foundI = i;
                                break;
                            }
                        }
                    }
                }

                if (foundMap) {
                    break;
                }

                //Check for a star map match, but just hold on to it,
                //if there is a shorter segment match later in a matching
                //config, then favor over this star map.
                if (!foundStarMap && starMap && starMap[nameSegment]) {
                    foundStarMap = starMap[nameSegment];
                    starI = i;
                }
            }

            if (!foundMap && foundStarMap) {
                foundMap = foundStarMap;
                foundI = starI;
            }

            if (foundMap) {
                nameParts.splice(0, foundI, foundMap);
                name = nameParts.join('/');
            }
        }

        return name;
    }

    function makeRequire(relName, forceSync) {
        return function () {
            //A version of a require function that passes a moduleName
            //value for items that may need to
            //look up paths relative to the moduleName
            var args = aps.call(arguments, 0);

            //If first arg is not require('string'), and there is only
            //one arg, it is the array form without a callback. Insert
            //a null so that the following concat is correct.
            if (typeof args[0] !== 'string' && args.length === 1) {
                args.push(null);
            }
            return req.apply(undef, args.concat([relName, forceSync]));
        };
    }

    function makeNormalize(relName) {
        return function (name) {
            return normalize(name, relName);
        };
    }

    function makeLoad(depName) {
        return function (value) {
            defined[depName] = value;
        };
    }

    function callDep(name) {
        if (hasProp(waiting, name)) {
            var args = waiting[name];
            delete waiting[name];
            defining[name] = true;
            main.apply(undef, args);
        }

        if (!hasProp(defined, name) && !hasProp(defining, name)) {
            throw new Error('No ' + name);
        }
        return defined[name];
    }

    //Turns a plugin!resource to [plugin, resource]
    //with the plugin being undefined if the name
    //did not have a plugin prefix.
    function splitPrefix(name) {
        var prefix,
            index = name ? name.indexOf('!') : -1;
        if (index > -1) {
            prefix = name.substring(0, index);
            name = name.substring(index + 1, name.length);
        }
        return [prefix, name];
    }

    //Creates a parts array for a relName where first part is plugin ID,
    //second part is resource ID. Assumes relName has already been normalized.
    function makeRelParts(relName) {
        return relName ? splitPrefix(relName) : [];
    }

    /**
     * Makes a name map, normalizing the name, and using a plugin
     * for normalization if necessary. Grabs a ref to plugin
     * too, as an optimization.
     */
    makeMap = function (name, relParts) {
        var plugin,
            parts = splitPrefix(name),
            prefix = parts[0],
            relResourceName = relParts[1];

        name = parts[1];

        if (prefix) {
            prefix = normalize(prefix, relResourceName);
            plugin = callDep(prefix);
        }

        //Normalize according
        if (prefix) {
            if (plugin && plugin.normalize) {
                name = plugin.normalize(name, makeNormalize(relResourceName));
            } else {
                name = normalize(name, relResourceName);
            }
        } else {
            name = normalize(name, relResourceName);
            parts = splitPrefix(name);
            prefix = parts[0];
            name = parts[1];
            if (prefix) {
                plugin = callDep(prefix);
            }
        }

        //Using ridiculous property names for space reasons
        return {
            f: prefix ? prefix + '!' + name : name, //fullName
            n: name,
            pr: prefix,
            p: plugin
        };
    };

    function makeConfig(name) {
        return function () {
            return (config && config.config && config.config[name]) || {};
        };
    }

    handlers = {
        require: function (name) {
            return makeRequire(name);
        },
        exports: function (name) {
            var e = defined[name];
            if (typeof e !== 'undefined') {
                return e;
            } else {
                return (defined[name] = {});
            }
        },
        module: function (name) {
            return {
                id: name,
                uri: '',
                exports: defined[name],
                config: makeConfig(name)
            };
        }
    };

    main = function (name, deps, callback, relName) {
        var cjsModule, depName, ret, map, i, relParts,
            args = [],
            callbackType = typeof callback,
            usingExports;

        //Use name if no relName
        relName = relName || name;
        relParts = makeRelParts(relName);

        //Call the callback to define the module, if necessary.
        if (callbackType === 'undefined' || callbackType === 'function') {
            //Pull out the defined dependencies and pass the ordered
            //values to the callback.
            //Default to [require, exports, module] if no deps
            deps = !deps.length && callback.length ? ['require', 'exports', 'module'] : deps;
            for (i = 0; i < deps.length; i += 1) {
                map = makeMap(deps[i], relParts);
                depName = map.f;

                //Fast path CommonJS standard dependencies.
                if (depName === "require") {
                    args[i] = handlers.require(name);
                } else if (depName === "exports") {
                    //CommonJS module spec 1.1
                    args[i] = handlers.exports(name);
                    usingExports = true;
                } else if (depName === "module") {
                    //CommonJS module spec 1.1
                    cjsModule = args[i] = handlers.module(name);
                } else if (hasProp(defined, depName) ||
                           hasProp(waiting, depName) ||
                           hasProp(defining, depName)) {
                    args[i] = callDep(depName);
                } else if (map.p) {
                    map.p.load(map.n, makeRequire(relName, true), makeLoad(depName), {});
                    args[i] = defined[depName];
                } else {
                    throw new Error(name + ' missing ' + depName);
                }
            }

            ret = callback ? callback.apply(defined[name], args) : undefined;

            if (name) {
                //If setting exports via "module" is in play,
                //favor that over return value and exports. After that,
                //favor a non-undefined return value over exports use.
                if (cjsModule && cjsModule.exports !== undef &&
                        cjsModule.exports !== defined[name]) {
                    defined[name] = cjsModule.exports;
                } else if (ret !== undef || !usingExports) {
                    //Use the return value from the function.
                    defined[name] = ret;
                }
            }
        } else if (name) {
            //May just be an object definition for the module. Only
            //worry about defining if have a module name.
            defined[name] = callback;
        }
    };

    requirejs = require = req = function (deps, callback, relName, forceSync, alt) {
        if (typeof deps === "string") {
            if (handlers[deps]) {
                //callback in this case is really relName
                return handlers[deps](callback);
            }
            //Just return the module wanted. In this scenario, the
            //deps arg is the module name, and second arg (if passed)
            //is just the relName.
            //Normalize module name, if it contains . or ..
            return callDep(makeMap(deps, makeRelParts(callback)).f);
        } else if (!deps.splice) {
            //deps is a config object, not an array.
            config = deps;
            if (config.deps) {
                req(config.deps, config.callback);
            }
            if (!callback) {
                return;
            }

            if (callback.splice) {
                //callback is an array, which means it is a dependency list.
                //Adjust args if there are dependencies
                deps = callback;
                callback = relName;
                relName = null;
            } else {
                deps = undef;
            }
        }

        //Support require(['a'])
        callback = callback || function () {};

        //If relName is a function, it is an errback handler,
        //so remove it.
        if (typeof relName === 'function') {
            relName = forceSync;
            forceSync = alt;
        }

        //Simulate async callback;
        if (forceSync) {
            main(undef, deps, callback, relName);
        } else {
            //Using a non-zero value because of concern for what old browsers
            //do, and latest browsers "upgrade" to 4 if lower value is used:
            //http://www.whatwg.org/specs/web-apps/current-work/multipage/timers.html#dom-windowtimers-settimeout:
            //If want a value immediately, use require('id') instead -- something
            //that works in almond on the global level, but not guaranteed and
            //unlikely to work in other AMD implementations.
            setTimeout(function () {
                main(undef, deps, callback, relName);
            }, 4);
        }

        return req;
    };

    /**
     * Just drops the config on the floor, but returns req in case
     * the config return value is used.
     */
    req.config = function (cfg) {
        return req(cfg);
    };

    /**
     * Expose module registry for debugging and tooling
     */
    requirejs._defined = defined;

    define = function (name, deps, callback) {
        if (typeof name !== 'string') {
            throw new Error('See almond README: incorrect module build, no module name');
        }

        //This module may not have dependencies
        if (!deps.splice) {
            //deps is not an array, so probably means
            //an object literal or factory function for
            //the value. Adjust args.
            callback = deps;
            deps = [];
        }

        if (!hasProp(defined, name) && !hasProp(waiting, name)) {
            waiting[name] = [name, deps, callback];
        }
    };

    define.amd = {
        jQuery: true
    };
}());

define("components/almond/almond", function(){});

define('app/lib/ready',[],function () {

    "use strict";

    var loaded = false;
    var once = function (callback) {
        if (!loaded) {
            loaded = true;
            callback();
        }
    };

    var domready = function (callback) {

        // HTML5 standard to listen for dom readiness
        document.addEventListener('DOMContentLoaded', function () {
            once(callback);
        });

        // if dom is already ready, just run callback
        if (document.readyState === "interactive" || document.readyState === "complete") {
            once(callback);
        }
    };

    return domready;

});
define('app/lib/promise',[],function () {

    "use strict";

    var stderr = function (text) { console.log(text); };

    var Promise = function () {
        this.success = [];
        this.errors = [];
    };

    Promise.prototype.then = function (onSuccess, onError) {
        this.success.push(onSuccess);
        if (onError) {
            this.errors.push(onError);
        } else {
            this.errors.push(stderr);
        }
    };

    var Defer = function () {
        this.promise = new Promise();
    };

    Defer.prototype = {
        promise: Promise,
        resolve: function (rv) {
            this.promise.success.forEach(function (callback) {
                window.setTimeout(function () {
                    callback(rv);
                }, 0);
            });
        },

        reject: function (error) {
            this.promise.errors.forEach(function (callback) {
                window.setTimeout(function () {
                    callback(error);
                }, 0);
            });
        }
    };

    var when = function (obj, func) {
        if (obj instanceof Promise) {
            return obj.then(func);
        } else {
            return func(obj);
        }
    };

    return {
        defer: function () { return new Defer(); },
        when: when
    };

});

define('app/globals',[],function () {
    "use strict";

    var Offset = function () {
        this.values = [];
    };

    Offset.prototype.update = function (remoteTime) {
        this.values.push(new Date().getTime() - remoteTime.getTime());
    };

    Offset.prototype.localTime = function () {
        return new Date(
            new Date().getTime() -
                this.values.reduce(function (a, b) {
                    return a + b;
                }) /
                    this.values.length
        );
    };

    return {
        offset: new Offset(),
    };
});

define('app/api',["app/lib/promise", "app/globals"], function (Q, globals) {
    "use strict";

    var salt = "Eech7co8Ohloopo9Ol6baimi",
        location = function () {
            return window.location.pathname;
        };

    var script,
        endpoint,
        js = document.getElementsByTagName("script");

    // prefer `data-nikas="//host/api/endpoint"` if provided
    for (var i = 0; i < js.length; i++) {
        if (js[i].hasAttribute("data-nikas")) {
            endpoint = js[i].getAttribute("data-nikas");
            break;
        }
    }

    // if no async-script is embedded, use the last script tag of `js`
    if (!endpoint) {
        for (i = 0; i < js.length; i++) {
            if (js[i].getAttribute("async") || js[i].getAttribute("defer")) {
                // Todo : set client-configuration url
                throw (
                    "Nikas's automatic configuration detection failed, please " +
                    "refer to client-configuration " +
                    "and add a custom `data-nikas` attribute."
                );
            }
        }

        script = js[js.length - 1];
        endpoint = script.src.substring(
            0,
            script.src.length - "/js/embed.min.js".length
        );
    }

    //  strip trailing slash
    if (endpoint[endpoint.length - 1] === "/") {
        endpoint = endpoint.substring(0, endpoint.length - 1);
    }

    var curl = function (method, url, data, resolve, reject) {
        var xhr = new XMLHttpRequest();

        function onload() {
            var date = xhr.getResponseHeader("Date");
            if (date !== null) {
                globals.offset.update(new Date(date));
            }

            var cookie = xhr.getResponseHeader("X-Set-Cookie");
            if (cookie && cookie.match(/^nikas-/)) {
                document.cookie = cookie;
            }

            if (xhr.status >= 500) {
                if (reject) {
                    reject(xhr.body);
                }
            } else {
                resolve({ status: xhr.status, body: xhr.responseText });
            }
        }

        try {
            xhr.open(method, url, true);
            xhr.withCredentials = true;
            xhr.setRequestHeader("Content-Type", "application/json");

            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    onload();
                }
            };
        } catch (exception) {
            (reject || console.log)(exception.message);
        }

        xhr.send(data);
    };

    var qs = function (params) {
        var rv = "";
        for (var key in params) {
            if (
                params.hasOwnProperty(key) &&
                params[key] !== null &&
                typeof params[key] !== "undefined"
            ) {
                rv += key + "=" + encodeURIComponent(params[key]) + "&";
            }
        }

        return rv.substring(0, rv.length - 1); // chop off trailing "&"
    };

    var create = function (tid, data) {
        var deferred = Q.defer();
        curl(
            "POST",
            endpoint + "/new?" + qs({ uri: tid || location() }),
            JSON.stringify(data),
            function (rv) {
                if (rv.status === 201 || rv.status === 202) {
                    deferred.resolve(JSON.parse(rv.body));
                } else {
                    deferred.reject(rv.body);
                }
            }
        );
        return deferred.promise;
    };

    var modify = function (id, data) {
        var deferred = Q.defer();
        curl("PUT", endpoint + "/id/" + id, JSON.stringify(data), function (
            rv
        ) {
            if (rv.status === 403) {
                deferred.reject("Not authorized to modify this comment!");
            } else if (rv.status === 200) {
                deferred.resolve(JSON.parse(rv.body));
            } else {
                deferred.reject(rv.body);
            }
        });
        return deferred.promise;
    };

    var remove = function (id) {
        var deferred = Q.defer();
        curl("DELETE", endpoint + "/id/" + id, null, function (rv) {
            if (rv.status === 403) {
                deferred.reject("Not authorized to remove this comment!");
            } else if (rv.status === 200) {
                deferred.resolve(JSON.parse(rv.body) === null);
            } else {
                deferred.reject(rv.body);
            }
        });
        return deferred.promise;
    };

    var view = function (id, plain) {
        var deferred = Q.defer();
        curl(
            "GET",
            endpoint + "/id/" + id + "?" + qs({ plain: plain }),
            null,
            function (rv) {
                deferred.resolve(JSON.parse(rv.body));
            }
        );
        return deferred.promise;
    };

    var fetch = function (tid, limit, nested_limit, parent, lastcreated) {
        if (typeof limit === "undefined") {
            limit = "inf";
        }
        if (typeof nested_limit === "undefined") {
            nested_limit = "inf";
        }
        if (typeof parent === "undefined") {
            parent = null;
        }

        var query_dict = {
            uri: tid || location(),
            after: lastcreated,
            parent: parent,
        };

        if (limit !== "inf") {
            query_dict["limit"] = limit;
        }
        if (nested_limit !== "inf") {
            query_dict["nested_limit"] = nested_limit;
        }

        var deferred = Q.defer();
        curl("GET", endpoint + "/?" + qs(query_dict), null, function (rv) {
            if (rv.status === 200) {
                deferred.resolve(JSON.parse(rv.body));
            } else if (rv.status === 404) {
                deferred.resolve({ total_replies: 0 });
            } else {
                deferred.reject(rv.body);
            }
        });
        return deferred.promise;
    };

    var count = function (urls) {
        var deferred = Q.defer();
        curl("POST", endpoint + "/count", JSON.stringify(urls), function (rv) {
            if (rv.status === 200) {
                deferred.resolve(JSON.parse(rv.body));
            } else {
                deferred.reject(rv.body);
            }
        });
        return deferred.promise;
    };

    var like = function (id) {
        var deferred = Q.defer();
        curl("POST", endpoint + "/id/" + id + "/like", null, function (rv) {
            deferred.resolve(JSON.parse(rv.body));
        });
        return deferred.promise;
    };

    var dislike = function (id) {
        var deferred = Q.defer();
        curl("POST", endpoint + "/id/" + id + "/dislike", null, function (rv) {
            deferred.resolve(JSON.parse(rv.body));
        });
        return deferred.promise;
    };

    var feed = function (tid) {
        return endpoint + "/feed?" + qs({ uri: tid || location() });
    };

    var preview = function (text) {
        var deferred = Q.defer();
        curl(
            "POST",
            endpoint + "/preview",
            JSON.stringify({ text: text }),
            function (rv) {
                if (rv.status === 200) {
                    deferred.resolve(JSON.parse(rv.body).text);
                } else {
                    deferred.reject(rv.body);
                }
            }
        );
        return deferred.promise;
    };

    return {
        endpoint: endpoint,
        salt: salt,

        create: create,
        modify: modify,
        remove: remove,
        view: view,
        fetch: fetch,
        count: count,
        like: like,
        dislike: dislike,
        feed: feed,
        preview: preview,
    };
});

define('app/dom',[],function () {
    "use strict";

    function Element(node) {
        this.obj = node;

        this.replace = function (el) {
            var element = DOM.htmlify(el);
            node.parentNode.replaceChild(element.obj, node);
            return element;
        };

        this.prepend = function (el) {
            var element = DOM.htmlify(el);
            node.insertBefore(element.obj, node.firstChild);
            return element;
        };

        this.append = function (el) {
            var element = DOM.htmlify(el);
            node.appendChild(element.obj);
            return element;
        };

        this.insertAfter = function (el) {
            var element = DOM.htmlify(el);
            node.parentNode.insertBefore(element.obj, node.nextSibling);
            return element;
        };

        /**
         * Shortcut for `Element.addEventListener`, prevents default event
         * by default, set :param prevents: to `false` to change that behavior.
         */
        this.on = function (type, listener, prevent) {
            node.addEventListener(type, function (event) {
                listener(event);
                if (prevent === undefined || prevent) {
                    event.preventDefault();
                }
            });
        };

        /**
         * Toggle between two internal states on event :param type: e.g. to
         * cycle form visibility. Callback :param a: is called on first event,
         * :param b: next time.
         *
         * You can skip to the next state without executing the callback with
         * `toggler.next()`. You can prevent a cycle when you call `toggler.wait()`
         * during an event.
         */
        this.toggle = function (type, a, b) {
            var toggler = new Toggle(a, b);
            this.on(type, function () {
                toggler.next();
            });
        };

        this.detach = function () {
            // Detach an element from the DOM and return it.
            node.parentNode.removeChild(this.obj);
            return this;
        };

        this.remove = function () {
            // IE quirks
            node.parentNode.removeChild(this.obj);
        };

        this.show = function () {
            node.style.display = "block";
        };

        this.hide = function () {
            node.style.display = "none";
        };

        this.setText = function (text) {
            node.textContent = text;
        };

        this.setHtml = function (html) {
            node.innerHTML = html;
        };

        this.blur = function () {
            node.blur();
        };
        this.focus = function () {
            node.focus();
        };
        this.scrollIntoView = function (args) {
            node.scrollIntoView(args);
        };

        this.checked = function () {
            return node.checked;
        };

        this.setAttribute = function (key, value) {
            node.setAttribute(key, value);
        };
        this.getAttribute = function (key) {
            return node.getAttribute(key);
        };

        this.classList = node.classList;

        Object.defineProperties(this, {
            textContent: {
                get: function () {
                    return node.textContent;
                },
                set: function (textContent) {
                    node.textContent = textContent;
                },
            },
            innerHTML: {
                get: function () {
                    return node.innerHTML;
                },
                set: function (innerHTML) {
                    node.innerHTML = innerHTML;
                },
            },
            value: {
                get: function () {
                    return node.value;
                },
                set: function (value) {
                    node.value = value;
                },
            },
            placeholder: {
                get: function () {
                    return node.placeholder;
                },
                set: function (placeholder) {
                    node.placeholder = placeholder;
                },
            },
        });
    }

    var Toggle = function (a, b) {
        this.state = false;

        this.next = function () {
            if (!this.state) {
                this.state = true;
                a(this);
            } else {
                this.state = false;
                b(this);
            }
        };

        this.wait = function () {
            this.state = !this.state;
        };
    };

    var DOM = function (query, root, single) {
        /*
        jQuery-like CSS selector which returns on :param query: either a
        single node (unless single=false), a node list or null.

        :param root: only queries within the given element.
         */

        if (typeof single === "undefined") {
            single = true;
        }

        if (!root) {
            root = window.document;
        }

        if (root instanceof Element) {
            root = root.obj;
        }
        var elements = [].slice.call(root.querySelectorAll(query), 0);

        if (elements.length === 0) {
            return null;
        }

        if (elements.length === 1 && single) {
            return new Element(elements[0]);
        }

        // convert NodeList to Array
        elements = [].slice.call(elements, 0);

        return elements.map(function (el) {
            return new Element(el);
        });
    };

    DOM.htmlify = function (el) {
        /*
        Convert :param html: into an Element (if not already).
        */

        if (el instanceof Element) {
            return el;
        }

        if (el instanceof window.Element) {
            return new Element(el);
        }

        var wrapper = DOM.new("div");
        wrapper.innerHTML = el;
        return new Element(wrapper.firstChild);
    };

    DOM.new = function (tag, content) {
        /*
        A helper to build HTML with pure JS. You can pass class names and
        default content as well:

            var par = DOM.new("p"),
                div = DOM.new("p.some.classes"),
                div = DOM.new("textarea.foo", "...")
         */

        var el = document.createElement(tag.split(".")[0]);
        tag.split(".")
            .slice(1)
            .forEach(function (val) {
                el.classList.add(val);
            });

        if (["A", "LINK"].indexOf(el.nodeName) > -1) {
            el.href = "#";
        }

        if (!content && content !== 0) {
            content = "";
        }
        if (["TEXTAREA", "INPUT"].indexOf(el.nodeName) > -1) {
            el.value = content;
        } else {
            el.textContent = content;
        }
        return el;
    };

    DOM.each = function (tag, func) {
        // XXX really needed? Maybe better as NodeList method
        Array.prototype.forEach.call(document.getElementsByTagName(tag), func);
    };

    return DOM;
});

define('app/config',[],function () {
    "use strict";

    var config = {
        css: true,
        lang: (navigator.language || navigator.userLanguage).split("-")[0],
        "reply-to-self": false,
        "require-email": false,
        "require-author": false,
        "reply-notifications": false,
        "max-comments-top": "inf",
        "max-comments-nested": 5,
        "reveal-on-click": 5,
        gravatar: false,
        avatar: true,
        "avatar-bg": "#f0f0f0",
        "avatar-fg": [
            "#9abf88",
            "#5698c4",
            "#e279a3",
            "#9163b6",
            "#be5168",
            "#f19670",
            "#e4bf80",
            "#447c69",
        ].join(" "),
        vote: true,
        "vote-levels": null,
        feed: false,
    };

    var js = document.getElementsByTagName("script");

    for (var i = 0; i < js.length; i++) {
        for (var j = 0; j < js[i].attributes.length; j++) {
            var attr = js[i].attributes[j];
            if (/^data-nikas-/.test(attr.name)) {
                try {
                    config[attr.name.substring(11)] = JSON.parse(attr.value);
                } catch (ex) {
                    config[attr.name.substring(11)] = attr.value;
                }
            }
        }
    }

    // split avatar-fg on whitespace
    config["avatar-fg"] = config["avatar-fg"].split(" ");

    return config;
});

define('app/i18n/fa',{
    "postbox-text": "متن نظر را اینجا وارد کنید - حداقل ۳ حرف",
    "postbox-author": "نام (اختیاری)",
    "postbox-email": "آدرس ایمیل (اختیاری)",
    "postbox-website": "آدرس وب سایت (اختیاری)",
    "postbox-preview": "پیش نمایش",
    "postbox-edit": "ویرایش",
    "postbox-submit": "ثبت",
    "postbox-notification": "اطلاع رسانی از طریق ایمیل",

    "num-comments": "یک نظر\n{{ n }} نظر",
    "no-comments": "هنوز نظری ثبت نشده است",
    "atom-feed": "فید اتم",

    "comment-reply": "پاسخ",
    "comment-edit": "ویرایش",
    "comment-save": "ذخیره",
    "comment-delete": "حذف",
    "comment-confirm": "تایید",
    "comment-close": "بستن",
    "comment-cancel": "لغو",
    "comment-deleted": "نظر حذف شد.",
    "comment-queued": "در انتظار بررسی توسط مدیریت.",
    "comment-anonymous": "ناشناس",
    "comment-hidden": "{{ n }} مخفی",

    "date-now": "همین الان",
    "date-minute": "یک دقیقه پیش\n{{ n }} دقیقه پیش",
    "date-hour": "یک ساعت پیش\n{{ n }} ساعت پیش",
    "date-day": "دیروز\n{{ n }} روز پیش",
    "date-week": "هفته پیش\n{{ n }} هفته پیش",
    "date-month": "ماه پیش\n{{ n }} ماه پیش",
    "date-year": "سال پیش\n{{ n }} سال پیش",
});

define('app/i18n',["app/config", "app/i18n/fa"], function (config, fa) {
    "use strict";

    var pluralforms = function (lang) {
        switch (lang) {
            case "fa":
                return function (msgs, n) {
                    return msgs[n === 1 ? 0 : 1];
                };
            default:
                return null;
        }
    };

    // useragent's preferred language (or manually overridden)
    var lang = config.lang;

    // fall back
    if (!pluralforms(lang)) {
        lang = "fa";
    }

    var catalogue = {
        fa: fa,
    };

    var plural = pluralforms(lang);

    var translate = function (msgid) {
        return (
            config[msgid + "-text-" + lang] ||
            catalogue[lang][msgid] ||
            fa[msgid] ||
            "???"
        );
    };

    var pluralize = function (msgid, n) {
        var msg;

        msg = translate(msgid);
        if (msg.indexOf("\n") > -1) {
            msg = plural(msg.split("\n"), +n);
        }

        return msg ? msg.replace("{{ n }}", +n) : msg;
    };

    return {
        lang: lang,
        translate: translate,
        pluralize: pluralize,
    };
});

define('app/count',["app/api", "app/dom", "app/i18n"], function (api, $, i18n) {
    return function () {
        var objs = {};

        $.each("a", function (el) {
            if (!el.href.match || !el.href.match(/#nikas-thread$/)) {
                return;
            }

            var tid =
                el.getAttribute("data-nikas-id") ||
                el.href
                    .match(/^(.+)#nikas-thread$/)[1]
                    .replace(/^.*\/\/[^\/]+/, "");

            if (tid in objs) {
                objs[tid].push(el);
            } else {
                objs[tid] = [el];
            }
        });

        var urls = Object.keys(objs);

        api.count(urls).then(function (rv) {
            for (var key in objs) {
                if (objs.hasOwnProperty(key)) {
                    var index = urls.indexOf(key);

                    for (var i = 0; i < objs[key].length; i++) {
                        objs[key][i].textContent = i18n.pluralize(
                            "num-comments",
                            rv[index]
                        );
                    }
                }
            }
        });
    };
});

require(["app/lib/ready", "app/count"], function (domready, count) {
    domready(function () {
        count();
    });
});

define("count", function(){});

}());