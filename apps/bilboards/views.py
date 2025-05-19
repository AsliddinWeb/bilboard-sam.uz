from django.shortcuts import render
from django.db.models import Q

# Folium
import folium
from folium import Map, Marker, Popup
from folium.features import CustomIcon

from .models import Billboard

def home_page(request):
    # Get filter parameters from request
    location_filter = request.GET.get('location', '')
    region_filter = request.GET.get('region', '')
    district_filter = request.GET.get('district', '')
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    # Start with all billboards
    billboards = Billboard.objects.select_related('location', 'region', 'district').all()
    
    # Apply filters if they exist
    if location_filter and location_filter != 'Локация':
        billboards = billboards.filter(location__name=location_filter)
    
    if region_filter and region_filter != 'Область':
        billboards = billboards.filter(region__name=region_filter)
        
    if district_filter and district_filter != 'Район':
        billboards = billboards.filter(district__name=district_filter)
        
    if status_filter and status_filter != 'Статус':
        billboards = billboards.filter(status=status_filter)
    
    # Search by billboard number
    if search_query:
        billboards = billboards.filter(billboard_number__icontains=search_query)

    # Create Folium Map
    m = Map(location=[39.6542, 66.9750], zoom_start=15, height='500px', 
            tiles='CartoDB positron', control_scale=True)

    # Add custom markers with popup info
    for billboard in billboards:
        # Define marker color based on status
        if hasattr(billboard, 'status') and billboard.status == 'occupied':
            icon_color = 'red'
        else:
            icon_color = 'green'
            
        # Create a custom marker icon
        icon = folium.Icon(color='white', icon_color=icon_color, icon='square', prefix='fa')
        
        # Format popup content
        if billboard.status == 'occupied':
            popup_html = f"""
                <div style="width:300px;">
                    <img src="{billboard.image.url if hasattr(billboard, 'image') and billboard.image else '/static/img/billboard_placeholder.jpg'}" 
                        style="width:100%; height:auto; margin-bottom:10px;">
                    <div style="background-color:#f8f9fa; padding:10px;">
                        <table style="width:100%;">
                            <tr>
                                <td><strong>Адрес:</strong></td>
                                <td>{billboard.address if hasattr(billboard, 'address') else 'Госпитальная'}</td>
                            </tr>
                            <tr>
                                <td><strong>Размер:</strong></td>
                                <td>{billboard.format if hasattr(billboard, 'format') else '3x6м'}</td>
                            </tr>
                            <tr>
                                <td><strong>Статус:</strong></td>
                                <td style='color: red;'>Занят</td>
                            </tr>
                            
                            <tr>
                                <td><strong>Срок до:</strong></td>
                                <td>{billboard.expiry_date.strftime('%d.%m.%Y') if hasattr(billboard, 'expiry_date') and billboard.expiry_date else '05.06.2026'}</td>
                            </tr>
                            <tr>
                                <td><strong>Номер:</strong></td>
                                <td>№ {billboard.billboard_number if hasattr(billboard, 'billboard_number') else '01'}</td>
                            </tr>
                            <tr>
                                <td><strong>Клиент:</strong></td>
                                <td>{billboard.client if hasattr(billboard, 'client') else 'SFT'}</td>
                            </tr>
                            
                            <tr>
                                <td><strong>Цена:</strong></td>
                                <td>{billboard.price if hasattr(billboard, 'price') else '700.000'}</td>
                            </tr>
                            <tr>
                                <td><strong>Сумма:</strong></td>
                                <td>{billboard.total_amount if hasattr(billboard, 'total_amount') else '8.400.000'}</td>
                            </tr>                            
                        </table>
                    </div>
                </div>
                """
        else:
            popup_html = f"""
                <div style="width:300px;">
                    <img src="{billboard.image.url if hasattr(billboard, 'image') and billboard.image else '/static/img/billboard_placeholder.jpg'}" 
                        style="width:100%; height:auto; margin-bottom:10px;">
                    <div style="background-color:#f8f9fa; padding:10px;">
                        <table style="width:100%;">
                            <tr>
                                <td><strong>Адрес:</strong></td>
                                <td>{billboard.address if hasattr(billboard, 'address') else 'Госпитальная'}</td>
                            </tr>
                            <tr>
                                <td><strong>Размер:</strong></td>
                                <td>{billboard.format if hasattr(billboard, 'format') else '3x6м'}</td>
                            </tr>
                            <tr>
                                <td><strong>Статус:</strong></td>
                                <td style='color: green;'>Свободен</td>
                            </tr>
                            
                            <tr>
                                <td><strong>Номер:</strong></td>
                                <td>№ {billboard.billboard_number if hasattr(billboard, 'billboard_number') else '01'}</td>
                            </tr>
                            
                            <tr>
                                <td><strong>Цена:</strong></td>
                                <td>{billboard.price if hasattr(billboard, 'price') else '700.000'}</td>
                            </tr>                          
                        </table>
                    </div>
                </div>
                """
        
        # Create popup
        popup = folium.Popup(folium.Html(popup_html, script=True), max_width=300)
        
        # Create marker with popup
        coordinates = (billboard.latitude, billboard.longitude)
        folium.Marker(coordinates, popup=popup, icon=icon).add_to(m)
    
    # If no billboards, add a sample one for demonstration
    if not billboards:
        sample_popup_html = """
        <div style="width:250px;">
            <img src="/static/assets/images/banner.jpg" style="width:100%; height:auto; margin-bottom:10px;">
            <div style="background-color:#f8f9fa; padding:10px;">
                <table style="width:100%;">
                    <tr>
                        <td><strong>Адрес:</strong></td>
                        <td>Госпитальная</td>
                    </tr>
                    <tr>
                        <td><strong>Номер:</strong></td>
                        <td>№ 01</td>
                    </tr>
                    <tr>
                        <td><strong>Размер:</strong></td>
                        <td>3x6м</td>
                    </tr>
                    <tr>
                        <td><strong>Статус:</strong></td>
                        <td>Занят</td>
                    </tr>
                    <tr>
                        <td><strong>Срок до:</strong></td>
                        <td>05.06.2026</td>
                    </tr>
                    <tr>
                        <td><strong>Клиент:</strong></td>
                        <td>SFT</td>
                    </tr>
                    <tr>
                        <td><strong>Цена:</strong></td>
                        <td>700.000</td>
                    </tr>
                    <tr>
                        <td><strong>Сумма:</strong></td>
                        <td>8.400.000</td>
                    </tr>
                </table>
            </div>
        </div>
        """
        sample_popup = folium.Popup(folium.Html(sample_popup_html, script=True), max_width=300)
        folium.Marker([39.667, 66.945], popup=sample_popup, 
                     icon=folium.Icon(color='white', icon_color='red', icon='square', prefix='fa')).add_to(m)
    
    # Get all unique filter options from database
    locations = Billboard.objects.values_list('location__name', flat=True).distinct() if billboards.exists() else []
    regions = Billboard.objects.values_list('region__name', flat=True).distinct() if billboards.exists() else []
    districts = Billboard.objects.values_list('district__name', flat=True).distinct() if billboards.exists() else []
    statuses = Billboard.objects.values_list('status', flat=True).distinct() if billboards.exists() else []
    
    ctx = {
        'map': m._repr_html_(),
        'locations': locations,
        'regions': regions,
        'districts': districts,
        'statuses': statuses,
        # Pass current filter values back to the template
        'current_filters': {
            'location': location_filter,
            'region': region_filter,
            'district': district_filter,
            'status': status_filter,
            'search': search_query
        }
    }

    return render(request, 'home.html', ctx)

def services_page(request):
    return render(request, 'services.html')

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')
