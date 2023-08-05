import React from 'react';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Type definitions
// -----------------------------------------------------------------------------
export const STR_INPUT = 'string';

export interface ITextProps {
  id: string;
  label: string;
  format: string;
  description: string;
  defaultValue: string;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
}

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface ITextInput extends ITextProps {
  error: string[];
  onChange: CallableFunction;
  className?: string;
}

const TextInput = ({
  id,
  label,
  format,
  description,
  defaultValue,
  minLength,
  maxLength,
  pattern,
  error,
  onChange,
  className
}: ITextInput): JSX.Element => (
  <div className={`TextInput ${className}`}>
    <h4>{label}</h4>
    <p>{description}</p>
    <label htmlFor={id}>
      <input
        id={id}
        type="text"
        placeholder={'Enter a value'}
        defaultValue={defaultValue}
        pattern={pattern}
        minLength={minLength}
        maxLength={maxLength}
        onChange={e => onChange(id, format, e.target.value)}
      />
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
const StyledTextInput = styled(TextInput)`
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

  input {
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

  input:hover {
    border: 1px solid #005c75;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;

export default StyledTextInput;
