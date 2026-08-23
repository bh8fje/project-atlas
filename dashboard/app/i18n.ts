export const LANGUAGE_STORAGE_KEY = 'project-atlas-language';

export const supportedLanguages = ['zh', 'en', 'ru', 'ko'] as const;
export type Language = (typeof supportedLanguages)[number];
export type LanguagePreference = Language | 'system';

export type PhaseTranslation = {
  name: string;
  summary: string;
  features: readonly [string, string, string];
};

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
  phases: readonly [PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation];
  implementedFeatures: string;
  showPhaseDetails: string;
  hidePhaseDetails: string;
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

// Chinese is the source of meaning for product copy. Other languages translate it.
export const translations: Record<Language, Translation> = {
  zh: {
    languageName: '中文', followSystem: '跟随系统', selectLanguage: '语言',
    nav: ['概览', '历史', '关系', '状态', '操作'],
    localOnly: '仅限本地', dataStays: '你的数据只保存在这台设备上', workspace: '项目工作区', greeting: '早上好。', planComplete: '项目建设计划 1.3 · 已完成',
    heroLead: '你的软件世界，', heroAccent: '在本地绘成地图。', heroCopy: '以平静、持久的方式了解项目是什么、如何变化，以及每个部分如何连接。', graphSummary: '项目关系图摘要',
    tests: '项测试', tasks: '项任务', decisionsShort: '项说明', systemsSteady: '所有系统稳定', mobileSummary: '移动端项目摘要', metricsLabel: '项目指标',
    metrics: [['完成事项', '已全部发布'], ['检查', '全部通过'], ['重要设计', '都有说明'], ['联网次数', '不会把数据发出去']],
    executionPlan: '项目建设', architectureEvolution: '建设进度', phasesComplete: '8 / 8 个阶段',
    phases: [
      { name: '基础架构', summary: '建立项目运行、领域模型与工程规范的基础。', features: ['项目与任务基础模型', '代码仓库与项目资产模型', '测试、版本与开发规范'] },
      { name: '项目发现', summary: '识别本地项目并描述其组成。', features: ['按指定范围发现本地项目', '分析文件结构与技术栈', '生成稳定的项目标识与结构指纹'] },
      { name: '项目历史', summary: '记录项目状态、变化与演进过程。', features: ['项目快照与历史事件', '新增、删除与修改检测', '按时间整理项目演进记录'] },
      { name: '知识地图', summary: '整理项目资料以及项目内部和项目之间的关系。', features: ['项目关系图', '本地知识存储', '项目资料查询'] },
      { name: 'AI 项目分析', summary: '为 AI 准备项目资料，并提供结构化分析与问答。', features: ['构建并脱敏 AI 上下文', '生成结构化项目分析', '基于项目资料回答问题'] },
      { name: '交互界面', summary: '提供本地项目的查看与操作入口。', features: ['本地项目仪表板', '移动端适配', '统一操作入口与确认机制'] },
      { name: '智能项目管理', summary: '汇总多个项目的状态，并提供可追踪的提醒与建议。', features: ['多项目综合概览', '共同风险与项目关系汇总', '基于已有变化生成提醒与建议'] },
      { name: '多语言支持', summary: '提供含义一致的多语言界面体验。', features: ['支持中文、英语、俄语与韩语', '默认跟随系统并保存用户选择', '以专业清晰的中文统一各语言含义'] },
    ], implementedFeatures: '已实现功能', showPhaseDetails: '查看阶段详情', hidePhaseDetails: '收起阶段详情', complete: '已完成',
    projectHealth: '项目状态', everythingSteady: '一切运行稳定', testsPassing: '项检查通过', workingTree: '文件状态', clean: '没有未保存改动', currentVersion: '当前版本', latestTask: '最近完成', mode: '工作方式', readOnly: '只查看，不修改',
    projectHistory: '版本记录', recentMilestones: '最近完成的功能', annotatedReleases: '每个版本都有备注',
    milestones: [['建设阶段功能详情', '可展开每个阶段，查看已实现功能'], ['专业清晰的界面文案', '中文统一功能含义，其他语言保持一致'], ['多语言界面', '支持中文、英语、俄语和韩语，也可以跟随系统'], ['多项目综合概览', '汇总多个项目的共同风险与关系']],
    knowledgeMap: '项目关系', howConnects: '项目各部分怎么连接', typedRelationships: '每条关系都有说明', relationshipDiagram: '项目关系图', project: '项目', repository: '代码仓库', domain: '核心功能', coreModels: '基础规则', knowledge: '项目资料', localMemory: '本地记录', mapNote: '这里只展示项目结构、历史和关系，不会修改任何内容。',
    commandCenter: '操作中心', controlBoundary: '所有操作都从这里进入', auditable: '本机运行 · 全程留痕', noHandlers: '目前没有可用操作', handlerNote: '系统启用某项操作后，它才会显示在这里。',
    guardrails: [['说明是否修改数据', '每项操作都会说明它只查看还是会修改。'], ['修改前先确认', '没有得到确认，就不会修改任何内容。'], ['每次结果都有记录', '会记录操作编号、时间、结果和返回内容。']], mobileNavigation: '移动端导航', map: '关系',
  },
  en: {
    languageName: 'English', followSystem: 'Follow system', selectLanguage: 'Language',
    nav: ['Overview', 'History', 'Connections', 'Status', 'Actions'],
    localOnly: 'Local only', dataStays: 'Your data stays on this device', workspace: 'Project workspace', greeting: 'Good morning.', planComplete: 'Project Plan 1.3 · Complete',
    heroLead: 'Your software world,', heroAccent: 'mapped locally.', heroCopy: 'A calm, durable view of what your project is, how it changed, and how every part connects.', graphSummary: 'Project graph summary',
    tests: 'tests', tasks: 'tasks', decisionsShort: 'notes', systemsSteady: 'All systems steady', mobileSummary: 'Mobile project summary', metricsLabel: 'Project metrics',
    metrics: [['Completed work', 'All published'], ['Checks', 'All passing'], ['Key designs', 'All explained'], ['Network requests', 'No data is sent out']],
    executionPlan: 'Project development', architectureEvolution: 'Development progress', phasesComplete: '8 / 8 stages',
    phases: [
      { name: 'Core architecture', summary: 'Establish the project runtime, domain models, and engineering standards.', features: ['Core project and task models', 'Repository and project asset models', 'Testing, versioning, and development standards'] },
      { name: 'Project discovery', summary: 'Identify local projects and describe their composition.', features: ['Discover local projects within a defined scope', 'Analyze file structure and technology stack', 'Create stable project identities and structure fingerprints'] },
      { name: 'Project history', summary: 'Record project states, changes, and evolution.', features: ['Project snapshots and history events', 'Added, removed, and modified item detection', 'Chronological project evolution records'] },
      { name: 'Knowledge map', summary: 'Organize project information and connections within and between projects.', features: ['Project relationship graph', 'Local knowledge storage', 'Project information queries'] },
      { name: 'AI project analysis', summary: 'Prepare project information for AI and provide structured analysis and answers.', features: ['Build and redact AI context', 'Produce structured project analysis', 'Answer questions from project information'] },
      { name: 'User interface', summary: 'Provide local views and controlled project actions.', features: ['Local project dashboard', 'Mobile layout', 'Unified action entry and confirmation'] },
      { name: 'Intelligent project management', summary: 'Summarize multiple projects and provide traceable alerts and suggestions.', features: ['Multi-project overview', 'Shared risk and project relationship summary', 'Alerts and suggestions based on recorded changes'] },
      { name: 'Language support', summary: 'Provide a consistent interface in multiple languages.', features: ['Chinese, English, Russian, and Korean', 'Follow the system by default and save the user choice', 'Use clear professional Chinese as the meaning source'] },
    ], implementedFeatures: 'Implemented features', showPhaseDetails: 'View stage details', hidePhaseDetails: 'Hide stage details', complete: 'Complete',
    projectHealth: 'Project status', everythingSteady: 'Everything is running well', testsPassing: 'checks passing', workingTree: 'File status', clean: 'No unsaved changes', currentVersion: 'Current version', latestTask: 'Last completed', mode: 'How it works', readOnly: 'View only, no changes',
    projectHistory: 'Version history', recentMilestones: 'Recently completed features', annotatedReleases: 'Every version has a note',
    milestones: [['Development stage details', 'Expand each stage to review its implemented features'], ['Clear professional interface copy', 'Chinese defines the meaning consistently across all languages'], ['Multilingual interface', 'Use Chinese, English, Russian, or Korean, or follow the system'], ['Multi-project overview', 'Summarize shared risks and relationships across projects']],
    knowledgeMap: 'Project connections', howConnects: 'How the project parts connect', typedRelationships: 'Every connection is explained', relationshipDiagram: 'Project connections diagram', project: 'Project', repository: 'Code repository', domain: 'Main features', coreModels: 'Basic rules', knowledge: 'Project information', localMemory: 'Local records', mapNote: 'This view only shows project structure, history, and connections. It changes nothing.',
    commandCenter: 'Action center', controlBoundary: 'All actions start here', auditable: 'Runs locally · Fully recorded', noHandlers: 'No actions are available yet', handlerNote: 'An action appears here only after the system enables it.',
    guardrails: [['Says whether data changes', 'Every action says whether it only views or also changes data.'], ['Confirm before changes', 'Nothing changes until you confirm it.'], ['Every result is recorded', 'The action number, time, result, and returned information are recorded.']], mobileNavigation: 'Mobile navigation', map: 'Connections',
  },
  ru: {
    languageName: 'Русский', followSystem: 'Как в системе', selectLanguage: 'Язык',
    nav: ['Обзор', 'История', 'Связи', 'Состояние', 'Действия'],
    localOnly: 'Только локально', dataStays: 'Ваши данные остаются на этом устройстве', workspace: 'Рабочее пространство', greeting: 'Доброе утро.', planComplete: 'План проекта 1.3 · Завершён',
    heroLead: 'Ваш мир программ,', heroAccent: 'на локальной карте.', heroCopy: 'Спокойное и надёжное представление о проекте, его изменениях и связях между всеми частями.', graphSummary: 'Сводка графа проекта',
    tests: 'тестов', tasks: 'задач', decisionsShort: 'пояснений', systemsSteady: 'Все системы стабильны', mobileSummary: 'Мобильная сводка проекта', metricsLabel: 'Метрики проекта',
    metrics: [['Выполнено', 'Всё опубликовано'], ['Проверки', 'Все пройдены'], ['Важные решения', 'Для каждого есть пояснение'], ['Сетевые запросы', 'Данные не отправляются']],
    executionPlan: 'Развитие проекта', architectureEvolution: 'Ход работ', phasesComplete: '8 из 8 этапов',
    phases: [
      { name: 'Базовая архитектура', summary: 'Основа для работы проекта, доменных моделей и инженерных стандартов.', features: ['Модели проектов и задач', 'Модели репозиториев и активов', 'Тесты, версии и правила разработки'] },
      { name: 'Обнаружение проектов', summary: 'Поиск локальных проектов и описание их состава.', features: ['Поиск в заданной области', 'Анализ структуры и технологий', 'Стабильные идентификаторы и отпечатки'] },
      { name: 'История проекта', summary: 'Учёт состояний, изменений и развития проекта.', features: ['Снимки и события', 'Обнаружение добавлений, удалений и изменений', 'Хронология развития'] },
      { name: 'Карта знаний', summary: 'Упорядочивание данных и связей проекта.', features: ['Граф связей', 'Локальное хранение знаний', 'Поиск по данным проекта'] },
      { name: 'Анализ проекта с ИИ', summary: 'Подготовка данных для ИИ, структурированный анализ и ответы.', features: ['Подготовка и защита контекста', 'Структурированный анализ', 'Ответы по данным проекта'] },
      { name: 'Интерфейс', summary: 'Локальные экраны и управляемые действия.', features: ['Локальная панель', 'Мобильная верстка', 'Единая точка действий и подтверждение'] },
      { name: 'Интеллектуальное управление проектами', summary: 'Сводка по нескольким проектам и отслеживаемые рекомендации.', features: ['Обзор нескольких проектов', 'Общие риски и связи', 'Предупреждения и советы по зафиксированным изменениям'] },
      { name: 'Многоязычная поддержка', summary: 'Единый по смыслу интерфейс на нескольких языках.', features: ['Китайский, английский, русский и корейский', 'Язык системы по умолчанию и сохранение выбора', 'Ясный профессиональный китайский как основа смысла'] },
    ], implementedFeatures: 'Реализованные функции', showPhaseDetails: 'Показать этап', hidePhaseDetails: 'Скрыть этап', complete: 'Готово',
    projectHealth: 'Статус проекта', everythingSteady: 'Всё работает стабильно', testsPassing: 'проверок пройдено', workingTree: 'Состояние файлов', clean: 'Нет несохранённых изменений', currentVersion: 'Текущая версия', latestTask: 'Последнее выполненное', mode: 'Как работает', readOnly: 'Только просмотр',
    projectHistory: 'История версий', recentMilestones: 'Недавно готовые функции', annotatedReleases: 'У каждой версии есть примечание',
    milestones: [['Детали этапов развития', 'Каждый этап можно раскрыть и увидеть его функции'], ['Ясные профессиональные тексты', 'Китайский задаёт единый смысл для всех языков'], ['Многоязычный интерфейс', 'Китайский, английский, русский, корейский или язык системы'], ['Обзор нескольких проектов', 'Общие риски и связи между проектами']],
    knowledgeMap: 'Связи проекта', howConnects: 'Как связаны части проекта', typedRelationships: 'У каждой связи есть пояснение', relationshipDiagram: 'Схема связей проекта', project: 'Проект', repository: 'Репозиторий кода', domain: 'Основные функции', coreModels: 'Базовые правила', knowledge: 'Данные проекта', localMemory: 'Локальные записи', mapNote: 'Здесь показаны только структура, история и связи проекта. Ничего не изменяется.',
    commandCenter: 'Центр действий', controlBoundary: 'Все действия начинаются здесь', auditable: 'Работает локально · Всё записывается', noHandlers: 'Пока нет доступных действий', handlerNote: 'Действие появится здесь только после включения системой.',
    guardrails: [['Показывает, изменятся ли данные', 'У каждого действия указано, только смотрит оно данные или меняет их.'], ['Подтверждение перед изменением', 'Без подтверждения ничего не изменится.'], ['Каждый результат записывается', 'Сохраняются номер действия, время, результат и полученные данные.']], mobileNavigation: 'Мобильная навигация', map: 'Связи',
  },
  ko: {
    languageName: '한국어', followSystem: '시스템 설정 따르기', selectLanguage: '언어',
    nav: ['개요', '기록', '관계', '상태', '작업'],
    localOnly: '로컬 전용', dataStays: '데이터는 이 기기에만 저장됩니다', workspace: '프로젝트 작업 공간', greeting: '좋은 아침입니다.', planComplete: '프로젝트 계획 1.3 · 완료',
    heroLead: '소프트웨어 세계를,', heroAccent: '로컬에서 지도로.', heroCopy: '프로젝트의 현재 모습과 변화, 모든 구성 요소의 연결을 차분하고 지속적으로 보여 줍니다.', graphSummary: '프로젝트 그래프 요약',
    tests: '테스트', tasks: '작업', decisionsShort: '설명', systemsSteady: '모든 시스템 안정', mobileSummary: '모바일 프로젝트 요약', metricsLabel: '프로젝트 지표',
    metrics: [['완료한 일', '모두 게시됨'], ['점검', '모두 통과'], ['중요한 설계', '모두 설명됨'], ['네트워크 요청', '데이터를 밖으로 보내지 않음']],
    executionPlan: '프로젝트 개발', architectureEvolution: '개발 현황', phasesComplete: '8 / 8 단계',
    phases: [
      { name: '기반 아키텍처', summary: '프로젝트 실행, 도메인 모델, 개발 표준의 기반을 구축합니다.', features: ['프로젝트와 작업 기본 모델', '코드 저장소와 프로젝트 자산 모델', '테스트, 버전, 개발 규칙'] },
      { name: '프로젝트 탐색', summary: '로컬 프로젝트를 식별하고 구성을 설명합니다.', features: ['지정한 범위에서 로컬 프로젝트 탐색', '파일 구조와 기술 스택 분석', '안정적인 프로젝트 식별자와 구조 지문 생성'] },
      { name: '프로젝트 이력', summary: '프로젝트 상태, 변경, 발전 과정을 기록합니다.', features: ['프로젝트 스냅샷과 이력 이벤트', '추가·삭제·수정 감지', '시간순 프로젝트 발전 기록'] },
      { name: '지식 지도', summary: '프로젝트 자료와 내부·프로젝트 간 관계를 정리합니다.', features: ['프로젝트 관계 그래프', '로컬 지식 저장', '프로젝트 자료 조회'] },
      { name: 'AI 프로젝트 분석', summary: 'AI에 프로젝트 자료를 제공하고 구조화된 분석과 답변을 제공합니다.', features: ['AI 문맥 구성과 민감 정보 제거', '구조화된 프로젝트 분석', '프로젝트 자료 기반 질문 답변'] },
      { name: '사용자 인터페이스', summary: '로컬 프로젝트를 보고 제어할 수 있는 화면을 제공합니다.', features: ['로컬 프로젝트 대시보드', '모바일 화면', '통합 작업 진입점과 확인 절차'] },
      { name: '지능형 프로젝트 관리', summary: '여러 프로젝트를 요약하고 추적 가능한 알림과 제안을 제공합니다.', features: ['다중 프로젝트 종합 현황', '공통 위험과 프로젝트 관계 요약', '기록된 변화를 바탕으로 알림과 제안 생성'] },
      { name: '다국어 지원', summary: '여러 언어에서 의미가 일치하는 인터페이스를 제공합니다.', features: ['중국어, 영어, 러시아어, 한국어', '기본적으로 시스템 언어를 따르고 사용자 선택 저장', '명확하고 전문적인 중국어를 의미 기준으로 사용'] },
    ], implementedFeatures: '구현된 기능', showPhaseDetails: '단계 상세 보기', hidePhaseDetails: '단계 상세 접기', complete: '완료',
    projectHealth: '프로젝트 상태', everythingSteady: '모두 안정적으로 작동합니다', testsPassing: '개 점검 통과', workingTree: '파일 상태', clean: '저장하지 않은 변경 없음', currentVersion: '현재 버전', latestTask: '최근 완료', mode: '작동 방식', readOnly: '보기만 가능',
    projectHistory: '버전 기록', recentMilestones: '최근 완료한 기능', annotatedReleases: '모든 버전에 설명이 있음',
    milestones: [['개발 단계 기능 상세', '각 단계를 펼쳐 구현된 기능을 확인'], ['명확하고 전문적인 화면 문구', '중국어로 정한 의미를 모든 언어에 일관되게 적용'], ['다국어 인터페이스', '중국어, 영어, 러시아어, 한국어 또는 시스템 언어 사용'], ['다중 프로젝트 종합 현황', '여러 프로젝트의 공통 위험과 관계를 요약']],
    knowledgeMap: '프로젝트 관계', howConnects: '프로젝트 구성 요소의 연결 방식', typedRelationships: '모든 관계에 설명이 있음', relationshipDiagram: '프로젝트 관계 그림', project: '프로젝트', repository: '코드 저장소', domain: '주요 기능', coreModels: '기본 규칙', knowledge: '프로젝트 자료', localMemory: '로컬 기록', mapNote: '프로젝트 구조, 기록, 관계만 보여 주며 아무것도 변경하지 않습니다.',
    commandCenter: '작업 센터', controlBoundary: '모든 작업은 여기에서 시작', auditable: '기기에서 실행 · 모두 기록', noHandlers: '아직 사용할 수 있는 작업 없음', handlerNote: '시스템에서 기능을 켠 뒤에만 여기에 표시됩니다.',
    guardrails: [['데이터 변경 여부 안내', '각 작업이 보기만 하는지 데이터를 바꾸는지 알려 줍니다.'], ['변경 전 확인', '확인하기 전에는 아무것도 바뀌지 않습니다.'], ['모든 결과 기록', '작업 번호, 시간, 결과와 반환 내용을 기록합니다.']], mobileNavigation: '모바일 탐색', map: '관계',
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
