require(MASS)
library(AER)
library(Hmisc)
library(stargazer)
library(brant)

results <- read.table(
  file='../frames/ordinal_logit.csv',
  sep=',',
  header = T)

results$assertion_roulette <- as.numeric(results$assertion_roulette)
results$score <- ordered(results$score, c(1,2,3,4,5))

### check the collinearity between the predictors ###
checkCorrelation = function(form, dataset){
  vc <- varclus(form, data=dataset)
  plot(vc)
  threshold <- 0.6
  abline(h=1-threshold, col = "red", lty = 2)
}

### formula with all the factors
full_formula <- results$score ~ results$assertion_roulette + 
  results$readability + results$cbo + results$wmc + results$rfc + results$nosi +
  results$loc + results$line_coverage + results$mutation_score + results$assertion_density 

checkCorrelation(full_formula, results)

### remove collinear predictors ###
clean_formula <- results$score ~ results$assertion_roulette + results$assertion_density +
  results$readability + results$cbo + results$wmc + results$rfc + results$nosi +
  results$loc + results$mutation_score + results$experience

### train the model ###
model <- polr(formula = clean_formula, data = results, Hess=TRUE)
summary(model)

## odds ratios (to improve explainability of the model)
exp(coef(model))

### calculate pvalues ###
coeftest(model)

### create latex table ###
stargazer(model, title="Regression Results", no.space=TRUE, single.row=TRUE)

## checking assumptions
brant(model)


