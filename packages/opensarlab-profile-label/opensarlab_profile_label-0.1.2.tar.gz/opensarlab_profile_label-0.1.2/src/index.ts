import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ITopBar } from 'jupyterlab-topbar';
import { Widget } from '@lumino/widgets';

import { requestAPI } from './handler';

class OpensarlabProfileLabelWidget extends Widget {
  constructor() {
    super();

    this.span = document.createElement('span');
    this.addClass('opensarlab-profile-label-widget');
    this.node.appendChild(this.span);
  }

  readonly span: HTMLSpanElement;
}

const opensarlab_profile_label_extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-topbar-opensarlab-profile-label',
  autoStart: true,
  requires: [ITopBar],
  activate: async (app: JupyterFrontEnd, topBar: ITopBar) => {
    let data = null;
    try {
      data = await requestAPI<any>('opensarlab-profile-label');
      console.log(data);
    } catch (reason) {
      console.error(
        `Error on GET /opensarlab-profile-label/opensarlab-profile-label.\n${reason}`
      );
    }

    const opensarlabProfileLabelWidget = new OpensarlabProfileLabelWidget();
    opensarlabProfileLabelWidget.span.innerText = data['data'];
    topBar.addItem('opensarlab_profile_label', opensarlabProfileLabelWidget);
  }
};

export default opensarlab_profile_label_extension;
