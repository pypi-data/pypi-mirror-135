import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the opensarlab-theme-light extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'opensarlab-theme-light',
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension opensarlab-theme-light is activated!');
    const style = 'opensarlab-theme-light/index.css';

    manager.register({
      name: 'opensarlab-theme-light',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default extension;

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module theme-light-extension
 */
