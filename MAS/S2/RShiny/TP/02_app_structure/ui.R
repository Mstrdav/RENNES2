library(shiny)
library(colourpicker)

fluidPage(
  navbarPage("Premiers pas avec shiny",
             tabPanel("Data",
                      navlistPanel("Au choix :",
                                   tabPanel("table",
                                            DT::dataTableOutput("table")),
                                   tabPanel("summary",
                                            verbatimTextOutput("summary"))
                                   )
             ),
             tabPanel("Visualisation", 
                      fluidRow(
                        column(width = 3,
                               wellPanel(sliderInput("bins",
                                                      "Number of bins:",
                                                      min = 1,
                                                      max = 50,
                                                      value = 30),
                                          
                                        colourInput(inputId = "color",
                                                    label = "Couleur :",
                                                    value = "purple"),
                                        textInput(inputId = "titre",
                                                  label = "Titre :",
                                                  value = "Histogramme"),
                                        radioButtons(inputId = "var",
                                                     label = "Variable : ", 
                                                     choices = c("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"))
                               )
                        ),
                        column(width = 9,
                               tabsetPanel(tabPanel("Dist Plot",
                                                    plotOutput("dist_plot"),
                                                    div(textOutput("n_bins"),
                                                        align = "center"),
                                                    ),
                                           tabPanel("Box Plot",
                                                    plotOutput("box_plot")),
                                           type = "pills"),
                        )
                      )
             )
            
  )
)
