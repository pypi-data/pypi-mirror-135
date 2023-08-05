import React from 'react';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface ITitle {
  title: string;
  className?: string;
}

const HeaderTitle = ({ title, className }: ITitle): JSX.Element => (
  <div className={`header-title ${className}`}>
    <h1>{title}</h1>
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledHeaderTitle = styled(HeaderTitle)`
  padding: 75px 50px 75px 50px;
  display: flex;
  align-items: center;
  flex-direction: column;
  background-color: white;

  h1 {
    padding: 25px 0;
    text-align: center;
  }
`;

export default StyledHeaderTitle;
