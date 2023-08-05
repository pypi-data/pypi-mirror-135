import React, { useEffect, useState } from 'react';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { GenericStringObject, GenericObject } from '../../types';
import { useParams, useNavigate } from 'react-router-dom';
import StyledStatusIndicator from './StatusIndicator';
import { requestAPI } from '../../handler';
import styled from 'styled-components';
import { Instance } from './types';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IInstanceComponent {
  className?: string;
  docTrack: IDocumentManager;
}

const InstanceComponent = ({
  className,
  docTrack
}: IInstanceComponent): JSX.Element => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const navigate = useNavigate();
  const routerParams = useParams();
  const [instanceData, setInstanceData] = useState<Instance | undefined>();
  const [instanceStatus, setInstanceStatus] = useState<string>('');
  const [instanceParams, setInstanceParams] = useState<GenericStringObject>({});
  const [instanceOutputs, setInstanceOutputs] = useState<GenericObject[]>([]);
  const [instanceLogs, setInstanceLogs] = useState<string[]>([]);

  // ------------------------------------
  // Handle instance initialisation
  // ------------------------------------
  const getInstanceData = async () => {
    const data = await requestAPI<any>(`instances/${routerParams.id}`);
    setInstanceData(data);
    setInstanceStatus(data.status);
    return data;
  };

  const getInstanceParams = async () => {
    const { params } = await requestAPI<any>(`params/${routerParams.id}`);
    if (params !== null) {
      setInstanceParams(params);
    }
  };

  useEffect(() => {
    const init = async () => {
      await getInstanceData();
      getInstanceParams();
      getInstanceLogs();
    };
    init();
    const statusMonitor = setInterval(() => getInstanceData(), 5000);
    return () => {
      clearInterval(statusMonitor);
    };
  }, []);

  // ------------------------------------
  // Handle instance logs / outputs
  // ------------------------------------
  const getInstanceLogs = async () => {
    const { logs } = await requestAPI<any>(`logs/${routerParams.id}`);
    setInstanceLogs(logs);
  };

  const getInstanceOutputs = async (instanceData: any) => {
    if (!instanceData) {
      return;
    }
    const path = `${instanceData.path}/output`;
    try {
      const files = await (
        await docTrack.services.contents.get(path)
      ).content.filter((Item: any) => Item.type !== 'directory');
      setInstanceOutputs(files);
    } catch (error) {
      console.log('Instance outputs not available yet');
    }
  };

  const handleOpenOutput = (path: string) => {
    docTrack.open(path);
  };

  useEffect(() => {
    if (
      ['COMPLETED_SUCCESSFULLY', 'TERMINATED', 'ENCOUNTERED_ERROR'].includes(
        instanceStatus
      )
    ) {
      getInstanceOutputs(instanceData);
      getInstanceLogs();
      return;
    } else {
      const filesMonitor = setInterval(
        () => getInstanceOutputs(instanceData),
        10000
      );
      const logsMonitor = setInterval(() => getInstanceLogs(), 7500);
      return () => {
        getInstanceOutputs(instanceData);
        getInstanceLogs();
        clearInterval(filesMonitor);
        clearInterval(logsMonitor);
      };
    }
  }, [instanceStatus]);

  // ------------------------------------
  // Handle instance deletion
  // ------------------------------------
  const handleInstanceDelete = async (d: boolean) => {
    const outcome = await requestAPI<any>(`instances/${routerParams.id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        delete: d
      })
    });
    if (d && outcome.deleted) {
      navigate('/instances');
    }
  };

  const isRunning = ['LAUNCHED'].includes(instanceStatus);

  if (!instanceData) {
    return <div className={`instance ${className}`}>Loading...</div>;
  }

  return (
    <div className={`instance ${className}`}>
      <div className="instance-container">
        {/* Instance header */}
        <div className="instance-section instance-header">
          <div className="instance-header-top">
            <h2 className="instance-workflow">
              Workflow: {instanceData.workflow}
            </h2>
            {isRunning ? (
              <button onClick={() => handleInstanceDelete(false)}>
                Stop Instance
              </button>
            ) : (
              ''
            )}
          </div>
          <h1>ID: {routerParams.id}</h1>
          <div className="instance-details">
            <div className="instance-status">
              <StyledStatusIndicator status={instanceStatus || 'UNKNOWN'} />
              <p>{instanceStatus}</p>
            </div>
            <p>Created: {instanceData.created_at}</p>
            <p>Updated: {instanceData.updated_at}</p>
          </div>
        </div>

        {/* Instance params */}
        <div className="instance-section instance-params">
          <h2>Instance params</h2>
          <div className="instance-section-contents">
            <ul>
              {Object.entries(instanceParams).map(([key, value]) => (
                <li>
                  {key}: {value.toString()}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Instance logs */}
        <div className="instance-section instance-logs">
          <h2>Instance logs</h2>
          <div className="instance-section-contents">
            {instanceLogs ? (
              <ul>
                {instanceLogs.map(Item => (
                  <li>
                    <span>{Item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div>Logs are loading...</div>
            )}
          </div>
        </div>

        {/* Instance outputs */}
        <div className="instance-section instance-outputs">
          <h2>Output files</h2>
          <div className="instance-section-contents">
            {instanceOutputs.length ? (
              <ul>
                {instanceOutputs.map(Item => (
                  <li>
                    <button onClick={() => handleOpenOutput(Item.path)}>
                      {Item.name}
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="instance-section-contents">No outputs yet...</div>
            )}
          </div>
        </div>

        {/* Instance delete */}
        <div className="instance-section instance-delete">
          <h2>Danger zone</h2>
          <div className="instance-section-contents">
            <div className={`${!isRunning ? 'active' : 'inactive'}`}>
              <button
                onClick={() => (!isRunning ? handleInstanceDelete(true) : null)}
              >
                Delete Instance
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledInstanceComponent = styled(InstanceComponent)`
  background-color: #f6f6f6;

  .instance-container {
    padding: 50px 0 100px 0 !important;
  }

  .instance-section {
    width: 100%;
    padding: 15px;
    max-width: 1200px;
    margin: 0 auto 25px auto;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .instance-section > h2 {
    padding-bottom: 15px;
  }

  .instance-section-contents {
    padding: 15px;
    border-radius: 4px;
  }

  .instance-header-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
  }

  .instance-header-top h2 {
    padding-bottom: 15px;
  }

  .instance-header-top button {
    cursor: pointer;
    padding: 8px 15px;
    border: 1px solid #e34040;
    color: #e34040;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: transparent;
  }

  .instance-header-top button:hover {
    cursor: pointer;
    background-color: #e34040;
    color: white;
  }

  .instance-details {
    display: flex;
    align-items: center;
  }

  .instance-details p {
    padding-left: 15px;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    color: rgba(0, 0, 0, 0.5);
  }

  .instance-status {
    display: flex;
    align-items: center;
  }

  .instance-status p {
    color: black;
    padding-left: 15px;
  }

  .instance-params .instance-section-contents {
    background-color: #f6f6f6;
  }

  .instance-params li {
    font-size: 12px;
    font-family: monospace;
  }

  .instance-logs .instance-section-contents {
    background-color: #f6f6f6;
    font-size: 12px;
    font-family: monospace;
    overflow: auto;
    text-overflow: initial;
    max-height: 500px;
    white-space: pre;
    color: black;
    border-radius: 4px;
  }

  .instance-logs .instance-section-contents span {
    font-size: 12px;
    font-family: monospace;
  }

  .instance-outputs li {
    margin: 0 0 5px 0;
    display: flex;
    background-color: #f6f6f6;
  }

  .instance-outputs button {
    width: 100%;
    text-align: left;
    padding: 5px;
    font-size: 12px;
    font-family: monospace;
    border: none;
    outline: none;
    background: transparent;
    border: 1px solid #f6f6f6;
  }

  .instance-outputs button:hover {
    border: 1px solid #005c75;
  }

  .instance-delete .instance-section-contents {
    background-color: #f6f6f6;
  }

  .instance-delete button {
    padding: 15px 25px;
    margin: 0 15px 0 0;
    border: 1px solid lightgray;
    color: lightgray;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: transparent;
  }
  .instance-delete .active button {
    border: 1px solid #e34040;
    color: #e34040;
  }
  .instance-delete .active button:hover {
    cursor: pointer;
    background-color: #e34040;
    color: white;
  }
`;

export default StyledInstanceComponent;
