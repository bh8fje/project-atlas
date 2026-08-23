export const LANGUAGE_STORAGE_KEY = 'project-atlas-language';

export const supportedLanguages = ['zh', 'en', 'ru', 'ko'] as const;
export type Language = (typeof supportedLanguages)[number];
export type LanguagePreference = Language | 'system';

export type PhaseTranslation = {
  name: string;
  summary: string;
  features: readonly [string, string, string];
};

export type WorkspaceTranslation = {
  section: string;
  title: string;
  description: string;
  chooseDirectory: string;
  selecting: string;
  connecting: string;
  serviceUnavailable: string;
  serviceHelp: string;
  retry: string;
  emptyTitle: string;
  emptyDescription: string;
  initialScanComplete: string;
  scanComplete: string;
  operationFailed: string;
  scanDirectory: string;
  lastChecked: string;
  neverScanned: string;
  scanNow: string;
  remove: string;
  confirmRemove: string;
  automaticChecks: string;
  interval: string;
  minutes: string;
  latestChanges: string;
  projectCount: string;
  newProjects: string;
  changedProjects: string;
  removedProjects: string;
  limitedProjects: string;
  discoveredProjects: string;
  noProjects: string;
  unknownTechnology: string;
  items: string;
  analysisLimited: string;
  assetCountUnavailable: string;
  changeStatus: Readonly<Record<'added' | 'changed' | 'unchanged' | 'recorded', string>>;
  localBoundary: string;
};

