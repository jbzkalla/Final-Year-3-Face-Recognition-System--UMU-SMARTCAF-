import datetime
import os
import json
import uuid

TICKETS_FILE = "data/support_tickets.json"

# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

def create_ticket(user_email, subject, message, category, ticket_type="Feedback"):
    """
    Creates a new support ticket and saves it.
    """
    ticket_id = str(uuid.uuid4())
    ticket = {
        "id": ticket_id,
        "user_email": user_email,
        "subject": subject,
        "message": message,
        "category": category,
        "type": ticket_type,
        "status": "Open",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    tickets = get_all_tickets()
    tickets.append(ticket)
    
    try:
        with open(TICKETS_FILE, 'w') as f:
            json.dump(tickets, f, indent=4)
        
        # Simulate sending email notification
        send_email_notification(ticket)
        
        return True, ticket_id
    except Exception as e:
        print(f"Error creating ticket: {e}")
        return False, str(e)

def get_all_tickets():
    """
    Retrieves all support tickets.
    """
    if not os.path.exists(TICKETS_FILE):
        return []
        
    try:
        with open(TICKETS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def update_ticket_status(ticket_id, new_status):
    """
    Updates the status of an existing ticket.
    """
    tickets = get_all_tickets()
    found = False
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            ticket['status'] = new_status
            ticket['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found = True
            break
            
    if not found:
        return False, "Ticket not found"
        
    try:
        with open(TICKETS_FILE, 'w') as f:
            json.dump(tickets, f, indent=4)
        return True, "Ticket updated successfully"
    except Exception as e:
        return False, str(e)

def send_email_notification(ticket):
    """
    Simulates sending an email notification to the support team.
    """
    print(f"--- EMAIL NOTIFICATION ---")
    print(f"To: support@umucanteen.com")
    print(f"Subject: New Support Ticket: {ticket['subject']}")
    print(f"From: {ticket['user_email']}")
    print(f"Message: {ticket['message']}")
    print(f"--------------------------")
