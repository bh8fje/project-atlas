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

// Chinese is the source of meaning for product copy. Other languages translate it.
export const translations: Record<Language, Translation> = {
  zh: {
    languageName: '中文', followSystem: '跟随系统', selectLanguage: '语言',
    nav: ['概览', '历史', '关系', '状态', '操作'],
    localOnly: '仅限本地', dataStays: '你的数据只保存在这台设备上', workspace: '项目工作区', greeting: '早上好。', planComplete: '项目建设计划 1.2 · 已完成',
    heroLead: '你的软件世界，', heroAccent: '在本地绘成地图。', heroCopy: '以平静、持久的方式了解项目是什么、如何变化，以及每个部分如何连接。', graphSummary: '项目关系图摘要',
    tests: '项测试', tasks: '项任务', decisionsShort: '项说明', systemsSteady: '所有系统稳定', mobileSummary: '移动端项目摘要', metricsLabel: '项目指标',
    metrics: [['完成事项', '已全部发布'], ['检查', '全部通过'], ['重要设计', '都有说明'], ['联网次数', '不会把数据发出去']],
    executionPlan: '项目建设', architectureEvolution: '建设进度', phasesComplete: '8 / 8 个阶段', phaseNames: ['打好基础', '找到项目', '记录变化', '整理项目关系', 'AI 帮助', '使用界面', '更多智能功能', '多语言体验'], complete: '已完成',
    projectHealth: '项目状态', everythingSteady: '一切运行稳定', testsPassing: '项检查通过', workingTree: '文件状态', clean: '没有未保存改动', currentVersion: '当前版本', latestTask: '最近完成', mode: '工作方式', readOnly: '只查看，不修改',
    projectHistory: '版本记录', recentMilestones: '最近完成的功能', annotatedReleases: '每个版本都有备注',
    milestones: [['选择界面语言', '支持中文、英语、俄语和韩语，也可以跟随系统'], ['多个项目一起看', '找出多个项目共有的问题和彼此关系'], ['向 AI 询问项目', '根据项目资料回答问题，不会自动修改'], ['AI 读懂项目', '可以更换 AI 服务，不影响项目分析']],
    knowledgeMap: '项目关系', howConnects: '项目各部分怎么连接', typedRelationships: '每条关系都有说明', relationshipDiagram: '项目关系图', project: '项目', repository: '代码仓库', domain: '核心功能', coreModels: '基础规则', knowledge: '项目资料', localMemory: '本地记录', mapNote: '这里只展示项目结构、历史和关系，不会修改任何内容。',
    commandCenter: '操作中心', controlBoundary: '所有操作都从这里进入', auditable: '本机运行 · 全程留痕', noHandlers: '目前没有可用操作', handlerNote: '系统启用某项操作后，它才会显示在这里。',
    guardrails: [['说明是否修改数据', '每项操作都会说明它只查看还是会修改。'], ['修改前先确认', '没有得到确认，就不会修改任何内容。'], ['每次结果都有记录', '会记录操作编号、时间、结果和返回内容。']], mobileNavigation: '移动端导航', map: '关系',
  },
  en: {
    languageName: 'English', followSystem: 'Follow system', selectLanguage: 'Language',
    nav: ['Overview', 'History', 'Connections', 'Status', 'Actions'],
    localOnly: 'Local only', dataStays: 'Your data stays on this device', workspace: 'Project workspace', greeting: 'Good morning.', planComplete: 'Project Plan 1.2 · Complete',
    heroLead: 'Your software world,', heroAccent: 'mapped locally.', heroCopy: 'A calm, durable view of what your project is, how it changed, and how every part connects.', graphSummary: 'Project graph summary',
    tests: 'tests', tasks: 'tasks', decisionsShort: 'notes', systemsSteady: 'All systems steady', mobileSummary: 'Mobile project summary', metricsLabel: 'Project metrics',
    metrics: [['Completed work', 'All published'], ['Checks', 'All passing'], ['Key designs', 'All explained'], ['Network requests', 'No data is sent out']],
    executionPlan: 'Project plan', architectureEvolution: 'Build progress', phasesComplete: '8 / 8 stages', phaseNames: ['Build the base', 'Find projects', 'Record changes', 'Organize connections', 'AI help', 'User interface', 'More smart features', 'Languages'], complete: 'Complete',
    projectHealth: 'Project status', everythingSteady: 'Everything is running well', testsPassing: 'checks passing', workingTree: 'File status', clean: 'No unsaved changes', currentVersion: 'Current version', latestTask: 'Last completed', mode: 'How it works', readOnly: 'View only, no changes',
    projectHistory: 'Version history', recentMilestones: 'Recently completed features', annotatedReleases: 'Every version has a note',
    milestones: [['Choose the interface language', 'Use Chinese, English, Russian, or Korean, or follow the system'], ['View projects together', 'Find shared problems and see how projects connect'], ['Ask AI about a project', 'Answers from project information without making changes'], ['AI reads the project', 'Switch AI services without changing project analysis']],
    knowledgeMap: 'Project connections', howConnects: 'How the project parts connect', typedRelationships: 'Every connection is explained', relationshipDiagram: 'Project connections diagram', project: 'Project', repository: 'Code repository', domain: 'Main features', coreModels: 'Basic rules', knowledge: 'Project information', localMemory: 'Local records', mapNote: 'This view only shows project structure, history, and connections. It changes nothing.',
    commandCenter: 'Action center', controlBoundary: 'All actions start here', auditable: 'Runs locally · Fully recorded', noHandlers: 'No actions are available yet', handlerNote: 'An action appears here only after the system enables it.',
    guardrails: [['Says whether data changes', 'Every action says whether it only views or also changes data.'], ['Confirm before changes', 'Nothing changes until you confirm it.'], ['Every result is recorded', 'The action number, time, result, and returned information are recorded.']], mobileNavigation: 'Mobile navigation', map: 'Connections',
  },
  ru: {
    languageName: 'Русский', followSystem: 'Как в системе', selectLanguage: 'Язык',
    nav: ['Обзор', 'История', 'Связи', 'Состояние', 'Действия'],
    localOnly: 'Только локально', dataStays: 'Ваши данные остаются на этом устройстве', workspace: 'Рабочее пространство', greeting: 'Доброе утро.', planComplete: 'План проекта 1.2 · Завершён',
    heroLead: 'Ваш мир программ,', heroAccent: 'на локальной карте.', heroCopy: 'Спокойное и надёжное представление о проекте, его изменениях и связях между всеми частями.', graphSummary: 'Сводка графа проекта',
    tests: 'тестов', tasks: 'задач', decisionsShort: 'пояснений', systemsSteady: 'Все системы стабильны', mobileSummary: 'Мобильная сводка проекта', metricsLabel: 'Метрики проекта',
    metrics: [['Выполнено', 'Всё опубликовано'], ['Проверки', 'Все пройдены'], ['Важные решения', 'Для каждого есть пояснение'], ['Сетевые запросы', 'Данные не отправляются']],
    executionPlan: 'План проекта', architectureEvolution: 'Ход работ', phasesComplete: '8 из 8 этапов', phaseNames: ['Подготовить основу', 'Найти проекты', 'Записать изменения', 'Упорядочить связи', 'Помощь ИИ', 'Интерфейс', 'Больше умных функций', 'Языки'], complete: 'Готово',
    projectHealth: 'Статус проекта', everythingSteady: 'Всё работает стабильно', testsPassing: 'проверок пройдено', workingTree: 'Состояние файлов', clean: 'Нет несохранённых изменений', currentVersion: 'Текущая версия', latestTask: 'Последнее выполненное', mode: 'Как работает', readOnly: 'Только просмотр',
    projectHistory: 'История версий', recentMilestones: 'Недавно готовые функции', annotatedReleases: 'У каждой версии есть примечание',
    milestones: [['Выбор языка интерфейса', 'Китайский, английский, русский, корейский или язык системы'], ['Проекты вместе', 'Общие проблемы и связи между проектами'], ['Спросить ИИ о проекте', 'Ответы по данным проекта без автоматических изменений'], ['ИИ изучает проект', 'Можно менять сервис ИИ, не меняя анализ проекта']],
    knowledgeMap: 'Связи проекта', howConnects: 'Как связаны части проекта', typedRelationships: 'У каждой связи есть пояснение', relationshipDiagram: 'Схема связей проекта', project: 'Проект', repository: 'Репозиторий кода', domain: 'Основные функции', coreModels: 'Базовые правила', knowledge: 'Данные проекта', localMemory: 'Локальные записи', mapNote: 'Здесь показаны только структура, история и связи проекта. Ничего не изменяется.',
    commandCenter: 'Центр действий', controlBoundary: 'Все действия начинаются здесь', auditable: 'Работает локально · Всё записывается', noHandlers: 'Пока нет доступных действий', handlerNote: 'Действие появится здесь только после включения системой.',
    guardrails: [['Показывает, изменятся ли данные', 'У каждого действия указано, только смотрит оно данные или меняет их.'], ['Подтверждение перед изменением', 'Без подтверждения ничего не изменится.'], ['Каждый результат записывается', 'Сохраняются номер действия, время, результат и полученные данные.']], mobileNavigation: 'Мобильная навигация', map: 'Связи',
  },
  ko: {
    languageName: '한국어', followSystem: '시스템 설정 따르기', selectLanguage: '언어',
    nav: ['개요', '기록', '관계', '상태', '작업'],
    localOnly: '로컬 전용', dataStays: '데이터는 이 기기에만 저장됩니다', workspace: '프로젝트 작업 공간', greeting: '좋은 아침입니다.', planComplete: '프로젝트 계획 1.2 · 완료',
    heroLead: '소프트웨어 세계를,', heroAccent: '로컬에서 지도로.', heroCopy: '프로젝트의 현재 모습과 변화, 모든 구성 요소의 연결을 차분하고 지속적으로 보여 줍니다.', graphSummary: '프로젝트 그래프 요약',
    tests: '테스트', tasks: '작업', decisionsShort: '설명', systemsSteady: '모든 시스템 안정', mobileSummary: '모바일 프로젝트 요약', metricsLabel: '프로젝트 지표',
    metrics: [['완료한 일', '모두 게시됨'], ['점검', '모두 통과'], ['중요한 설계', '모두 설명됨'], ['네트워크 요청', '데이터를 밖으로 보내지 않음']],
    executionPlan: '프로젝트 계획', architectureEvolution: '진행 상황', phasesComplete: '8 / 8 단계', phaseNames: ['기초 만들기', '프로젝트 찾기', '변화 기록하기', '연결 정리하기', 'AI 도움', '사용 화면', '더 많은 스마트 기능', '언어 지원'], complete: '완료',
    projectHealth: '프로젝트 상태', everythingSteady: '모두 안정적으로 작동합니다', testsPassing: '개 점검 통과', workingTree: '파일 상태', clean: '저장하지 않은 변경 없음', currentVersion: '현재 버전', latestTask: '최근 완료', mode: '작동 방식', readOnly: '보기만 가능',
    projectHistory: '버전 기록', recentMilestones: '최근 완료한 기능', annotatedReleases: '모든 버전에 설명이 있음',
    milestones: [['화면 언어 선택', '중국어, 영어, 러시아어, 한국어 또는 시스템 언어 사용'], ['여러 프로젝트 함께 보기', '공통 문제와 프로젝트 사이의 관계 찾기'], ['AI에게 프로젝트 묻기', '프로젝트 자료로 답하고 자동 변경하지 않음'], ['AI가 프로젝트 읽기', '프로젝트 분석 방식은 그대로 두고 AI 서비스 교체 가능']],
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
