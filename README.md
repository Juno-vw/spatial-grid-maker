# Grid Creator

## Creates a geographic grid

This was build for the Maidenhead Grid, but can build any grid with the same number of rows/columns per level.

### To Configure:
If you want to add another level, just add to the grid['levels'] definition. If you wanted to add another level of 0-9, add "3:range(0,10)"

### Running the code:
You can just run the code as it is and it will create a 2nd level grid. You can change the level by changing "main(1)" or call the code externally by "main(x)".

### Set the aoi for any grid past the 2nd level (index 1) because the file size gets BIG fast.
