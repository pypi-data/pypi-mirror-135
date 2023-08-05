import React from 'react';
import { logoSVG } from '../asset';
import { Link } from 'react-router-dom';
import styled from 'styled-components';

export const LabsLogo = (): JSX.Element => {
  const logoSVGBlob = new Blob([logoSVG], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(logoSVGBlob);

  return (
    <div className="labsLogo">
      <img src={url} alt="The EPI2ME Labs logo" />
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IHeader {
  className?: string;
}

const Header = ({ className }: IHeader): JSX.Element => (
  <header className={`header ${className}`}>
    <div className="header-section left-navigation">
      <Link to="/workflows">Workflows</Link>
      <Link to="/instances">History</Link>
    </div>
    <div className="header-section center-navigation">
      <Link to="/">
        <LabsLogo />
      </Link>
    </div>
    <div className="header-section right-navigation">
      <a href="https://labs.epi2me.io/">Labs Blog</a>
    </div>
  </header>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledHeader = styled(Header)`
  padding: 15px 25px;
  display: flex;
  justify-content: space-between;
  background-color: #00485b;
  color: white;

  .labsLogo img {
    width: 25px;
  }

  .header-section {
    width: calc(100% / 3);
    display: flex;
    align-items: center;
  }

  .left-navigation a {
    padding-right: 25px;
  }

  .center-navigation {
    justify-content: center;
  }

  .right-navigation {
    justify-content: right;
  }

  a {
    font-weight: bold;
  }
`;

export default StyledHeader;
