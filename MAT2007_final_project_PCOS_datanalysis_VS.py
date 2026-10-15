
# MAT2007_20262027_Final_project
#i6390492, Veerle Senkowski

#import all necessary packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import openpyxl

    #for mac you can use the command 'pip install matplotlib numpy pandas seaborn scipy openpyxl' to install all the necessary packages in the terminal 
    #i personally used pip3, but pip should work as well 

# ___________________________________________________________
#load data from excel file

excel_path = 'Table-S1.xlsx' #please make sure the excel file is in the same directory as this script 
    #alternatively, you can provide the full path to the excel file 
df_control = pd.read_excel(excel_path, sheet_name='CON')
df_pcos = pd.read_excel(excel_path, sheet_name='PCOS')
    #this laods the data is into two separate pandas dataframes, one for the control group and one for the PCOS group

df_control['Group'] = 'Control' 
df_pcos['Group'] = 'PCOS'
    #these lines add a new column to each dataframe to specify the group name

df_control.columns = df_control.columns.str.strip()
df_pcos.columns = df_pcos.columns.str.strip()
    #strip() removes any leading or trailing whitespace from the column names

df_all = pd.concat([df_control, df_pcos], ignore_index=True)
    #this combines the two dataframes into a single dataframe
df_all.rename(columns={'Serum testosterone (ng/ml)': 'Testosterone'}, inplace=True)
    #renames the column 'Serum testosterone (ng/ml)' to 'Testosterone' for easier access, less bulky column name

# ___________________________________________________________
#extract arrays

control_test = (df_all[df_all['Group'] == 'Control']['Testosterone'].dropna().values)
pcos_test = df_all[df_all['Group'] == 'PCOS']['Testosterone'].dropna().values
    #dropna() removes any missing values (NaN) from the data define in [testoterone], essentially looks at the defines column 
    #.values returns the values of the series as a numpy array, a more efficient data structure for numerical operation

# ___________________________________________________________
#statistical analysis

t_stat, p_val = stats.ttest_ind(pcos_test, control_test, equal_var=False)
    #statistical Analysis (Welch's t-test for independent samples)
    #stats.ttest_ind() performs a two-sample t-test for the means of two independent samples 
        #a t-test is used to determine if there is a significant difference between the means of two groups by measuring the difference between the means relative to the variability of the samples
    #equal_var=False specifies that the two samples have unequal variances --> a welchs t-test
# ________________
# Sample statistics from raw data
n_control, n_pcos = len(control_test), len(pcos_test)
    #len() returns the number of elements in an array, this is the sample size n
mean_control, mean_pcos = np.mean(control_test), np.mean(pcos_test)
    #np.mean() returns the arithmetic mean of the array, this is the sample mean (in this case the groups is the same as the chosen sample)
sd_control, sd_pcos = np.std(control_test, ddof=1), np.std(pcos_test, ddof=1)
    #np.std() returns the standard deviation of the array, how far the datapoints typically lie from the mean
    #ddof=1 is used to calculate the sample standard deviation
se_control, se_pcos = sd_control / np.sqrt(n_control), sd_pcos / np.sqrt(n_pcos)
    #the standard error (SE) is calculated by dividing the standard deviation by the square root of the sample size
    #gives an estimate of how much the sample mean is expected to vary from the true population mean
    #np.sqrt() returns the square root of the array, 
# ________________
raw_mean_diff = mean_pcos - mean_control
    #calculates the difference between the two sample means 
se_diff = np.sqrt((sd_pcos**2 / n_pcos) + (sd_control**2 / n_control))
    #se_diff is the standard error of the difference between the two means, calculated using the formula for the standard error of the difference between two independent samples
# ________________
# Welch-Satterthwaite degrees of freedom & 95% Confidence Intervals
df_welch = ((sd_pcos**2 / n_pcos + sd_control**2 / n_control)**2) / (((sd_pcos**2 / n_pcos)**2 / (n_pcos - 1)) + ((sd_control**2 / n_control)**2 / (n_control - 1)))
    #welch-satterthwaite equation is used to calculate the degrees of freedom for the Welch's t-test, which accounts for unequal variances and sample sizes between the two groups
