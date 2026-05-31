from django.shortcuts import render
from django.db.models import Sum, Count, F
from .models import SalesData
import json
from collections import defaultdict

def dashboard(request):
    sales = SalesData.objects.all()

    total_sales   = sum(s.sales for s in sales)
    total_profit  = sum(s.profit for s in sales)
    total_orders  = sales.values('order_id').distinct().count()
    total_qty     = sum(s.quantity for s in sales)
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0

    # Category breakdown
    cat_map = defaultdict(lambda: {'sales': 0, 'profit': 0})
    for s in sales:
        cat_map[s.category]['sales']  += s.sales
        cat_map[s.category]['profit'] += s.profit
    category_data = [{'category': k, 'sales': round(v['sales'], 2), 'profit': round(v['profit'], 2)}
                     for k, v in cat_map.items()]

    # Sub-category breakdown
    sub_map = defaultdict(lambda: {'sales': 0, 'profit': 0})
    for s in sales:
        sub_map[s.sub_category]['sales']  += s.sales
        sub_map[s.sub_category]['profit'] += s.profit
    sub_data = [{'sub_category': k, 'sales': round(v['sales'], 2), 'profit': round(v['profit'], 2)}
                for k, v in sub_map.items()]
    sub_data.sort(key=lambda x: x['profit'], reverse=True)

    # Region breakdown
    region_map = defaultdict(lambda: {'sales': 0, 'profit': 0})
    for s in sales:
        region_map[s.region]['sales']  += s.sales
        region_map[s.region]['profit'] += s.profit
    region_data = [{'region': k, 'sales': round(v['sales'], 2), 'profit': round(v['profit'], 2)}
                   for k, v in region_map.items()]
    region_data.sort(key=lambda x: x['sales'], reverse=True)

    # Segment breakdown
    seg_map = defaultdict(lambda: {'sales': 0, 'profit': 0})
    for s in sales:
        seg_map[s.segment]['sales']  += s.sales
        seg_map[s.segment]['profit'] += s.profit
    segment_data = [{'segment': k, 'sales': round(v['sales'], 2), 'profit': round(v['profit'], 2)}
                    for k, v in seg_map.items()]

    # Monthly trend
    monthly_map = defaultdict(lambda: {'sales': 0, 'profit': 0})
    for s in sales:
        key = s.order_date.strftime('%Y-%m')
        monthly_map[key]['sales']  += s.sales
        monthly_map[key]['profit'] += s.profit
    monthly_data = [{'month': k, 'sales': round(v['sales'], 2), 'profit': round(v['profit'], 2)}
                    for k, v in sorted(monthly_map.items())]

    # Ship mode
    ship_map = defaultdict(int)
    for s in sales:
        ship_map[s.ship_mode] += 1
    ship_data = [{'mode': k, 'count': v} for k, v in ship_map.items()]

    context = {
        'total_sales':   round(total_sales, 2),
        'total_profit':  round(total_profit, 2),
        'total_orders':  total_orders,
        'total_qty':     total_qty,
        'profit_margin': round(profit_margin, 1),
        'category_data': json.dumps(category_data),
        'sub_data':      json.dumps(sub_data),
        'region_data':   json.dumps(region_data),
        'segment_data':  json.dumps(segment_data),
        'monthly_data':  json.dumps(monthly_data),
        'ship_data':     json.dumps(ship_data),
    }
    return render(request, 'dashboard.html', context)
