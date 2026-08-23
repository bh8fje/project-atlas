'use client';

import { useEffect, useState } from 'react';
import {
  isLanguagePreference,
  LANGUAGE_STORAGE_KEY,
  type Language,
  type LanguagePreference,
  resolveSystemLanguage,
  supportedLanguages,
  translations,
} from './i18n';

const milestoneVersions = ['v0.23.0', 'v0.22.0', 'v0.21.0', 'v0.19.0'];
const metricValues = ['23', '151', '22', '0'];

const Icon = ({ children }: { children: React.ReactNode }) => (
  <span className="nav-icon" aria-hidden="true">{children}</span>
);

function detectSystemLanguage(): Language {
  const candidates = navigator.languages.length ? navigator.languages : [navigator.language];
  return resolveSystemLanguage(candidates);
}

export default function Home() {
  const [preference, setPreference] = useState<LanguagePreference>('system');
  const [systemLanguage, setSystemLanguage] = useState<Language>('en');
  const [expandedPhase, setExpandedPhase] = useState<number | null>(0);
  const language = preference === 'system' ? systemLanguage : preference;
  const t = translations[language];

  useEffect(() => {
    const updateSystemLanguage = () => setSystemLanguage(detectSystemLanguage());
    updateSystemLanguage();
    try {
      const stored = localStorage.getItem(LANGUAGE_STORAGE_KEY);
      if (isLanguagePreference(stored)) setPreference(stored);
    } catch {
      // Browser privacy settings may disable storage; system following still works.
    }
    window.addEventListener('languagechange', updateSystemLanguage);
    return () => window.removeEventListener('languagechange', updateSystemLanguage);
  }, []);

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  const chooseLanguage = (nextPreference: LanguagePreference) => {
    setPreference(nextPreference);
    try {
      if (nextPreference === 'system') localStorage.removeItem(LANGUAGE_STORAGE_KEY);
      else localStorage.setItem(LANGUAGE_STORAGE_KEY, nextPreference);
    } catch {
      // The active choice still applies for this session when storage is unavailable.
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">A</span><span>Atlas</span></div>
        <nav aria-label={t.nav[0]}>
          <a className="nav-link active" href="#overview"><Icon>◫</Icon>{t.nav[0]}</a>
          <a className="nav-link" href="#history"><Icon>↗</Icon>{t.nav[1]}</a>
          <a className="nav-link" href="#relationships"><Icon>⌘</Icon>{t.nav[2]}</a>
          <a className="nav-link" href="#health"><Icon>◇</Icon>{t.nav[3]}</a>
          <a className="nav-link" href="#command-center"><Icon>›_</Icon>{t.nav[4]}</a>
        </nav>
        <div className="local-card">
          <span className="pulse" />
          <div><strong>{t.localOnly}</strong><small>{t.dataStays}</small></div>
        </div>
        <p className="sidebar-foot">Project Atlas · v0.23.0</p>
      </aside>

      <main className="content">
        <header className="topbar">
          <div><p className="eyebrow">{t.workspace}</p><h1>{t.greeting}</h1></div>
          <div className="topbar-actions">
            <label className="language-picker">
              <span>{t.selectLanguage}</span>
              <select value={preference} onChange={(event) => chooseLanguage(event.target.value as LanguagePreference)} aria-label={t.selectLanguage}>
                <option value="system">{t.followSystem}</option>
                {supportedLanguages.map((item) => <option value={item} key={item}>{translations[item].languageName}</option>)}
              </select>
            </label>
            <div className="status-chip"><span className="pulse" /> {t.planComplete}</div>
          </div>
        </header>

        <section id="overview" className="hero">
          <div>
            <p className="section-kicker">Project Atlas</p>
            <h2>{t.heroLead}<br /><em>{t.heroAccent}</em></h2>
            <p className="hero-copy">{t.heroCopy}</p>
          </div>
          <div className="hero-orbit" aria-label={t.graphSummary}>
            <span className="orbit orbit-one" /><span className="orbit orbit-two" />
            <span className="node node-core">Atlas</span>
            <span className="node node-a">151<small>{t.tests}</small></span>
            <span className="node node-b">23<small>{t.tasks}</small></span>
            <span className="node node-c">22<small>{t.decisionsShort}</small></span>
          </div>
        </section>

        <section className="mobile-glance" aria-label={t.mobileSummary}>
          <div><span className="pulse" /><strong>{t.systemsSteady}</strong></div>
          <span>151 {t.tests} · v0.23.0</span>
        </section>

        <section className="metrics" aria-label={t.metricsLabel}>
          {t.metrics.map(([label, detail], index) => <article key={label}><span>{label}</span><strong>{metricValues[index]}</strong><small>{detail}</small></article>)}
        </section>

        <div className="two-column">
          <section className="panel phase-panel">
            <div className="panel-heading"><div><p className="eyebrow">{t.executionPlan}</p><h3>{t.architectureEvolution}</h3></div><span>{t.phasesComplete}</span></div>
            <div className="phase-list">
              {t.phases.map((phase, index) => (
                <div className={`phase-card${expandedPhase === index ? ' expanded' : ''}`} key={phase.name}>
                  <button
                    className="phase-row"
                    type="button"
                    aria-expanded={expandedPhase === index}
                    aria-controls={`phase-details-${index}`}
                    aria-label={`${expandedPhase === index ? t.hidePhaseDetails : t.showPhaseDetails}: ${phase.name}`}
                    onClick={() => setExpandedPhase(expandedPhase === index ? null : index)}
                  >
                    <span className="phase-index">0{index}</span>
                    <span className="phase-detail"><span><strong>{phase.name}</strong><small>{t.complete}</small></span><span className="progress"><i style={{ width: '100%' }} /></span></span>
                    <span className="phase-toggle" aria-hidden="true">{expandedPhase === index ? '−' : '+'}</span>
                  </button>
                  {expandedPhase === index && (
                    <div className="phase-expanded" id={`phase-details-${index}`} role="region" aria-label={phase.name}>
                      <p>{phase.summary}</p>
                      <strong>{t.implementedFeatures}</strong>
                      <ul>{phase.features.map((feature) => <li key={feature}>{feature}</li>)}</ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>

          <section id="health" className="panel health-panel">
            <div className="panel-heading"><div><p className="eyebrow">{t.projectHealth}</p><h3>{t.everythingSteady}</h3></div><span className="score">A</span></div>
            <div className="health-ring"><div><strong>100%</strong><small>{t.testsPassing}</small></div></div>
            <div className="health-grid">
              <div><span>{t.workingTree}</span><strong>{t.clean}</strong></div>
              <div><span>{t.currentVersion}</span><strong>v0.23.0</strong></div>
              <div><span>{t.latestTask}</span><strong>TASK-023</strong></div>
              <div><span>{t.mode}</span><strong>{t.readOnly}</strong></div>
            </div>
          </section>
        </div>

        <section id="history" className="panel history-panel">
          <div className="panel-heading"><div><p className="eyebrow">{t.projectHistory}</p><h3>{t.recentMilestones}</h3></div><span>{t.annotatedReleases}</span></div>
          <div className="timeline">
            {t.milestones.map(([name, detail], index) => (
              <article key={milestoneVersions[index]}><span className="timeline-dot" /><time>{milestoneVersions[index]}</time><div><strong>{name}</strong><p>{detail}</p></div><span className="complete-mark">✓</span></article>
            ))}
          </div>
        </section>

        <section id="relationships" className="panel relationship-panel">
          <div className="panel-heading"><div><p className="eyebrow">{t.knowledgeMap}</p><h3>{t.howConnects}</h3></div><span>{t.typedRelationships}</span></div>
          <div className="relationship-map" aria-label={t.relationshipDiagram}>
            <div className="map-line line-one" /><div className="map-line line-two" /><div className="map-line line-three" />
            <div className="map-node main-node"><small>{t.project}</small><strong>Project Atlas</strong></div>
            <div className="map-node repository-node"><small>{t.repository}</small><strong>project-atlas</strong></div>
            <div className="map-node domain-node"><small>{t.domain}</small><strong>{t.coreModels}</strong></div>
            <div className="map-node memory-node"><small>{t.knowledge}</small><strong>{t.localMemory}</strong></div>
          </div>
          <p className="map-note">{t.mapNote}</p>
        </section>

        <section id="command-center" className="panel command-panel">
          <div className="panel-heading"><div><p className="eyebrow">{t.commandCenter}</p><h3>{t.controlBoundary}</h3></div><span>{t.auditable}</span></div>
          <div className="command-layout">
            <div className="command-terminal">
              <span className="terminal-prompt">atlas / command</span>
              <strong>{t.noHandlers}</strong>
              <p>{t.handlerNote}</p>
            </div>
            <div className="guardrails">
              {t.guardrails.map(([title, detail], index) => <div key={title}><span>0{index + 1}</span><p><strong>{title}</strong><small>{detail}</small></p></div>)}
            </div>
          </div>
        </section>
      </main>
      <nav className="mobile-nav" aria-label={t.mobileNavigation}>
        <a className="active" href="#overview"><span>◫</span>{t.nav[0]}</a>
        <a href="#history"><span>↗</span>{t.nav[1]}</a>
        <a href="#relationships"><span>⌘</span>{t.map}</a>
        <a href="#command-center"><span>›_</span>{t.nav[4]}</a>
      </nav>
    </div>
  );
}