# ________________
t_crit_con = stats.t.ppf(0.975, df=n_control - 1)
t_crit_pcos = stats.t.ppf(0.975, df=n_pcos - 1)
t_crit_diff = stats.t.ppf(0.975, df=df_welch)
    #the critical t-value is calculated using the percent point function (ppf) of the t-distribution, gives the value of t for a given cumulative probability 
# ________________
ci_control = (mean_control - t_crit_con * se_control, mean_control + t_crit_con * se_control,)
ci_pcos = (mean_pcos - t_crit_pcos * se_pcos, mean_pcos + t_crit_pcos * se_pcos,)
ci_diff = (raw_mean_diff - t_crit_diff * se_diff,raw_mean_diff + t_crit_diff * se_diff,)
    #the confidence intervals are calculated by taking the sample mean +/- ( product of the critical t-value x the standard error)
    #which gives the range of values within which we can be 95% confident that the true population mean lies
# ___________________________________________________________

# printing the results from the previous code 
print("\nWelch's Two-Sample t-Test Results")
print(f't-statistic: {t_stat:.4f}') # :.x gives the number of decimal places to round to
print(f'p-value:     {p_val:.6f}\n')
# ________________
print('Raw Data Summary')
print(f'Mean of Control Group   : {mean_control:.4f} ng/ml')
print(f'Standard Deviation (SD) : {sd_control:.4f} ng/ml')
print(f'Standard Error (SE)     : {se_control:.4f} ng/ml')
print(f'95% CI of Mean          : {ci_control[0]:.4f} ng/ml,  {ci_control[1]:.4f} ng/ml \n')
    #0 gives the lower bound of the confidence interval, 1 gives the upper bound of the confidence interval
# ________________
print(f'Mean of PCOS Group      : {mean_pcos:.4f} ng/ml')
print(f'Standard Deviation (SD) : {sd_pcos:.4f} ng/ml')
print(f'Standard Error (SE)     : {se_pcos:.4f} ng/ml')
print(f'95% CI of Mean          : {ci_pcos[0]:.4f} ng/ml,  {ci_pcos[1]:.4f} ng/ml\n')
# ________________
print(f'Difference in Means   : {raw_mean_diff:.4f} ng/ml')
print(f'Difference SE         : {se_diff:.4f} ng/ml')
print(f'Difference 95% CI     : {ci_diff[0]:.4f} ng/ml,  {ci_diff[1]:.4f} ng/ml\n')
# ___________________________________________________________
sns.set_theme(style='whitegrid') 
    #whitegrid is a clean and simple style with a white background and gridlines, which is suitable for scientific plots
plt.rcParams['font.size'] = 11

# ___________________________________________________________
#figure 1: group comparison bar plot with raw data dual error bars
def show_figure_1():
  fig1, ax1 = plt.subplots(figsize=(7, 5))

  sns.barplot(x='Group', y='Testosterone', hue='Group', data=df_all, ax=ax1, alpha=0.4, palette=['#17C0EB', '#D81B60'], errorbar=None,)
    #plots the bar plot for each group, showing the mean of the data, alpha=0.4 makes the bars semi-transparent, palette specifies the colors for each group, errorbar=None disables the default error bars
  sns.stripplot( x='Group', y='Testosterone', data=df_all, ax=ax1, color='black', alpha=0.6, jitter=0.2, size=5,)
    #overlays the individual data points on top of the bar plot, jitter=0.2 adds random noise to the x-coordinates of the data points to prevent overlap, size=5 specifies the size of the data points

  groups = ['Control', 'PCOS'] #tells the code which groups to use for the error bars 
  x_coords = [0, 1] #this is the x-coordinates for the error bars, which correspond to the positions of the bars in the bar plot

  for i, group in enumerate(groups):
    vals = df_all[df_all['Group'] == group]['Testosterone'].dropna() #define the values for each group, dropna() removes any missing values from the data define in [testoterone]
    mean = np.mean(vals)        #takes the mean of the values for each group, np.mean() returns the arithmetic mean of the array
    sd = np.std(vals, ddof=1)   #takes the standard deviation of the values for each group, np.std() returns the standard deviation of the array, ddof=1 is used to calculate the sample standard deviation
    se = sd / np.sqrt(len(vals))    #calculates the standard error of the mean for each group (SD / √n), where SD is the standard deviation and n is the sample size

    ax1.errorbar( x=x_coords[i], y=mean, yerr=sd, fmt='none',ecolor='black',elinewidth=1.2, capsize=8, label='±1 SD (Patient Spread)' if i == 0 else '',)
        #plots the error bars for the standard deviation (SD) of the data, which represents the spread of the data points around the mean
    ax1.errorbar( x=x_coords[i], y=mean, yerr=se, fmt='none', ecolor='black', elinewidth=3.5, capsize=0, label='±1 SE (Mean Precision)' if i == 0 else '',)
        #plots the error bars for the standard error (SE) of the mean, which represents the precision of the mean estimate
  
  ax1.set_title(f'Group Comparison (t = {t_stat:.2f}, p = {p_val:.4f})', fontweight='bold') #sets the title of the plot
  ax1.set_ylabel('Serum Testosterone (ng/ml)')  #sets the y-axis label of the plot
  ax1.set_xlabel('Group')                       #shows the x-axis label of the plot
  ax1.legend(loc='upper left')                  #sets the legend of the plot to the upper left corner

  plt.show()     #this shows the plot in a new window, if you would like to save the plot as a PNG file, you can uncomment the following two lines of code and comment out the plt.show() line above
  #plt.tight_layout()                            #sets the layout of the plot to be tight, subplots will be adjusted to fit within the figure area
  #plt.savefig('Group Comparison.png', dpi=300)  #saves the plot as a PNG file with a resolution of 300 dpi

