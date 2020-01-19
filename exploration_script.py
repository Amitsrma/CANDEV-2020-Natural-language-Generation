import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

def main():
    sales_data = pd.read_csv("https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadDbLoadingData-nonTraduit.action?pid=1610001101&latestN=5&startDate=&endDate=&csvLocale=en&selectedMembers=%5B%5B4%2C2%2C10%2C6%2C12%2C1%2C3%2C9%2C7%2C5%2C8%2C11%5D%2C%5B1%5D%2C%5B2%2C1%5D%2C%5B1%5D%5D")
    sales_date = sales_data.groupby("REF_DATE").sum()

    sales_date = sales_date.drop(sales_date.columns.difference(['VALUE']),1)

    sales_data_cleaned = sales_data.drop(sales_data.columns.difference(['REF_DATE','GEO','VALUE']),1)
    sales_address = [i.split(', ') for i in sales_data_cleaned.GEO]

    sales_data_cleaned['CITY'] = [i[0] for i in sales_address]
    sales_data_cleaned['PROVINCE'] = [i[1] for i in sales_address]

    sales_data_cleaned['PERCENTAGE_CONTRIB'] = [sales_data_cleaned.VALUE[index]/sales_date.loc[date,'VALUE'] for index, date in enumerate(sales_data_cleaned.REF_DATE)]

    # change% keeps track of the % change in the sales of most recent sales with respect to sales of immediate past
    sales_date['change%'] = np.nan
    # Trend keeps track if there has been observed a trend until the specific point in time.
    # a row will have 1 if the trend has been observed until that point. For example if there is continuous increment of
    # sales for 5 months, it will be 0 until fourth month and will be 1 at fifth month so it is easier to extract the
    # number of month trend was observed for
    sales_date['Trend'] = np.nan

    sales_date['num_months'] = np.nan

    count = 0
    for i in range(1,len(sales_date)):
        sales_date['change%'][i] = (sales_date.VALUE[i]-sales_date.VALUE[i-1])/sales_date.VALUE[i-1]
        # check if the percentage change followed the trend or deviated .i.e.
        # if it was decreasing (negative), it remained decreasing and if it was increasing
        # it kept increasing
        # if previous % change and current % change were decreasing, or increasing, the product of % change will be +ve
        # so if product is greater than 0, trend is followed
        if sales_date['change%'][i]*sales_date['change%'][i-1] > 0:
            count += 1
            if count >=2:
                sales_date['num_months'][i] = count
                sales_date.Trend[i-1] = 0
                sales_date.Trend[i] = 1
        else:
            count = 0

    sales_date.num_months = sales_date.num_months.fillna(0)

#    for i in range(1,len(sales_date)):
    size = len(sales_date)
    perc_change = sales_date.iloc[size-1,1]
    if perc_change>0:
        inc_dec = 'increased'
    else:
        inc_dec = 'decreased'
    get_text(perc_change,inc_dec,num_months=sales_date.iloc[size-1,3], trend=True)
    print(sales_date.iloc[size-1,:])
    sales_date.to_csv("sales_aggregated.csv")

def get_text(percent_change,inc_dec,num_months=None,trend=False):
    if trend:
        if isinstance(num_months, (int,float)):
            if num_months > 0.0:
                print("There was "+str(round(percent_change*100,3))+"% "+inc_dec[:-4]+"ment of sales. Continuous "+inc_dec[:-4]+"ment was observed for last "+str(int(num_months))+" months.")
            else:
                print("There was "+str(round(percent_change*100,3))+"% "+inc_dec[:-4]+"ment of sales.")
        else:
            raise ValueError("num_months must be int")
    else:
        print("There was "+str(round(percent_change*100,3))+"% "+inc_dec[:-4]+"ment of sales.")

if __name__ == "__main__":
	main()
