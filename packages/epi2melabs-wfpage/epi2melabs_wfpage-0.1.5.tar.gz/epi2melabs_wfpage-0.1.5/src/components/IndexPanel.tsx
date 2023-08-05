import React from 'react';
import styled from 'styled-components';
import StyledWorkflowList from './workflow/WorkflowList';
import StyledInstanceList from './instance/InstanceList';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowsList {
  className?: string;
}

const IndexPanel = ({ className }: IWorkflowsList): JSX.Element => (
  <div className={`index-panel ${className}`}>
    <div className="index-panel-intro">
      <h1>EPI2ME Labs Workflows (Beta)</h1>
      <p>
        EPI2ME Labs maintains a growing collection of workflows covering a range
        of everyday bioinformatics needs. These are free and open to use by
        anyone. Browse the list below and get started.
      </p>
    </div>

    {/* Workflows */}
    <div className="index-panel-section">
      <h2>Available workflows</h2>
      <StyledWorkflowList />
    </div>

    {/* Instances */}
    <div className="index-panel-section">
      <h2>Tracked instances</h2>
      <StyledInstanceList onlyTracked />
    </div>
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledIndexPanel = styled(IndexPanel)`
  background-color: #f6f6f6;
  padding-bottom: 100px;

  .index-panel-intro {
    padding: 75px 50px 75px 50px;
    display: flex;
    align-items: center;
    flex-direction: column;
    background-color: white;
  }

  .index-panel-intro h1 {
    padding: 25px 0;
    text-align: center;
  }

  .index-panel-intro p {
    max-width: 800px;
    text-align: center;
    font-size: 16px;
    line-height: 1.7em;
  }

  .index-panel-section {
    padding: 0 35px;
    max-width: 1200px;
    margin: 50px auto 0 auto;
  }
`;

export default StyledIndexPanel;
