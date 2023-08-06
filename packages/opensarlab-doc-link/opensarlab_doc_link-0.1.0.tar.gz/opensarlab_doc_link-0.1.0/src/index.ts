import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin,
  } from '@jupyterlab/application';
  
  // pip install jupyterlab-topbar
  // jlpm add jupyterlab-topbar
  import { ITopBar } from 'jupyterlab-topbar';
  
  import { Widget } from '@lumino/widgets';
  
  class DocsAnchorWidget extends Widget {
    constructor() {
      super();
  
      this.hyperlink = document.createElement('a');
      this.hyperlink.text = 'OpenSARlab Docs';
      this.hyperlink.href = 'https://opensarlab-docs.asf.alaska.edu/user-guides/how_to_run_a_notebook/';
      this.hyperlink.target = 'blank';
      this.addClass('docs-anchor-widget');
  
      this.node.appendChild(this.hyperlink);
    }
  
    readonly hyperlink: HTMLAnchorElement;
  }

  const extension: JupyterFrontEndPlugin<void> = {
    id: 'jupyterlab-topbar-doclink',
    autoStart: true,
    requires: [ITopBar],
    activate: (app: JupyterFrontEnd, topBar: ITopBar) => {
        const docLinkWidget = new DocsAnchorWidget();
        topBar.addItem('doc_link', docLinkWidget);
    }
};

export default extension;
