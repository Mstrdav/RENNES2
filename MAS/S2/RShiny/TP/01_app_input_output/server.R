library(shiny)

function(input, output) {
   
  output$distPlot <- renderPlot({
    x    <- faithful[, input$colonne] 
    bins <- seq(min(x), max(x), length.out = input$bins + 1)
    
    hist(x, breaks = bins, col = input$color, border = 'white',
         main = input$hist_title)
    
    output$summary <- renderPrint({
      summary(faithful)
    })
    
    output$my_dt <- DT::renderDT({
      faithful
    })
    
    output$nb_bins <- renderText({
      paste0("Le nombre de bins est : ", input$bins)
    })
  })
}
