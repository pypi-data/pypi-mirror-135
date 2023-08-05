import React from 'react';
import styled from 'styled-components';
import StyledHeaderTitle from './HeaderTitle';
import StyledWorkflowList from './workflow/WorkflowList';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowsList {
  className?: string;
}

const WorkflowsPanel = ({ className }: IWorkflowsList): JSX.Element => (
  <div className={`workflows-panel ${className}`}>
    <StyledHeaderTitle title="Workflows" />

    {/* Workflows */}
    <div className="workflows-panel-section">
      <StyledWorkflowList />
    </div>
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledWorkflowsPanel = styled(WorkflowsPanel)`
  background-color: #f6f6f6;
  padding-bottom: 100px;

  .workflows-panel-section {
    padding: 0 35px;
    max-width: 1200px;
    margin: 50px auto 0 auto;
  }
`;

export default StyledWorkflowsPanel;
