import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
plt.plot(np.linspace(0,10,1000), [np.sin(x) for x in np.linspace(0,10,1000)])
plt.show()

