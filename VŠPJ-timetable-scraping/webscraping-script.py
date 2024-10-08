import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import re

def format_description(description):
    # Replace multiple spaces with a single space
    formatted_desc = re.sub(r'\s+', ' ', description)
    # Replace multiple newlines with a single newline
    formatted_desc = re.sub(r'\n+', '\n', formatted_desc).strip()
    return formatted_desc

def login_to_is(session, username, password):
    login_url = 'https://is.vspj.cz/prihlasit'
    
    # Step 1: Access login page to get the CSRF token
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract CSRF token
    csrf_token = soup.find('input', {'name': '_csrf_token'})['value']

    # Login data
    login_data = {
        '_username': username,
        '_password': password,
        '_csrf_token': csrf_token,
        '_target_path': '/dashboard/'
    }
    
    # Step 2: Post login data and follow redirects
    response = session.post(login_url, data=login_data, allow_redirects=True)
    
    if 'dashboard' in response.url or response.status_code == 200:
        print("Login successful!")
        return True
    else:
        print("Login failed, please check your credentials.")
        return False

def fetch_timetable_html(session):
    timetable_url = 'https://isz.vspj.cz/student/rozvrh/muj-rozvrh'
    
    # Step 3: Fetch the timetable page after login
    response = session.get(timetable_url)
    if response.status_code == 200 and 'muj-rozvrh' in response.url:
        print("Timetable page accessed successfully.")
        return response.text
    else:
        print("Failed to access the timetable page.")
        return None

def parse_timetable(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')

    if len(tables) < 2:
        print("Second timetable table not found in HTML.")
        return []
    
    # Select the second table
    table = tables[1]

    events = []

    # Define the days and times
    days = ['po', 'út', 'st', 'čt', 'pá', 'so', 'ne']
    time_slots = [
        '7:10', '8:00', '8:50', '9:45', '10:35', '11:30', '12:35',
        '13:30', '14:20', '15:15', '16:05', '17:00', '17:50', '18:45'
    ]
    
    end_times = [
        '7:55', '8:45', '9:35', '10:30', '11:20', '12:15', '13:20',
        '14:15', '15:05', '16:00', '16:50', '17:45', '18:35', '19:30'
    ]

    # Loop through rows in the timetable table
    for row in table.find_all('tr')[1:]:
        day = row.find('th').text.strip().lower()
        if day not in days:
            continue
        day_index = days.index(day)

        for i, cell in enumerate(row.find_all('td')):
            if cell.get('colspan'):
                event = cell.find('b')
                if event:
                    subject = event.text.strip()
                    details = cell.find('small').text.strip() if cell.find('small') else 'No details'

                     # Format the details using the format_description function
                    formatted_details = format_description(details)

                    start_time = time_slots[i]
                    end_time = end_times[i + int(cell['colspan']) - 1]  # Capture the end time for the last slot
                    
                    events.append({
                        'subject': subject,
                        'details': formatted_details,
                        'day': day,
                        'start_time': start_time,
                        'end_time': end_time
                    })

    return events

def generate_ical(events):
    cal = Calendar()
    cal.add('prodid', '-//VSPJ Timetable//EN')
    cal.add('version', '2.0')

    tz = pytz.timezone('Europe/Prague')
    today = datetime.now(tz).date()
    start_of_week = today - timedelta(days=today.weekday())

    for event in events:
        e = Event()
        e.add('summary', event['subject'])
        e.add('description', event['details'])

        day_offset = ['po', 'út', 'st', 'čt', 'pá', 'so', 'ne'].index(event['day'])
        event_date = start_of_week + timedelta(days=day_offset)

        start_time = datetime.strptime(event['start_time'], '%H:%M').time()
        end_time = datetime.strptime(event['end_time'], '%H:%M').time()

        e.add('dtstart', tz.localize(datetime.combine(event_date, start_time)))
        e.add('dtend', tz.localize(datetime.combine(event_date, end_time)))

        cal.add_component(e)

    return cal.to_ical()

def main(username, password):
    session = requests.Session()

    # Step 1: Login to the VSPJ system
    if login_to_is(session, username, password):
        # Step 2: Fetch timetable HTML
        html = fetch_timetable_html(session)
        
        if html:
            # Step 3: Parse timetable events
            events = parse_timetable(html)
            
            if events:
                # Step 4: Generate .ics file
                ical_data = generate_ical(events)
                with open('timetable.ics', 'wb') as f:
                    f.write(ical_data)
                print("Timetable exported to timetable.ics")
            else:
                print("No events found in the timetable.")
        else:
            print("Failed to retrieve timetable.")
    else:
        print("Login failed.")

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    main(username, password)
