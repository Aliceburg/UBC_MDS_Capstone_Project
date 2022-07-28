mb_join<-read.csv("mb_join.csv",as.is = TRUE)

summary(mb_join)

mbpca <- prcomp(mb_join[,-c(1:7)], scale.=TRUE)
summary(mbpca)


plot(mbpca, type="lines", npcs=26)

round(mbpca$rotation[,1:6], 2)

loadi <- round(mbpca$rotation[,1:6], 2)
loadi[abs(loadi)<0.2] <- NA
loadi

head(mb_join[order(mbpca$x[,1], decreasing=TRUE),c(1:7)])

tail(mb_join[order(mbpca$x[,1], decreasing=TRUE),c(1:7)])

head(mb_join[order(mbpca$x[,2], decreasing=TRUE),c(1:7)])

tail(mb_join[order(mbpca$x[,2], decreasing=TRUE),c(1:7)])

head(mb_join[order(mbpca$x[,3], decreasing=TRUE),c(1:7)])

tail(mb_join[order(mbpca$x[,3], decreasing=TRUE),c(1:7)])

biplot(mbpca)
