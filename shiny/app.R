# ==========================================
# Weather Forecast Dashboard (Shiny + API)
# ==========================================
# This Shiny app fetches weather forecast data
# directly from your Spring Boot API and
# displays:
# 1. Temperature over time
# 2. Humidity over time
# 3. Wind speed over time
# 4. Raw data table
# Users can select the city from a dropdown
# Datetime is formatted nicely for display
# ==========================================

# -------------------------------
# 1. Load required libraries
# -------------------------------
library(shiny)
library(ggplot2)
library(dplyr)
library(httr)
library(jsonlite)
library(DT)  # for interactive table display

# -------------------------------
# 2. Function to fetch data from API
# -------------------------------
load_weather_api <- function() {
  
  url <- "http://localhost:8080/api/weather"  # your API URL
  res <- GET(url)
  if(status_code(res) != 200) stop("API request failed")
  
  data <- content(res, "text", encoding = "UTF-8")
  json <- fromJSON(data, flatten = TRUE)  # flatten nested fields
  
  # Convert JSON array to dataframe
  df <- as.data.frame(json)
  
  # Convert datetime to POSIXct for plotting
  df$datetime <- as.POSIXct(df$datetime, format="%Y-%m-%dT%H:%M:%S")
  
  # Add a nicely formatted datetime string for display in tables
  df$datetime_str <- format(df$datetime, "%Y-%m-%d %H:%M")
  
  return(df)
}

# -------------------------------
# 3. Define UI (User Interface)
# -------------------------------
ui <- fluidPage(
  
  titlePanel("Weather Forecast"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("city", "Select City:", choices = NULL)
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel("Temperature", plotOutput("tempPlot")),
        tabPanel("Humidity", plotOutput("humidityPlot")),
        tabPanel("Wind Speed", plotOutput("windPlot")),
        tabPanel("Data Table", DTOutput("dataTable"))  # use DT for nice display
      )
    )
  )
)

# -------------------------------
# 4. Server logic
# -------------------------------
server <- function(input, output, session) {
  
  # Load API data once
  df <- load_weather_api()
  
  # Update city dropdown dynamically
  observe({
    updateSelectInput(session, "city",
                      choices = unique(df$city),
                      selected = unique(df$city)[1])
  })
  
  # Reactive dataframe filtered by selected city
  filtered <- reactive({
    df %>% filter(city == input$city)
  })
  
  # Render temperature plot
  output$tempPlot <- renderPlot({
    ggplot(filtered(), aes(x=datetime, y=temperature)) +
      geom_line(color="red") +
      geom_point() +
      labs(title = paste("Temperature -", input$city),
           x = "Date/Time",
           y = "Temperature (°C)") +
      scale_x_datetime(date_labels = "%d %b %H:%M") +
      theme_minimal()
  })
  
  # Render humidity plot
  output$humidityPlot <- renderPlot({
    ggplot(filtered(), aes(x=datetime, y=humidity)) +
      geom_line(color="blue") +
      geom_point() +
      labs(title = paste("Humidity -", input$city),
           x = "Date/Time",
           y = "Humidity (%)") +
      scale_x_datetime(date_labels = "%d %b %H:%M") +
      theme_minimal()
  })
  
  # Render wind speed plot
  output$windPlot <- renderPlot({
    ggplot(filtered(), aes(x=datetime, y=windSpeed)) +
      geom_line(color="darkgreen") +
      geom_point() +
      labs(title = paste("Wind Speed -", input$city),
           x = "Date/Time",
           y = "Wind Speed (m/s)") +
      scale_x_datetime(date_labels = "%d %b %H:%M") +
      theme_minimal()
  })
  
  # Render raw data table
  output$dataTable <- renderDT({
    df_table <- filtered()
    
    # Show datetime nicely in table
    df_table <- df_table %>% 
      select(datetime_str, temperature, humidity, windSpeed, description, city, id) %>%
      rename(datetime = datetime_str)
    
    datatable(df_table, options = list(pageLength = 10, scrollX = TRUE))
  })
}

# -------------------------------
# 5. Run Shiny app
# -------------------------------
shinyApp(ui = ui, server = server)
