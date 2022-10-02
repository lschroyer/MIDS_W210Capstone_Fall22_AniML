from altair import Chart, X, Y, Axis, Data, DataFormat
import pandas as pd
import numpy as np
from flask import render_template, url_for, flash, redirect, request, make_response, jsonify, abort
from web import app
from web.utils import utils
import json
import altair as alt


@app.route("/")
@app.route("/allcategory")
def plot_all_category_global():
    # Loading raw data and clean it
    df = utils.load_data()
    df = utils.clean_data(df)

    
    #########################################
    # ploting - AMZN Product Data ScatterPlot
    #########################################

    brush = alt.selection_interval()

    points = alt.Chart(df).mark_circle().encode(
        x='Est_Monthly_Sales:Q',
        y='Est_Monthly_Revenue:Q',
        color=alt.condition(brush, 'Category:N', alt.value('lightgray')), 
        tooltip=['Sellers', 'LQS', 'Reviews', 'Rank', 'Fees', 'Net', 'Est_Monthly_Sales','Est_Monthly_Revenue', 'Category', 'Product_Name']
    ).properties(width=1000, height=500).add_selection(
        brush
    )

    bars = alt.Chart(df).mark_bar().encode(
        y='Category:N',
        color='Category:N',
        x='count(Category):Q'
    ).properties(width=1000, height=200).transform_filter(
        brush
    )

    plot_product_scatterchart =  points & bars
    
    plot_product_scatterchart_json = plot_product_scatterchart.to_json()
    
    
    #########################################
    # ploting - AMZN Product Data Bar Chart
    #########################################
    
    plot_product_bar = alt.Chart(df).mark_bar().encode(
    x='LQS',
    y='Net:Q',
    color= 'Category:N', 
    tooltip=['Sellers', 'LQS', 'Reviews', 'Rank', 'Fees', 'Net', 'Est_Monthly_Sales','Est_Monthly_Revenue', 'Category', 'Product_Name']
).properties(width=375, height=200)
    
    plot_product_bar_json = plot_product_bar.to_json()

    #########################################
    # ploting - AMZN Product Data Line Chart
    #########################################
    
    plot_product_line = alt.Chart(df).mark_line().encode(
    x='Rank',
    y='Reviews:Q',
    color= 'Category:N', 
    tooltip=['Sellers', 'LQS', 'Reviews', 'Rank', 'Fees', 'Net', 'Est_Monthly_Sales','Est_Monthly_Revenue', 'Category', 'Product_Name']
).properties(width=375, height=200)

    plot_product_line_json = plot_product_line.to_json()
    
    ###############################################
    # ploting - AMZN Product Data Bar Chart by Year
    ###############################################
    
    plot_product_bar_year = alt.Chart(df).mark_bar().encode(
    x='year(Date_First_Available):T',
    y='Price',
    color='Category',    
    tooltip=['year(Date_First_Available)', 'Sellers', 'LQS', 'Reviews', 'Rank', 'Fees', 'Net', 'Est_Monthly_Sales','Est_Monthly_Revenue', 'Category', 'Product_Name']
).properties(
            height=200,
            width=375,
            ).interactive()
    
    plot_product_bar_year_json = plot_product_bar_year.to_json()
    
    #########################################################
    # ploting - AMZN Product Data Bar Chart by Year/Qtr/Month
    #########################################################
    
    plot_product_bar_yearqtrmonth = alt.Chart(df).mark_bar().encode(
    x='yearquartermonth(Date_First_Available):T',
    y='Price',
    color='Category',    
    tooltip=['yearquartermonth(Date_First_Available)', 'Sellers', 'LQS', 'Reviews', 'Rank', 'Fees', 'Net', 'Est_Monthly_Sales','Est_Monthly_Revenue', 'Category', 'Product_Name']
).properties(
            height=200,
            width=375,
            ).interactive()
    
    plot_product_bar_yearqtrmonth_json = plot_product_bar_yearqtrmonth.to_json()
    
    ################################
    # finalize data send to template
    ################################
    total_category_count = "23"
    total_product_count = df.shape[0]
    average_rank = "5"
    
    
    context = {"total_category_count": total_category_count,
               "total_product_count": total_product_count, 
               "average_rank": average_rank,
               "plot_scatterchart_product": plot_product_scatterchart_json, 
               "plot_bar_product": plot_product_bar_json,
               "plot_line_product": plot_product_line_json, 
               "plot_bar_year_product": plot_product_bar_year_json,
               "plot_bar_yearqtrmonth_product": plot_product_bar_yearqtrmonth_json
               }
    
    return render_template('all_category.html', context=context )




# Ivan changed code 2-3-2021
@app.route("/category", methods=['POST'])
def plot_category():
    category_name = request.form['category_name'] + " "
    
    # Loading raw data and clean it
    df = utils.load_category_data(category_name)
    df = utils.clean_data(df)


    ################################
    # Plot per category data
    ################################

    brush = alt.selection_interval()

    category_points = alt.Chart(df).mark_circle().encode(
        x='Est_Monthly_Sales:Q',
        y='Est_Monthly_Revenue:Q',
        color=alt.condition(brush, 'Category:N', alt.value('lightgray')), 
        tooltip=['Sellers', 'LQS', 'Reviews', 'Rank', 'Fees', 'Net', 'Est_Monthly_Sales','Est_Monthly_Revenue', 'Category', 'Product_Name']
    ).properties(width=1000, height=500).add_selection(
        brush
    )

    category_bars = alt.Chart(df).mark_bar().encode(
        y='Category:N',
        color='Category:N',
        x='count(Category):Q'
    ).properties(width=1000, height=100).transform_filter(
        brush
    )

    plot_category_product_scatterchart =  category_points & category_bars
    
    plot_category_product_scatterchart_json = plot_category_product_scatterchart.to_json()

    
    ################################
    # finalize data send to template
    ################################
    total_product_count = df.shape[0]
    average_rank = df[['Rank']].mean().values.round(2)
    
    context = {"category_name": category_name, 
                "total_product_count": total_product_count,
               "average_rank": average_rank,
               'altair_category_product_plot': plot_category_product_scatterchart_json
               }
    
    return render_template('category.html', context=context)    
    