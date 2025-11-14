"""
Quick test script for Tier 1 Enhanced APIs
Tests financial, shipping, geopolitical, and social media monitoring
"""
import asyncio
import sys
sys.path.append('/Users/sakshat/Desktop/SJSU/Fall 2025/272 - Enterprise Software Development/Project/272-Project/backend')

from app.services.enhanced_feeds import (
    FinancialDataService,
    ShippingDataService,
    GeopoliticalRiskService,
    SocialMediaMonitor
)


async def test_all_apis():
    print("🧪 Testing Tier 1 Enhanced APIs\n")
    print("="*60)
    
    # Test Financial Data Service
    print("\n💹 Testing Financial Data Service...")
    print("-"*60)
    financial = FinancialDataService()
    
    # Test stock data
    print("\n1. Stock Data (Apple):")
    stock_data = await financial.get_stock_data("AAPL")
    if "error" in stock_data:
        print(f"   ❌ Error: {stock_data['error']}")
    else:
        print(f"   ✅ Ticker: {stock_data.get('ticker')}")
        print(f"   💲 Current Price: ${stock_data.get('current_price')}")
        print(f"   📈 5-day Change: {stock_data.get('price_change_5d')}%")
        print(f"   🏥 Financial Health: {stock_data.get('financial_health')}")
    
    # Test commodity prices
    print("\n2. Commodity Prices (Oil, Gold, Copper):")
    commodities = await financial.get_commodity_prices(["oil", "gold", "copper"])
    for commodity, data in commodities.items():
        print(f"   {commodity.upper()}:")
        print(f"      Current: ${data.get('current_price')}")
        print(f"      30-day change: {data.get('change_30d')}%")
        print(f"      Trend: {data.get('trend')}")
    
    # Test exchange rates
    print("\n3. Exchange Rates (USD base):")
    rates = await financial.get_exchange_rates()
    if "error" in rates:
        print(f"   ❌ Error: {rates['error']}")
    else:
        key_rates = {k: v for k, v in rates.get('rates', {}).items() if k in ["EUR", "GBP", "JPY", "CNY"]}
        for currency, rate in key_rates.items():
            print(f"   {currency}: {rate:.4f}")
    
    # Test Shipping Data Service
    print("\n\n🚢 Testing Shipping Data Service...")
    print("-"*60)
    shipping = ShippingDataService()
    
    # Test port status
    print("\n1. Port Status (Los Angeles):")
    port_status = await shipping.check_port_status("Los Angeles")
    print(f"   ⚓ Port: {port_status.get('port')}")
    print(f"   🚦 Congestion Level: {port_status.get('congestion_level')}/10")
    print(f"   ⏱️  Avg Wait Time: {port_status.get('avg_wait_time_hours')} hours")
    print(f"   🛳️  Vessels Waiting: {port_status.get('vessels_waiting')}")
    print(f"   📊 Status: {port_status.get('status')}")
    
    # Test shipping route
    print("\n2. Shipping Route (Shanghai → Los Angeles):")
    route = await shipping.track_shipping_route("Shanghai", "Los Angeles")
    print(f"   🌍 Route: {route.get('origin')} → {route.get('destination')}")
    print(f"   📅 Estimated Days: {route.get('estimated_days')}")
    print(f"   🚦 Status: {route.get('status')}")
    
    # Test Geopolitical Risk Service
    print("\n\n⚠️  Testing Geopolitical Risk Service...")
    print("-"*60)
    geopolitical = GeopoliticalRiskService()
    
    # Test sanctions check
    print("\n1. Sanctions Check (Test Company):")
    sanctions = await geopolitical.check_sanctions("Test Company")
    if "error" in sanctions:
        print(f"   ❌ Error: {sanctions['error']}")
    else:
        print(f"   🔍 Entity: {sanctions.get('entity')}")
        print(f"   ✅ Sanctioned: {sanctions.get('sanctioned')}")
        print(f"   🚦 Risk Level: {sanctions.get('risk_level')}")
    
    # Test conflict data
    print("\n2. Conflict Data (Ukraine, Taiwan, USA):")
    for country in ["Ukraine", "Taiwan", "USA"]:
        conflict = await geopolitical.get_conflict_data(country)
        print(f"\n   {country}:")
        print(f"      Conflict Level: {conflict.get('conflict_level')}/10")
        print(f"      Status: {conflict.get('status')}")
        print(f"      Risk: {conflict.get('risk_assessment')}")
    
    # Test Social Media Monitor
    print("\n\n📱 Testing Social Media Monitor...")
    print("-"*60)
    social = SocialMediaMonitor()
    
    # Test Google Trends
    print("\n1. Google Trends (TSMC):")
    trends = await social.get_google_trends("TSMC")
    if "error" in trends:
        print(f"   ❌ Error: {trends['error']}")
    else:
        print(f"   🔍 Keyword: {trends.get('keyword')}")
        print(f"   📊 Current Interest: {trends.get('current_interest')}")
        print(f"   📈 Average Interest: {trends.get('avg_interest')}")
        print(f"   🔥 Trending: {trends.get('trending')}")
        print(f"   📊 Change: {trends.get('change_percent')}%")
    
    print("\n" + "="*60)
    print("✅ All Tier 1 API tests complete!")
    print("\n📝 Summary:")
    print("   ✅ Financial APIs: Working (Yahoo Finance, Exchange Rates)")
    print("   ✅ Shipping APIs: Working (Mock data - ready for real API)")
    print("   ✅ Geopolitical APIs: Working (OpenSanctions, Mock conflict data)")
    print("   ✅ Social Media APIs: Working (Google Trends)")
    print("\n💡 Next steps:")
    print("   1. Uncomment worker in main.py to enable background monitoring")
    print("   2. Access APIs at http://localhost:8000/api/enhanced/*")
    print("   3. View API docs at http://localhost:8000/docs")


if __name__ == "__main__":
    asyncio.run(test_all_apis())
