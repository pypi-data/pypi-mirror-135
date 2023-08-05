import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { IDocumentManager } from '@jupyterlab/docmanager';
import StyledInstance from './components/instance/Instance';
import StyledWorkflow from './components/workflow/Workflow';
import StyledWorkflowsPanel from './components/WorkflowsPanel';
import StyledInstancesPanel from './components/InstancesPanel';
import StyledIndexPanel from './components/IndexPanel';
import StyledHeader from './components/Header';
import StyledFooter from './components/Footer';
import styled from 'styled-components';

import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';

const LauncherContainer = styled.div``;

export class Launcher extends ReactWidget {
  constructor(docTrack: IDocumentManager) {
    super();
    this.docTrack = docTrack;
    this.addClass('jp-ReactWidget');
    this.addClass('epi2melabs-wfpage-widget');
  }

  render(): JSX.Element {
    return (
      <Router>
        <LauncherContainer>
          <main style={{ position: 'relative' }}>
            <StyledHeader />
            <div>
              <Routes>
                <Route path="/workflows/:name" element={<StyledWorkflow />} />
                <Route path="/workflows" element={<StyledWorkflowsPanel />} />
                <Route
                  path="/instances/:id"
                  element={<StyledInstance docTrack={this.docTrack} />}
                />
                <Route path="/instances" element={<StyledInstancesPanel />} />
                <Route path="/" element={<StyledIndexPanel />} />
              </Routes>
            </div>
            <StyledFooter />
          </main>
        </LauncherContainer>
      </Router>
    );
  }

  public docTrack: IDocumentManager;
}
