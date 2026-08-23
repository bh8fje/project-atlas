export const LANGUAGE_STORAGE_KEY = 'project-atlas-language';

export const supportedLanguages = ['zh', 'en', 'ru', 'ko'] as const;
export type Language = (typeof supportedLanguages)[number];
export type LanguagePreference = Language | 'system';

export type Translation = {
  languageName: string;
  followSystem: string;
  selectLanguage: string;
  nav: readonly [string, string, string, string, string];
  localOnly: string;
  dataStays: string;
  workspace: string;
  greeting: string;
  planComplete: string;
  heroLead: string;
  heroAccent: string;
  heroCopy: string;
  graphSummary: string;
  tests: string;
  tasks: string;
  decisionsShort: string;
  systemsSteady: string;
  mobileSummary: string;
  metricsLabel: string;
  metrics: readonly [readonly [string, string], readonly [string, string], readonly [string, string], readonly [string, string]];
  executionPlan: string;
  architectureEvolution: string;
  phasesComplete: string;
  phaseNames: readonly [string, string, string, string, string, string, string, string];
  complete: string;
  projectHealth: string;
  everythingSteady: string;
  testsPassing: string;
  workingTree: string;
  clean: string;
  currentVersion: string;
  latestTask: string;
  mode: string;
  readOnly: string;
  projectHistory: string;
  recentMilestones: string;
  annotatedReleases: string;
  milestones: readonly [readonly [string, string], readonly [string, string], readonly [string, string], readonly [string, string]];
  knowledgeMap: string;
  howConnects: string;
  typedRelationships: string;
  relationshipDiagram: string;
  project: string;
  repository: string;
  domain: string;
  coreModels: string;
  knowledge: string;
  localMemory: string;
  mapNote: string;
  commandCenter: string;
  controlBoundary: string;
  auditable: string;
  noHandlers: string;
  handlerNote: string;
  guardrails: readonly [readonly [string, string], readonly [string, string], readonly [string, string]];
  mobileNavigation: string;
  map: string;
};

