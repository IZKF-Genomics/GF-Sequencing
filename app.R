library(shiny)
library(shinydashboard)
library(DT)
library(ggplot2)
library(plotly)

# Load your CSV data
csv_data <- read.csv("sequencing_statistics.csv")
project_names <- unique(csv_data$Project.Name)

# Define the UI
ui <- dashboardPage(
  dashboardHeader(title = "GF Sequencing Monitor"),
  dashboardSidebar(
    selectInput("plot_type", "Choose Plot Type",
                choices = c("Scatter Plot", "Bar Plot"),
                selected = "Scatter Plot"),
    dateRangeInput("date_range_filter", "Date Range Filter", start = "2022-01-01", end = format(Sys.Date(), "%Y-%m-%d")),
    checkboxGroupInput("sequencer_filter", "Sequencer Filter", choices = unique(csv_data$Sequencer), selected = unique(csv_data$Sequencer)),
    actionButton("reset_filters", "Reset Filters"),
    selectInput("color_variable", "Choose Color Variable", choices = colnames(csv_data), selected = "Application")
  ),
  dashboardBody(
    navbarPage(
      "Plots",
      tabPanel("Statistics Plots",
               fluidRow(
                 tabsetPanel(
                   tabPanel(
                     title = "Total Read Count - in Millions",
                     icon = icon("chart-line"),
                     plotlyOutput("selected_plot_3")
                   ),
                   tabPanel(
                     title = "Q 30",
                     icon = icon("chart-line"),
                     plotlyOutput("selected_plot")
                   ),
                   tabPanel(
                     title = "Coefficient of Variation",
                     icon = icon("chart-line"),
                     plotlyOutput("selected_plot_2")
                   ),
                   # New tab panels
                   tabPanel(
                     title = "Undetermined Reads Percentage",
                     icon = icon("chart-line"),
                     plotlyOutput("selected_plot_4")
                   ),
                   tabPanel(
                     title = "Read to Expected Clusters Ratio",
                     icon = icon("chart-line"),
                     plotlyOutput("selected_plot_5")
                   ),
                   tabPanel(
                     title = "PhiX Input",
                     icon = icon("chart-line"),
                     plotlyOutput("selected_plot_6")
                   ),
                   tabPanel(
                     title = "PhiX Output",
                     icon = icon("chart-line"),
                     plotlyOutput("selected_plot_7")
                   ),
                 )
               )
      ),
      tabPanel("Distribution Reads Plots",
               fluidRow(
                 selectInput("selected_project", "Please selcet a Project to display", choices = project_names, selected = project_names[1]),
                 plotlyOutput("selected_distribution_plot")
               )
      ), 
      tabPanel("Undetermined Distribution Plots",
               fluidRow(
                 selectInput("selected_undetermined_distrinuton_to_display", "Please select an Undetermined distribution to display", choices = project_names, selected = project_names[1]),
                 plotlyOutput("selected_unditermined_distribution_plot")
               )
      )
    ),
    # New navbarPage for Tables
    tags$hr(), # Add a horizontal line for visual separation
    tags$hr(),
    tags$hr(),
    tags$hr(),
    tags$hr(),
    navbarPage(
      "Tables",
      tabPanel("Overview",
               fluidRow(
                 tabPanel(
                   title = "Overview table",
                   icon = icon("table"),
                   box(
                     title = "Overview table",
                     status = "warning",
                     solidHeader = TRUE,
                     width = 12, # Set the width to 12 to take the entire row
                     DTOutput("table_1"),
                     height = "auto",  # Set height to "auto" for automatic adjustment
                     style = "overflow-x: auto;" # Add horizontal scrolling
                   )
                 )
               )
      ),
      tabPanel("Run Statistics",
               fluidRow(
                 tabPanel(
                   title = "Run statistics table",
                   icon = icon("table"),
                   box(
                     status = "warning",
                     title = "Run statistics table",
                     solidHeader = TRUE,
                     width = 12, # Set the width to 12 to take the entire row
                     DTOutput("table_4"),
                     style = "overflow-x: auto;" # Add horizontal scrolling
                   )
                 )
               )
      ),
      tabPanel("Sample reads",
               fluidRow(
                 tabPanel(
                   title = "Sample reads table",
                   icon = icon("table"),
                   box(
                     status = "warning",
                     title = "Sample reads table",
                     solidHeader = TRUE,
                     width = 12, # Set the width to 12 to take the entire row
                     DTOutput("table_5"),
                     style = "overflow-x: auto;" # Add horizontal scrolling
                   )
                 )
               )
      ),
      tabPanel("Undetermined reads",
               fluidRow(
                 tabPanel(
                   title = "Undetermined reads table",
                   icon = icon("table"),
                   box(
                     status = "warning",
                     title = "Undetermined reads table",
                     solidHeader = TRUE,
                     width = 12, # Set the width to 12 to take the entire row
                     DTOutput("table_6"),
                     style = "overflow-x: auto;" # Add horizontal scrolling
                   )
                 )
               )
      ),
      tabPanel("PhiX",
               fluidRow(
                 tabPanel(
                   title = "PhiX table",
                   icon = icon("table"),
                   box(
                     status = "warning",
                     title = "PhiX table",
                     solidHeader = TRUE,
                     width = 12, # Set the width to 12 to take the entire row
                     DTOutput("table_3"),
                     style = "overflow-x: auto;" # Add horizontal scrolling
                   )
                 )
               )
      ),
      tabPanel("Protocol",
               fluidRow(
                 tabPanel(
                   title = "Protocol table",
                   icon = icon("table"),
                   box(
                     status = "warning",
                     title = "Protocol table",
                     solidHeader = TRUE,
                     width = 12, # Set the width to 12 to take the entire row
                     DTOutput("table_7"),
                     style = "overflow-x: auto;" # Add horizontal scrolling
                   )
                 )
               )
      ),
      tabPanel("All info",
               fluidRow(
                 tabPanel(
                   title = "All info table",
                   icon = icon("table"),
                   box(
                     title = "All info table",
                     status = "warning",
                     solidHeader = TRUE,
                     width = 12, # Set the width to 12 to take the entire row
                     DTOutput("table_2"),
                     style = "overflow-x: auto;" # Add horizontal scrolling
                   )
                 )
                 
               )
      )
    ),
  )
)


