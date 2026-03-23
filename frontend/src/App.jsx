import React, { useState } from "react";
import "./App.css";
import { computeGbfsScore } from "./algorithms/gbfs";
import { computePsoScore } from "./algorithms/pso";
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, 
  CartesianGrid, Tooltip, Legend, ResponsiveContainer, LabelList
} from "recharts";

const STEPS = [
  "Data Input & Generation",
  "Algorithms Applied",
  "Decision Evaluated",
  "Task Processed",
  "Execution Completed"
];

// --- Subcomponents ---

const SidebarNavigation = ({ currentStep, onJump }) => (
  <div className="sidebar">
    <h1>SmartEdge</h1>
    <p>Task Offloading System</p>
    {STEPS.map((step, idx) => (
      <button 
        key={idx} 
        className={`nav-item ${idx === currentStep ? "active" : ""}`}
        onClick={() => onJump(idx)}
      >
        {idx + 1}. {step}
      </button>
    ))}
  </div>
);

const SystemFlow = ({ currentStep, maxReached, onJump }) => (
  <div className="top-bar">
    {STEPS.map((step, idx) => (
      <React.Fragment key={idx}>
        <div className="flow-step">
          <span 
            className={`flow-dot ${idx < currentStep ? "completed" : idx === currentStep ? "active" : ""} ${idx <= maxReached ? "clickable" : ""}`}
            onClick={() => idx <= maxReached && onJump(idx)}
          >●</span>
          <span 
            className={`flow-label ${idx < currentStep ? "completed" : idx === currentStep ? "active" : ""} ${idx <= maxReached ? "clickable" : ""}`}
            onClick={() => idx <= maxReached && onJump(idx)}
          >
            {step}
          </span>
        </div>
        {idx < STEPS.length - 1 && <span className="flow-arrow">→</span>}
      </React.Fragment>
    ))}
  </div>
);

const StepNavigation = ({ currentStep, maxReached, onNext, onPrev }) => (
  <div className="bottom-nav">
    <button className="nav-btn" onClick={onPrev} disabled={currentStep === 0}>← BACK</button>
    <button className="nav-btn next" onClick={onNext} disabled={currentStep >= maxReached || currentStep >= 4}>NEXT →</button>
  </div>
);

// --- Panels ---

const InputGuidePanel = () => (
  <div className="card">
    <h2 className="card-title cyan-text">INPUT GUIDE</h2>
    <div className="guide-text">
      <p>Welcome to the Task Offloading Simulator.</p><br/>
      <p>• <strong>Select Machine:</strong> Choose the machine generating the task.</p>
      <p>• <strong>Input values:</strong> Enter specific operation data (ensure no blanks).</p>
      <p>• <strong>Click Generate:</strong> The system will simulate offloading choices.</p><br/>
      <p><strong>Navigating the System:</strong></p>
      <p>You can use NEXT and BACK buttons to review the simulation outcomes.</p>
    </div>
  </div>
);

