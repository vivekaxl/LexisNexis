require(graphics)
# scale data to mean=0, sd=1 and convert to matrix
mtscaled <- as.matrix(scale(mtcars))

# create heatmap and don't reorder columns
heatmap(mtscaled, Colv=F, scale='none')