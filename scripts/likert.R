require(grid)
require(lattice)
require(latticeExtra)
require(HH)

data <- read.csv('../data/likert.csv')
names(data) <- c('index', 'I do not know', 'Not at all', 'Slightly', 'Moderately', 'Very', 'Extremely')
index <- c('readability (7.1)', 'maintainability (7.2)', 'I/O pairs (7.3)', 'fault revealing (7.4)', 'flakiness (7.5)', 
            'design (7.6)', 'longevity (7.7)', 'reusability (7.8)', 'complexity (7.9)', 'mut. score (7,10)', 
            'exec. time (7.11)')
data = data[,2:7]
data = cbind(index, data)
l <- likert(index ~ .,data=data,
            ylab=NULL, 
            ReferenceZero=4,
       as.percent=TRUE, positive.order=TRUE,
       main = list("",x=unit(.55, "npc")),
       xlim=c(-70,-60,-40,-20,0,20,40,60,80,100), strip=FALSE,
       par.strip.text=list(cex=.7),
       rightAxis=TRUE, # for the raw total
       scales = list(y = list(cex = 1.2)))
plot(l)
