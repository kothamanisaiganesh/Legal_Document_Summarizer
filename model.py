from jinja2 import Environment, FileSystemLoader
import os

def generate_rental_agreement(landlord_info, tenant_info, property_info, lease_info):
    # Set up Jinja2 environment
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Load the template
    template = env.get_template('rental_template.txt')
    
    # Render the template with provided data
    rental_agreement = template.render(
        landlord=landlord_info,
        tenant=tenant_info,
        property=property_info,
        lease=lease_info
    )
    
    return rental_agreement

def save_to_file(rental_agreement, file_path):
    with open(file_path, 'w') as file:
        file.write(rental_agreement)

if __name__ == "__main__":
    # Example data
    landlord_info = {
        'name': 'John Doe',
        'address': '123 Main St, Cityville, State'
    }
    
    tenant_info = {
        'name': 'Jane Smith',
        'address': '456 Oak St, Townsville, State'
    }
    
    property_info = {
        'address': '789 Elm St, Villageton, State'
    }
    
    lease_info = {
        'start_date': 'January 1, 2023',
        'end_date': 'December 31, 2023',
        'rent_amount': '$1,000',
        'due_date': '1st of each month',
        'deposit_amount': '$1,500',
        'days_notice_termination': '30',
    }

    # Generate the rental agreement
    rental_agreement = generate_rental_agreement(landlord_info, tenant_info, property_info, lease_info)

    # Save the rental agreement to a file
    save_to_file(rental_agreement, 'LegalDocument.txt')