const OperationalMetricsPanel = ({ machine, setMachine, category, autoTask, inputs, setInputs, onRun, isProcessing }) => {
  const isFormValid = machine !== "Select Machine" && Object.keys(inputs).length > 0 && Object.values(inputs).every(v => v !== "");
  
  const handleSelect = (e) => {
    const m = e.target.value;
    setMachine(m);
    if(m === "Select Machine") {
      setInputs({});
      return;
    }
    const metricsMap = {
      "CNC Milling Machine": ["Temperature (°C)", "Vibration (Hz)", "Spindle Speed (RPM)", "Motor Load (%)"],
      "Arc Welding Machine": ["Welding Current (A)", "Machine Temperature (°C)", "Power Consumption (W)"],
      "Plasma Cutting Machine": ["Cutting Speed (mm/s)", "Machine Temperature (°C)", "Energy Consumption (kWh)"],
      "Conveyor Systems": ["Queue Length", "Processing Time (s)", "Idle Time (s)"],
      "Electro-Deposition Coating System": ["Temperature (°C)", "Humidity (%)", "Cycle Time (s)"]
    };
    const newInputs = {};
    (metricsMap[m] || []).forEach(k => newInputs[k] = "");
    setInputs(newInputs);
  };

  return (
    <div className="card">
      <h2 className="card-title text-main">OPERATIONAL METRICS</h2>
      
      <div className="section-title">Machine Information</div>
      <div className="data-row">
        <span className="data-label">Specific Machine</span>
        <select className="data-select" value={machine} onChange={handleSelect}>
          <option>Select Machine</option>
          <option>CNC Milling Machine</option>
          <option>Arc Welding Machine</option>
          <option>Plasma Cutting Machine</option>
          <option>Conveyor Systems</option>
          <option>Electro-Deposition Coating System</option>
        </select>
      </div>
      <div className="data-row">
        <span className="data-label">Machine Category</span>
        <span className="data-value">{category || "-"}</span>
      </div>
      <div className="data-row">
        <span className="data-label">Auto-Assigned Task Type</span>
        <span className="data-value">{autoTask || "-"}</span>
      </div>

      {machine !== "Select Machine" && (
        <>
          <div className="section-title">Machine Data</div>
          {Object.keys(inputs).map(k => (
            <div className="data-row" key={k}>
              <span className="data-label">{k}</span>
              <input 
                className="data-input" 
                type="number"
                placeholder={`Enter ${k.split("(")[0].trim()}`}
                value={inputs[k]} 
                onChange={e => setInputs({...inputs, [k]: e.target.value})} 
              />
            </div>
          ))}
          {!isFormValid && <p style={{color: "var(--yellow)", fontSize: "13px", marginTop: "10px"}}>Please fill out all fields.</p>}
        </>
      )}

      <button className="btn-primary" disabled={!isFormValid || isProcessing} onClick={onRun}>
        {isProcessing ? "Processing..." : "GENERATE & OFFLOAD TASK"}
      </button>
    </div>
  );
};

// Error boundary catch
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  render() {
    if (this.state.hasError) {
      return <div style={{padding: '20px', color: 'red'}}><h1>Something went wrong.</h1><pre>{this.state.error?.toString()}</pre></div>;
    }
    return this.props.children; 
  }
}

const AlgoPanel = ({ title, colorClass, data }) => (
  <div className="card">
    <h2 className={`card-title ${colorClass}`}>{title}</h2>
    <p className="subtitle">Note: Lower delay means faster performance. Higher processing speed is better.</p>
    <div className="data-row"><span className="data-label">Score</span><span className="data-value">{data?.score || '-'}</span></div>
    <div className="data-row"><span className="data-label">Delay (ms)</span><span className="data-value">{data?.latency || '-'} ms</span></div>
    <div className="data-row"><span className="data-label">Response Time (ms)</span><span className="data-value">{data?.time || '-'} ms</span></div>
    <div className="data-row"><span className="data-label">Processing Speed (tps)</span><span className="data-value">{data?.throughput || '-'} tps</span></div>
    <div className="data-row"><span className="data-label">Resource Usage (%)</span><span className="data-value">{data?.utilization || '-'} %</span></div>
    <div className="data-row"><span className="data-label">Target Location</span><span className="data-value">{data?.location || '-'}</span></div>
    <div className="data-row"><span className="data-label">Remark</span><span className="data-value">{data?.remark || '-'}</span></div>
  </div>
);

