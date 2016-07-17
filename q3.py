import pandas as pd
from bs4 import BeautifulSoup as bs
import numpy as np
import matplotlib.pyplot as plt

# Read in the diabetes rate data
df_Access = pd.read_excel('DataDownload.xls', sheetname = 4)
df_Health = pd.read_excel('DataDownload.xls', sheetname = 6)
plot1 = np.array(df_Health[['FIPS', 'PCT_DIABETES_ADULTS10']].dropna())
plot1[:, 0] = plot1[:,0].astype(int)
plot1[:, 1] = plot1[:,1]

# First plot
# Load the SVG Map
svg = open('counties.svg', 'r').read()
# Load into Beautiful Soup
soup = bs(svg, selfClosingTags=['defs','sodipodi:namedview'])
# Find counties
paths = soup.findAll('path')
# Map colors
colors = ["#fff5eb", "#fee6ce", "#fdd0a2", "#fdae6b", "#fd8d3c", "#f16913", "#d94801", "#a63603", "#7f2704"]
# County style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;\
    stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;\
    marker-start:none;stroke-linejoin:bevel;fill:'
# Color the counties based on unemployment rate
for p in paths:
  if p['id'] not in ["State_Lines", "separator"]:
    # pass
    try:
      i = np.where(plot1[:, 0] == int(p['id']))[0][0]
      rate = plot1[i][1]
    except:
      continue
    color_class = min(int(rate)/2-1, 9)
    color = colors[color_class]
    p['style'] = path_style + color

# output to diabetes10.svg
output = open('diabetes10.svg', 'w')
output.write(soup.prettify())
output.close()

# Second plot, correlation between low access and diabete rate
p1 = np.array(df_Health.groupby(by = 'State')['PCT_DIABETES_ADULTS09'].mean().dropna())
p2 = np.array(df_Access.groupby(by = 'State')['PCT_LACCESS_POP10'].mean().dropna())

plt.close()
plt.scatter(p1, p2)
plt.xlabel('Adult diabetes rate, 2010')
plt.ylabel('Population, low access to store (%), 2010')
plt.savefig('laccess10.tif')
