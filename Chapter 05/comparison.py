# Models comparison

import numpy as np
import pandas as pd

N = [200, 1000, 5000]
D = 20
convRanges = [(0., 0.1), (0., 0.3), (0., 0.5)]

results = list()
for n in N:
    for ranges in convRanges:
        results.append([])
        for d  in range(3, D + 1):
            p1 = 0
            p2 = 0

            for rounds in range(1000):
                
                conversionRates = list()
                for i in range(d):
                    conversionRates.append(np.random.uniform(low = ranges[0], high = ranges[1]))
                    
                X = np.zeros((n,d))
                for i in range(n):
                    for j in range(d):
                        if np.random.rand() < conversionRates[j]:
                            X[i][j] = 1
                
                nPosReward = np.zeros(d)
                nNegReward = np.zeros(d)
                
                for i in range(n):
                    selected = 0
                    maxRandom = 0
                    
                    for j in range(d):
                        randomBeta = np.random.beta(nPosReward[j] + 1, nNegReward[j] + 1)
                        if randomBeta > maxRandom:
                            maxRandom = randomBeta
                            selected = j
                        
                    if X[i][selected] == 1:
                        nPosReward[selected] += 1
                    else:
                        nNegReward[selected] += 1
                
                nSelected = nPosReward + nNegReward
                
                left = n - max(nSelected)
                
                countStandard = np.zeros(d)
                
                x = int(left / d)
                for i in range(x):
                    for j in range(d):
                        if X[i][j] == 1:
                            countStandard[j] += 1
                
                bestStandard = np.argmax(countStandard)
                bestReal = np.argmax(conversionRates)
                bestTS = np.argmax(nSelected)

                if bestTS == bestReal:
                    p1 += 1
                if bestStandard == bestReal:
                    p2 += 1
                
            print('N = ' + str(n) + ' d = ' + str(d) + ' range = ' + str(ranges) + ' | result Thompson Sampling = ' + str(p1) + ' result Standard solution = ' + str(p2))
            results.append([n, ranges, d, p1, p2])
                
df = pd.DataFrame(results)
df.to_excel('results.xlsx', sheet_name = 'Result', index = False)