# ___________________________________________________________
# figure 2: kernel density distributions of raw measurements
def show_figure_2(): 
  fig2, ax2 = plt.subplots(figsize=(7, 5))

  sns.kdeplot( control_test,fill=True, color='#17C0EB', label='Control Data',ax=ax2, alpha=0.4,)
    #plots the kernel density estimate of the control group data, that estimates the probability density 
  sns.kdeplot(pcos_test, fill=True, color='#D81B60', label='PCOS Data', ax=ax2, alpha=0.4) 
    #overlays the two density distributions on the same plot

  ax2.set_title('Raw Data Kernel Density Distribution', fontweight='bold') #sets the title of the plot
  ax2.set_xlabel('Serum Testosterone (ng/ml)')                   #sets the x-axis label of the plot
  ax2.set_ylabel('Density')                                      #sets the y-axis label of the plot
  ax2.legend(loc='upper right')                                  #sets the legend of the plot to the upper right corner

  plt.show()     #this shows the plot in a new window, if you would like to save the plot as a PNG file, you can uncomment the following two lines of code and comment out the plt.show() line above
  #plt.tight_layout()                                                 #sets the layout of the plot to be tight, subplots will be adjusted to fit within the figure area
  #plt.savefig('Raw Data Kernel Density Distribution.png', dpi=300)   #saves the plot as a PNG file with a resolution of 300 dpi
# ___________________________________________________________
#figure 3: violin plot  
def show_figure_3():
  fig3, ax3 = plt.subplots(figsize=(7, 5))

  sns.violinplot(x='Group', y='Testosterone',hue='Group', data=df_all, ax=ax3, palette=['#17C0EB', '#D81B60'], inner=None, alpha=0.4,)
    #plots the violin plot for each group, showing the distribution of the data, the width of the violin represents the density of the data at different values
  sns.stripplot( x='Group', y='Testosterone', data=df_all, ax=ax3, color='black', alpha=0.6, jitter=0.15, size=5,)
    #overlays the individual data points on top of the violin plot

  ax3.set_title('Violin Plot', fontsize=12, fontweight='bold')
  ax3.set_ylabel('Serum Testosterone (ng/ml)')
  ax3.set_xlabel('Group')

  plt.show()    #this shows the plot in a new window, if you would like to save the plot as a PNG file, you can uncomment the following two lines of code and comment out the plt.show() line above
  #plt.tight_layout()                            #sets the layout of the plot to be tight, subplots will be adjusted to fit within the figure area
  #plt.savefig('Violin Plot.png', dpi=300)

#this calls the functions to show the plots, you can comment out any of these lines if you do not want to see a specific plot
show_figure_1()
show_figure_2()
show_figure_3()

