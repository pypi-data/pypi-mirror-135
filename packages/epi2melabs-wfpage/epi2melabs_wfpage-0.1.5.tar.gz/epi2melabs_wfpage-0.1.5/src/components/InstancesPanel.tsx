import React from 'react';
import styled from 'styled-components';
import StyledHeaderTitle from './HeaderTitle';
import StyledInstanceList from './instance/InstanceList';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowsList {
  className?: string;
}

const InstancesPanel = ({ className }: IWorkflowsList): JSX.Element => (
  <div className={`instances-panel ${className}`}>
    <StyledHeaderTitle title="History" />

    {/* Instances */}
    <div className="instances-panel-section">
      <StyledInstanceList />
    </div>
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledInstancesPanel = styled(InstancesPanel)`
  background-color: #f6f6f6;
  padding-bottom: 100px;

  .instances-panel-section {
    padding: 0 35px;
    max-width: 1200px;
    margin: 50px auto 0 auto;
  }
`;

export default StyledInstancesPanel;