# Define the server logic
server <- function(input, output, session) {
  # Reactive values for date and sequencer filtering
  filters <- reactiveValues(
    date_range_selected = NULL,
    sequencer_selected = unique(csv_data$Sequencer)
  )
  
  # reactive values for storing selected projects in each tab
  selected_project_distribution <- reactiveVal(project_names[1])
  selected_project_undetermined_distribution <- reactiveVal(project_names[1])
  
  observeEvent(input$date_range_filter, {
    filters$date_range_selected <- input$date_range_filter
  })
  
  observeEvent(input$sequencer_filter, {
    filters$sequencer_selected <- input$sequencer_filter
  })
  
  observeEvent(input$reset_filters, {
    filters$date_range_selected <- NULL
    filters$sequencer_selected <- unique(csv_data$Sequencer)
  })
  
  observeEvent(input$selected_project, {
    selected_project_distribution(input$selected_project)
  })
  
  observeEvent(input$selected_undetermined_distrinuton_to_display, {
    selected_project_undetermined_distribution(input$selected_undetermined_distrinuton_to_display)
  })
  
  
  # Reactive expression for filtered data
  filtered_data <- reactive({
    data <- csv_data
    if (!is.null(filters$date_range_selected)) {
      data <- subset(data, Date >= filters$date_range_selected[1] & Date <= filters$date_range_selected[2])
    }
    if (!is.null(filters$sequencer_selected)) {
      data <- subset(data, Sequencer %in% filters$sequencer_selected)
    }
    data
  })
  
  # Render the DataTable with the loaded CSV data
  output$table <- renderDT({
    datatable(filtered_data())
  })
  
  # Render the selected columns table
  output$selected_columns_table <- renderDT({
    selected_columns <- c("Project.Name", "Date", "Sequencer", "Most.Common.Undetermined.Barcode", "Undetermined.Reads.Percentage")  # Add the columns you want to display
    datatable(filtered_data()[, selected_columns, drop = FALSE])
  })
  
  # Render the selected plot based on user input (Plot 1)
  output$selected_plot <- renderPlotly({
    # Call the function to get the data
    y_variable <- "Q.30"
    y_axis_label <- "Q 30"
    selected_date_range <- filters$date_range_selected
    selected_sequencers <- filters$sequencer_selected
    color_variable <- input$color_variable
    
    plotting_data <- filtered_data()
    
    if (!is.null(selected_date_range)) {
      plotting_data <- subset(plotting_data, Date >= selected_date_range[1] & Date <= selected_date_range[2])
    }
    if (!is.null(selected_sequencers)) {
      plotting_data <- subset(plotting_data, Sequencer %in% selected_sequencers)
    }
    
    # Filter out rows where the color variable or q30 variable has NA values
    plotting_data$Q.30 <- as.numeric(as.character(plotting_data$Q.30))
    plotting_data <- plotting_data[!is.na(plotting_data$Q.30), ]
    
    if (input$plot_type == "Scatter Plot") {
      p <- ggplot(plotting_data, aes(x = Date, y = !!sym(y_variable), text = paste(Project.Name, "\n", Protocol.Name), color = !!sym(color_variable))) +
        geom_point() +
        labs(title = paste(input$plot_type, "Plot"), x = "X Axis", y = y_axis_label) +
        theme(axis.text.x = element_text(angle = 90, hjust = 1))
    } else if (input$plot_type == "Bar Plot") {
      p <- ggplot(plotting_data, aes(x = Date, y = !!sym(y_variable), text = paste(Project.Name, "\n", Protocol.Name), fill = !!sym(color_variable))) +
        geom_bar(stat = "identity") +
        labs(title = paste(input$plot_type, "Plot"), x = "X Axis", y = y_axis_label) +
        theme(axis.text.x = element_text(angle = 90, hjust = 1))
    }
    
    ggplotly(p, tooltip = "text", width = 1000, height = 500, dynamicTicks = TRUE, margin = list(l = 0, r = 0, b = 0, t = 0))
  })
  
  # Render the selected plot based on user input (Plot 2)
  output$selected_plot_2 <- renderPlotly({
    render_selected_plot("CV", "coefficient of variation", filters$date_range_selected, filters$sequencer_selected, input$color_variable)
  })
  
  # Render the selected plot based on user input (Plot 3)
  output$selected_plot_3 <- renderPlotly({
    render_selected_plot("Total.Read.Count.in.Millions", "Read Count", filters$date_range_selected, filters$sequencer_selected, input$color_variable)
  })
  
  # Render the selected plot based on user input (Plot 4)
  output$selected_plot_4 <- renderPlotly({
    render_selected_plot("Undetermined.Reads.Percentage", "Percentage", filters$date_range_selected, filters$sequencer_selected, input$color_variable)
  })
  
  # Render the selected plot based on user input (Plot 5)
  output$selected_plot_5 <- renderPlotly({
    render_selected_plot("Ratio.Total.Read.Count.and.Expected.Cluster", "Ratio", filters$date_range_selected, filters$sequencer_selected, input$color_variable)
  })
  
  # Render the selected plot based on user input (Plot 6)
  output$selected_plot_6 <- renderPlotly({
    render_selected_plot("Phix.Input.Percent", "Phix Input", filters$date_range_selected, filters$sequencer_selected, input$color_variable)
  })
  
  # Render the selected plot based on user input (Plot 7)
  output$selected_plot_7 <- renderPlotly({
    render_selected_plot("Phix.Output.Percent", "Phix Output", filters$date_range_selected, filters$sequencer_selected, input$color_variable)
  })
  
  # Function to render selected plot
  render_selected_plot <- function(y_variable, y_axis_label, selected_date_range, selected_sequencers, color_variable) {
    data <- filtered_data()
    
    if (!is.null(selected_date_range)) {
      data <- subset(data, Date >= selected_date_range[1] & Date <= selected_date_range[2])
    }
    if (!is.null(selected_sequencers)) {
      data <- subset(data, Sequencer %in% selected_sequencers)
    }
    
    # Filter out rows where the color variable has NA values
    data <- data[!is.na(data[[color_variable]]), ]
    
    if (input$plot_type == "Scatter Plot") {
      p <- ggplot(data, aes(x = Date, y = !!sym(y_variable), text = paste(Project.Name, "\n", Protocol.Name), color = !!sym(color_variable))) +
        geom_point() +
        labs(title = paste(input$plot_type, "Plot"), x = "X Axis", y = y_axis_label) +
        theme(axis.text.x = element_text(angle = 90, hjust = 1))
    } else if (input$plot_type == "Bar Plot") {
      p <- ggplot(data, aes(x = Date, y = !!sym(y_variable), text = paste(Project.Name, "\n", Protocol.Name), fill = !!sym(color_variable))) +
        geom_bar(stat = "identity") +
        labs(title = paste(input$plot_type, "Plot"), x = "X Axis", y = y_axis_label) +
        theme(axis.text.x = element_text(angle = 90, hjust = 1))
    }
    
    ggplotly(p, tooltip = "text", width = 1000, height = 500, dynamicTicks = TRUE, margin = list(l = 0, r = 0, b = 0, t = 0))
  }
  
  
  
  # Function to render Table 1
  output$table_1 <- renderDT({
    selected_columns <- c("Project.Name", "Protocol.Name", "Date", "Application" ,"Sequencer", "Undetermined.Reads.Percentage", "Yields")  # Add the columns you want to display
    datatable(
      filtered_data()[, selected_columns, drop = FALSE],
      options = list(
        scrollY = "400px",  # Set the height of the scrollable area
        fixedColumns = TRUE,  # Enable fixed columns
        scrollX = TRUE  # Enable horizontal scrolling
      ),
      filter = 'top'  # Display filters at the top of the table
    )
  })
  
  # Function to render Table 2
  output$table_2 <- renderDT({
    # Define columns to exclude
    excluded_columns <- c("Read.Distribution", "Undetermined.Distribution.String")
    # Get column names from the data
    all_columns <- colnames(filtered_data())
    # Determine which columns to display
    display_columns <- setdiff(all_columns, excluded_columns)
    # Render the datatable with fixed columns and scroll options
    datatable(
      filtered_data()[, display_columns, drop = FALSE],
      options = list(
        scrollY = "400px",  # Set the height of the scrollable area
        fixedColumns = TRUE,  # Enable fixed columns
        scrollX = TRUE  # Enable horizontal scrolling
      ),
      filter = 'top'  # Display filters at the top of the table
    )
  })
  
  # Function to render Table 3
  output$table_3 <- renderDT({
    selected_columns <- c("Project.Name", "Protocol.Name", "Phix.Input.Percent","Phix.Output.Percent", "Phix.Barcode")  # Add the columns you want to display
    datatable(
      filtered_data()[, selected_columns, drop = FALSE],
      options = list(
        scrollY = "400px",  # Set the height of the scrollable area
        fixedColumns = TRUE,  # Enable fixed columns
        scrollX = TRUE  # Enable horizontal scrolling
      ),
      filter = 'top'  # Display filters at the top of the table
    )
  })
  
  # Function to render Table 4
  output$table_4 <- renderDT({
    selected_columns <- c("Project.Name", "Sequencer", "Sequencing.Kit", "Cycles.Read.1", "Cycles.Index.1", "Cycles.Read.2", "Cycles.Index.2", "Density", "Clusters.PF", "Yields", "Q.30")  # Add the columns you want to display
    datatable(
      filtered_data()[, selected_columns, drop = FALSE],
      options = list(
        scrollY = "400px",  # Set the height of the scrollable area
        fixedColumns = TRUE,  # Enable fixed columns
        scrollX = TRUE  # Enable horizontal scrolling
      ),
      filter = 'top'  # Display filters at the top of the table
    )
  })
  
  # Function to render Table 5
  output$table_5 <- renderDT({
    selected_columns <- c("Project.Name", "Application", "Sequencing.Kit", "STD.in.Millions", "CV", "Number.of.Samples.Above.Requirement", "Number.of.Samples.Below.Requirement", "Total.Read.Count.in.Millions", "Expected.Clusters", "Ratio.Total.Read.Count.and.Expected.Cluster")  # Add the columns you want to display
    datatable(
      filtered_data()[, selected_columns, drop = FALSE],
      options = list(
        scrollY = "400px",  # Set the height of the scrollable area
        fixedColumns = TRUE,  # Enable fixed columns
        scrollX = TRUE  # Enable horizontal scrolling
      ),
      filter = 'top'  # Display filters at the top of the table
    )
  })
  
  # Function to render Table 6
  output$table_6 <- renderDT({
    selected_columns <- c("Project.Name", "Undetermined.Reads.Percentage", "Most.Common.Undetermined.Barcode","Most.Common.Undetermined.Barcode.Percentage")  # Add the columns you want to display
    datatable(
      filtered_data()[, selected_columns, drop = FALSE],
      options = list(
        scrollY = "400px",  # Set the height of the scrollable area
        fixedColumns = TRUE,  # Enable fixed columns
        scrollX = TRUE  # Enable horizontal scrolling
      ),
      filter = 'top'  # Display filters at the top of the table
    )
  })
  
  # Function to render Table 7
  output$table_7 <- renderDT({
    selected_columns <- c("Project.Name", "Protocol.Name", "Sciebo.Found", "Application")  # Add the columns you want to display
    datatable(
      filtered_data()[, selected_columns, drop = FALSE],
      options = list(
        scrollY = "400px",  # Set the height of the scrollable area
        fixedColumns = TRUE,  # Enable fixed columns
        scrollX = TRUE  # Enable horizontal scrolling
      ),
      filter = 'top'  # Display filters at the top of the table
    )
  })
  
  # Function to render selected distribution plot
  output$selected_distribution_plot <- renderPlotly({
    # Filter data based on selected project
    selected_project_data <- subset(filtered_data(), Project.Name == selected_project_distribution())
    
    # Extract and process Read.Distribution string
    distribution_string <- selected_project_data$Read.Distribution
    distribution_values <- as.numeric(unlist(strsplit(distribution_string, "-")))
    
    # Create a data frame for plotting
    samples <- if (length(distribution_values) > 0) {
      paste(c(seq_along(distribution_values)[-length(distribution_values)], "undetermined"), sep = " ")
    } else {
      paste(seq_along(distribution_values), sep = " ")
    }
    plot_data <- data.frame(Sample = samples, Value = distribution_values)
    
    # Plot histogram
    p <- ggplot(plot_data, aes(x = Sample, y = Value)) +
      geom_bar(stat = "identity", fill = "blue", color = "black", alpha = 0.7) +
      labs(title = "Distribution Plot", x = "Sample", y = "Percentage") +
      theme_minimal()
    
    ggplotly(p, width = 800, height = 400)
  })
  
  # Function to render selected distribution plot
  output$selected_unditermined_distribution_plot <- renderPlotly({
    # Filter data based on selected project
    selected_project_data <- subset(filtered_data(), Project.Name == selected_project_undetermined_distribution())
    
    # Extract and process Read.Distribution string
    distribution_string <- selected_project_data$Undetermined.Distribution.String
    distribution_values <- as.numeric(unlist(strsplit(distribution_string, "-")))
    
    # Create a data frame for plotting
    samples <- paste(seq_along(distribution_values), sep = " ")
    plot_data <- data.frame(Sample = samples, Value = distribution_values)
    
    # Plot histogram
    p <- ggplot(plot_data, aes(x = Sample, y = Value)) +
      geom_bar(stat = "identity", fill = "blue", color = "black", alpha = 0.7) +
      labs(title = "Distribution Plot", x = "Barcode", y = "Percentages") +
      theme_minimal()
    
    ggplotly(p, width = 800, height = 400)
  })
}

# Run the Shiny app
shinyApp(ui, server)