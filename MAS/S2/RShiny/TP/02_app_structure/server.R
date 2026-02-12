library(shiny)

function(input, output) {
   
  output$dist_plot <- renderPlot({
    
    x    <- iris[, input$var] 
    bins <- seq(min(x), max(x), length.out = input$bins + 1)
    
    hist(x, breaks = bins, col = input$color, border = 'white', main = input$titre)
    
  })
  
  output$box_plot <- renderPlot({
    
    x    <- iris[, input$var] 
    bins <- seq(min(x), max(x), length.out = input$bins + 1)
    
    boxplot(x, col = input$color, border = "black", main = input$titre)
    
  })

    output$summary <- renderPrint({
    summary(iris)
  })
  
  output$table <- DT::renderDT({
    iris
  })
  
  output$n_bins <- renderText({
    paste("Nombre de classes : ", input$bins)
  })
  
}
