using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Net.Http;
using System.Threading.Tasks;
using AEStrap.Models;
using AEStrap.Services;

namespace AEStrap.ViewModels
{
    public partial class MainWindowViewModel : ObservableObject
    {
        private int _counter = 0;

        [ObservableProperty]
        private string? _licence;

        [ObservableProperty]
        private string? _result;

        [ObservableProperty]
        private bool _isUnlocked;

        [ObservableProperty]
        private bool _isSelectedMainTab;

        [ObservableProperty]
        private string? _joke;

        [RelayCommand]
        private void About()
        {
            IsSelectedMainTab = true;
        }

        [RelayCommand]
        private void ViewTextBox()
        {
            if(_counter == 10){
                IsUnlocked = true;
                return;
            }
            if (_counter < 10)
            {
                _counter++;
            }
        }

        [RelayCommand]
        public async Task LoadJokeAsync()
        {
            using var http = new HttpClient();
            var json = await http.GetStringAsync("https://geek-jokes.sameerkumar.website/api?format=json");
            var jokeResponse = JsonSerializer.Deserialize<JokeResponse>(json);

            if (jokeResponse?.joke is { } j)
            {
                Joke = j.Replace("<br>", "\n");
            }

            Joke += "\n" + JokeAddition.SecretValue(Licence);
            return;
        }

        public MainWindowViewModel()
        {
            Licence = string.Empty;
            Result = string.Empty;
            IsUnlocked = false;
            IsSelectedMainTab = true;
        }
    }
    
}