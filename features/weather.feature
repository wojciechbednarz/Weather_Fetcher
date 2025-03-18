Feature: Fetching weather for a city
  To provide users with accurate weather data, the system should fetch and display the temperature for a single city.

  @single_city
  Scenario: Get temperature from weather data for a single city
    Given the city "London" is provided to the Weather Fetcher
     When the weather data is fetched for the "London" city
     Then the temperature for the city should be displayed


#    @then('the temperature for the city "{London}" should be displayed')