export const translations: Record<Language, Translation> = {
  zh: {
    languageName: '中文', followSystem: '跟随系统', selectLanguage: '语言',
    nav: ['概览', '历史', '关系', '状态', '命令'],
    localOnly: '仅限本地', dataStays: '你的数据保留在这里', workspace: '项目工作区', greeting: '早上好。', planComplete: '执行计划 1.1 · 已完成',
    heroLead: '你的软件世界，', heroAccent: '在本地绘成地图。', heroCopy: '以平静、持久的方式了解项目是什么、如何变化，以及每个部分如何连接。', graphSummary: '项目关系图摘要',
    tests: '项测试', tasks: '项任务', decisionsShort: '项 ADR', systemsSteady: '所有系统稳定', mobileSummary: '移动端项目摘要', metricsLabel: '项目指标',
    metrics: [['里程碑', '已全部发布'], ['测试', '基线全部通过'], ['决策', '架构决策记录'], ['外部调用', '本地优先设计']],
    executionPlan: '执行计划', architectureEvolution: '架构演进', phasesComplete: '8 / 8 个阶段', phaseNames: ['工程基础', '项目发现', '项目记忆', '知识地图', 'AI 智能', '交互界面', '高级智能', '全球化体验'], complete: '已完成',
    projectHealth: '项目健康度', everythingSteady: '一切运行稳定', testsPassing: '测试通过', workingTree: '工作目录', clean: '干净', currentVersion: '当前版本', latestTask: '最近任务', mode: '模式', readOnly: '只读',
    projectHistory: '项目历史', recentMilestones: '最近里程碑', annotatedReleases: '带备注版本',
    milestones: [['多项目智能', '共同风险与项目组合关系'], ['命令中心', '具有可审计边界的显式命令'], ['AI 项目助手', '基于项目上下文的只读回答'], ['AI 项目理解', '供应商无关的分析契约']],
    knowledgeMap: '知识地图', howConnects: '项目如何连接', typedRelationships: '类型化关系', relationshipDiagram: '项目关系图', project: '项目', repository: '仓库', domain: '领域', coreModels: '核心模型', knowledge: '知识', localMemory: '本地记忆', mapNote: 'Project Atlas 领域、历史与知识关系的只读视图。',
    commandCenter: '命令中心', controlBoundary: '统一且显式的控制边界', auditable: '进程内 · 可审计', noHandlers: '尚未注册处理器', handlerNote: '只有宿主应用显式注册后，命令才会出现在这里。',
    guardrails: [['声明副作用', '每个命令都明确为只读或变更型。'], ['显式确认', '变更在确认前会被拒绝。'], ['结果可追踪', '请求 ID、时间、状态和输出均会保留。']], mobileNavigation: '移动端导航', map: '地图',
  },
  en: {
    languageName: 'English', followSystem: 'Follow system', selectLanguage: 'Language',
    nav: ['Overview', 'History', 'Relationships', 'Health', 'Commands'],
    localOnly: 'Local only', dataStays: 'Your data stays here', workspace: 'Project workspace', greeting: 'Good morning.', planComplete: 'Execution Plan 1.1 · Complete',
    heroLead: 'Your software world,', heroAccent: 'mapped locally.', heroCopy: 'A calm, durable view of what your project is, how it changed, and how every part connects.', graphSummary: 'Project graph summary',
    tests: 'tests', tasks: 'tasks', decisionsShort: 'ADRs', systemsSteady: 'All systems steady', mobileSummary: 'Mobile project summary', metricsLabel: 'Project metrics',
    metrics: [['Milestones', 'All published'], ['Tests', 'Passing baseline'], ['Decisions', 'Architecture records'], ['External calls', 'Local-first by design']],
    executionPlan: 'Execution plan', architectureEvolution: 'Architecture evolution', phasesComplete: '8 / 8 phases', phaseNames: ['Foundation', 'Discovery', 'Memory', 'Knowledge Map', 'AI Intelligence', 'Interface', 'Advanced Intelligence', 'Global Experience'], complete: 'Complete',
    projectHealth: 'Project health', everythingSteady: 'Everything is steady', testsPassing: 'tests passing', workingTree: 'Working tree', clean: 'Clean', currentVersion: 'Current version', latestTask: 'Latest task', mode: 'Mode', readOnly: 'Read only',
    projectHistory: 'Project history', recentMilestones: 'Recent milestones', annotatedReleases: 'Annotated releases',
    milestones: [['Multi Project Intelligence', 'Shared risks and portfolio relationships'], ['Command Center', 'Explicit commands with auditable guardrails'], ['AI Project Assistant', 'Read-only answers grounded in project context'], ['AI Project Understanding', 'Provider-neutral analysis contracts']],
    knowledgeMap: 'Knowledge map', howConnects: 'How the project connects', typedRelationships: 'Typed relationships', relationshipDiagram: 'Project relationship diagram', project: 'Project', repository: 'Repository', domain: 'Domain', coreModels: 'Core models', knowledge: 'Knowledge', localMemory: 'Local memory', mapNote: 'A read-only projection of Project Atlas’ domain, history, and knowledge relationships.',
    commandCenter: 'Command Center', controlBoundary: 'One explicit control boundary', auditable: 'In-process · Auditable', noHandlers: 'No handlers registered', handlerNote: 'Commands appear only when the host application explicitly registers them.',
    guardrails: [['Declared effects', 'Every command is read-only or mutating.'], ['Explicit confirmation', 'Mutations are rejected until confirmed.'], ['Traceable result', 'Request ID, time, status, and output are retained.']], mobileNavigation: 'Mobile navigation', map: 'Map',
  },
  ru: {
    languageName: 'Русский', followSystem: 'Как в системе', selectLanguage: 'Язык',
    nav: ['Обзор', 'История', 'Связи', 'Состояние', 'Команды'],
    localOnly: 'Только локально', dataStays: 'Ваши данные остаются здесь', workspace: 'Рабочее пространство', greeting: 'Доброе утро.', planComplete: 'План выполнения 1.1 · Завершён',
    heroLead: 'Ваш мир программ,', heroAccent: 'на локальной карте.', heroCopy: 'Спокойное и надёжное представление о проекте, его изменениях и связях между всеми частями.', graphSummary: 'Сводка графа проекта',
    tests: 'тестов', tasks: 'задач', decisionsShort: 'ADR', systemsSteady: 'Все системы стабильны', mobileSummary: 'Мобильная сводка проекта', metricsLabel: 'Метрики проекта',
    metrics: [['Этапы', 'Все опубликованы'], ['Тесты', 'Базовая проверка пройдена'], ['Решения', 'Архитектурные записи'], ['Внешние вызовы', 'Локальность по замыслу']],
    executionPlan: 'План выполнения', architectureEvolution: 'Развитие архитектуры', phasesComplete: '8 из 8 фаз', phaseNames: ['Основа', 'Обнаружение', 'Память', 'Карта знаний', 'ИИ-интеллект', 'Интерфейс', 'Расширенный интеллект', 'Глобальный опыт'], complete: 'Завершено',
    projectHealth: 'Состояние проекта', everythingSteady: 'Всё стабильно', testsPassing: 'тестов пройдено', workingTree: 'Рабочее дерево', clean: 'Чисто', currentVersion: 'Текущая версия', latestTask: 'Последняя задача', mode: 'Режим', readOnly: 'Только чтение',
    projectHistory: 'История проекта', recentMilestones: 'Последние этапы', annotatedReleases: 'Релизы с примечаниями',
    milestones: [['Интеллект нескольких проектов', 'Общие риски и связи портфеля'], ['Центр команд', 'Явные команды с проверяемыми ограничениями'], ['ИИ-помощник проекта', 'Ответы только для чтения на основе контекста'], ['ИИ-понимание проекта', 'Контракты анализа без привязки к провайдеру']],
    knowledgeMap: 'Карта знаний', howConnects: 'Как связан проект', typedRelationships: 'Типизированные связи', relationshipDiagram: 'Диаграмма связей проекта', project: 'Проект', repository: 'Репозиторий', domain: 'Домен', coreModels: 'Основные модели', knowledge: 'Знания', localMemory: 'Локальная память', mapNote: 'Представление домена, истории и связей знаний Project Atlas только для чтения.',
    commandCenter: 'Центр команд', controlBoundary: 'Единая явная граница управления', auditable: 'В процессе · Проверяемо', noHandlers: 'Обработчики не зарегистрированы', handlerNote: 'Команды появляются только после явной регистрации в основном приложении.',
    guardrails: [['Заявленные эффекты', 'Каждая команда доступна только для чтения или изменяет данные.'], ['Явное подтверждение', 'Изменения отклоняются до подтверждения.'], ['Прослеживаемый результат', 'ID запроса, время, статус и результат сохраняются.']], mobileNavigation: 'Мобильная навигация', map: 'Карта',
  },
  ko: {
    languageName: '한국어', followSystem: '시스템 설정 따르기', selectLanguage: '언어',
    nav: ['개요', '기록', '관계', '상태', '명령'],
    localOnly: '로컬 전용', dataStays: '데이터는 이 기기에 유지됩니다', workspace: '프로젝트 작업 공간', greeting: '좋은 아침입니다.', planComplete: '실행 계획 1.1 · 완료',
    heroLead: '소프트웨어 세계를,', heroAccent: '로컬에서 지도로.', heroCopy: '프로젝트의 현재 모습과 변화, 모든 구성 요소의 연결을 차분하고 지속적으로 보여 줍니다.', graphSummary: '프로젝트 그래프 요약',
    tests: '테스트', tasks: '작업', decisionsShort: 'ADR', systemsSteady: '모든 시스템 안정', mobileSummary: '모바일 프로젝트 요약', metricsLabel: '프로젝트 지표',
    metrics: [['마일스톤', '모두 게시됨'], ['테스트', '기준선 통과'], ['결정', '아키텍처 기록'], ['외부 호출', '로컬 우선 설계']],
    executionPlan: '실행 계획', architectureEvolution: '아키텍처 발전', phasesComplete: '8 / 8 단계', phaseNames: ['기반', '발견', '메모리', '지식 지도', 'AI 인텔리전스', '인터페이스', '고급 인텔리전스', '글로벌 경험'], complete: '완료',
    projectHealth: '프로젝트 상태', everythingSteady: '모든 것이 안정적입니다', testsPassing: '테스트 통과', workingTree: '작업 트리', clean: '깨끗함', currentVersion: '현재 버전', latestTask: '최근 작업', mode: '모드', readOnly: '읽기 전용',
    projectHistory: '프로젝트 기록', recentMilestones: '최근 마일스톤', annotatedReleases: '주석이 있는 릴리스',
    milestones: [['다중 프로젝트 인텔리전스', '공통 위험과 포트폴리오 관계'], ['명령 센터', '감사 가능한 보호 장치가 있는 명시적 명령'], ['AI 프로젝트 어시스턴트', '프로젝트 맥락에 근거한 읽기 전용 답변'], ['AI 프로젝트 이해', '공급자 중립적 분석 계약']],
    knowledgeMap: '지식 지도', howConnects: '프로젝트 연결 구조', typedRelationships: '유형이 지정된 관계', relationshipDiagram: '프로젝트 관계 다이어그램', project: '프로젝트', repository: '저장소', domain: '도메인', coreModels: '핵심 모델', knowledge: '지식', localMemory: '로컬 메모리', mapNote: 'Project Atlas의 도메인, 기록, 지식 관계를 보여 주는 읽기 전용 화면입니다.',
    commandCenter: '명령 센터', controlBoundary: '하나의 명시적 제어 경계', auditable: '프로세스 내부 · 감사 가능', noHandlers: '등록된 핸들러 없음', handlerNote: '호스트 애플리케이션이 명시적으로 등록한 명령만 표시됩니다.',
    guardrails: [['선언된 효과', '모든 명령은 읽기 전용 또는 변경형입니다.'], ['명시적 확인', '확인 전에는 변경이 거부됩니다.'], ['추적 가능한 결과', '요청 ID, 시간, 상태와 출력이 유지됩니다.']], mobileNavigation: '모바일 탐색', map: '지도',
  },
};

export function resolveSystemLanguage(languages: readonly string[]): Language {
  for (const rawLanguage of languages) {
    const language = rawLanguage.toLowerCase().split('-')[0];
    if (supportedLanguages.includes(language as Language)) return language as Language;
  }
  return 'en';
}

export function isLanguagePreference(value: string | null): value is LanguagePreference {
  return value === 'system' || supportedLanguages.includes(value as Language);
}
