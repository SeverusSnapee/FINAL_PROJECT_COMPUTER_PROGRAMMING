import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Use 'Agg' backend for non-interactive environments
matplotlib.use('Agg')

# Function to calculate carbon footprint based on input data
def calculate_footprint(energy, distance, waste):
    return energy * 0.233 + distance * 0.12 + waste * 0.5

# Function to create a PDF report for each client
def create_report(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    pdf = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    # Add title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 40, "Carbon Footprint Report")
    
    pdf.setFont("Helvetica", 12)
    y_position = height - 80
    
    # Add client data
    pdf.drawString(50, y_position, f"Client: {data['Client']}")
    y_position -= 20
    pdf.drawString(50, y_position, f"Energy: {data['energy_kwh']} kWh")
    y_position -= 20
    pdf.drawString(50, y_position, f"Transport: {data['transport_km']} km")
    y_position -= 20
    pdf.drawString(50, y_position, f"Waste: {data['waste_kg']} kg")
    y_position -= 20
    pdf.drawString(50, y_position, f"Footprint: {data['total_footprint']} kg CO2")
    y_position -= 30
    
    # Suggestions for lowering footprint
    pdf.drawString(50, y_position, "Suggestions:")
    y_position -= 20
    pdf.drawString(50, y_position, "- Use energy-efficient appliances.")
    y_position -= 15
    pdf.drawString(50, y_position, "- Carpool or use public transport.")
    y_position -= 15
    pdf.drawString(50, y_position, "- Recycle and reduce waste.")
    
    # Save PDF
    pdf.save()
    print(f"PDF Report Created: {file_path}")

# Function to generate a trend graph for multiple clients
def generate_graph(data_list):
    clients = [data['Client'] for data in data_list]
    energy = [data['energy_kwh'] for data in data_list]
    transport = [data['transport_km'] for data in data_list]
    waste = [data['waste_kg'] for data in data_list]
    footprint = [data['total_footprint'] for data in data_list]
    
    # Create a DataFrame
    df = pd.DataFrame({
        'Client': clients,
        'Energy (kWh)': energy,
        'Transport (km)': transport,
        'Waste (kg)': waste,
        'Footprint (kg CO2)': footprint
    })
    
    # Plot data
    plt.figure(figsize=(10, 6))
    plt.bar(df['Client'], df['Footprint (kg CO2)'], color='skyblue', label='Carbon Footprint')
    plt.plot(df['Client'], df['Energy (kWh)'], color='green', marker='o', label='Energy', linestyle='--')
    plt.plot(df['Client'], df['Transport (km)'], color='orange', marker='o', label='Transport', linestyle='--')
    plt.plot(df['Client'], df['Waste (kg)'], color='red', marker='o', label='Waste', linestyle='--')

    # Labels and title
    plt.xlabel('Clients')
    plt.ylabel('Metrics')
    plt.title('Carbon Footprint Trends')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.legend()
    
    # Save graph
    plt.savefig('carbon_trends.png', dpi=300)
    plt.close()
    print("Graph Saved as 'carbon_trends.png'")

# Main function to handle input and generate reports for multiple clients
def main():
    client_data = []

    while True:
        print("Enter client data:")

        try:
            energy_kwh = float(input("Energy (kWh): "))
            transport_km = float(input("Transport (km): "))
            waste_kg = float(input("Waste (kg): "))
        except ValueError:
            print("Invalid input. Please enter numbers.")
            continue

        total_footprint = calculate_footprint(energy_kwh, transport_km, waste_kg)

        client_name = input("Client Name: ")
        client_details = {
            'Client': client_name,
            'energy_kwh': energy_kwh,
            'transport_km': transport_km,
            'waste_kg': waste_kg,
            'total_footprint': total_footprint
        }
        client_data.append(client_details)

        # Create the report
        report_filename = f"Reports/{client_name}_report.pdf"
        create_report(client_details, report_filename)
        print(f"Report created for {client_name}: {report_filename}")

        # Check if more data should be entered
        continue_input = input("Add data for another client? (yes/no): ").strip().lower()
        if continue_input != 'yes':
            break
    
    # Generate the summary graph
    generate_graph(client_data)
    print("Graph generated successfully.")

if __name__ == "__main__":
    main()
