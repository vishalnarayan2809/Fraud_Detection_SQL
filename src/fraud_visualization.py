"""
Fraud Detection Visualization Module
This script creates visualizations for fraud detection analysis
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import numpy as np
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FraudVisualizer:
    def __init__(self):
        """Initialize the fraud visualizer"""
        self.color_palette = px.colors.qualitative.Set3
        
    def plot_transaction_amount_distribution(self, transactions_df):
        """
        Create a histogram of transaction amounts
        
        Args:
            transactions_df (pandas.DataFrame): Transaction data
            
        Returns:
            plotly.graph_objects.Figure: Distribution plot
        """
        fig = px.histogram(
            transactions_df, 
            x='amount', 
            nbins=50,
            title='Distribution of Transaction Amounts',
            labels={'amount': 'Transaction Amount ($)', 'count': 'Frequency'},
            color_discrete_sequence=[self.color_palette[0]]
        )
        
        fig.update_layout(
            xaxis_title="Transaction Amount ($)",
            yaxis_title="Frequency",
            showlegend=False
        )
        
        return fig
    
    def plot_hourly_transaction_patterns(self, hourly_data):
        """
        Create visualization of transaction patterns by hour
        
        Args:
            hourly_data (pandas.DataFrame): Hourly transaction data
            
        Returns:
            plotly.graph_objects.Figure: Hourly patterns plot
        """
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Transaction Count by Hour', 'Average Amount by Hour'),
            vertical_spacing=0.1
        )
        
        # Transaction count
        fig.add_trace(
            go.Scatter(
                x=hourly_data['hour_of_day'],
                y=hourly_data['transaction_count'],
                mode='lines+markers',
                name='Transaction Count',
                line=dict(color=self.color_palette[1], width=3),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # Average amount
        fig.add_trace(
            go.Scatter(
                x=hourly_data['hour_of_day'],
                y=hourly_data['avg_amount'],
                mode='lines+markers',
                name='Average Amount',
                line=dict(color=self.color_palette[2], width=3),
                marker=dict(size=8)
            ),
            row=2, col=1
        )
        
        # Highlight suspicious hours (7-9 AM)
        fig.add_vrect(
            x0=7, x1=9,
            fillcolor="red", opacity=0.2,
            layer="below", line_width=0,
            row=1, col=1
        )
        
        fig.add_vrect(
            x0=7, x1=9,
            fillcolor="red", opacity=0.2,
            layer="below", line_width=0,
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Hour of Day", row=1, col=1)
        fig.update_xaxes(title_text="Hour of Day", row=2, col=1)
        fig.update_yaxes(title_text="Transaction Count", row=1, col=1)
        fig.update_yaxes(title_text="Average Amount ($)", row=2, col=1)
        
        fig.update_layout(
            title="Transaction Patterns by Hour of Day",
            height=600,
            showlegend=False
        )
        
        return fig
    
    def plot_merchant_vulnerability_analysis(self, vulnerable_merchants):
        """
        Create visualization of merchant vulnerability to small transactions
        
        Args:
            vulnerable_merchants (pandas.DataFrame): Vulnerable merchants data
            
        Returns:
            plotly.graph_objects.Figure: Merchant vulnerability plot
        """
        fig = px.bar(
            vulnerable_merchants.head(10),
            x='merchant_name',
            y='small_transaction_count',
            color='merchant_category',
            title='Top 10 Merchants Most Vulnerable to Small Transaction Fraud',
            labels={
                'small_transaction_count': 'Number of Small Transactions (<$2)',
                'merchant_name': 'Merchant Name'
            }
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        
        return fig
    
    def plot_cardholder_risk_analysis(self, small_transactions_df):
        """
        Create visualization of cardholder risk based on small transactions
        
        Args:
            small_transactions_df (pandas.DataFrame): Small transactions by cardholder
            
        Returns:
            plotly.graph_objects.Figure: Risk analysis plot
        """
        # Create risk categories
        small_transactions_df['risk_level'] = pd.cut(
            small_transactions_df['small_transaction_count'],
            bins=[0, 2, 5, 10, float('inf')],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
        
        fig = px.scatter(
            small_transactions_df,
            x='small_transaction_count',
            y='avg_small_amount',
            color='risk_level',
            size='max_amount',
            hover_data=['cardholder_name'],
            title='Cardholder Risk Analysis Based on Small Transaction Patterns',
            labels={
                'small_transaction_count': 'Number of Small Transactions',
                'avg_small_amount': 'Average Small Transaction Amount ($)',
                'risk_level': 'Risk Level'
            },
            color_discrete_map={
                'Low': 'green',
                'Medium': 'yellow',
                'High': 'orange',
                'Critical': 'red'
            }
        )
        
        fig.update_layout(height=500)
        
        return fig
    
    def plot_outlier_analysis(self, outliers_df):
        """
        Create visualization of outlier transactions
        
        Args:
            outliers_df (pandas.DataFrame): Outlier transactions data
            
        Returns:
            plotly.graph_objects.Figure: Outlier analysis plot
        """
        fig = px.scatter(
            outliers_df,
            x='date',
            y='amount',
            color='outlier_type',
            size='z_score',
            hover_data=['cardholder_name', 'merchant_name', 'merchant_category'],
            title='Outlier Transaction Analysis',
            labels={
                'amount': 'Transaction Amount ($)',
                'date': 'Transaction Date',
                'outlier_type': 'Outlier Detection Method'
            }
        )
        
        fig.update_layout(height=500)
        
        return fig
    
    def plot_transaction_timeline(self, transactions_df, card_number=None):
        """
        Create timeline visualization of transactions for a specific card or all cards
        
        Args:
            transactions_df (pandas.DataFrame): Transaction data
            card_number (str, optional): Specific card to analyze
            
        Returns:
            plotly.graph_objects.Figure: Timeline plot
        """
        if card_number:
            df = transactions_df[transactions_df['card'] == card_number].copy()
            title = f'Transaction Timeline for Card {card_number}'
        else:
            # Sample data for visualization if too many transactions
            if len(transactions_df) > 1000:
                df = transactions_df.sample(n=1000).copy()
                title = 'Transaction Timeline (Sample of 1000 transactions)'
            else:
                df = transactions_df.copy()
                title = 'Transaction Timeline (All transactions)'
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        fig = px.scatter(
            df,
            x='date',
            y='amount',
            color='merchant_category' if 'merchant_category' in df.columns else None,
            hover_data=['cardholder_name', 'merchant_name'] if 'cardholder_name' in df.columns else None,
            title=title,
            labels={
                'amount': 'Transaction Amount ($)',
                'date': 'Transaction Date'
            }
        )
        
        fig.update_layout(height=500)
        
        return fig
    
    def create_fraud_summary_dashboard(self, summary_data, transactions_df, hourly_data, 
                                     vulnerable_merchants, small_transactions, outliers):
        """
        Create a comprehensive fraud detection dashboard
        
        Args:
            summary_data (dict): Summary statistics
            transactions_df (pandas.DataFrame): All transaction data
            hourly_data (pandas.DataFrame): Hourly transaction patterns
            vulnerable_merchants (pandas.DataFrame): Vulnerable merchants data
            small_transactions (pandas.DataFrame): Small transactions data
            outliers (pandas.DataFrame): Outlier transactions data
            
        Returns:
            dict: Dictionary of plotly figures
        """
        dashboard_plots = {}
        
        try:
            # 1. Transaction amount distribution
            dashboard_plots['amount_distribution'] = self.plot_transaction_amount_distribution(transactions_df)
            
            # 2. Hourly patterns
            dashboard_plots['hourly_patterns'] = self.plot_hourly_transaction_patterns(hourly_data)
            
            # 3. Merchant vulnerability
            dashboard_plots['merchant_vulnerability'] = self.plot_merchant_vulnerability_analysis(vulnerable_merchants)
            
            # 4. Cardholder risk analysis
            if len(small_transactions) > 0:
                dashboard_plots['cardholder_risk'] = self.plot_cardholder_risk_analysis(small_transactions)
            
            # 5. Outlier analysis
            if len(outliers) > 0:
                dashboard_plots['outlier_analysis'] = self.plot_outlier_analysis(outliers)
            
            # 6. Summary metrics visualization
            dashboard_plots['summary_metrics'] = self.create_summary_metrics_plot(summary_data)
            
            logger.info("Created comprehensive fraud detection dashboard")
            return dashboard_plots
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {e}")
            return {}
    
    def create_summary_metrics_plot(self, summary_data):
        """
        Create a summary metrics visualization
        
        Args:
            summary_data (dict): Summary statistics
            
        Returns:
            plotly.graph_objects.Figure: Summary metrics plot
        """
        try:
            # Extract key metrics
            basic_stats = summary_data.get('basic_statistics', {})
            fraud_indicators = summary_data.get('fraud_indicators', {})
            risk_assessment = summary_data.get('risk_assessment', {})
            
            # Create subplots for different metric categories
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Transaction Overview', 'Fraud Indicators', 
                              'Risk Assessment', 'Financial Summary'),
                specs=[[{"type": "indicator"}, {"type": "indicator"}],
                       [{"type": "indicator"}, {"type": "indicator"}]]
            )
            
            # Transaction Overview
            fig.add_trace(
                go.Indicator(
                    mode="number",
                    value=basic_stats.get('total_transactions', 0),
                    title={"text": "Total Transactions"},
                    number={'font': {'size': 40}}
                ),
                row=1, col=1
            )
            
            # Fraud Indicators
            fig.add_trace(
                go.Indicator(
                    mode="number",
                    value=fraud_indicators.get('cards_with_small_transactions', 0),
                    title={"text": "Cards with Small Transactions"},
                    number={'font': {'size': 40, 'color': 'red'}}
                ),
                row=1, col=2
            )
            
            # Risk Assessment
            fig.add_trace(
                go.Indicator(
                    mode="number",
                    value=risk_assessment.get('high_risk_cards', 0),
                    title={"text": "High Risk Cards"},
                    number={'font': {'size': 40, 'color': 'orange'}}
                ),
                row=2, col=1
            )
            
            # Financial Summary
            fig.add_trace(
                go.Indicator(
                    mode="number",
                    value=basic_stats.get('total_volume', 0),
                    title={"text": "Total Transaction Volume ($)"},
                    number={'font': {'size': 30}, 'prefix': '$'}
                ),
                row=2, col=2
            )
            
            fig.update_layout(
                title="Fraud Detection Summary Metrics",
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating summary metrics plot: {e}")
            return go.Figure()
    
    def save_plots_to_html(self, plots_dict, output_dir="c:\\Users\\guruk\\Fraud Detection\\reports"):
        """
        Save all plots to HTML files
        
        Args:
            plots_dict (dict): Dictionary of plotly figures
            output_dir (str): Output directory for HTML files
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        for plot_name, fig in plots_dict.items():
            try:
                filename = os.path.join(output_dir, f"{plot_name}.html")
                fig.write_html(filename)
                logger.info(f"Saved plot '{plot_name}' to {filename}")
            except Exception as e:
                logger.error(f"Error saving plot '{plot_name}': {e}")
