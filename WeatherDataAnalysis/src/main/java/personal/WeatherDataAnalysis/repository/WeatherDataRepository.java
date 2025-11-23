package personal.WeatherDataAnalysis.repository;



import personal.WeatherDataAnalysis.Models.WeatherData;
import org.springframework.data.jpa.repository.JpaRepository;

public interface WeatherDataRepository extends JpaRepository<WeatherData, Long> {
}

