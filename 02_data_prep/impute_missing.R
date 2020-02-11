##################################################################################
# Name of Script: impute_missing.R
# Description:
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

## require folders

##################################
# DEFINE LIBRARIES AND FUNCTIONS #
##################################
pacman::p_load(data.table, assertthat, tidyr, 
                mice, lattice, wNNsel, WaverR,
                VIM, mix)

vet_data <- function(input_df, stage = "missing"){
    ## for missing values
    if(stage == "missing"){
        barMiss(input_df)
        barMiss(input_df, only.miss = FALSE)
    } else{
        ## for imputed values
        barMiss(input_df, delimiter = "_imp")
        barMiss(input_df, delimiter = "_imp", only.miss = FALSE)
    }
}

impute_method_selection <- function(method = "", input_df){
    # This method takes in a dataset with missing values and depending on
    # imputation method selected, returned imputed dataset
    #
    # Parameters:
    #   method: [knn, random_forest, hot_deck, linear, em]
    #   input_df: dataframe with missing values
    #
    # Returns: imputed dataset
    #
    if (method == "knn"){
        # weighted knn 
        input_mat <- as.matrix(input_df)

        # cross validate for best lambda
        cv_best <- cv.wNNSel(x, kernel = "gaussian", x.dist = "euclidean", 
                            method = "2", m.values = seq(2, 8, by = 2),
                            lambda.values = seq(0, 0.6, by = 0.01)[-1], times.max = 5)

        imputed_df <- wNNSel.impute(x, k, useAll = TRUE, 
                                    x.initial = NULL, x.dist = "euclidean",
                                    kernel = "gaussian", lambda = cv_best$lambda.opt, 
                                    convex = TRUE,
                                    method = "2", m = cv_best$m.opt, c = 0.3,
                                    verbose = TRUE, verbose2 = FALSE)
    } else if (method == "random_forest"){
        input_mat <- as.matrix(input_df)
        imputed_df <- missForest(input_mat, maxiter = 10, ntree = 100, variablewise = FALSE,
                    decreasing = FALSE, verbose = FALSE,
                    mtry = floor(sqrt(ncol(xmis))), replace = TRUE,
                    classwt = NULL, cutoff = NULL, strata = NULL,
                    sampsize = NULL, nodesize = NULL, maxnodes = NULL,
                    xtrue = NA, parallelize = c('no', 'variables', 'forests'))

    } else if (method == "hot_deck"){
        imputed_df <- hotdeck(data, variable = c(), ord_var = c(),
                             impNA = TRUE, imp_var = TRUE,
                            imp_suffix = "imp")

    } else if (method == "linear"){
        imputed_df <- waverr(RawData = input_mat, Nrepeats = 5)
    } else if (method == "em"){
        imputed_df = em.mix(s, start, prior=1, maxits=1000, showits=TRUE, eps=0.0001)
    }
    return(imputed_df)
}
