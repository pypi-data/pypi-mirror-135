import React from 'react';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Type definitions
// -----------------------------------------------------------------------------
export const SELECT_INPUT = 'select';

interface ISelectChoice {
  value: string;
  label: string;
}

export interface ISelectProps {
  id: string;
  label: string;
  format: string;
  description: string;
  defaultValue?: string;
  choices: ISelectChoice[];
}

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface ISelectInput extends ISelectProps {
  error: string[];
  onChange: CallableFunction;
  className?: string;
}

const SelectInput = ({
  id,
  label,
  format,
  description,
  defaultValue,
  choices,
  error,
  onChange,
  className
}: ISelectInput): JSX.Element => (
  <div className={`SelectInput ${className}`}>
    <h4>{label}</h4>
    <p>{description}</p>
    <label htmlFor={id}>
      <select
        id={id}
        onChange={(e: any) => onChange(id, format, e.target.value)}
      >
        {defaultValue ? (
          ''
        ) : (
          <option
            className="placeholder"
            selected
            disabled
            hidden
            value="Select an option"
          >
            Select an option
          </option>
        )}
        {choices.map(Choice => (
          <option
            key={Choice.label}
            selected={!!(Choice.value === defaultValue)}
            value={Choice.value}
          >
            {Choice.label}
          </option>
        ))}
      </select>
    </label>
    {error ? (
      <div className="error">
        <p>Error: {error}</p>
      </div>
    ) : (
      ''
    )}
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledSelectInput = styled(SelectInput)`
  h4 {
    padding: 0 0 5px 0;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    color: black;
  }

  p {
    padding: 0 0 10px 0;
    font-size: 13px;
    color: #333;
  }

  label {
    display: flex;
  }

  select {
    margin: 0;
    min-width: 50%;
    padding: 15px 25px;

    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    line-height: 1em;

    color: black;
    background-color: #f3f3f3;
    border: 0;
    border: 1px solid transparent;
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  select:hover {
    border: 1px solid #005c75;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;

export default StyledSelectInput;
