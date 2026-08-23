const phases = [
  { name: 'Foundation', progress: '100%', state: 'Complete' },
  { name: 'Discovery', progress: '100%', state: 'Complete' },
  { name: 'Memory', progress: '100%', state: 'Complete' },
  { name: 'Knowledge Map', progress: '100%', state: 'Complete' },
  { name: 'AI Intelligence', progress: '100%', state: 'Complete' },
  { name: 'Interface', progress: '100%', state: 'Complete' },
  { name: 'Advanced Intelligence', progress: '100%', state: 'Complete' },
];

const milestones = [
  ['v0.19.0', 'Multi Project Intelligence', 'Shared risks and portfolio relationships'],
  ['v0.18.0', 'Command Center', 'Explicit commands with auditable guardrails'],
  ['v0.15.0', 'AI Project Assistant', 'Read-only answers grounded in project context'],
  ['v0.14.0', 'AI Project Understanding', 'Provider-neutral analysis contracts'],
];

const Icon = ({ children }: { children: React.ReactNode }) => (
  <span className="nav-icon" aria-hidden="true">{children}</span>
);

export default function Home() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">A</span><span>Atlas</span></div>
        <nav aria-label="Primary navigation">
          <a className="nav-link active" href="#overview"><Icon>◫</Icon>Overview</a>
          <a className="nav-link" href="#history"><Icon>↗</Icon>History</a>
          <a className="nav-link" href="#relationships"><Icon>⌘</Icon>Relationships</a>
          <a className="nav-link" href="#health"><Icon>◇</Icon>Health</a>
          <a className="nav-link" href="#command-center"><Icon>›_</Icon>Commands</a>
        </nav>
        <div className="local-card">
          <span className="pulse" />
          <div><strong>Local only</strong><small>Your data stays here</small></div>
        </div>
        <p className="sidebar-foot">Project Atlas · v0.20.0</p>
      </aside>

      <main className="content">
        <header className="topbar">
          <div><p className="eyebrow">Project workspace</p><h1>Good morning.</h1></div>
          <div className="status-chip"><span className="pulse" /> Execution Plan 1.0 · Complete</div>
        </header>

        <section id="overview" className="hero">
          <div>
            <p className="section-kicker">Project Atlas</p>
            <h2>Your software world,<br /><em>mapped locally.</em></h2>
            <p className="hero-copy">A calm, durable view of what your project is, how it changed, and how every part connects.</p>
          </div>
          <div className="hero-orbit" aria-label="Project graph summary">
            <span className="orbit orbit-one" /><span className="orbit orbit-two" />
            <span className="node node-core">Atlas</span>
            <span className="node node-a">138<small>tests</small></span>
            <span className="node node-b">20<small>tasks</small></span>
            <span className="node node-c">19<small>ADRs</small></span>
          </div>
        </section>

        <section className="mobile-glance" aria-label="Mobile project summary">
          <div><span className="pulse" /><strong>All systems steady</strong></div>
          <span>138 tests · v0.20.0</span>
        </section>

        <section className="metrics" aria-label="Project metrics">
          <article><span>Milestones</span><strong>20</strong><small>All published</small></article>
          <article><span>Tests</span><strong>138</strong><small>Passing baseline</small></article>
          <article><span>Decisions</span><strong>19</strong><small>Architecture records</small></article>
          <article><span>External calls</span><strong>0</strong><small>Local-first by design</small></article>
        </section>

        <div className="two-column">
          <section className="panel phase-panel">
            <div className="panel-heading"><div><p className="eyebrow">Execution plan</p><h3>Architecture evolution</h3></div><span>7 / 7 phases</span></div>
            <div className="phase-list">
              {phases.map((phase, index) => (
                <div className="phase-row" key={phase.name}>
                  <span className="phase-index">0{index}</span>
                  <div className="phase-detail"><div><strong>{phase.name}</strong><small>{phase.state}</small></div><div className="progress"><i style={{ width: phase.progress }} /></div></div>
                </div>
              ))}
            </div>
          </section>

          <section id="health" className="panel health-panel">
            <div className="panel-heading"><div><p className="eyebrow">Project health</p><h3>Everything is steady</h3></div><span className="score">A</span></div>
            <div className="health-ring"><div><strong>100%</strong><small>tests passing</small></div></div>
            <div className="health-grid">
              <div><span>Working tree</span><strong>Clean</strong></div>
              <div><span>Current version</span><strong>v0.20.0</strong></div>
              <div><span>Latest task</span><strong>TASK-020</strong></div>
              <div><span>Mode</span><strong>Read only</strong></div>
            </div>
          </section>
        </div>

        <section id="history" className="panel history-panel">
          <div className="panel-heading"><div><p className="eyebrow">Project history</p><h3>Recent milestones</h3></div><span>Annotated releases</span></div>
          <div className="timeline">
            {milestones.map(([version, name, detail]) => (
              <article key={version}><span className="timeline-dot" /><time>{version}</time><div><strong>{name}</strong><p>{detail}</p></div><span className="complete-mark">✓</span></article>
            ))}
          </div>
        </section>

        <section id="relationships" className="panel relationship-panel">
          <div className="panel-heading"><div><p className="eyebrow">Knowledge map</p><h3>How the project connects</h3></div><span>Typed relationships</span></div>
          <div className="relationship-map" aria-label="Project relationship diagram">
            <div className="map-line line-one" /><div className="map-line line-two" /><div className="map-line line-three" />
            <div className="map-node main-node"><small>Project</small><strong>Project Atlas</strong></div>
            <div className="map-node repository-node"><small>Repository</small><strong>project-atlas</strong></div>
            <div className="map-node domain-node"><small>Domain</small><strong>Core models</strong></div>
            <div className="map-node memory-node"><small>Knowledge</small><strong>Local memory</strong></div>
          </div>
          <p className="map-note">A read-only projection of Project Atlas’ domain, history, and knowledge relationships.</p>
        </section>

        <section id="command-center" className="panel command-panel">
          <div className="panel-heading"><div><p className="eyebrow">Command Center</p><h3>One explicit control boundary</h3></div><span>In-process · Auditable</span></div>
          <div className="command-layout">
            <div className="command-terminal">
              <span className="terminal-prompt">atlas / command</span>
              <strong>No handlers registered</strong>
              <p>Commands appear only when the host application explicitly registers them.</p>
            </div>
            <div className="guardrails">
              <div><span>01</span><p><strong>Declared effects</strong><small>Every command is read-only or mutating.</small></p></div>
              <div><span>02</span><p><strong>Explicit confirmation</strong><small>Mutations are rejected until confirmed.</small></p></div>
              <div><span>03</span><p><strong>Traceable result</strong><small>Request ID, time, status, and output are retained.</small></p></div>
            </div>
          </div>
        </section>
      </main>
      <nav className="mobile-nav" aria-label="Mobile navigation">
        <a className="active" href="#overview"><span>◫</span>Overview</a>
        <a href="#history"><span>↗</span>History</a>
        <a href="#relationships"><span>⌘</span>Map</a>
        <a href="#command-center"><span>›_</span>Commands</a>
      </nav>
    </div>
  );
}
