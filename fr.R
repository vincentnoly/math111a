library(ggplot2)
library(rpart)
library(randomForest)
library(forestFloor)
library(pdp)
library(plotmo)
library(randomForestExplainer)

set.seed(123)

# Import data
allManga <- read.csv("D:\\homelab\\math111a\\data\\rtReadyNoTitle.csv")
allManga <- allManga[-1,]
allManga <- allManga[sample(1:nrow(allManga)),]

longManga <- read.csv("D:\\homelab\\math111a\\data\\demographic\\longStrip.csv")
longManga <- longManga[-1,]
longManga <- longManga[sample(1:nrow(longManga)),]

shounen <- read.csv("D:\\homelab\\math111a\\data\\demographic\\shounen.csv")
shounen <- shounen[-1,]
shounen <- shounen[sample(1:nrow(shounen)),]

shoujo <- read.csv("D:\\homelab\\math111a\\data\\demographic\\shoujo.csv")
shoujo <- shoujo[-1,]
shoujo <- shoujo[sample(1:nrow(shoujo)),]

seinen <- read.csv("D:\\homelab\\math111a\\data\\demographic\\seinen.csv")
seinen <- seinen[-1,]
seinen <- seinen[sample(1:nrow(seinen)),]

josei <- read.csv("D:\\homelab\\math111a\\data\\demographic\\josei.csv")
josei <- josei[-1,]
josei <- josei[sample(1:nrow(josei)),]

# Change data to numeric
allManga$Mean.Rating <- as.numeric(as.character(allManga$Mean.Rating))
allManga$Follows <- as.numeric(as.character(allManga$Follows))

longManga$Mean.Rating <- as.numeric(as.character(longManga$Mean.Rating))
longManga$Follows <- as.numeric(as.character(longManga$Follows))

shounen$Mean.Rating <- as.numeric(as.character(shounen$Mean.Rating))
shounen$Follows <- as.numeric(as.character(shounen$Follows))

shoujo$Mean.Rating <- as.numeric(as.character(shoujo$Mean.Rating))
shoujo$Follows <- as.numeric(as.character(shoujo$Follows))

seinen$Mean.Rating <- as.numeric(as.character(seinen$Mean.Rating))
seinen$Follows <- as.numeric(as.character(seinen$Follows))

josei$Mean.Rating <- as.numeric(as.character(josei$Mean.Rating))
josei$Follows <- as.numeric(as.character(josei$Follows))

# Bagging data
train <- sample(nrow(allManga), 0.7*nrow(allManga), replace=FALSE)
trainAllManga <- allManga[train,]
testAllManga <- allManga[-train,]

train <- sample(nrow(longManga), 0.7*nrow(longManga), replace=FALSE)
trainLongManga <- longManga[train,]
testLongManga <- longManga[-train,]

train <- sample(nrow(shounen), 0.7*nrow(shounen), replace=FALSE)
trainShounen <- shounen[train,]
testShounen <- shounen[-train,]

train <- sample(nrow(shoujo), 0.7*nrow(shoujo), replace=FALSE)
trainShoujo <- shoujo[train,]
testShoujo <- shoujo[-train,]

train <- sample(nrow(seinen), 0.7*nrow(seinen), replace=FALSE)
trainSeinen <- seinen[train,]
testSeinen <- seinen[-train,]

train <- sample(nrow(josei), 0.7*nrow(josei), replace=FALSE)
trainJosei <- josei[train,]
testJosei <- josei[-train,]

# Models
allModel = randomForest(Mean.Rating ~. - Self.Published - Doujinshi - Official.Colored, data = trainAllManga, ntree=128, proximity=TRUE, importance = TRUE, mtry=60, do.trace=128)
longModel = randomForest(Mean.Rating ~. - Self.Published - Doujinshi - Official.Colored, data = trainLongManga, ntree=128, proximity=TRUE, importance = TRUE, mtry=60, do.trace=128)
shounenModel = randomForest(Mean.Rating ~. - Self.Published - Doujinshi - Official.Colored, data = trainShounen, ntree=128, proximity=TRUE, importance = TRUE, mtry=60, do.trace=128)
shoujoModel = randomForest(Mean.Rating ~. - Self.Published - Doujinshi - Official.Colored, data = trainShoujo, ntree=128, proximity=TRUE, importance = TRUE, mtry=60, do.trace=128)
seinenModel = randomForest(Mean.Rating ~. - Self.Published - Doujinshi - Official.Colored, data = trainSeinen, ntree=128, proximity=TRUE, importance = TRUE, mtry=60, do.trace=128)
joseiModel = randomForest(Mean.Rating ~. - Self.Published - Doujinshi - Official.Colored, data = trainJosei, ntree=128, proximity=TRUE, importance = TRUE, mtry=60, do.trace=128)

