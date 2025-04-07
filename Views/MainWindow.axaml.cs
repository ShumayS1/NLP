using Avalonia.Controls;
using Avalonia.Interactivity;
using System;
using DIPLOMKA.ViewModels;

namespace DIPLOMKA.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void OnUploadPortfolioClick(object sender, RoutedEventArgs e)
        {
            var dialog = new OpenFileDialog();
            dialog.Filters.Add(new FileDialogFilter() { Name = "Text Files", Extensions = { "txt", "md" } });
            var result = dialog.ShowAsync(this).Result;

            if (result != null && result.Length > 0)
            {
                // Обновляем свойство в ViewModel
                var viewModel = (MainWindowViewModel)this.DataContext;
                viewModel.OnUploadPortfolio(result[0]);
            }
        }

        private void OnUploadTaskThoughtsClick(object sender, RoutedEventArgs e)
        {
            var dialog = new OpenFileDialog();
            dialog.Filters.Add(new FileDialogFilter() { Name = "Text Files", Extensions = { "txt", "md" } });
            var result = dialog.ShowAsync(this).Result;

            if (result != null && result.Length > 0)
            {
                // Обновляем свойство в ViewModel
                var viewModel = (MainWindowViewModel)this.DataContext;
                viewModel.OnUploadTaskThoughts(result[0]);
            }
        }

        private void OnAnalyzeClick(object sender, RoutedEventArgs e)
        {
            var viewModel = (MainWindowViewModel)this.DataContext;
            viewModel.OnAnalyze();
        }
    }
}