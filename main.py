import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Use 'Agg' backend for plotting in non-interactive environments
matplotlib.use('Agg')

# Function to compute the environmental impact based on input data
def compute_footprint(energy_usage, travel_distance, waste_produced):
    return energy_usage * 0.233 + travel_distance * 0.12 + waste_produced * 0.5

# Function to create individual PDF reports for each client
def create_pdf_report(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Initialize PDF creation using ReportLab
    pdf = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    # Adding Title to the PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 40, "Carbon Footprint Report")
    
    pdf.setFont("Helvetica", 12)
    y_position = height - 80
    
    # Displaying Client Information
    pdf.drawString(50, y_position, f"Client: {data['Client']}")
    y_position -= 20
    pdf.drawString(50, y_position, f"Energy Consumption: {data['energy_kwh']} kWh")
    y_position -= 20
    pdf.drawString(50, y_position, f"Transport Distance: {data['transport_km']} km")
    y_position -= 20
    pdf.drawString(50, y_position, f"Waste Generated: {data['waste_kg']} kg")
    y_position -= 20
    pdf.drawString(50, y_position, f"Total Carbon Footprint: {data['total_footprint']} kg CO2")
    y_position -= 30
    
    # Recommendations section
    pdf.drawString(50, y_position, "Suggestions to Lower Carbon Footprint:")
    y_position -= 20
    pdf.drawString(50, y_position, "- Use energy-saving appliances.")
    y_position -= 15
    pdf.drawString(50, y_position, "- Consider carpooling or public transport.")
    y_position -= 15
    pdf.drawString(50, y_position, "- Minimize waste through recycling and reuse.")
    
    # Save the PDF file
    pdf.save()
    print(f"PDF Report Created: {file_path}")

# Function to generate a graph summarizing trends across clients
def generate_trend_graph(data_list):
    # Extracting data for graph plotting
    clients = [data['Client'] for data in data_list]
    energy_usage = [data['energy_kwh'] for data in data_list]
    travel_distance = [data['transport_km'] for data in data_list]
    waste_produced = [data['waste_kg'] for data in data_list]
    carbon_footprint = [data['total_footprint'] for data in data_list]
    
    # Creating a DataFrame for organized data handling
    df = pd.DataFrame({
        'Client': clients,
        'Energy Usage (kWh)': energy_usage,
        'Transport (km)': travel_distance,
        'Waste (kg)': waste_produced,
        'Carbon Footprint (kg CO2)': carbon_footprint
    })
    
    # Create a plot for trends in carbon footprints
    plt.figure(figsize=(10, 6))
    
    # Plotting the carbon footprint data
    plt.bar(df['Client'], df['Carbon Footprint (kg CO2)'], color='skyblue', label='Carbon Footprint')
    
    # Adding other metrics for comparison
    plt.plot(df['Client'], df['Energy Usage (kWh)'], color='green', marker='o', label='Energy Usage', linestyle='--')
    plt.plot(df['Client'], df['Transport (km)'], color='orange', marker='o', label='Transport Distance', linestyle='--')
    plt.plot(df['Client'], df['Waste (kg)'], color='red', marker='o', label='Waste Production', linestyle='--')

    # Adding labels and title to the plot
    plt.xlabel('Clients')
    plt.ylabel('Metrics')
    plt.title('Trends of Carbon Footprint and Related Metrics')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()  # Ensures proper layout without clipping labels
    plt.legend()
    
    # Save the plot as an image file
    plt.savefig('client_carbon_trends.png', dpi=300)
    plt.close()
    print("Trend Graph Saved as 'client_carbon_trends.png'")

# Function to handle input and generate reports for multiple clients
def main():
    client_data = []

    while True:
        print("Enter the client's data:")

        try:
            energy_kwh = float(input("Energy consumption (kWh): "))
            transport_km = float(input("Transport distance (km): "))
            waste_kg = float(input("Waste generated (kg): "))
        except ValueError:
            print("Invalid input. Please enter numerical values.")
            continue

        total_footprint = compute_footprint(energy_kwh, transport_km, waste_kg)

        # Collecting client-specific data
        client_name = input("Client Name: ")
        client_details = {
            'Client': client_name,
            'energy_kwh': energy_kwh,
            'transport_km': transport_km,
            'waste_kg': waste_kg,
            'total_footprint': total_footprint
        }
        client_data.append(client_details)

        # Generate individual reports
        report_filename = f"Reports/{client_name}_carbon_report.pdf"
        create_pdf_report(client_details, report_filename)
        print(f"Report created for {client_name}: {report_filename}")

        # Check if more client data needs to be entered
        continue_input = input("Do you want to add data for another client? (yes/no): ").strip().lower()
        if continue_input != 'yes':
            break
    
    # After collecting all data, generate the trend graph
    generate_trend_graph(client_data)
    print("Generated the trend graph successfully.")

if __name__ == "__main__":
    main()
