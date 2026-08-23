'use client';

import { useCallback, useEffect, useState } from 'react';

import type { Language, WorkspaceTranslation } from './i18n';


const LOCAL_SERVICE = 'http://127.0.0.1:43821';

type ProjectRow = {
  id: string;
  name: string;
  path: string;
  artifact_count: number;
  technologies: string[];
  change_status: 'added' | 'changed' | 'unchanged' | 'recorded';
};

type WorkspaceRow = {
  id: string;
  path: string;
  monitoring_enabled: boolean;
  scan_interval_minutes: number;
  added_at: string;
  last_scanned_at: string | null;
  projects: ProjectRow[];
  last_summary: {
    project_count: number;
    added: number;
    changed: number;
    removed: number;
  };
};

type WorkspaceResponse = { workspaces: WorkspaceRow[] };

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${LOCAL_SERVICE}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data as T;
}

export default function WorkspaceManager({ copy, language }: { copy: WorkspaceTranslation; language: Language }) {
  const [workspaces, setWorkspaces] = useState<WorkspaceRow[]>([]);
  const [connection, setConnection] = useState<'connecting' | 'ready' | 'unavailable'>('connecting');
  const [busy, setBusy] = useState<string | null>(null);
  const [message, setMessage] = useState('');

  const load = useCallback(async () => {
    try {
      const data = await request<WorkspaceResponse>('/api/workspaces');
      setWorkspaces(data.workspaces);
      setConnection('ready');
    } catch {
      setConnection('unavailable');
    }
  }, []);

  useEffect(() => {
    void load();
    const refresh = window.setInterval(() => { void load(); }, 10_000);
    return () => window.clearInterval(refresh);
  }, [load]);

  const chooseDirectory = async () => {
    setBusy('select');
    setMessage('');
    try {
      const data = await request<{ cancelled: boolean }>('/api/workspaces/select', {
        method: 'POST', body: JSON.stringify({ language, monitoring_enabled: false, scan_interval_minutes: 15 }),
      });
      if (!data.cancelled) setMessage(copy.initialScanComplete);
      await load();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : copy.operationFailed);
    } finally {
      setBusy(null);
    }
  };

  const scan = async (workspace: WorkspaceRow) => {
    setBusy(workspace.id);
    setMessage('');
    try {
      await request(`/api/workspaces/${workspace.id}/scan`, { method: 'POST', body: '{}' });
      setMessage(copy.scanComplete);
      await load();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : copy.operationFailed);
    } finally {
      setBusy(null);
    }
  };

  const setMonitoring = async (workspace: WorkspaceRow, enabled: boolean, interval = workspace.scan_interval_minutes) => {
    setBusy(workspace.id);
    setMessage('');
    try {
      await request(`/api/workspaces/${workspace.id}/monitoring`, {
        method: 'POST', body: JSON.stringify({ enabled, scan_interval_minutes: interval }),
      });
      await load();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : copy.operationFailed);
    } finally {
      setBusy(null);
    }
  };

  const remove = async (workspace: WorkspaceRow) => {
    if (!window.confirm(copy.confirmRemove)) return;
    setBusy(workspace.id);
    try {
      await request(`/api/workspaces/${workspace.id}`, { method: 'DELETE' });
      await load();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : copy.operationFailed);
    } finally {
      setBusy(null);
    }
  };

  const formatTime = (value: string | null) => value
    ? new Intl.DateTimeFormat(language, { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value))
    : copy.neverScanned;

  return (
    <section id="workspaces" className="panel workspace-panel">
      <div className="panel-heading workspace-heading">
        <div><p className="eyebrow">{copy.section}</p><h3>{copy.title}</h3><p className="workspace-intro">{copy.description}</p></div>
        <button className="primary-action" type="button" onClick={chooseDirectory} disabled={busy !== null || connection !== 'ready'}>{busy === 'select' ? copy.selecting : copy.chooseDirectory}</button>
      </div>

      {connection === 'connecting' && <div className="service-state">{copy.connecting}</div>}
      {connection === 'unavailable' && <div className="service-state warning"><strong>{copy.serviceUnavailable}</strong><span>{copy.serviceHelp}</span><button type="button" onClick={load}>{copy.retry}</button></div>}
      {connection === 'ready' && workspaces.length === 0 && <div className="workspace-empty"><strong>{copy.emptyTitle}</strong><p>{copy.emptyDescription}</p></div>}
      {message && <p className="workspace-message" role="status">{message}</p>}

      <div className="workspace-list">
        {workspaces.map((workspace) => (
          <article className="workspace-card" key={workspace.id}>
            <div className="workspace-card-head">
              <div><span>{copy.scanDirectory}</span><strong>{workspace.path}</strong><small>{copy.lastChecked}: {formatTime(workspace.last_scanned_at)}</small></div>
              <div className="workspace-actions"><button type="button" onClick={() => scan(workspace)} disabled={busy !== null}>{copy.scanNow}</button><button className="danger-action" type="button" onClick={() => remove(workspace)} disabled={busy !== null}>{copy.remove}</button></div>
            </div>
            <div className="monitor-controls">
              <label><input type="checkbox" checked={workspace.monitoring_enabled} onChange={(event) => setMonitoring(workspace, event.target.checked)} disabled={busy !== null} /> <span>{copy.automaticChecks}</span></label>
              <label><span>{copy.interval}</span><select value={workspace.scan_interval_minutes} onChange={(event) => setMonitoring(workspace, workspace.monitoring_enabled, Number(event.target.value))} disabled={busy !== null}>{[15, 30, 60].map((minutes) => <option value={minutes} key={minutes}>{minutes} {copy.minutes}</option>)}</select></label>
            </div>
            <div className="workspace-summary" aria-label={copy.latestChanges}>
              <span><strong>{workspace.last_summary.project_count}</strong>{copy.projectCount}</span>
              <span><strong>{workspace.last_summary.added}</strong>{copy.newProjects}</span>
              <span><strong>{workspace.last_summary.changed}</strong>{copy.changedProjects}</span>
              <span><strong>{workspace.last_summary.removed}</strong>{copy.removedProjects}</span>
            </div>
            <div className="project-list">
              <div className="project-list-title"><strong>{copy.discoveredProjects}</strong><span>{workspace.projects.length}</span></div>
              {workspace.projects.length === 0 && <p className="no-projects">{copy.noProjects}</p>}
              {workspace.projects.map((project) => (
                <div className="project-row" key={project.id}>
                  <div><strong>{project.name}</strong><small>{project.path}</small></div>
                  <div className="project-meta"><span className={`change-status ${project.change_status}`}>{copy.changeStatus[project.change_status]}</span><span>{project.technologies.join(' · ') || copy.unknownTechnology}</span><small>{project.artifact_count} {copy.items}</small></div>
                </div>
              ))}
            </div>
          </article>
        ))}
      </div>
      <p className="workspace-boundary">{copy.localBoundary}</p>
    </section>
  );
}
