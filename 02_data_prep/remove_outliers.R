##################################################################################
# Name of Script: remove_outliers.R
# Description: This code will detect outliers and deal with it in one of a few 
#               ways: 
#               - turn them into NAs (and let impute missing handle)
#               - capping outliers, for outside 1.5 * IQR limits, we use 
#                 5 percentile for lower limit and 95% percentile for upper limit
#               
# Arguments: N/A
# Output: 
# Contributors: rxu17
###################################################################################

#############################
# DEFINE PARAMETERS         #
#############################
# set working directories by operating system
rm(list=ls())

user <- Sys.info()[["user"]]

##################################
# DEFINE LIBRARIES AND FUNCTIONS #
##################################

detect_outliers <- function(input_df, dep_var, predictors = c()){
    # This method uses various outlier detection methods
    #
    # Parameters: 
    #   predictors: list, list of predictor var to use in outlier model
    #   input_df: data.table
    #   dep_var: dependent variable of model
    #
    # Returns: 
    #

    if(length(predictors) == 0) formula <- "{dep_var} ~ ." %>% glue
    else formula <- paste0("{dep_var} ~", paste0(predictors, collapse = " + ")) %>% glue
    mod <- lm(formula, data = input_df)
    cooksd <- cooks.distance(mod)

    plot(cooksd, pch = "*", cex = 2, main="Influential Obs by Cooks distance")  # plot cook's distance
    abline(h = 4 * mean(cooksd, na.rm = T), col="red")  # add cutoff line
    text(x = 1:length(cooksd)+1, y = cooksd, 
        labels=ifelse(cooksd > 4 * mean(cooksd, na.rm = T), names(cooksd),""), col = "red")  # add labels

    # threshold is 4* line
    input_df[, is_outlier := ifelse(cookds, 1, 0)]
}

treat_outliers <- function(input_df, out_method = "NA"){
    # This method uses various outlier treatment methods to 
    # deal with the outliers detected from detect_outliers function
    #
    # Parameters:
    #   input_df: data.table
    #   out_method: str, ['NA', 'cap', '']
    # 
    # Returns:

    if(out_method == "NA"){
        input_df[, (col) := NA]
    }
    else if (out_method == "cap"){
        input_df[, .(lower_cap) = lapply(.SD, FUN = quantile(probs = 0.05)), .SDcols = cols_to_treat]
        input_df[, .(upper_cap) = lapply(.SD, FUN = quantile(probs = 0.95)), .SDcols = cols_to_treat]
        input_df[]
    } 

}