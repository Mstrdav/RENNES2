library(shiny)
library(colourpicker)

fluidPage(
  
  titlePanel("Old Faithful Geyser Data"),
  
  sidebarLayout(
    sidebarPanel(
      sliderInput("bins",
                  "Number of bins:",
                  min = 1,
                  max = 50,
                  value = 30),
      selectInput("colonne",
                  "Colonne à afficher",
                  colnames(faithful),
                  selected = colnames(faithful)[2]),
      colourInput("color",
                  "Couleur",
                  value = "blue"),
      textInput("hist_title",
                "Titre du graphique",
                value = "Histogramme")
    ),
    
    mainPanel(
      plotOutput("distPlot")
    )
  )
)