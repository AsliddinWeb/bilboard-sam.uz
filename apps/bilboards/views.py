from django.shortcuts import render

# Folium
import folium
from folium import Map, Marker, Popup
from folium.features import CustomIcon

from .models import Billboard

def home_page(request):
    billboards = Billboard.objects.select_related('location', 'region', 'district').all()

    # Create Folium Map
    m = Map(location=[39.6542, 66.9750], zoom_start=12, height='500px', 
            tiles='CartoDB positron', control_scale=True)

    # Add custom markers with popup info
    for billboard in billboards:
        # Define marker color based on status
        if hasattr(billboard, 'status') and billboard.status == 'occupied':
            icon_color = 'red'
        else:
            icon_color = 'green'
            
        # Create a custom marker icon
        # icon = folium.Icon(color='white', icon_color=icon_color, icon='square', prefix='fa')
        
        # Format popup content
        print(billboard.status)
        if billboard.status == 'occupied': # zaynt
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
                                <td>{billboard.size if hasattr(billboard, 'size') else '3x6м'}</td>
                            </tr>
                            <tr>
                                <td><strong>Статус:</strong></td>
                                <td style='color: red;'>Занят</td>
                            </tr>
                            
                            <tr>
                                <td><strong>Срок до:</strong></td>
                                <td>{billboard.rental_end_date.strftime('%d.%m.%Y') if hasattr(billboard, 'rental_end_date') and billboard.rental_end_date else '05.06.2026'}</td>
                            </tr>
                            <tr>
                                <td><strong>Номер:</strong></td>
                                <td>№ {billboard.number if hasattr(billboard, 'number') else '01'}</td>
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
                                <td>{billboard.total_price if hasattr(billboard, 'total_price') else '8.400.000'}</td>
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
                                <td>{billboard.size if hasattr(billboard, 'size') else '3x6м'}</td>
                            </tr>
                            <tr>
                                <td><strong>Статус:</strong></td>
                                <td style='color: green;'>Свободен</td>
                            </tr>
                            
                            <tr>
                                <td><strong>Номер:</strong></td>
                                <td>№ {billboard.number if hasattr(billboard, 'number') else '01'}</td>
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
        # folium.Marker(coordinates, popup=popup, icon=icon).add_to(m)
        folium.Marker(coordinates, popup=popup).add_to(m)
    
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
    locations = Billboard.objects.values_list('location__name', flat=True).distinct() if billboards else []
    regions = Billboard.objects.values_list('region__name', flat=True).distinct() if billboards else []
    districts = Billboard.objects.values_list('district__name', flat=True).distinct() if billboards else []
    statuses = Billboard.objects.values_list('status', flat=True).distinct() if billboards else []
    
    ctx = {
        'map': m._repr_html_(),
        'locations': locations,
        'regions': regions,
        'districts': districts,
        'statuses': statuses,
    }

    return render(request, 'home.html', ctx)

def services_page(request):
    return render(request, 'services.html')

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')