const ComparisonEvaluationPanel = ({ gbfs, pso, winner }) => {
  if (!gbfs || !pso) return null;
  const getW = (metric) => {
    if(metric === "Delay") return parseFloat(gbfs.latency) < parseFloat(pso.latency) ? "GBFS" : "PSO";
    if(metric === "Processing Speed") return parseFloat(gbfs.throughput) > parseFloat(pso.throughput) ? "GBFS" : "PSO";
    if(metric === "Energy") return parseFloat(gbfs.energy) < parseFloat(pso.energy) ? "GBFS" : "PSO";
    if(metric === "Resource Usage") return parseFloat(gbfs.utilization) < parseFloat(pso.utilization) ? "GBFS" : "PSO";
  };
  return (
    <div className="card">
      <h2 className="card-title text-main">COMPARISON EVALUATION</h2>
      <table className="data-table">
        <thead>
          <tr><th>Metric</th><th>GBFS</th><th>PSO</th><th>Winner</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>Delay</td><td>{gbfs.latency} ms</td><td>{pso.latency} ms</td>
            <td className={`val-bold ${getW('Delay') === 'GBFS' ? 'cyan-text' : 'magenta-text'}`}>{getW('Delay')}</td>
          </tr>
          <tr>
            <td>Processing Speed</td><td>{gbfs.throughput} tps</td><td>{pso.throughput} tps</td>
            <td className={`val-bold ${getW('Processing Speed') === 'GBFS' ? 'cyan-text' : 'magenta-text'}`}>{getW('Processing Speed')}</td>
          </tr>
          <tr>
            <td>Energy</td><td>{gbfs.energy} W</td><td>{pso.energy} W</td>
            <td className={`val-bold ${getW('Energy') === 'GBFS' ? 'cyan-text' : 'magenta-text'}`}>{getW('Energy')}</td>
          </tr>
          <tr>
            <td>Resource Usage</td><td>{gbfs.utilization} %</td><td>{pso.utilization} %</td>
            <td className={`val-bold ${getW('Resource Usage') === 'GBFS' ? 'cyan-text' : 'magenta-text'}`}>{getW('Resource Usage')}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

const ProcessingDecisionPanel = ({ decision, reason }) => (
  <div className="card">
    <h2 className="card-title yellow-text">PROCESSING DECISION</h2>
    <div className={`decision-large ${decision === 'Edge' ? 'cyan-text' : 'magenta-text'}`}>
      OFFLOAD TO {decision ? decision.toUpperCase() : "..."}
    </div>
    <div className="decision-reason">Chosen because {reason}</div>
  </div>
);

const InterpretationAnalysisPanel = ({ winner, server, taskType }) => (
  <div className="card">
    <h2 className="card-title text-main">INTERPRETATION & ANALYSIS</h2>
    <div className="interpretation-panel">
      <div className="interpretation-item">
        <p><strong>Algorithm Result:</strong> {winner} was deemed the better algorithm for this cycle because it optimized critical metrics better than its counterpart.</p>
      </div>
      <div className="interpretation-item">
        <p><strong>Decision Explanation:</strong> The system selected <strong>{server} processing</strong> primarily to handle the {taskType} task effectively.</p>
      </div>
      <div className="interpretation-item">
        <p><strong>Final Interpretation:</strong> Overall, deploying via {winner} to the {server} provided the most efficient compute solution for the system load.</p>
      </div>
    </div>
  </div>
);

const TaskAssignmentPanel = ({ taskType, server, summary }) => (
  <div className="card">
    <h2 className="card-title text-main">TASK ASSIGNMENT</h2>
    <div className="data-row"><span className="data-label">Task Type</span><span className="data-value">{taskType}</span></div>
    <div className="data-row"><span className="data-label">Assigned Server</span><span className={`data-value ${server === 'Edge' ? 'cyan-text' : 'magenta-text'}`}>{server} Server</span></div>
    <div className="data-row"><span className="data-label">Summary</span><span className="data-value">{summary}</span></div>
  </div>
);

const ResultTransmissionPanel = () => (
  <div className="card">
    <h2 className="card-title text-main">RESULT TRANSMISSION</h2>
    <div className="data-row"><span className="data-label">Processing Status</span><span className="data-value green-text">Complete</span></div>
    <div className="data-row"><span className="data-label">Transmission Status</span><span className="data-value green-text">Complete</span></div>
    <div className="data-row"><span className="data-label">Network Return Status</span><span className="data-value green-text">Confirmed</span></div>
    <div className="data-row"><span className="data-label">Final Task Status</span><span className="data-value green-text">Success</span></div>
  </div>
);

const PerformanceMonitoringPanel = ({ gbfs, pso }) => {
  if (!gbfs || !pso) {
    return (
      <div className="card" style={{height: "400px", display: "flex", justifyContent: "center", alignItems: "center"}}>
        <p style={{color: "var(--text-muted)"}}>No performance data available yet.</p>
      </div>
    );
  }

  const chartData = [
    { metric: 'Delay', GBFS: Number(gbfs.latency || 0), PSO: Number(pso.latency || 0) },
    { metric: 'Processing Speed', GBFS: Number(gbfs.throughput || 0), PSO: Number(pso.throughput || 0) },
    { metric: 'Energy', GBFS: Number(gbfs.energy || 0), PSO: Number(pso.energy || 0) },
    { metric: 'Resource Usage', GBFS: Number(gbfs.utilization || 0), PSO: Number(pso.utilization || 0) }
  ];

  console.log("Rendering Performance Chart Data:", chartData);

  return (
    <div className="card" style={{minHeight: "450px"}}>
      <h2 className="card-title text-main" style={{textAlign: "center", marginBottom: "15px"}}>System Performance Metrics</h2>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis dataKey="metric" stroke="#6B7280" />
          <YAxis stroke="#6B7280" />
          <Tooltip contentStyle={{backgroundColor: "#FFFFFF", borderColor: "#E5E7EB", color: "#111827"}} />
          <Legend />
          <Bar dataKey="GBFS" fill="#06B6D4" radius={[4, 4, 0, 0]}>
            <LabelList dataKey="GBFS" position="top" fill="#6B7280" fontSize={12} />
          </Bar>
          <Bar dataKey="PSO" fill="#A855F7" radius={[4, 4, 0, 0]}>
            <LabelList dataKey="PSO" position="top" fill="#6B7280" fontSize={12} />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div style={{ textAlign: "center", color: "var(--text-muted)", fontSize: "13px", marginTop: "15px" }}>
        Note: Lower delay is better. Higher processing speed is better. Lower resource usage is better.
      </div>
    </div>
  );
};

const ExecutionLogsPanel = ({ logs }) => (
  <div className="card">
    <h2 className="card-title text-main">EXECUTION LOGS</h2>
    <table className="data-table">
      <thead>
        <tr>
          <th>No.</th><th>Machine Category</th><th>Task Type</th><th>Delay</th><th>Speed</th><th>Winner</th><th>Server</th><th>Status</th>
        </tr>
      </thead>
      <tbody>
        {logs.map((L, i) => (
          <tr key={i}>
            <td className="text-muted">{L.id}</td>
            <td>{L.category}</td>
            <td>{L.type}</td>
            <td>{L.delay}</td>
            <td>{L.speed}</td>
            <td className={L.winner === 'GBFS' ? 'cyan-text val-bold' : 'magenta-text val-bold'}>{L.winner}</td>
            <td className={L.server === 'Edge' ? 'cyan-text val-bold' : 'magenta-text val-bold'}>{L.server}</td>
            <td><span className="status-badge">{L.status}</span></td>
          </tr>
        ))}
        {logs.length === 0 && <tr><td colSpan="8" style={{textAlign: "center", fontStyle: "italic", paddingTop: "20px"}}>No logs available.</td></tr>}
      </tbody>
    </table>
  </div>
);

export default function App() {
  const [currentStep, setCurrentStep] = useState(0);
  const [maxReached, setMaxReached] = useState(0);
  
  const [isProcessing, setIsProcessing] = useState(false);
  const [machine, setMachine] = useState("Select Machine");
  const [inputs, setInputs] = useState({});
  
  const [gbfsData, setGbfsData] = useState(null);
  const [psoData, setPsoData] = useState(null);
  const [decisionData, setDecisionData] = useState({});
  const [history, setHistory] = useState([]);
  const [logs, setLogs] = useState([]);

  const categoryMap = {
    "CNC Milling Machine": "Metal Fabrication",
    "Arc Welding Machine": "Welding Machines",
    "Plasma Cutting Machine": "Cutting Machines",
    "Conveyor Systems": "Assembly Line",
    "Electro-Deposition Coating System": "Painting Machines"
  };
  const taskMap = {
    "CNC Milling Machine": "Computation-Intensive",
    "Arc Welding Machine": "Latency-Sensitive",
    "Plasma Cutting Machine": "Computation-Intensive",
    "Conveyor Systems": "Latency-Sensitive",
    "Electro-Deposition Coating System": "Balanced"
  };

  const category = categoryMap[machine] || "";
  const autoTask = taskMap[machine] || "";

  const handleRun = () => {
    setIsProcessing(true);
    setTimeout(() => {
      // Mock params
      const params = {
        "Net Latency (ms)": Math.random() * 40 + 10,
        "CPU Load (%)": Math.random() * 45 + 50,
        "Task Queue": Math.random() * 9 + 1,
        "Power Usage (W)": Math.random() * 20 + 10,
        "Temperature (°C)": parseFloat(inputs["Temperature (°C)"] || Math.random()*20+40),
        "Task Type": autoTask
      };
      
      const gbfs = computeGbfsScore(params);
      const pso = computePsoScore(params);
      setGbfsData(gbfs);
      setPsoData(pso);

      let winner, server, reason;
      if (autoTask === "Latency-Sensitive") {
        winner = parseFloat(gbfs.latency) < parseFloat(pso.latency) ? "GBFS" : "PSO";
        reason = "it has a faster response (lower delay).";
        server = "Edge";
      } else if (autoTask === "Computation-Intensive") {
        winner = parseFloat(gbfs.throughput) > parseFloat(pso.throughput) ? "GBFS" : "PSO";
        reason = "it has higher processing speed.";
        server = "Cloud";
      } else {
        winner = parseFloat(gbfs.energy) < parseFloat(pso.energy) ? "GBFS" : "PSO";
        reason = "it has better energy efficiency.";
        server = parseFloat(pso.utilization) > 80 ? "Cloud" : "Edge";
      }
      
      setDecisionData({ winner, server, reason, taskType: autoTask });
      
      const newId = logs.length + 1;
      setHistory(prev => [...prev.slice(-10), { id: newId, gbfsLat: parseFloat(gbfs.latency), psoLat: parseFloat(pso.latency) }]);
      setLogs(prev => [...prev, {
        id: newId, category, type: autoTask, 
        delay: `${gbfs.latency}/${pso.latency}`,
        speed: `${gbfs.throughput}/${pso.throughput}`,
        winner, server, status: "SUCCESS"
      }]);

      setCurrentStep(1);
      setMaxReached(4);
      setIsProcessing(false);
    }, 800);
  };

  const renderStepContent = () => {
    switch(currentStep) {
      case 0:
        return (
          <div className="step-container">
            <div className="row-container">
              <OperationalMetricsPanel 
                {...{machine, setMachine, category, autoTask, inputs, setInputs, onRun: handleRun, isProcessing}}
              />
              <InputGuidePanel />
            </div>
          </div>
        );
      case 1:
        return (
          <div className="step-container">
            <div className="row-container">
              <AlgoPanel title="GBFS EVALUATION" colorClass="cyan-text" data={gbfsData} />
              <AlgoPanel title="PSO EVALUATION" colorClass="magenta-text" data={psoData} />
            </div>
          </div>
        );
      case 2:
        return (
          <div className="step-container">
            <div className="row-container">
              <ProcessingDecisionPanel decision={decisionData.server} reason={decisionData.reason} />
            </div>
            <div className="row-container">
              <ComparisonEvaluationPanel gbfs={gbfsData} pso={psoData} winner={decisionData.winner} />
              <InterpretationAnalysisPanel winner={decisionData.winner} server={decisionData.server} taskType={decisionData.taskType} />
            </div>
          </div>
        );
      case 3:
        return (
          <div className="step-container">
            <div className="row-container">
              <TaskAssignmentPanel taskType={decisionData.taskType} server={decisionData.server} summary={`${decisionData.winner} optimally assigned to ${decisionData.server} server.`} />
              <ResultTransmissionPanel />
            </div>
          </div>
        );
      case 4:
        return (
          <div className="step-container" style={{paddingBottom: "40px"}}>
            <PerformanceMonitoringPanel gbfs={gbfsData} pso={psoData} />
            <ExecutionLogsPanel logs={logs} />
          </div>
        );
      default: return null;
    }
  };

  return (
    <ErrorBoundary>
      <div className="dashboard-layout">
        <SidebarNavigation currentStep={currentStep} onJump={(i) => setCurrentStep(i)} />
        <div className="content-area">
          <SystemFlow currentStep={currentStep} maxReached={maxReached} onJump={(i) => setCurrentStep(i)} />
          <div className="main-content">
            {renderStepContent()}
          </div>
          <StepNavigation 
            currentStep={currentStep} maxReached={maxReached} 
            onPrev={() => setCurrentStep(prev => prev - 1)}
            onNext={() => setCurrentStep(prev => prev + 1)} 
          />
        </div>
      </div>
    </ErrorBoundary>
  );
}
