package personal.WeatherDataAnalysis.Controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import personal.WeatherDataAnalysis.Models.WeatherData;
import personal.WeatherDataAnalysis.repository.WeatherDataRepository;

@RestController
@RequestMapping("/api/weather")
public class WeatherController {

    private final WeatherDataRepository repository;

    public WeatherController(WeatherDataRepository repository) {
        this.repository = repository;
    }

    // Get all weather data
    @GetMapping
    public List<WeatherData> getAll() {
        return repository.findAll();
    }

    // Add new weather data
    @PostMapping
    public WeatherData addWeather(@RequestBody WeatherData data) {
        return repository.save(data);
    }
}