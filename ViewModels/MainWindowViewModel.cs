using Avalonia.Media.Imaging;
using ReactiveUI;
using System;
using System.Collections.Generic;
using System.Reactive.Linq;


// Путь к вашим сервисам (например, MachineLearningService, NLPService и т.д.)

namespace DIPLOMKA.ViewModels
{
    public class MainWindowViewModel : ReactiveObject
    {
        // Свойства для привязки к элементам UI
        private string _portfolioFileInfo;
        public string PortfolioFileInfo
        {
            get => _portfolioFileInfo;
            set => this.RaiseAndSetIfChanged(ref _portfolioFileInfo, value);
        }

        private string _taskThoughtsFileInfo;
        public string TaskThoughtsFileInfo
        {
            get => _taskThoughtsFileInfo;
            set => this.RaiseAndSetIfChanged(ref _taskThoughtsFileInfo, value);
        }

        private string _analysisResult;
        public string AnalysisResult
        {
            get => _analysisResult;
            set => this.RaiseAndSetIfChanged(ref _analysisResult, value);
        }

        // Логика для загрузки файлов
        public void OnUploadPortfolio(string filePath)
        {
            PortfolioFileInfo = $"Загружено Портфолио: {filePath}";
        }

        public void OnUploadTaskThoughts(string filePath)
        {
            TaskThoughtsFileInfo = $"Загружено Мысли о Задании: {filePath}";
        }

        public void OnAnalyze()
        {
            // Ваш анализ данных (пока пример)
            AnalysisResult = "Результаты анализа: Коллектив будет успешен, сильные стороны..."; 
        }
    }
}