# Calculate MAE
allErrors <- abs(predict(allModel, testAllManga) - testAllManga$Mean.Rating)
longErrors <- abs(predict(longModel, testLongManga) - testLongManga$Mean.Rating)
shounenErrors <- abs(predict(shounenModel, testShounen) - testShounen$Mean.Rating)
shoujoErrors <- abs(predict(shoujoModel, testShoujo) - testShoujo$Mean.Rating)
seinenErrors <- abs(predict(seinenModel, testSeinen) - testSeinen$Mean.Rating)
joseiErrors <- abs(predict(joseiModel, testJosei) - testJosei$Mean.Rating)

mae <- c(mean(allErrors), mean(longErrors), mean(shounenErrors), mean(shoujoErrors), mean(seinenErrors), mean(joseiErrors))

print(mae)

importanceAll <- importance(allModel)
topVarAll <- rownames(importanceAll)[order(importanceAll[, 1], decreasing = TRUE)[1:9]]
pdpPlotsAll <- list()
for (variable in topVarAll) {
  pdpPlotsAll[[variable]] <- partial(allModel, pred.var = variable, train=trainAllManga, plot_type="lines")
}
par(mfrow = c(3, 3)) 
for (i in 1:9) {
  plot(pdpPlotsAll[[topVarAll[i]]], main = topVarAll[i], type='l')
}

importanceLong <- importance(longModel)
topVarLong <- rownames(importanceLong)[order(importanceLong[, 1], decreasing = TRUE)[1:9]]
pdpPlotsLong <- list()
for (variable in topVarLong) {
  pdpPlotsLong[[variable]] <- partial(longModel, pred.var = variable, train=trainLongManga, plot_type="lines")
}
par(mfrow = c(3, 3)) 
for (i in 1:9) {
  plot(pdpPlotsLong[[topVarLong[i]]], main = topVarLong[i], type='l')
}

importanceShounen <- importance(shounenModel)
topVarShounen <- rownames(importanceShounen)[order(importanceShounen[, 1], decreasing = TRUE)[1:9]]
pdpPlotsShounen <- list()
for (variable in topVarShounen) {
  pdpPlotsShounen[[variable]] <- partial(shounenModel, pred.var = variable, train=trainShounen, plot_type="lines")
}
par(mfrow = c(3, 3)) 
for (i in 1:9) {
  plot(pdpPlotsShounen[[topVarShounen[i]]], main = topVarShounen[i], type='l')
}

importanceShoujo <- importance(shoujoModel)
topVarShoujo <- rownames(importanceShoujo)[order(importanceShoujo[, 1], decreasing = TRUE)[1:9]]
pdpPlotsShoujo <- list()
for (variable in topVarShoujo) {
  pdpPlotsShoujo[[variable]] <- partial(shoujoModel, pred.var = variable, train=trainShoujo, plot_type="lines")
}
par(mfrow = c(3, 3)) 
for (i in 1:9) {
  plot(pdpPlotsShoujo[[topVarShoujo[i]]], main = topVarShoujo[i], type='l')
}

importanceSeinen <- importance(seinenModel)
topVarSeinen <- rownames(importanceSeinen)[order(importanceSeinen[, 1], decreasing = TRUE)[1:9]]
pdpPlotsSeinen <- list()
for (variable in topVarSeinen) {
  pdpPlotsSeinen[[variable]] <- partial(seinenModel, pred.var = variable, train=trainSeinen, plot_type="lines")
}
par(mfrow = c(3, 3)) 
for (i in 1:9) {
  plot(pdpPlotsSeinen[[topVarSeinen[i]]], main = topVarSeinen[i], type='l')
}

importanceJosei <- importance(joseiModel)
topVarJosei <- rownames(importanceJosei)[order(importanceJosei[, 1], decreasing = TRUE)[1:9]]
pdpPlotsJosei <- list()
for (variable in topVarJosei) {
  pdpPlotsJosei[[variable]] <- partial(joseiModel, pred.var = variable, train=trainJosei, plot_type="lines")
}
par(mfrow = c(3, 3)) 
for (i in 1:9) {
  plot(pdpPlotsJosei[[topVarJosei[i]]], main = topVarJosei[i], type='l')
}


ggplot(allManga, aes(y = Mean.Rating)) +
  geom_boxplot(fill="slateblue", alpha=0.2) +
  ggtitle("Boxplot of Values") +
  xlab("Data") +
  ylab("Values") +
  ylim(6.5, 10) 

ggplot(combined_data, aes(x = dataset, y = values, fill = dataset)) +
  geom_boxplot(alpha = 0.7) +
  ggtitle("Boxplot Comparison of Datasets") +
  xlab("Datasets") +
  ylab("Values") +
  scale_fill_manual(values = c("Dataset 1" = "lightblue", "Dataset 2" = "lightgreen")) +
  theme_minimal() +
  theme(axis.text = element_text(size = 12),
        axis.title = element_text(size = 14, face = "bold"),
        plot.title = element_text(size = 16, face = "bold"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.title = element_blank())


