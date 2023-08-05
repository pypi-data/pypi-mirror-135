import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
import os 
import wget

def main():
    #データを読み込み
    if os.path.exists('covid-vaccination-vs-death_ratio.csv') is False:
        output_dir = './'
        output_file = 'covid-vaccination-vs-death_ratio.csv'
        assert os.path.exists(output_dir)
        url = "https://raw.githubusercontent.com/G-Y3/covid-19-vaccination-vs.-mortality/main/src/covid-vaccination-vs-death_ratio.csv"#

        wget.download(url, out = os.path.join(output_dir,output_file))
    df = pd.read_csv("covid-vaccination-vs-death_ratio.csv")
    print('iso code samples:')
    print('Japan: JPN')
    print('Italy: ITA')
    print('France: FRA')
    print('America: USA')
    print('The United Kingdom: GBR')
    print('Please enter iso code:')
    
    #iso code を取得
    iso_code = input()

    #iso codeが対応する国のデータを取得
    df_target = df[(df["iso_code"] == iso_code)]
    df_target = df_target[['date','ratio', 'New_deaths']]

    #ワクチンの接種率と新規死亡者数の可視化
    tick_spacing = df_target.index.size/5
    x_lambda = df_target.date
    y1 = df_target.ratio
    y2 = df_target.New_deaths

    fig, ax1 = plt.subplots()
    fig.set_size_inches(12,6)
    ax1.plot(x_lambda, y1, c='orangered', label='ratio', linewidth = 1) 
    plt.legend(loc=2)
    ax2 = ax1.twinx() 
    ax2.plot(x_lambda, y2, c='blue', label='New_deaths', linewidth = 1) 
    plt.legend(loc=4)
    plt.grid(True)
    ax1.xaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))
    ax1.set_title("vaccination vs. mortality",size=22)  
    ax1.set_xlabel('date',size=18)  
    ax1.set_ylabel('vaccination ratio(%)',size=18)
    ax2.set_ylabel('new deaths',size=18)
    plt.show()

    #ワクチンの接種率と新規死亡者数の相関係数を表示
    print('Correlation coefficient:')
    print(df_target.corr())
    
if __name__ == "__main__":
    main()