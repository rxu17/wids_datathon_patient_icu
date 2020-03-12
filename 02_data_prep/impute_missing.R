##################################################################################
# Name of Script: impute_missing.R
# Description: This script searches for missingness in a dataset and based on
#               user selection, takes an imputation method and fills in the missingness
# Arguments: output from transform_data.py
# Output: imputed dataset
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
pacman::p_load(data.table, assertthat, tidyr, mice, lattice, wNNsel, WaverR,
                VIM, mix, glue)


vet_data <- function(input_df, stage = "missing"){
    # This method generates plots for showing distribution of
    # missing data within the dataset for each variable
    #
    # Parameters:
    #   input_df: dataframe with missing values
    #   stage: str, ['missing', 'filled'] - missing stage is when 
    #                variables are not filled in, filled is when values
    #                have been imputed 
    #
    if(stage == "missing"){
        aggr_plot <- aggr(data, col=c('navyblue','red'), numbers=TRUE, 
                          sortVars=TRUE, labels=names(data), cex.axis=.7, 
                          gap=3, ylab=c("Histogram of missing data","Pattern"))
    } 
    if(stage == "filled"){
        ## for imputed values
        barMiss(input_df, delimiter = "_imp")
        barMiss(input_df, delimiter = "_imp", only.miss = FALSE)
    }
}


check_threshold <- function(input_df, th_pct = 5){
    # This method checks the percentage of missing
    # and drops variables that are greater than that threshold
    #
    # Parameters:
    #   input_df: dataframe with missing values
    #   th_pct: int, {0...100} percentage of missing val
    #           in dataset that you would like to be cutoff pt
    #
    # Returns: data.table with not meeting threshold 
    # variables removed
    #
    assert_that(th_pct <= 1 & th_pct >= 0, 
                msg = "threshold precentage is not in the range of 0...1")
    p_miss <- function(x){  # helper function checks for pctage missing in a col
                    (sum(is.na(x))/length(x))*100
                    }
    p_miss_mat <- apply(input_df, 2, p_miss) # applies check across all cols
    p_miss_mat$id_col <- 1
    setDT(p_miss_mat)
    # reshapes data, from variables being wide to long
    p_miss_mat <- melt(p_miss_mat, id.vars = "id_col")

    # find vars that don't meet threshold and drop
    var_to_drop <- p_miss_mat[value > th_pct]$var %>% unique
    missing_removed <- input_df[, !(var_to_drop), with = F]
    return(missing_removed)
}


impute_method_selection <- function(method = "knn", input_df){
    # This method takes in a dataset with missing values and depending on
    # imputation method selected, returned imputed dataset
    #
    # Parameters:
    #   method: [knn, random_forest, hot_deck, linear, em]
    #   input_df: dataframe with missing values
    #
    # Returns: imputed dataset
    #
    allowed_met <- c('knn', 'random_forest', 'mice','hot_deck', 'linear', 'em')
    assert_that(method %in% allowed_met, 
            msg = glue("You must pick a method from available methods: {allowed_met}"))
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
        imputed_df <- em.mix(s, start, prior=1, maxits=1000, showits=TRUE, eps=0.0001)
    } else if (method == "mice"){
        imputed_df <- mice(input_df, m = 5, method = "rf")
        imputed_df <- complete(imputed_df)
    }
    return(imputed_df)
}

main <- function(){
    # reads in data, imputes and saves
    input_df <- fread(paste0(getwd(), "/encoded_df.csv"))
    thres_df <- check_threshold(input_df)
    imputed_df <- impute_method_selection(thres_df)
    fwrite(imputed_df, paste0(getwd(), "/imputed_df.csv"))
}

if(!interactive){
    main()
} else{
    main()
}