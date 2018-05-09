from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# lons_lats_vect = np.column_stack((lons_vect, lats_vect)) # Reshape coordinates
# polygon = Polygon([(71.5905714395,91.473704378), (71.3894312771,92.6528126702), (72.7703550325, 92.3449414336), (72.1714376248, 91.5848174553)]) # create polygon
a = {}
a['x1'] = 91.473704378
a['x2'] = 92.6528126702
a['x3'] = 92.3449414336

a['y1'] = 71.5905714395
a['y2'] = 71.3894312771
a['y3'] = 72.7703550325

polygon = Polygon([(91.473704378,71.5905714395),(92.6528126702,71.3894312771),(92.3449414336,72.7703550325),(91.5848174553,72.1714376248)]) # create polygon
# final = {}
# for i in range(len(a)):


# polygon = Polygon(list(a.items())) # create polygon

# point = Point(72.19524581118354,92.999267578125) # create point
point1 = Point(-991.79,71.9) # create point
point2 = Point(92.3,71.9) # create point
point3 = Point(92.3,72.1) # create point

print(polygon.contains(point1)) # check if polygon contains point
print(polygon.contains(point2)) # check if polygon contains point
print(polygon.contains(point3)) # check if polygon contains point

# 91.473704378,71.5905714395,92.6528126702,71.3894312771,92.3449414336,72.7703550325,91.5848174553,72.1714376248