import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df["overweight"] = df["weight"] / (df["height"] / 100)**2
df.loc[df["overweight"] <= 25, "overweight"] = 0
df.loc[df["overweight"] != 0, "overweight"] = 1
df["overweight"] = df["overweight"].astype("int8")



# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[df["cholesterol"] == 1, "cholesterol"] = 0
df.loc[df["cholesterol"] != 0, "cholesterol"] = 1
df["cholesterol"] = df["cholesterol"].astype("int8")

df.loc[df["gluc"] == 1, "gluc"] = 0
df.loc[df["gluc"] != 0, "gluc"] = 1
df["gluc"] = df["gluc"].astype("int8")


# print(df.info())
# print(df.head())
# print(df.describe())

# Draw Categorical Plot
def draw_cat_plot():
    plt.clf()
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    value_vars = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    df_cat = df.melt(id_vars=["cardio"], value_vars=value_vars)
    

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat["total"] = np.nan
    for variable in value_vars:
        df_cat.loc[(df_cat["cardio"] == 0) & (df_cat["variable"] == variable) & (df_cat["value"] == 0), "total"] = df_cat[(df_cat["cardio"] == 0) & (df_cat["variable"] == variable) & (df_cat["value"] == 0)]["value"].shape[0]
        df_cat.loc[(df_cat["cardio"] == 0) & (df_cat["variable"] == variable) & (df_cat["value"] == 1), "total"] = df_cat[(df_cat["cardio"] == 0) & (df_cat["variable"] == variable) & (df_cat["value"] == 1)]["value"].shape[0]
        df_cat.loc[(df_cat["cardio"] == 1) & (df_cat["variable"] == variable) & (df_cat["value"] == 0), "total"] = df_cat[(df_cat["cardio"] == 1) & (df_cat["variable"] == variable) & (df_cat["value"] == 0)]["value"].shape[0]
        df_cat.loc[(df_cat["cardio"] == 1) & (df_cat["variable"] == variable) & (df_cat["value"] == 1), "total"] = df_cat[(df_cat["cardio"] == 1) & (df_cat["variable"] == variable) & (df_cat["value"] == 1)]["value"].shape[0]

    df_cat["total"] = df_cat["total"].astype("int32")
    df_cat = df_cat.drop_duplicates()

    # print(df_cat.info())
    # print(df_cat)
    # print(df_cat.describe())
    
    

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(data=df_cat, x="variable", y="total", hue="value", col="cardio", kind="bar")


    # Get the figure for the output
    fig = g.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    plt.clf()
    
    pd.options.display.float_format = "{:,.1f}".format
    
    # Clean the data
    df_heat = df[(df["ap_lo"] <= df["ap_hi"]) & (df['height'] >= df['height'].quantile(0.025)) & (df["height"] <= df["height"].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df["weight"] <= df["weight"].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()
    # corr = round(corr, 1)
    # print(corr)
    # print(corr.info())
    
    #columns = ["id", "age", "sex", "height", "weight", "ap_hi", "ap_lo"  cholesterol  gluc  smoke  alco  active  cardio  overweight]

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool8)
    mask[np.triu_indices_from(mask)] = True


    # Set up the matplotlib figure
    ax = sns.heatmap(data=corr, mask=mask, square=True, annot=True, fmt=".1f")
    # Draw the heatmap with 'sns.heatmap()'
    fig2 = ax.get_figure()

    
    # Do not modify the next two lines
    fig2.savefig('heatmap.png')
    return fig2
