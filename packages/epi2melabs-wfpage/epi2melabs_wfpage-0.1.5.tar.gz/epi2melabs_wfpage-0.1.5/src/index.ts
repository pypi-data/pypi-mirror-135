import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { IDocumentManager } from '@jupyterlab/docmanager';

import { MainAreaWidget } from '@jupyterlab/apputils';

import { ILauncher } from '@jupyterlab/launcher';

import { labsLogoIcon } from './asset';

import { Launcher } from './widget';

const PLUGIN_ID = '@epi2melabs/epi2melabs-wfpage:plugin';

const COMMAND = 'create-epi2me-labs-launcher';

const CATEGORY = 'EPI2ME Labs';

/**
 * Initialization data for the epi2melabs-wfpage extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [ILauncher, ISettingRegistry, IDocumentManager],
  activate: (
    app: JupyterFrontEnd,
    launcher: ILauncher,
    settings: ISettingRegistry,
    docTrack: IDocumentManager
  ) => {
    const { commands, shell } = app;

    Promise.all([app.restored, settings.load(PLUGIN_ID)]).then(
      ([, setting]) => {
        commands.addCommand(COMMAND, {
          caption: 'Create an EPI2ME Labs workflow launcher',
          label: 'Workflows (Beta)',
          icon: labsLogoIcon,
          execute: () => {
            const content = new Launcher(docTrack);
            const widget = new MainAreaWidget<Launcher>({ content });
            widget.title.label = 'EPI2ME Labs';
            shell.add(widget, 'main');
          }
        });

        if (launcher) {
          launcher.add({
            command: COMMAND,
            category: CATEGORY
          });
        }
      }
    );
  }
};

export default plugin;
