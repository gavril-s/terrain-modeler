
var currentLanguage = 'ru';
const translations = {
    "en": {
        "language-button": "English",
        "page-title": "Terrain Modeler",
        "card-title": "Terrain Modeler",
        "card-text": "Choose the top left and bottom right corners of the area you want to model, then click on the buttons. The format of the records in the CSV file is X,Y,Z (values in meters), it can be imported into Revit.",
        "top-left-label": "Coordinates of the top left corner:",
        "bottom-right-label": "Coordinates of the bottom right corner:",
        "api-label": "API for getting heights:",
        "points-slider-label": "Number of points:",
        "show-points-label": "Show points",
        "generate": "Generate model",
        "open-preview": "Open visualization",
        "download-csv": "Download CSV"
    },
    "ru": {
        "language-button": "Русский",
        "page-title": "Terrain Modeler",
        "card-title": "Terrain Modeler",
        "card-text": "Выберите левый верхний и правый нижний углы участка, который хотите смоделировать, дальше жмите на кнопки. Формат записей в CSV-файле - X,Y,Z (значения в метрах), его можно импортировать в Revit.",
        "top-left-label": "Координаты верхнего левого угла:",
        "bottom-right-label": "Координаты правого нижнего угла:",
        "api-label": "API для получения высот:",
        "points-slider-label": "Количество точек:",
        "show-points-label": "Показывать точки",
        "generate": "Сгенерировать модель",
        "open-preview": "Открыть визуализацию",
        "download-csv": "Скачать CSV"
    }
};


function updateLanguageButton(lang) {
    const languageButton = document.getElementById('language-button');
    languageButton.textContent = lang === 'en' ? 'English' : 'Русский';
}

function switchLanguage(lang) {
    currentLanguage = lang;
    updateLanguageButton(lang);
}

function switchLanguage(lang) {
    for (const key in translations[lang]) {
        const element = document.getElementById(key);
        if (element) {
            element.textContent = translations[lang][key];
        }
    }
}
