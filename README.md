# PointInPolygon

A Python Flask app to find if a point is present in a polygon or not 

## Question1:
http://localhost:5000/houseprice?GrLivArea=1795&TotalBsmtSF=1777&GarageArea=534&YearBuilt=20

This is the sample API GET request to the app; which is running on the localhost. 
It accepts 4 parameters
 - GrLivArea: The above-ground living area of the house, in square feet.
- TotalBsmtSF: The total basement area, in square feet
- GarageArea: The total garage area, in square feet
- YearBuilt: The year the house was built

The call to the API can handle non-sanitized inputs

## Question2:
http://localhost:5000/houselookup?x1=50&y1=30&x2=57.5&y2=34&x3=62&y3=39&x4=65.5&y4=31.5&x5=60.25&y5=27.5&x6=58&y6=24.87&x7=50&y7=30

This API call accepts >=6 even parameters to create a *polygon* and find all the houses which are contained inside the *polygon*. The houses list is present [here](house_coordinates.csv)