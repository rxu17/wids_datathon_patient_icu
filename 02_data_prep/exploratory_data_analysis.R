##################################################################################
# Name of Script: exploratory_data_analysis.R
# Description:
# Arguments: N/A
# Output: 
# Contributors: Rixing Xu
###################################################################################

#############################
# DEFINE PARAMETERS         #
#############################
# set working directories by operating system
rm(list=ls())

user <- Sys.info()[["user"]]

## require folders

##################################
# DEFINE LIBRARIES AND FUNCTIONS #
##################################
pacman::p_load(data.table, assertthat, tidyr, shiny, ggplot2, RMariaDB,
               shinydashboard, plotly, formattable, ini, shinythemes, RColorBrewer,
               scales, ggthemes, DBI, RMySQL, memoise)
