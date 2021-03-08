import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib 
import matplotlib.pyplot as plt

# Temperature = {very_cold, cold, warm, hot, very_hot}
temperature = ctrl.Antecedent(np.arange(0, 41, 0.1), 'temperature')
# Target = {very_cold, cold, warm, hot, very_hot}
target = ctrl.Antecedent(np.arange(0, 11, 0.1), 'target')
# Change = {heat, no_change, cool} 
change = ctrl.Consequent(np.arange(0, 51, 1), 'change')

# Auto-membership function population and changing labels
temperature.automf(5)
names = ['very_cold', 'cold', 'warm', 'hot', 'very_hot']
temperature.automf(names=names)
target.automf(names=names)

change['cool'] = fuzz.trimf(change.universe, [0, 0, 20])
change['no_change'] = fuzz.trimf(change.universe, [18, 28, 32])
change['heat'] = fuzz.trimf(change.universe, [30, 50, 50])

# You can see how these look with .view()
#temperature.view()
#target.view()
#change.view()
#plt.show()

# Some rules examples
rule1 = ctrl.Rule(temperature['cold'] | temperature['very_cold'] & target['warm'], change['heat'])
rule2 = ctrl.Rule(temperature['hot'] | temperature['very_hot'] & target['warm'], change['cool'])
rule3 = ctrl.Rule(temperature['warm'] & target['warm'], change['no_change'])

# Create system
temperature_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
air_conditioner = ctrl.ControlSystemSimulation(temperature_ctrl)

# Pass example inputs to the ControlSystem using Antecedent labels 
air_conditioner.input['temperature'] = 20
air_conditioner.input['target'] = 5

# Compute
air_conditioner.compute()

# Print result
print(air_conditioner.output['change'])
change.view(sim=air_conditioner)
plt.show()