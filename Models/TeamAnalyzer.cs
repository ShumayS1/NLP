using Microsoft.ML;
using Microsoft.ML.Transforms.Text;
using DIPLOMKA.Models;
using System.Collections.Generic;
using System.Linq;
namespace DIPLOMKA.Models;

public class TeamAnalyzer
{
     private static readonly string modelPath = "team_analysis_model.zip";
        
        public static bool PredictTeamSuccess(List<PersonProfile> profiles)
        {
            // Загрузка данных в формат, который понимает ML.NET
            var mlContext = new MLContext();
            
            // Преобразуем профили в TeamAnalysisInput
            var inputData = profiles.Select(p => new TeamAnalysisInput
            {
                ExperienceYears = p.ExperienceYears,
                Skills = p.Skills
            }).ToList();
            
            // Загрузим модель, если она существует, иначе обучим новую модель
            ITransformer model = null;
            if (System.IO.File.Exists(modelPath))
            {
                model = mlContext.Model.Load(modelPath, out _);
            }
            else
            {
                var trainingData = mlContext.Data.LoadFromEnumerable(inputData);
                
                // Преобразование навыков в вектор
                var dataProcessPipeline = mlContext.Transforms.Conversion.MapValueToKey("Label")
                    .Append(mlContext.Transforms.Text.FeaturizeText("Skills"));
                
                // Тренировка модели
                var trainer = mlContext.Regression.Trainers.Sdca(labelColumnName: "WillBeSuccessful", featureColumnName: "Features");
                var trainingPipeline = dataProcessPipeline.Append(trainer);
                model = trainingPipeline.Fit(trainingData);
                
                // Сохраняем модель
                mlContext.Model.Save(model, trainingData.Schema, modelPath);
            }
            
            // Прогнозируем успешность коллектива
            var predictionEngine = mlContext.Model.CreatePredictionEngine<TeamAnalysisInput, TeamAnalysisPrediction>(model);
            var prediction = predictionEngine.Predict(inputData.First()); // Прогнозируем для первого человека (это можно изменить)
            return prediction.WillBeSuccessful;
        }
}