export type Translation = {
  languageName: string;
  followSystem: string;
  selectLanguage: string;
  nav: readonly [string, string, string, string, string, string];
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
  releaseVerifiedShort: string;
  mobileSummary: string;
  metricsLabel: string;
  localSource: string;
  metrics: readonly [readonly [string, string], readonly [string, string], readonly [string, string], readonly [string, string]];
  workspaceManager: WorkspaceTranslation;
  executionPlan: string;
  architectureEvolution: string;
  phasesComplete: string;
  phases: readonly [PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation, PhaseTranslation];
  implementedFeatures: string;
  showPhaseDetails: string;
  hidePhaseDetails: string;
  complete: string;
  releaseStatus: string;
  releaseVerified: string;
  releaseRecordNote: string;
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
  projectComposition: string;
  compositionTitle: string;
  compositionStatus: string;
  compositionDiagram: string;
  compositionRelations: readonly [string, string, string];
  project: string;
  repository: string;
  coreFeatures: string;
  coreModels: string;
  localData: string;
  localMemory: string;
  compositionNote: string;
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
    nav: ['概览', '历史', '组成', '状态', '操作', '项目目录'],
    localOnly: '仅限本地', dataStays: '你的数据只保存在这台设备上', workspace: '项目工作区', greeting: '项目概览', planComplete: '项目建设计划 1.5 · 已完成',
    heroLead: 'Project Atlas，', heroAccent: '本地项目知识系统。', heroCopy: '查看 Project Atlas 当前版本的建设进度、项目组成和发布记录。当前页面仅展示本地发布资料，不进行实时扫描或分析。', graphSummary: '当前版本摘要',
    tests: '项测试', tasks: '项任务', decisionsShort: '项说明', releaseVerifiedShort: '发布记录已验证', mobileSummary: '移动端发布摘要', metricsLabel: '发布记录指标', localSource: '本地',
    metrics: [['完成任务', '已记录'], ['自动测试', '最近一次全部通过'], ['设计说明', '可追溯'], ['数据来源', '当前页面使用本地发布记录']],
    workspaceManager: { section: '项目识别', title: '选择需要管理的目录', description: '选择一个本地目录，Project Atlas 将识别其中的软件项目。自动检查需要由你明确开启。', chooseDirectory: '选择目录', selecting: '等待选择…', connecting: '正在连接本地服务…', serviceUnavailable: '本地服务未启动', serviceHelp: '请先启动 Project Atlas 本地服务，然后重新连接。', retry: '重新连接', emptyTitle: '尚未添加项目目录', emptyDescription: '选择目录后将立即执行首次项目识别。', initialScanComplete: '目录已添加，首次项目识别已完成。', scanComplete: '项目检查已完成。', operationFailed: '操作失败。', scanDirectory: '扫描目录', lastChecked: '最近检查', neverScanned: '尚未检查', scanNow: '立即检查', remove: '移除', confirmRemove: '确定移除该目录及其本地检查记录吗？目录中的文件不会被删除。', automaticChecks: '自动检查', interval: '检查间隔', minutes: '分钟', latestChanges: '最近一次检查结果', projectCount: '个项目', newProjects: '个新增', changedProjects: '个变化', removedProjects: '个移除', limitedProjects: '个受限', discoveredProjects: '已识别项目', noProjects: '当前目录中未识别到软件项目。', unknownTechnology: '技术栈未识别', items: '个资产', analysisLimited: '项目规模超过当前检查范围', assetCountUnavailable: '资产数量未统计', changeStatus: { added: '新增', changed: '有变化', unchanged: '无变化', recorded: '已记录' }, localBoundary: '目录路径、项目资料与检查记录只保存在本机。关闭本地服务后，自动检查将停止。' },
    executionPlan: '项目建设', architectureEvolution: '建设进度', phasesComplete: '9 / 9 个阶段',
    phases: [
      { name: '基础架构', summary: '建立项目运行、领域模型与工程规范的基础。', features: ['项目与任务基础模型', '代码仓库与项目资产模型', '测试、版本与开发规范'] },
      { name: '项目发现', summary: '识别本地项目并描述其组成。', features: ['选择并管理本地扫描目录', '识别项目、文件结构与技术栈', '生成结构指纹并定时检查变化'] },
      { name: '项目历史', summary: '记录项目状态、变化与演进过程。', features: ['项目快照与历史事件', '新增、删除与修改检测', '按时间整理项目演进记录'] },
      { name: '知识地图', summary: '整理项目资料以及项目内部和项目之间的关系。', features: ['项目关系图', '本地知识存储', '项目资料查询'] },
      { name: 'AI 项目分析', summary: '为 AI 准备项目资料，并提供结构化分析与问答。', features: ['构建并脱敏 AI 上下文', '生成结构化项目分析', '基于项目资料回答问题'] },
      { name: '交互界面', summary: '提供本地项目的查看与操作入口。', features: ['本地项目仪表板', '移动端适配', '统一操作入口与确认机制'] },
      { name: '智能项目管理', summary: '汇总多个项目的状态，并提供可追踪的提醒与建议。', features: ['多项目综合概览', '共同风险与项目关系汇总', '基于已有变化生成提醒与建议'] },
      { name: '多语言支持', summary: '提供含义一致的多语言界面体验。', features: ['支持中文、英语、俄语与韩语', '默认跟随系统并保存用户选择', '以专业清晰的中文统一各语言含义'] },
      { name: '本地运行管理', summary: '管理本地扫描目录和项目结构检查。', features: ['通过系统选择器登记扫描目录', '执行首次识别与手动检查', '明确开启并设置定时检查间隔'] },
    ], implementedFeatures: '已实现功能', showPhaseDetails: '查看阶段详情', hidePhaseDetails: '收起阶段详情', complete: '已完成',
    releaseStatus: '版本状态', releaseVerified: '当前发布已通过验证', releaseRecordNote: '以下内容来自最近一次发布记录，不是实时监控结果。', testsPassing: '项测试通过', workingTree: '发布时文件状态', clean: '无未提交改动', currentVersion: '当前版本', latestTask: '最近完成', mode: '界面模式', readOnly: '本机运行',
    projectHistory: '版本记录', recentMilestones: '最近完成的功能', annotatedReleases: '每个版本都有备注',
    milestones: [['超大项目不中断目录识别', '超过检查范围的项目明确标记为受限，其他项目继续识别'], ['本地项目目录管理', '选择扫描目录，识别项目并按设定间隔检查变化'], ['明确的项目组成与发布记录', '区分项目组成、项目关系与实时分析'], ['建设阶段功能详情', '可展开每个阶段，查看已实现功能']],
    projectComposition: '项目组成', compositionTitle: 'Project Atlas 包含哪些部分', compositionStatus: '当前版本示意', compositionDiagram: 'Project Atlas 项目组成图', compositionRelations: ['源代码存放于', '包含', '项目资料保存在本机'], project: '项目', repository: '代码仓库', coreFeatures: '核心功能', coreModels: '领域模型与服务', localData: '本地资料', localMemory: '项目记录与知识', compositionNote: '这是当前版本的项目组成示意，不是自动扫描或实时分析结果。',
    commandCenter: '操作中心', controlBoundary: '所有操作都从这里进入', auditable: '本机运行 · 全程留痕', noHandlers: '目前没有可用操作', handlerNote: '系统启用某项操作后，它才会显示在这里。',
    guardrails: [['说明是否修改数据', '每项操作都会说明它只查看还是会修改。'], ['修改前先确认', '没有得到确认，就不会修改任何内容。'], ['每次结果都有记录', '会记录操作编号、时间、结果和返回内容。']], mobileNavigation: '移动端导航', map: '组成',
  },
  en: {
    languageName: 'English', followSystem: 'Follow system', selectLanguage: 'Language',
    nav: ['Overview', 'History', 'Composition', 'Status', 'Actions', 'Project folders'],
    localOnly: 'Local only', dataStays: 'Your data stays on this device', workspace: 'Project workspace', greeting: 'Project overview', planComplete: 'Project Plan 1.5 · Complete',
    heroLead: 'Project Atlas,', heroAccent: 'a local project knowledge system.', heroCopy: 'Review the current version’s development progress, project composition, and release history. This page uses local release records and does not perform real-time scanning or analysis.', graphSummary: 'Current version summary',
    tests: 'tests', tasks: 'tasks', decisionsShort: 'notes', releaseVerifiedShort: 'Release record verified', mobileSummary: 'Mobile release summary', metricsLabel: 'Release record metrics', localSource: 'Local',
    metrics: [['Completed tasks', 'Recorded'], ['Automated tests', 'Last run passed'], ['Design notes', 'Traceable'], ['Data source', 'Local release records']],
    workspaceManager: { section: 'Project discovery', title: 'Choose folders to manage', description: 'Choose a local folder and Project Atlas will identify the software projects inside it. Automatic checks start only when you enable them.', chooseDirectory: 'Choose folder', selecting: 'Waiting for selection…', connecting: 'Connecting to the local service…', serviceUnavailable: 'Local service is not running', serviceHelp: 'Start the Project Atlas local service, then reconnect.', retry: 'Reconnect', emptyTitle: 'No project folders added', emptyDescription: 'Choosing a folder runs the first project discovery immediately.', initialScanComplete: 'Folder added and initial project discovery completed.', scanComplete: 'Project check completed.', operationFailed: 'The operation failed.', scanDirectory: 'Scan folder', lastChecked: 'Last checked', neverScanned: 'Not checked yet', scanNow: 'Check now', remove: 'Remove', confirmRemove: 'Remove this folder and its local check records? Files in the folder will not be deleted.', automaticChecks: 'Automatic checks', interval: 'Check interval', minutes: 'minutes', latestChanges: 'Latest check result', projectCount: 'projects', newProjects: 'new', changedProjects: 'changed', removedProjects: 'removed', limitedProjects: 'limited', discoveredProjects: 'Discovered projects', noProjects: 'No software projects were identified in this folder.', unknownTechnology: 'Technology not identified', items: 'assets', analysisLimited: 'Project size exceeds the current check scope', assetCountUnavailable: 'Asset count unavailable', changeStatus: { added: 'New', changed: 'Changed', unchanged: 'Unchanged', recorded: 'Recorded' }, localBoundary: 'Folder paths, project information, and check records stay on this device. Automatic checks stop when the local service is closed.' },
    executionPlan: 'Project development', architectureEvolution: 'Development progress', phasesComplete: '9 / 9 stages',
    phases: [
      { name: 'Core architecture', summary: 'Establish the project runtime, domain models, and engineering standards.', features: ['Core project and task models', 'Repository and project asset models', 'Testing, versioning, and development standards'] },
      { name: 'Project discovery', summary: 'Identify local projects and describe their composition.', features: ['Choose and manage local scan folders', 'Identify projects, file structures, and technologies', 'Create structure fingerprints and check changes on schedule'] },
      { name: 'Project history', summary: 'Record project states, changes, and evolution.', features: ['Project snapshots and history events', 'Added, removed, and modified item detection', 'Chronological project evolution records'] },
      { name: 'Knowledge map', summary: 'Organize project information and connections within and between projects.', features: ['Project relationship graph', 'Local knowledge storage', 'Project information queries'] },
      { name: 'AI project analysis', summary: 'Prepare project information for AI and provide structured analysis and answers.', features: ['Build and redact AI context', 'Produce structured project analysis', 'Answer questions from project information'] },
      { name: 'User interface', summary: 'Provide local views and controlled project actions.', features: ['Local project dashboard', 'Mobile layout', 'Unified action entry and confirmation'] },
      { name: 'Intelligent project management', summary: 'Summarize multiple projects and provide traceable alerts and suggestions.', features: ['Multi-project overview', 'Shared risk and project relationship summary', 'Alerts and suggestions based on recorded changes'] },
      { name: 'Language support', summary: 'Provide a consistent interface in multiple languages.', features: ['Chinese, English, Russian, and Korean', 'Follow the system by default and save the user choice', 'Use clear professional Chinese as the meaning source'] },
      { name: 'Local operations', summary: 'Manage local scan folders and project structure checks.', features: ['Register scan folders through the system picker', 'Run initial discovery and manual checks', 'Explicitly enable and schedule automatic checks'] },
    ], implementedFeatures: 'Implemented features', showPhaseDetails: 'View stage details', hidePhaseDetails: 'Hide stage details', complete: 'Complete',
    releaseStatus: 'Release status', releaseVerified: 'Current release passed validation', releaseRecordNote: 'The information below comes from the latest release record. It is not real-time monitoring.', testsPassing: 'tests passed', workingTree: 'File status at release', clean: 'No uncommitted changes', currentVersion: 'Current version', latestTask: 'Last completed', mode: 'Interface mode', readOnly: 'Local operation',
    projectHistory: 'Version history', recentMilestones: 'Recently completed features', annotatedReleases: 'Every version has a note',
    milestones: [['Oversized projects no longer stop folder discovery', 'Projects beyond the check scope are marked as limited while other projects continue'], ['Local project folder management', 'Choose scan folders, identify projects, and check changes on schedule'], ['Clear project composition and release records', 'Distinguishes composition, project relationships, and real-time analysis'], ['Development stage details', 'Expand each stage to review its implemented features']],
    projectComposition: 'Project composition', compositionTitle: 'What Project Atlas contains', compositionStatus: 'Current version illustration', compositionDiagram: 'Project Atlas composition diagram', compositionRelations: ['Source code is stored in', 'Contains', 'Project information is stored locally'], project: 'Project', repository: 'Code repository', coreFeatures: 'Core features', coreModels: 'Domain models and services', localData: 'Local information', localMemory: 'Project records and knowledge', compositionNote: 'This illustrates the current version’s composition. It is not an automatic scan or real-time analysis.',
    commandCenter: 'Action center', controlBoundary: 'All actions start here', auditable: 'Runs locally · Fully recorded', noHandlers: 'No actions are available yet', handlerNote: 'An action appears here only after the system enables it.',
    guardrails: [['Says whether data changes', 'Every action says whether it only views or also changes data.'], ['Confirm before changes', 'Nothing changes until you confirm it.'], ['Every result is recorded', 'The action number, time, result, and returned information are recorded.']], mobileNavigation: 'Mobile navigation', map: 'Composition',
  },
  ru: {
    languageName: 'Русский', followSystem: 'Как в системе', selectLanguage: 'Язык',
    nav: ['Обзор', 'История', 'Состав', 'Статус', 'Действия', 'Папки проектов'],
    localOnly: 'Только локально', dataStays: 'Ваши данные остаются на этом устройстве', workspace: 'Рабочее пространство', greeting: 'Обзор проекта', planComplete: 'План проекта 1.5 · Завершён',
    heroLead: 'Project Atlas —', heroAccent: 'локальная система знаний о проектах.', heroCopy: 'Обзор хода разработки, состава проекта и истории релизов. Страница использует локальные записи и не выполняет сканирование или анализ в реальном времени.', graphSummary: 'Сводка текущей версии',
    tests: 'тестов', tasks: 'задач', decisionsShort: 'пояснений', releaseVerifiedShort: 'Запись релиза проверена', mobileSummary: 'Мобильная сводка релиза', metricsLabel: 'Показатели релиза', localSource: 'Локально',
    metrics: [['Завершённые задачи', 'Записаны'], ['Автотесты', 'Последний запуск пройден'], ['Пояснения по дизайну', 'Прослеживаются'], ['Источник данных', 'Локальные записи релиза']],
    workspaceManager: { section: 'Обнаружение проектов', title: 'Выберите папки для управления', description: 'Выберите локальную папку, и Project Atlas найдёт в ней программные проекты. Автоматические проверки включаются только вами.', chooseDirectory: 'Выбрать папку', selecting: 'Ожидание выбора…', connecting: 'Подключение к локальной службе…', serviceUnavailable: 'Локальная служба не запущена', serviceHelp: 'Запустите локальную службу Project Atlas и повторите подключение.', retry: 'Подключиться снова', emptyTitle: 'Папки проектов не добавлены', emptyDescription: 'Первый поиск проектов начнётся сразу после выбора папки.', initialScanComplete: 'Папка добавлена, первый поиск завершён.', scanComplete: 'Проверка проектов завершена.', operationFailed: 'Операция не выполнена.', scanDirectory: 'Папка сканирования', lastChecked: 'Последняя проверка', neverScanned: 'Ещё не проверялась', scanNow: 'Проверить', remove: 'Удалить', confirmRemove: 'Удалить эту папку и её локальные записи? Файлы в папке не будут удалены.', automaticChecks: 'Автоматические проверки', interval: 'Интервал', minutes: 'минут', latestChanges: 'Результат последней проверки', projectCount: 'проектов', newProjects: 'новых', changedProjects: 'изменено', removedProjects: 'удалено', limitedProjects: 'ограничено', discoveredProjects: 'Найденные проекты', noProjects: 'В этой папке не найдены программные проекты.', unknownTechnology: 'Технологии не определены', items: 'объектов', analysisLimited: 'Размер проекта превышает текущий объём проверки', assetCountUnavailable: 'Число объектов не определено', changeStatus: { added: 'Новый', changed: 'Изменён', unchanged: 'Без изменений', recorded: 'Записан' }, localBoundary: 'Пути к папкам, данные проектов и записи проверок остаются на этом устройстве. Автопроверки остановятся после закрытия локальной службы.' },
    executionPlan: 'Развитие проекта', architectureEvolution: 'Ход работ', phasesComplete: '9 из 9 этапов',
    phases: [
      { name: 'Базовая архитектура', summary: 'Основа для работы проекта, доменных моделей и инженерных стандартов.', features: ['Модели проектов и задач', 'Модели репозиториев и активов', 'Тесты, версии и правила разработки'] },
      { name: 'Обнаружение проектов', summary: 'Поиск локальных проектов и описание их состава.', features: ['Выбор и управление папками сканирования', 'Поиск проектов, структур и технологий', 'Отпечатки структуры и плановая проверка изменений'] },
      { name: 'История проекта', summary: 'Учёт состояний, изменений и развития проекта.', features: ['Снимки и события', 'Обнаружение добавлений, удалений и изменений', 'Хронология развития'] },
      { name: 'Карта знаний', summary: 'Упорядочивание данных и связей проекта.', features: ['Граф связей', 'Локальное хранение знаний', 'Поиск по данным проекта'] },
      { name: 'Анализ проекта с ИИ', summary: 'Подготовка данных для ИИ, структурированный анализ и ответы.', features: ['Подготовка и защита контекста', 'Структурированный анализ', 'Ответы по данным проекта'] },
      { name: 'Интерфейс', summary: 'Локальные экраны и управляемые действия.', features: ['Локальная панель', 'Мобильная верстка', 'Единая точка действий и подтверждение'] },
      { name: 'Интеллектуальное управление проектами', summary: 'Сводка по нескольким проектам и отслеживаемые рекомендации.', features: ['Обзор нескольких проектов', 'Общие риски и связи', 'Предупреждения и советы по зафиксированным изменениям'] },
      { name: 'Многоязычная поддержка', summary: 'Единый по смыслу интерфейс на нескольких языках.', features: ['Китайский, английский, русский и корейский', 'Язык системы по умолчанию и сохранение выбора', 'Ясный профессиональный китайский как основа смысла'] },
      { name: 'Локальное управление', summary: 'Управление папками сканирования и проверками структуры.', features: ['Выбор папок через системный диалог', 'Первый поиск и ручные проверки', 'Явное включение и настройка плановых проверок'] },
    ], implementedFeatures: 'Реализованные функции', showPhaseDetails: 'Показать этап', hidePhaseDetails: 'Скрыть этап', complete: 'Готово',
    releaseStatus: 'Статус релиза', releaseVerified: 'Текущий релиз прошёл проверку', releaseRecordNote: 'Сведения ниже взяты из последней записи релиза. Это не мониторинг в реальном времени.', testsPassing: 'тестов пройдено', workingTree: 'Файлы при релизе', clean: 'Нет незафиксированных изменений', currentVersion: 'Текущая версия', latestTask: 'Последнее выполненное', mode: 'Режим интерфейса', readOnly: 'Локальная работа',
    projectHistory: 'История версий', recentMilestones: 'Недавно готовые функции', annotatedReleases: 'У каждой версии есть примечание',
    milestones: [['Большие проекты не останавливают поиск', 'Проекты за пределами проверки отмечаются как ограниченные, остальные продолжают обрабатываться'], ['Управление локальными папками проектов', 'Выбор папок, поиск проектов и плановая проверка изменений'], ['Ясный состав проекта и записи релизов', 'Состав, связи проектов и анализ в реальном времени разделены'], ['Детали этапов развития', 'Каждый этап можно раскрыть и увидеть его функции']],
    projectComposition: 'Состав проекта', compositionTitle: 'Из чего состоит Project Atlas', compositionStatus: 'Схема текущей версии', compositionDiagram: 'Схема состава Project Atlas', compositionRelations: ['Исходный код хранится в', 'Содержит', 'Данные проекта хранятся локально'], project: 'Проект', repository: 'Репозиторий кода', coreFeatures: 'Основные функции', coreModels: 'Доменные модели и сервисы', localData: 'Локальные данные', localMemory: 'Записи и знания проекта', compositionNote: 'Это схема состава текущей версии, а не результат автоматического сканирования или анализа в реальном времени.',
    commandCenter: 'Центр действий', controlBoundary: 'Все действия начинаются здесь', auditable: 'Работает локально · Всё записывается', noHandlers: 'Пока нет доступных действий', handlerNote: 'Действие появится здесь только после включения системой.',
    guardrails: [['Показывает, изменятся ли данные', 'У каждого действия указано, только смотрит оно даные или меняет их.'], ['Подтверждение перед изменением', 'Без подтверждения ничего не изменится.'], ['Каждый результат записывается', 'Сохраняются номер действия, время, результат и полученные данные.']], mobileNavigation: 'Мобильная навигация', map: 'Состав',
  },
  ko: {
    languageName: '한국어', followSystem: '시스템 설정 따르기', selectLanguage: '언어',
    nav: ['개요', '기록', '구성', '상태', '작업', '프로젝트 폴더'],
    localOnly: '로컬 전용', dataStays: '데이터는 이 기기에만 저장됩니다', workspace: '프로젝트 작업 공간', greeting: '프로젝트 개요', planComplete: '프로젝트 계획 1.5 · 완료',
    heroLead: 'Project Atlas,', heroAccent: '로컬 프로젝트 지식 시스템.', heroCopy: '현재 버전의 개발 현황, 프로젝트 구성, 릴리스 기록을 확인합니다. 이 화면은 로컬 릴리스 기록을 사용하며 실시간 스캔이나 분석을 하지 않습니다.', graphSummary: '현재 버전 요약',
    tests: '테스트', tasks: '작업', decisionsShort: '설명', releaseVerifiedShort: '릴리스 기록 검증 완료', mobileSummary: '모바일 릴리스 요약', metricsLabel: '릴리스 기록 지표', localSource: '로컬',
    metrics: [['완료한 작업', '기록됨'], ['자동 테스트', '최근 실행 통과'], ['설계 설명', '추적 가능'], ['데이터 출처', '로컬 릴리스 기록']],
    workspaceManager: { section: '프로젝트 탐색', title: '관리할 폴더 선택', description: '로컬 폴더를 선택하면 Project Atlas가 그 안의 소프트웨어 프로젝트를 식별합니다. 자동 점검은 사용자가 직접 켜야 시작됩니다.', chooseDirectory: '폴더 선택', selecting: '선택 대기 중…', connecting: '로컬 서비스에 연결 중…', serviceUnavailable: '로컬 서비스가 실행 중이 아닙니다', serviceHelp: 'Project Atlas 로컬 서비스를 시작한 다음 다시 연결하세요.', retry: '다시 연결', emptyTitle: '추가된 프로젝트 폴더가 없습니다', emptyDescription: '폴더를 선택하면 첫 프로젝트 탐색이 즉시 실행됩니다.', initialScanComplete: '폴더가 추가되었고 첫 프로젝트 탐색이 완료되었습니다.', scanComplete: '프로젝트 점검이 완료되었습니다.', operationFailed: '작업을 완료하지 못했습니다.', scanDirectory: '스캔 폴더', lastChecked: '최근 점검', neverScanned: '아직 점검하지 않음', scanNow: '지금 점검', remove: '제거', confirmRemove: '이 폴더와 로컬 점검 기록을 제거할까요? 폴더의 파일은 삭제되지 않습니다.', automaticChecks: '자동 점검', interval: '점검 간격', minutes: '분', latestChanges: '최근 점검 결과', projectCount: '개 프로젝트', newProjects: '개 추가', changedProjects: '개 변경', removedProjects: '개 제거', limitedProjects: '개 제한', discoveredProjects: '식별된 프로젝트', noProjects: '이 폴더에서 소프트웨어 프로젝트를 식별하지 못했습니다.', unknownTechnology: '기술 스택 미식별', items: '개 자산', analysisLimited: '프로젝트 규모가 현재 점검 범위를 초과함', assetCountUnavailable: '자산 수 미집계', changeStatus: { added: '추가됨', changed: '변경됨', unchanged: '변경 없음', recorded: '기록됨' }, localBoundary: '폴더 경로, 프로젝트 정보, 점검 기록은 이 기기에만 저장됩니다. 로컬 서비스를 종료하면 자동 점검도 멈춥니다.' },
    executionPlan: '프로젝트 개발', architectureEvolution: '개발 현황', phasesComplete: '9 / 9 단계',
    phases: [
      { name: '기반 아키텍처', summary: '프로젝트 실행, 도메인 모델, 개발 표준의 기반을 구축합니다.', features: ['프로젝트와 작업 기본 모델', '코드 저장소와 프로젝트 자산 모델', '테스트, 버전, 개발 규칙'] },
      { name: '프로젝트 탐색', summary: '로컬 프로젝트를 식별하고 구성을 설명합니다.', features: ['로컬 스캔 폴더 선택 및 관리', '프로젝트, 파일 구조, 기술 스택 식별', '구조 지문 생성 및 정기 변경 점검'] },
      { name: '프로젝트 이력', summary: '프로젝트 상태, 변경, 발전 과정을 기록합니다.', features: ['프로젝트 스냅샷과 이력 이벤트', '추가·삭제·수정 감지', '시간순 프로젝트 발전 기록'] },
      { name: '지식 지도', summary: '프로젝트 자료와 내부·프로젝트 간 관계를 정리합니다.', features: ['프로젝트 관계 그래프', '로컬 지식 저장', '프로젝트 자료 조회'] },
      { name: 'AI 프로젝트 분석', summary: 'AI에 프로젝트 자료를 제공하고 구조화된 분석과 답변을 제공합니다.', features: ['AI 문맥 구성과 민감 정보 제거', '구조화된 프로젝트 분석', '프로젝트 자료 기반 질문 답변'] },
      { name: '사용자 인터페이스', summary: '로컬 프로젝트를 보고 제어할 수 있는 화면을 제공합니다.', features: ['로컬 프로젝트 대시보드', '모바일 화면', '통합 작업 진입점과 확인 절차'] },
      { name: '지능형 프로젝트 관리', summary: '여러 프로젝트를 요약하고 추적 가능한 알림과 제안을 제공합니다.', features: ['다중 프로젝트 종합 현황', '공통 위험과 프로젝트 관계 요약', '기록된 변화를 바탕으로 알림과 제안 생성'] },
      { name: '다국어 지원', summary: '여러 언어에서 의미가 일치하는 인터페이스를 제공합니다.', features: ['중국어, 영어, 러시아어, 한국어', '기본적으로 시스템 언어를 따르고 사용자 선택 저장', '명확하고 전문적인 중국어를 의미 기준으로 사용'] },
      { name: '로컬 운영 관리', summary: '로컬 스캔 폴더와 프로젝트 구조 점검을 관리합니다.', features: ['시스템 선택기로 스캔 폴더 등록', '첫 탐색 및 수동 점검 실행', '자동 점검을 명시적으로 켜고 간격 설정'] },
    ], implementedFeatures: '구현된 기능', showPhaseDetails: '단계 상세 보기', hidePhaseDetails: '단계 상세 접기', complete: '완료',
    releaseStatus: '릴리스 상태', releaseVerified: '현재 릴리스 검증 통과', releaseRecordNote: '아래 정보는 최근 릴리스 기록입니다. 실시간 모니터링 결과가 아닙니다.', testsPassing: '개 테스트 통과', workingTree: '릴리스 시점 파일 상태', clean: '커밋하지 않은 변경 없음', currentVersion: '현재 버전', latestTask: '최근 완료', mode: '인터페이스 모드', readOnly: '로컬 실행',
    projectHistory: '버전 기록', recentMilestones: '최근 완료한 기능', annotatedReleases: '모든 버전에 설명이 있음',
    milestones: [['대규모 프로젝트가 폴더 탐색을 중단하지 않음', '점검 범위를 넘는 프로젝트는 제한으로 표시하고 나머지는 계속 식별'], ['로컬 프로젝트 폴더 관리', '스캔 폴더를 선택하고 프로젝트를 식별하여 정기적으로 변경 점검'], ['명확한 프로젝트 구성과 릴리스 기록', '프로젝트 구성, 프로젝트 관계, 실시간 분석을 구분'], ['개발 단계 기능 상세', '각 단계를 펼쳐 구현된 기능을 확인']],
    projectComposition: '프로젝트 구성', compositionTitle: 'Project Atlas의 구성 요소', compositionStatus: '현재 버전 예시', compositionDiagram: 'Project Atlas 구성도', compositionRelations: ['소스 코드 저장 위치', '포함', '프로젝트 자료는 기기에 저장'], project: '프로젝트', repository: '코드 저장소', coreFeatures: '핵심 기능', coreModels: '도메인 모델과 서비스', localData: '로컬 자료', localMemory: '프로젝트 기록과 지식', compositionNote: '현재 버전의 프로젝트 구성 예시입니다. 자동 스캔이나 실시간 분석 결과가 아닙니다.',
    commandCenter: '작업 센터', controlBoundary: '모든 작업은 여기에서 시작', auditable: '기기에서 실행 · 모두 기록', noHandlers: '아직 사용할 수 있는 작업 없음', handlerNote: '시스템에서 기능을 켠 뒤에만 여기에 표시됩니다.',
    guardrails: [['데이터 변경 여부 안내', '각 작업이 보기만 하는지 데이터를 바꾸는지 알려 줍니다.'], ['변경 전 확인', '확인하기 전에는 아무것도 바뀌지 않습니다.'], ['모든 결과 기록', '작업 번호, 시간, 결과와 반환 내용을 기록합니다.']], mobileNavigation: '모바일 탐색', map: '구성',
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
