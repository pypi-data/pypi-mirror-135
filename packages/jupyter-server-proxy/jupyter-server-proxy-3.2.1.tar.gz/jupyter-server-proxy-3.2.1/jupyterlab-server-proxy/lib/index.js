"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const application_1 = require("@jupyterlab/application");
const launcher_1 = require("@jupyterlab/launcher");
const coreutils_1 = require("@jupyterlab/coreutils");
const apputils_1 = require("@jupyterlab/apputils");
function newServerProxyWidget(id, url, text) {
    const content = new apputils_1.IFrame({
        sandbox: ['allow-same-origin', 'allow-scripts', 'allow-popups', 'allow-forms'],
    });
    content.title.label = text;
    content.title.closable = true;
    content.url = url;
    content.addClass('jp-ServerProxy');
    content.id = id;
    const widget = new apputils_1.MainAreaWidget({ content });
    widget.addClass('jp-ServerProxy');
    return widget;
}
function activate(app, launcher, restorer) {
    return __awaiter(this, void 0, void 0, function* () {
        const response = yield fetch(coreutils_1.PageConfig.getBaseUrl() + 'server-proxy/servers-info');
        if (!response.ok) {
            console.log('Could not fetch metadata about registered servers. Make sure jupyter-server-proxy is installed.');
            console.log(response);
            return;
        }
        const { commands, shell } = app;
        const data = yield response.json();
        const namespace = 'server-proxy';
        const tracker = new apputils_1.WidgetTracker({
            namespace
        });
        const command = namespace + ':' + 'open';
        if (restorer) {
            void restorer.restore(tracker, {
                command: command,
                args: widget => ({
                    url: widget.content.url,
                    title: widget.content.title.label,
                    newBrowserTab: false,
                    id: widget.content.id
                }),
                name: widget => widget.content.id
            });
        }
        commands.addCommand(command, {
            label: args => args['title'],
            execute: args => {
                const id = args['id'];
                const title = args['title'];
                const url = args['url'];
                const newBrowserTab = args['newBrowserTab'];
                if (newBrowserTab) {
                    window.open(url, '_blank');
                    return;
                }
                let widget = tracker.find((widget) => { return widget.content.id == id; });
                if (!widget) {
                    widget = newServerProxyWidget(id, url, title);
                }
                if (!tracker.has(widget)) {
                    void tracker.add(widget);
                }
                if (!widget.isAttached) {
                    shell.add(widget);
                    return widget;
                }
                else {
                    shell.activateById(widget.id);
                }
            }
        });
        for (let server_process of data.server_processes) {
            if (!server_process.launcher_entry.enabled) {
                continue;
            }
            const url = coreutils_1.PageConfig.getBaseUrl() + server_process.launcher_entry.path_info;
            const title = server_process.launcher_entry.title;
            const newBrowserTab = server_process.new_browser_tab;
            const id = namespace + ':' + server_process.name;
            const launcher_item = {
                command: command,
                args: {
                    url: url,
                    title: title + (newBrowserTab ? ' [↗]' : ''),
                    newBrowserTab: newBrowserTab,
                    id: id
                },
                category: 'Notebook'
            };
            if (server_process.launcher_entry.icon_url) {
                launcher_item.kernelIconUrl = server_process.launcher_entry.icon_url;
            }
            launcher.add(launcher_item);
        }
    });
}
/**
 * Initialization data for the jupyterlab-server-proxy extension.
 */
const extension = {
    id: 'jupyterlab-server-proxy',
    autoStart: true,
    requires: [launcher_1.ILauncher, application_1.ILayoutRestorer],
    activate: activate
};
exports.default = extension;
