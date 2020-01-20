import pygame
import math
from random import randint
import pandas, numpy
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import csv

data = pandas.read_csv('jumps.csv')
data.head()
X_train = data.iloc[:, 0:3]
y_train = data.iloc[:, 3]

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
jumpd = encoder.fit_transform(X_train.iloc[:, 2])

X_train.iloc[:, 2] = numpy.reshape(jumpd, (-1, 1))

from sklearn.model_selection import GridSearchCV
param_grid = [
    {'n_estimators': [3, 10, 30], 'max_features': [2, 3]},
    {'bootstrap': [False], 'n_estimators': [1,2,  3, 10], 'max_features': [1, 2, 3]}
]

classifier = RandomForestClassifier()
optimized = GridSearchCV(classifier, param_grid, cv=5, scoring='neg_mean_squared_error')
optimized.fit(X_train, y_train)
classifier = optimized.best_estimator_
print(classifier)

display_width = 800
display_height = 600
white = (255, 255, 255)
green = (0, 255, 0)

pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Focus')
clock = pygame.time.Clock()

ingame = True
jumping = False
airtime = 0
count = 0
objpos = 600
rate_of_change = 5 # Speed at which the incoming object moves

file = open('jumps.csv', 'a')
writer = csv.writer(file)

while ingame: 
    objpos -= rate_of_change

    if jumping:
        count += 3 # every tick (or frame), the jump distance will change by 3

        if count < 60:
            airtime = count % 60
        else:
            airtime = 60 - (count - 60)

    if airtime == 0:
        jumping = False
        count = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ingame = False
        
    X_test = numpy.reshape(numpy.array([objpos, rate_of_change, 1]), (1, -1))
    if classifier.predict(X_test) == 1 and airtime == 0:
        jumping = True
        saved_pos = objpos

    gameDisplay.fill((0, 0, 0))
    pygame.draw.rect(gameDisplay, white, (200, 300 - airtime, 30, 30))
    pygame.draw.rect(gameDisplay, green, (objpos, 310, 25, 10))
    
    if 200 < objpos < 230 or 200 < objpos + 25 < 230: # Player starts at 200, rectangle is 30 pixels
        if 310 < 300 - airtime + 30 <= 330: # Collision with bullet
            ingame = False
            if jumping:
                writer.writerow([saved_pos, rate_of_change, jumping, 0])
            else:
                writer.writerow([objpos, rate_of_change, jumping, 0])

            file.close()   

    pygame.display.update()
    if objpos < 100:
        writer.writerow([saved_pos, rate_of_change, True, 1])
        objpos = 800
        rate_of_change = randint(4, 8)

    clock.tick(60)

